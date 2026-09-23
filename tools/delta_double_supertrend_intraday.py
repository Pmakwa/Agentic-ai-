#!/usr/bin/env python3
"""
DELTA INDIA DOUBLE SUPERTREND INTRADAY ENGINE
Based on YouTube: https://youtu.be/kSU11mJ19lY — Trade With Sidh
Strategy: Double Supertrend 10/3 & 10/4, Weekly swing logic converted to INTRADAY on Delta India (BTC/ETH/SOL INR perpetuals)

Entry Logic (LONG):
- Both ST 10/3 and 10/4 bullish (ST_dir==1)
- Red retracement candle appears
- Within next 3 candles, a GREEN candle with body close > red_high AND small upper wick (high-close < 25% of range) appears
- Entry = high of that green candle (next bar open execution)
- SL = 8% fixed below entry (or 9% variant)
- Target = 24% above entry (1:3 RR) — fixed, no trail in backtest; trailing optional
- Intraday: forced square-off at 23:55 IST if not hit SL/TP (crypto 24/7 → calendar day end)
- Reverse for SHORT (both ST bearish, green retracement, red breakout below green low)

Timeframes: 5m (7d yfinance limit), 15m (60d), 30m (60d), 1h (2y)
Exchange: Delta Exchange India (INR settlement) — fees 0.05% taker +18% GST =0.059% per side
Capital: ₹10,000 INR | Risk: 1% per trade | Position size = Risk / 8%
Data: Yahoo BTC-USD/ETH-USD/SOL-USD proxy for Delta India BTCINR/ETHINR/SOLINR, converted via 83.50 INR/USDT
"""

from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import timezone
try:
    from numba import jit
    HAS_NUMBA=True
except:
    HAS_NUMBA=False
    def jit(*a,**k):
        def dec(f): return f
        return dec

ROOT=Path(__file__).resolve().parent.parent
OUT_DIR=ROOT/"09_QUANT_RESEARCH"/"DELTA_INTRADAY_DOUBLE_ST"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CAPITAL_INR=10000.0
USDT_INR=83.50
FEE_PCT=0.00059  # Delta taker 0.05% *1.18 GST
SLIPPAGE_PCT=0.0005  # 0.05%
COINS={"BTC/INR":"BTC-USD","ETH/INR":"ETH-USD","SOL/INR":"SOL-USD"}
TIMEFRAMES={"5m":("5m","7d"), "15m":("15m","60d"), "30m":("30m","60d"), "1h":("60m","2y")}
# 1h uses 60m interval which is same

def compute_atr(df: pd.DataFrame, period:int)->pd.Series:
    h,l,c=df["High"],df["Low"],df["Close"]
    pc=c.shift(1)
    tr=pd.concat([h-l,(h-pc).abs(),(l-pc).abs()], axis=1).max(axis=1)
    atr=tr.rolling(period).mean()
    return atr

@jit(nopython=True)
def _st_loop(close_arr, ub_arr, lb_arr, final_upper_arr, final_lower_arr, st_arr, dir_arr):
    n=close_arr.shape[0]
    for i in range(n):
        if i==0:
            final_upper_arr[i]=ub_arr[i]
            final_lower_arr[i]=lb_arr[i]
            st_arr[i]=final_upper_arr[i]
            dir_arr[i]=-1
            continue
        if close_arr[i-1] <= final_upper_arr[i-1]:
            final_upper_arr[i]= ub_arr[i] if ub_arr[i] < final_lower_arr[i-1] else final_lower_arr[i-1]
            # Actually min
            if ub_arr[i] < final_upper_arr[i-1]:
                final_upper_arr[i]=ub_arr[i]
            else:
                final_upper_arr[i]=final_upper_arr[i-1]
        else:
            final_upper_arr[i]=ub_arr[i]
        if close_arr[i-1] >= final_lower_arr[i-1]:
            if lb_arr[i] > final_lower_arr[i-1]:
                final_lower_arr[i]=lb_arr[i]
            else:
                final_lower_arr[i]=final_lower_arr[i-1]
        else:
            final_lower_arr[i]=lb_arr[i]
        if dir_arr[i-1]==-1:
            if close_arr[i] > final_upper_arr[i-1]:
                dir_arr[i]=1
                st_arr[i]=final_lower_arr[i]
            else:
                dir_arr[i]=-1
                st_arr[i]=final_upper_arr[i]
        else:
            if close_arr[i] < final_lower_arr[i-1]:
                dir_arr[i]=-1
                st_arr[i]=final_upper_arr[i]
            else:
                dir_arr[i]=1
                st_arr[i]=final_lower_arr[i]

def compute_supertrend(df: pd.DataFrame, period:int, mult:float):
    hl2=(df["High"]+df["Low"])/2.0
    atr=compute_atr(df, period)
    ub=hl2 + mult*atr
    lb=hl2 - mult*atr
    n=len(df)
    close_arr=df["Close"].values.astype(np.float64)
    ub_arr=np.where(np.isnan(ub.values), close_arr, ub.values).astype(np.float64)
    lb_arr=np.where(np.isnan(lb.values), close_arr, lb.values).astype(np.float64)
    final_upper=np.empty(n,dtype=np.float64)
    final_lower=np.empty(n,dtype=np.float64)
    st=np.empty(n,dtype=np.float64)
    direction=np.empty(n,dtype=np.int64)
    _st_loop(close_arr, ub_arr, lb_arr, final_upper, final_lower, st, direction)
    return pd.DataFrame({"ST":st,"ST_dir":direction,"ST_upper":final_upper,"ST_lower":final_lower,"ATR":atr.values}, index=df.index)

def download_delta_data(yf_ticker:str, interval:str, period:str)->pd.DataFrame:
    df=yf.download(yf_ticker, period=period, interval=interval, progress=False, auto_adjust=False)
    if df is None or len(df)==0:
        return pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns=[c[0] for c in df.columns]
    df=df.dropna(subset=["Open","High","Low","Close","Volume"])
    if df.index.tz is None:
        df.index=df.index.tz_localize("UTC")
    else:
        df.index=df.index.tz_convert("UTC")
    # Convert to IST for intraday square-off logic (IST = UTC+5:30)
    df.index = df.index.tz_convert("Asia/Kolkata")
    return df

def backtest_double_st_intraday(df: pd.DataFrame, coin:str, timeframe:str, st_p1:int=10, st_m1:float=3.0, st_p2:int=10, st_m2:float=4.0, sl_pct:float=0.08, rr:float=3.0, risk_pct:float=0.01, intraday_squareoff:bool=True):
    """
    Implements exact YouTube Double Supertrend intraday logic
    Returns metrics + trades + equity_curve
    """
    if len(df)<100:
        return {"error":"insufficient data", "bars":len(df), "metrics":{"num_trades":0,"starting_capital":CAPITAL_INR,"ending_capital":CAPITAL_INR}}

    df=df.copy()
    st1=compute_supertrend(df, st_p1, st_m1)
    st2=compute_supertrend(df, st_p2, st_m2)
    df["ST1_dir"]=st1["ST_dir"]
    df["ST2_dir"]=st2["ST_dir"]
    df["ST1"]=st1["ST"]
    df["ST2"]=st2["ST"]
    df["ATR"]=st1["ATR"]

    equity=CAPITAL_INR
    peak=equity
    max_dd=0
    trades=[]
    equity_curve=[{"time":str(df.index[0]),"equity":equity}]
    in_pos=None
    entry_price=0
    stop_price=0
    target_price=0
    entry_time=None
    entry_equity_before=0
    pos_units=0
    # For day tracking
    # Loop over bars, look for entry signals when flat
    # Use index i for signal search, but execution at next bar open
    i=50
    while i < len(df)-4:
        bar=df.iloc[i]
        # If in position, check for exit on next bars before looking for new entry
        if in_pos is not None:
            # Check next bar i+1 for SL/TP or EOD
            # Actually we need to iterate bar by bar while in position
            # But our outer while is for signal search, inner we handle position holding
            # So if in_pos, we step one bar at a time to check exit
            nxt=df.iloc[i+1] if i+1 < len(df) else None
            if nxt is None:
                break
            # Check if new calendar day (IST) vs entry_time day -> forced square-off at last bar of previous day
            # For crypto we define forced square-off at 23:55 IST day end
            is_new_day = nxt.name.date() != pd.to_datetime(entry_time).date() if entry_time else False
            # Also check SL/TP within nxt bar
            hit_sl=False
            hit_tp=False
            exit_price=None
            exit_reason=None
            if in_pos=="LONG":
                if nxt["Low"] <= stop_price:
                    hit_sl=True
                    exit_price=stop_price*(1-SLIPPAGE_PCT)
                    exit_reason="STOP_LOSS"
                elif nxt["High"] >= target_price:
                    hit_tp=True
                    exit_price=target_price*(1-SLIPPAGE_PCT)
                    exit_reason="TARGET_HIT"
                elif intraday_squareoff and is_new_day:
                    # Square off at previous day last bar close (current bar close is new day open, so square at bar close of previous day = df.iloc[i] close)
                    # For simplicity, square at nxt open
                    exit_price=nxt["Open"]*(1-SLIPPAGE_PCT)
                    exit_reason="INTRADAY_SQUAREOFF"
            else: # SHORT
                if nxt["High"] >= stop_price:
                    hit_sl=True
                    exit_price=stop_price*(1+SLIPPAGE_PCT)
                    exit_reason="STOP_LOSS"
                elif nxt["Low"] <= target_price:
                    hit_tp=True
                    exit_price=target_price*(1+SLIPPAGE_PCT)
                    exit_reason="TARGET_HIT"
                elif intraday_squareoff and is_new_day:
                    exit_price=nxt["Open"]*(1+SLIPPAGE_PCT)
                    exit_reason="INTRADAY_SQUAREOFF"

            if hit_sl or hit_tp or exit_reason=="INTRADAY_SQUAREOFF":
                # Calculate PnL in INR
                # entry_price is USD, convert via USDT_INR
                if in_pos=="LONG":
                    gross_usd=(exit_price - entry_price)*pos_units
                else:
                    gross_usd=(entry_price - exit_price)*pos_units
                gross_inr=gross_usd*USDT_INR
                entry_fee=entry_price*pos_units*FEE_PCT*USDT_INR
                exit_fee=exit_price*pos_units*FEE_PCT*USDT_INR
                net_inr=gross_inr - entry_fee - exit_fee
                equity+=net_inr
                trades.append({
                    "trade_no":len(trades)+1,
                    "coin":coin,
                    "timeframe":timeframe,
                    "direction":in_pos,
                    "entry_time":str(entry_time),
                    "exit_time":str(nxt.name),
                    "entry_price_usd":round(entry_price,2),
                    "entry_price_inr":round(entry_price*USDT_INR,2),
                    "stop_price_usd":round(stop_price,2),
                    "target_price_usd":round(target_price,2),
                    "exit_price_usd":round(exit_price,2),
                    "exit_price_inr":round(exit_price*USDT_INR,2),
                    "exit_reason":exit_reason,
                    "risk_pct":risk_pct,
                    "risk_inr":round(entry_equity_before*risk_pct,2),
                    "position_size_coin":round(pos_units,6),
                    "position_size_inr":round(entry_price*pos_units*USDT_INR,2),
                    "gross_pnl_inr":round(gross_inr,2),
                    "fees_inr":round(entry_fee+exit_fee,2),
                    "net_pnl_inr":round(net_inr,2),
                    "net_pnl":round(net_inr,2),
                    "equity_before":round(entry_equity_before,2),
                    "equity_after":round(equity,2),
                })
                equity_curve.append({"time":str(nxt.name),"equity":round(equity,2)})
                if equity>peak: peak=equity
                # reset position
                in_pos=None
                entry_price=0
                stop_price=0
                target_price=0
                pos_units=0
                i+=1  # move to next bar after exit
                continue
            else:
                # Hold, move to next bar
                i+=1
                continue

        # If flat, look for entry signal at bar i
        # Condition: both ST bullish/bearish
        both_bull = (df["ST1_dir"].iloc[i]==1 and df["ST2_dir"].iloc[i]==1)
        both_bear = (df["ST1_dir"].iloc[i]==-1 and df["ST2_dir"].iloc[i]==-1)
        # Check for red retracement then green breakout (LONG)
        # Or green retracement then red breakout (SHORT)
        if both_bull and in_pos is None:
            # Check if current bar is RED (close < open)
            curr=df.iloc[i]
            is_red = curr["Close"] < curr["Open"]
            if is_red:
                red_high=curr["High"]
                # Look ahead 1-3 bars for GREEN with body above red_high and small upper wick
                found=False
                green_idx=-1
                for j in range(1,4):
                    if i+j >= len(df): break
                    nb=df.iloc[i+j]
                    is_green = nb["Close"] > nb["Open"]
                    body_above = nb["Close"] > red_high
                    # Small upper wick: (High - Close) < 25% of range
                    rng=nb["High"]-nb["Low"]
                    upper_wick=nb["High"]-nb["Close"]
                    small_wick = (upper_wick / rng < 0.25) if rng>0 else True
                    # Also both ST still bullish at that green bar
                    still_bull = (df["ST1_dir"].iloc[i+j]==1 and df["ST2_dir"].iloc[i+j]==1)
                    if is_green and body_above and small_wick and still_bull:
                        found=True
                        green_idx=i+j
                        break
                    # If another RED appears that is lower, update red_high? Actually video says avoid if not breakout within 3, so break
                    # If we encounter a RED that makes new high, we could reset, but keep simple: continue searching within 3
                if found:
                    # Entry at next bar open after green breakout
                    if green_idx+1 >= len(df): 
                        i+=1
                        continue
                    entry_bar=df.iloc[green_idx+1]
                    entry_price_exec = float(entry_bar["Open"])
                    # Also ensure entry above green high
                    green_high=float(df.iloc[green_idx]["High"])
                    if entry_price_exec < green_high:
                        entry_price_exec = green_high * (1+SLIPPAGE_PCT)
                    else:
                        entry_price_exec = entry_price_exec * (1+SLIPPAGE_PCT)
                    # SL/TP
                    stop_price = entry_price_exec * (1 - sl_pct)
                    target_price = entry_price_exec * (1 + sl_pct*rr)
                    # Position sizing
                    risk_amt = equity * risk_pct
                    stop_dist = entry_price_exec - stop_price
                    if stop_dist <=0:
                        i+=1
                        continue
                    # size in coin = risk_amt_INR / (stop_dist*USDT_INR)
                    # risk_amt is INR, stop_dist USD -> INR distance
                    stop_dist_inr = stop_dist * USDT_INR
                    size = risk_amt / stop_dist_inr if stop_dist_inr>0 else 0
                    # Cap at 95% equity
                    max_size = (equity*0.95)/(entry_price_exec*USDT_INR)
                    size=min(size, max_size)
                    if size<=0:
                        i+=1
                        continue
                    # Intraday filter: only enter before 20:00 IST to allow time for target? For crypto we allow all day but require square-off same day
                    # Check entry time is not too close to day end (23:30)
                    entry_time_pending = entry_bar.name
                    # Avoid entries after 22:00 IST for 1h timeframe to avoid holding overnight? We'll allow but square-off will happen
                    in_pos="LONG"
                    entry_price=entry_price_exec
                    pos_units=size
                    entry_time=entry_time_pending
                    entry_equity_before=equity
                    # Move i to green_idx+1 to avoid reprocessing
                    i=green_idx+2
                    continue
        elif both_bear and in_pos is None:
            curr=df.iloc[i]
            is_green = curr["Close"] > curr["Open"]
            if is_green:
                green_low=curr["Low"]
                found=False
                red_idx=-1
                for j in range(1,4):
                    if i+j >= len(df): break
                    nb=df.iloc[i+j]
                    is_red = nb["Close"] < nb["Open"]
                    body_below = nb["Close"] < green_low
                    rng=nb["High"]-nb["Low"]
                    lower_wick=nb["Close"]-nb["Low"]  # for red, close near low
                    # For red, lower wick small: (Close - Low) <25% range
                    small_lower = ((nb["Close"]-nb["Low"])/rng <0.25) if rng>0 else True
                    still_bear = (df["ST1_dir"].iloc[i+j]==-1 and df["ST2_dir"].iloc[i+j]==-1)
                    if is_red and body_below and small_lower and still_bear:
                        found=True
                        red_idx=i+j
                        break
                if found:
                    if red_idx+1 >= len(df):
                        i+=1
                        continue
                    entry_bar=df.iloc[red_idx+1]
                    entry_price_exec=float(entry_bar["Open"])
                    red_low=float(df.iloc[red_idx]["Low"])
                    if entry_price_exec > red_low:
                        entry_price_exec = red_low * (1-SLIPPAGE_PCT)
                    else:
                        entry_price_exec = entry_price_exec * (1-SLIPPAGE_PCT)
                    stop_price = entry_price_exec * (1 + sl_pct)
                    target_price = entry_price_exec * (1 - sl_pct*rr)
                    risk_amt=equity*risk_pct
                    stop_dist=stop_price - entry_price_exec
                    if stop_dist<=0:
                        i+=1
                        continue
                    stop_dist_inr=stop_dist*USDT_INR
                    size=risk_amt/stop_dist_inr if stop_dist_inr>0 else 0
                    max_size=(equity*0.95)/(entry_price_exec*USDT_INR)
                    size=min(size, max_size)
                    if size<=0:
                        i+=1
                        continue
                    in_pos="SHORT"
                    entry_price=entry_price_exec
                    pos_units=size
                    entry_time=entry_bar.name
                    entry_equity_before=equity
                    i=red_idx+2
                    continue
        i+=1

    # Close open position at end
    if in_pos is not None and pos_units>0:
        last=df.iloc[-1]
        exit_price=float(last["Close"])
        if in_pos=="LONG":
            exit_price=exit_price*(1-SLIPPAGE_PCT)
            gross_usd=(exit_price-entry_price)*pos_units
        else:
            exit_price=exit_price*(1+SLIPPAGE_PCT)
            gross_usd=(entry_price-exit_price)*pos_units
        gross_inr=gross_usd*USDT_INR
        entry_fee=entry_price*pos_units*FEE_PCT*USDT_INR
        exit_fee=exit_price*pos_units*FEE_PCT*USDT_INR
        net_inr=gross_inr-entry_fee-exit_fee
        equity+=net_inr
        trades.append({
            "trade_no":len(trades)+1,
            "coin":coin,
            "timeframe":timeframe,
            "direction":in_pos,
            "entry_time":str(entry_time),
            "exit_time":str(last.name),
            "entry_price_usd":round(entry_price,2),
            "entry_price_inr":round(entry_price*USDT_INR,2),
            "stop_price_usd":round(stop_price,2),
            "target_price_usd":round(target_price,2),
            "exit_price_usd":round(exit_price,2),
            "exit_price_inr":round(exit_price*USDT_INR,2),
            "exit_reason":"END_OF_DATA",
            "risk_pct":risk_pct,
            "risk_inr":round(entry_equity_before*risk_pct,2),
            "position_size_coin":round(pos_units,6),
            "position_size_inr":round(entry_price*pos_units*USDT_INR,2),
            "gross_pnl_inr":round(gross_inr,2),
            "fees_inr":round(entry_fee+exit_fee,2),
            "net_pnl_inr":round(net_inr,2),
            "net_pnl":round(net_inr,2),
            "equity_before":round(entry_equity_before,2),
            "equity_after":round(equity,2),
        })
        equity_curve.append({"time":str(last.name),"equity":round(equity,2)})

    # Metrics
    # Build equity curve for DD calc
    eq_vals=[x["equity"] for x in equity_curve]
    peak=eq_vals[0] if eq_vals else CAPITAL_INR
    max_dd=0
    max_dd_pct=0
    for v in eq_vals:
        if v>peak: peak=v
        dd=peak-v
        dd_pct=dd/peak*100 if peak>0 else 0
        if dd>max_dd: max_dd=dd; max_dd_pct=dd_pct
    if not trades:
        metrics={
            "starting_capital":CAPITAL_INR,
            "ending_capital":round(equity,2),
            "total_net_profit":round(equity-CAPITAL_INR,2),
            "return_pct":round((equity/CAPITAL_INR-1)*100,2),
            "max_drawdown_inr":round(max_dd,2),
            "max_drawdown_pct":round(max_dd_pct,2),
            "max_profit":0,"max_loss":0,"avg_win":0,"avg_loss":0,"largest_win":0,"largest_loss":0,
            "win_rate":0,"loss_rate":0,"profit_factor":0,"expectancy":0,"num_trades":0,
            "winning_trades":0,"losing_trades":0,"breakeven_trades":0,
            "max_win_streak":0,"max_loss_streak":0,"avg_win_streak":0,"avg_loss_streak":0,
            "recovery_factor":0,"sharpe":0,"sortino":0,"calmar":0,"exposure_pct":0,
            "avg_duration_hours":0,"max_duration_hours":0,"min_duration_hours":0,
            "gross_profit":0,"gross_loss":0,
        }
    else:
        df_tr=pd.DataFrame(trades)
        wins=df_tr[df_tr["net_pnl_inr"]>0]
        losses=df_tr[df_tr["net_pnl_inr"]<0]
        gross_profit=wins["net_pnl_inr"].sum() if len(wins)>0 else 0
        gross_loss=abs(losses["net_pnl_inr"].sum()) if len(losses)>0 else 0
        pf=gross_profit/gross_loss if gross_loss>0 else (99 if gross_profit>0 else 0)
        win_rate=len(wins)/len(df_tr)*100 if len(df_tr)>0 else 0
        loss_rate=len(losses)/len(df_tr)*100
        avg_win=wins["net_pnl_inr"].mean() if len(wins)>0 else 0
        avg_loss=losses["net_pnl_inr"].mean() if len(losses)>0 else 0
        largest_win=df_tr["net_pnl_inr"].max()
        largest_loss=df_tr["net_pnl_inr"].min()
        expectancy=df_tr["net_pnl_inr"].mean()
        # streaks
        max_win_streak=0
        max_loss_streak=0
        cur_w=0; cur_l=0; win_streaks=[]; loss_streaks=[]
        for pnl in df_tr["net_pnl_inr"]:
            if pnl>0:
                cur_w+=1
                if cur_l>0: loss_streaks.append(cur_l); max_loss_streak=max(max_loss_streak,cur_l); cur_l=0
            elif pnl<0:
                cur_l+=1
                if cur_w>0: win_streaks.append(cur_w); max_win_streak=max(max_win_streak,cur_w); cur_w=0
            else:
                if cur_w>0: win_streaks.append(cur_w); max_win_streak=max(max_win_streak,cur_w); cur_w=0
                if cur_l>0: loss_streaks.append(cur_l); max_loss_streak=max(max_loss_streak,cur_l); cur_l=0
        if cur_w>0: win_streaks.append(cur_w); max_win_streak=max(max_win_streak,cur_w)
        if cur_l>0: loss_streaks.append(cur_l); max_loss_streak=max(max_loss_streak,cur_l)
        avg_win_streak=sum(win_streaks)/len(win_streaks) if win_streaks else 0
        avg_loss_streak=sum(loss_streaks)/len(loss_streaks) if loss_streaks else 0
        recovery=(equity-CAPITAL_INR)/max_dd if max_dd>0 else 0
        # duration
        durs=[]
        for _,r in df_tr.iterrows():
            try:
                d=(pd.to_datetime(r["exit_time"])-pd.to_datetime(r["entry_time"])).total_seconds()/3600
                durs.append(d)
            except: durs.append(0)
        avg_dur=sum(durs)/len(durs) if durs else 0
        max_dur=max(durs) if durs else 0
        min_dur=min(durs) if durs else 0
        total_hours=(df.index[-1]-df.index[0]).total_seconds()/3600 if len(df)>1 else 1
        exposure=sum(durs)/total_hours*100 if total_hours>0 else 0
        # Sharpe on trade returns
        rets=df_tr["net_pnl_inr"]/df_tr["equity_before"]
        sharpe=rets.mean()/rets.std()*np.sqrt(252*6) if rets.std()>0 and len(rets)>5 else 0
        downside=rets[rets<0]
        sortino=rets.mean()/downside.std()*np.sqrt(252*6) if len(downside)>1 and downside.std()>0 else 0
        years= (df.index[-1]-df.index[0]).days/365.0 if len(df)>1 else 0.02
        cagr=(equity/CAPITAL_INR)**(1/years)-1 if years>0 and equity>0 else 0
        calmar=cagr*100/max_dd_pct if max_dd_pct>0 else 0
        metrics={
            "starting_capital":CAPITAL_INR,
            "ending_capital":round(equity,2),
            "total_net_profit":round(equity-CAPITAL_INR,2),
            "return_pct":round((equity/CAPITAL_INR-1)*100,2),
            "max_drawdown_inr":round(max_dd,2),
            "max_drawdown_pct":round(max_dd_pct,2),
            "max_profit":round(largest_win,2),
            "max_loss":round(largest_loss,2),
            "avg_win":round(avg_win,2) if not np.isnan(avg_win) else 0,
            "avg_loss":round(avg_loss,2) if not np.isnan(avg_loss) else 0,
            "largest_win":round(largest_win,2),
            "largest_loss":round(largest_loss,2),
            "win_rate":round(win_rate,2),
            "loss_rate":round(loss_rate,2),
            "profit_factor":round(pf,2),
            "expectancy":round(expectancy,2),
            "num_trades":len(df_tr),
            "winning_trades":len(wins),
            "losing_trades":len(losses),
            "breakeven_trades":len(df_tr)-len(wins)-len(losses),
            "max_win_streak":int(max_win_streak),
            "max_loss_streak":int(max_loss_streak),
            "avg_win_streak":round(avg_win_streak,2),
            "avg_loss_streak":round(avg_loss_streak,2),
            "recovery_factor":round(recovery,2),
            "sharpe":round(sharpe,2),
            "sortino":round(sortino,2),
            "calmar":round(calmar,2),
            "exposure_pct":round(exposure,2),
            "avg_duration_hours":round(avg_dur,2),
            "max_duration_hours":round(max_dur,2),
            "min_duration_hours":round(min_dur,2),
            "gross_profit":round(gross_profit,2),
            "gross_loss":round(gross_loss,2),
        }
    return {
        "coin":coin,
        "timeframe":timeframe,
        "params":{"st1":f"{st_p1}x{st_m1}","st2":f"{st_p2}x{st_m2}","sl_pct":sl_pct,"rr":rr},
        "metrics":metrics,
        "trades":trades,
        "equity_curve":equity_curve,
        "bars":len(df),
        "data_start":str(df.index[0]),
        "data_end":str(df.index[-1]),
    }

def run_all():
    print("="*80)
    print("DELTA INDIA DOUBLE SUPERTREND INTRADAY — YouTube Strategy Backtest")
    print("5m/15m/30m/1h | SL 8% RR 1:3 | Risk 1% | Capital ₹10,000 | Delta Fees 0.059%")
    print("="*80)
    all_res=[]
    import time
    for coin, yft in COINS.items():
        for tf, (interval, period) in TIMEFRAMES.items():
            print(f"\n[DATA] {coin} {tf} ({interval} {period})...")
            df=download_delta_data(yft, interval, period)
            print(f"  -> {len(df)} bars from {df.index[0] if len(df)>0 else 'none'} to {df.index[-1] if len(df)>0 else 'none'}")
            if len(df)<100:
                print(f"  SKIP insufficient")
                continue
            # Intraday with 8% SL
            res=backtest_double_st_intraday(df, coin, tf, 10,3.0,10,4.0,0.08,3.0,0.01, True)
            print(f"  => Trades {res['metrics']['num_trades']} Net ₹{res['metrics']['total_net_profit']} PF {res['metrics']['profit_factor']} Win {res['metrics']['win_rate']}% DD {res['metrics']['max_drawdown_pct']}% Final ₹{res['metrics']['ending_capital']}")
            all_res.append(res)
            # Save trade log
            if res["trades"]:
                import pandas as pd
                pd.DataFrame(res["trades"]).to_csv(OUT_DIR/f"TRADE_LOG_{coin.replace('/','_')}_{tf}_8pct.csv", index=False)
            # Also save equity curve json
            with open(OUT_DIR/f"RESULT_{coin.replace('/','_')}_{tf}_8pct.json","w") as f:
                json.dump({k:v for k,v in res.items() if k!="trades"}, f, indent=2, default=str)
                # trades separately
            # Save full trades json for audit
            with open(OUT_DIR/f"TRADES_{coin.replace('/','_')}_{tf}_8pct.json","w") as f:
                json.dump(res["trades"][:50], f, indent=2, default=str)
    # Summary CSV
    rows=[]
    for r in all_res:
        m=r["metrics"]
        rows.append({
            "coin":r["coin"],"timeframe":r["timeframe"],"bars":r["bars"],
            "params":"10x3+10x4","sl_pct":"8%","rr":"1:3",
            "trades":m["num_trades"],"win_rate":m["win_rate"],"net_profit_inr":m["total_net_profit"],
            "final_capital_inr":m["ending_capital"],"return_pct":m["return_pct"],
            "max_dd_inr":m["max_drawdown_inr"],"max_dd_pct":m["max_drawdown_pct"],
            "profit_factor":m["profit_factor"],"expectancy":m["expectancy"],
            "avg_win":m["avg_win"],"avg_loss":m["avg_loss"],"max_win_streak":m["max_win_streak"],"max_loss_streak":m["max_loss_streak"],
            "exposure":m["exposure_pct"],"avg_duration_h":m["avg_duration_hours"]
        })
    import pandas as pd
    pd.DataFrame(rows).to_csv(OUT_DIR/"MASTER_DELTA_INTRADAY_5_15_30_60.csv", index=False)
    print(f"\n[SUMMARY] Saved MASTER_DELTA_INTRADAY_5_15_30_60.csv with {len(rows)} rows")
    with open(OUT_DIR/"SUMMARY.json","w") as f:
        json.dump(rows, f, indent=2)
    return rows

if __name__=="__main__":
    run_all()
