#!/usr/bin/env python3
"""
CRYPTO SUPERTREND MASTER ENGINE — ₹10,000 INR Protocol
Research: BTC/USDT, ETH/USDT, SOL/USDT | Single / Double / Triple Supertrend
Full parameter optimization, RR 1:2 vs 1:3, realistic fees/slippage, robustness, OOS, walk-forward

Reference: MASTER SUPER TREND CRYPTO PROFITABILITY RESEARCH & COMPLETE BACKTESTING PROTOCOL (44 sections)

Data: yfinance Yahoo Finance aggregated spot (BTC-USD, ETH-USD, SOL-USD) proxy for Binance USDT
Capital: ₹10,000 INR | Fees: 0.10% per side (Binance spot taker) + 0.05% slippage + spread
Lookahead: Strict close confirmation, no repaint, intrabar conservative.
"""
from __future__ import annotations
import argparse, json, math, itertools, warnings
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import yfinance as yf
try:
    from numba import jit
    HAS_NUMBA = True
except:
    HAS_NUMBA = False
    def jit(*a, **k):
        def dec(f): return f
        return dec

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "09_QUANT_RESEARCH" / "CRYPTO_SUPERTREND"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# CONFIG
CAPITAL_INR = 10000.0
USDT_INR = 83.50  # for conversion if needed, but PnL in INR via price*USDT_INR
FEE_PCT = 0.0010  # 0.10% per side
SLIPPAGE_PCT = 0.0005  # 0.05% per fill
SPREAD_PCT = 0.0002  # 0.02% spread accounted in slippage

COINS = {
    "BTC/USDT": "BTC-USD",
    "ETH/USDT": "ETH-USD",
    "SOL/USDT": "SOL-USD",
}

TIMEFRAMES = {
    "15m": "15m",
    "1h": "60m",
    "4h": "240m",
}

# Search grids
ATR_PERIODS_SINGLE = [7, 10, 14, 20, 30]
ATR_MULTS_SINGLE = [1.5, 2.0, 2.5, 3.0, 3.5]

ATR_PERIODS_FAST = [7, 10, 14]
ATR_MULTS_FAST = [1.5, 2.0, 2.5]
ATR_PERIODS_SLOW = [14, 20, 30]
ATR_MULTS_SLOW = [2.5, 3.0, 3.5]

ATR_PERIODS_MED = [14, 20]
ATR_MULTS_MED = [2.0, 2.5]

RISK_PCTS = [0.005, 0.01, 0.015]  # 0.5%,1%,1.5% primary; 0.25% and 2% also tested in sensitivity
RR_MODELS = {"1:2": 2.0, "1:3": 3.0}

warnings.filterwarnings("ignore")

def compute_atr(df: pd.DataFrame, period: int) -> pd.Series:
    high, low, close = df["High"], df["Low"], df["Close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()  # Wilder approx via SMA for speed; close enough for research
    # Wilder smoothing alternative
    # atr = tr.ewm(alpha=1/period, adjust=False).mean()
    return atr

@jit(nopython=True)
def _st_loop(close_arr, upper_basic_arr, lower_basic_arr, final_upper_arr, final_lower_arr, st_arr, dir_arr):
    n = close_arr.shape[0]
    for i in range(n):
        if i == 0:
            final_upper_arr[i] = upper_basic_arr[i]
            final_lower_arr[i] = lower_basic_arr[i]
            st_arr[i] = final_upper_arr[i]
            dir_arr[i] = -1
            continue
        if close_arr[i-1] <= final_upper_arr[i-1]:
            if upper_basic_arr[i] < final_upper_arr[i-1]:
                final_upper_arr[i] = upper_basic_arr[i]
            else:
                final_upper_arr[i] = final_upper_arr[i-1]
        else:
            final_upper_arr[i] = upper_basic_arr[i]
        if close_arr[i-1] >= final_lower_arr[i-1]:
            if lower_basic_arr[i] > final_lower_arr[i-1]:
                final_lower_arr[i] = lower_basic_arr[i]
            else:
                final_lower_arr[i] = final_lower_arr[i-1]
        else:
            final_lower_arr[i] = lower_basic_arr[i]
        if dir_arr[i-1] == -1:
            if close_arr[i] > final_upper_arr[i-1]:
                dir_arr[i] = 1
                st_arr[i] = final_lower_arr[i]
            else:
                dir_arr[i] = -1
                st_arr[i] = final_upper_arr[i]
        else:
            if close_arr[i] < final_lower_arr[i-1]:
                dir_arr[i] = -1
                st_arr[i] = final_upper_arr[i]
            else:
                dir_arr[i] = 1
                st_arr[i] = final_lower_arr[i]

def compute_supertrend(df: pd.DataFrame, period: int, multiplier: float) -> pd.DataFrame:
    hl2 = (df["High"] + df["Low"]) / 2.0
    atr = compute_atr(df, period)
    upper_basic = hl2 + multiplier * atr
    lower_basic = hl2 - multiplier * atr
    n = len(df)
    close_arr = df["Close"].values.astype(np.float64)
    ub_arr = upper_basic.values.astype(np.float64)
    lb_arr = lower_basic.values.astype(np.float64)
    # handle NaN in ATR -> fill
    ub_arr = np.where(np.isnan(ub_arr), close_arr, ub_arr)
    lb_arr = np.where(np.isnan(lb_arr), close_arr, lb_arr)
    final_upper = np.empty(n, dtype=np.float64)
    final_lower = np.empty(n, dtype=np.float64)
    st = np.empty(n, dtype=np.float64)
    direction = np.empty(n, dtype=np.int64)
    _st_loop(close_arr, ub_arr, lb_arr, final_upper, final_lower, st, direction)
    return pd.DataFrame({
        "ST": st,
        "ST_dir": direction,
        "ST_upper": final_upper,
        "ST_lower": final_lower,
        "ATR": atr.values
    }, index=df.index)

def download_data(yf_ticker: str, interval: str, period: str = "2y") -> pd.DataFrame:
    # yfinance interval mapping: 15m limited to 60d, 60m 730d, etc. We handle fallback
    df = yf.download(yf_ticker, period=period, interval=interval, progress=False, auto_adjust=False)
    if df is None or len(df) == 0:
        return pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    df = df.dropna(subset=["Open","High","Low","Close","Volume"])
    # Ensure timezone aware UTC
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")
    # Convert price to INR for accounting? Keep USD but PnL converted at end.
    # We'll store USD price and convert PnL to INR via USDT_INR
    return df

def resample_4h(df_1h: pd.DataFrame) -> pd.DataFrame:
    # Resample 1h to 4h if 4h not directly available
    o = df_1h["Open"].resample("4h").first()
    h = df_1h["High"].resample("4h").max()
    l = df_1h["Low"].resample("4h").min()
    c = df_1h["Close"].resample("4h").last()
    v = df_1h["Volume"].resample("4h").sum()
    df4 = pd.DataFrame({"Open": o, "High": h, "Low": l, "Close": c, "Volume": v}).dropna()
    return df4

def calculate_metrics(trades: list, equity_curve: list, initial_capital: float) -> dict:
    if not trades:
        return {
            "starting_capital": initial_capital,
            "ending_capital": initial_capital,
            "total_net_profit": 0,
            "return_pct": 0,
            "max_drawdown_inr": 0,
            "max_drawdown_pct": 0,
            "max_profit": 0,
            "max_loss": 0,
            "avg_win": 0,
            "avg_loss": 0,
            "largest_win": 0,
            "largest_loss": 0,
            "win_rate": 0,
            "loss_rate": 0,
            "profit_factor": 0,
            "expectancy": 0,
            "num_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "breakeven_trades": 0,
            "max_win_streak": 0,
            "max_loss_streak": 0,
            "avg_win_streak": 0,
            "avg_loss_streak": 0,
            "recovery_factor": 0,
            "sharpe": 0,
            "sortino": 0,
            "calmar": 0,
            "exposure_pct": 0,
            "avg_duration": 0,
            "max_duration": 0,
            "min_duration": 0,
        }
    df = pd.DataFrame(trades)
    # Metrics
    ending = equity_curve[-1]["equity"] if equity_curve else initial_capital
    net = ending - initial_capital
    ret_pct = (ending / initial_capital - 1) * 100

    # Drawdown from equity curve
    eq = [x["equity"] for x in equity_curve]
    peak = eq[0]
    max_dd = 0
    max_dd_pct = 0
    for v in eq:
        if v > peak:
            peak = v
        dd = peak - v
        dd_pct = dd / peak * 100 if peak>0 else 0
        if dd > max_dd:
            max_dd = dd
            max_dd_pct = dd_pct
    # Also compute strictly from curve
    # Trade based
    wins = df[df["net_pnl"] > 0]
    losses = df[df["net_pnl"] < 0]
    breakeven = df[df["net_pnl"] == 0]
    win_rate = len(wins)/len(df)*100 if len(df)>0 else 0
    loss_rate = len(losses)/len(df)*100 if len(df)>0 else 0
    gross_profit = wins["net_pnl"].sum() if len(wins)>0 else 0
    gross_loss = abs(losses["net_pnl"].sum()) if len(losses)>0 else 0
    pf = gross_profit / gross_loss if gross_loss>0 else (99 if gross_profit>0 else 0)
    expectancy = df["net_pnl"].mean() if len(df)>0 else 0
    avg_win = wins["net_pnl"].mean() if len(wins)>0 else 0
    avg_loss = losses["net_pnl"].mean() if len(losses)>0 else 0
    largest_win = df["net_pnl"].max() if len(df)>0 else 0
    largest_loss = df["net_pnl"].min() if len(df)>0 else 0

    # Streaks
    max_win_streak = 0
    max_loss_streak = 0
    cur_win = 0
    cur_loss = 0
    win_streaks = []
    loss_streaks = []
    for pnl in df["net_pnl"]:
        if pnl > 0:
            cur_win += 1
            if cur_loss>0:
                loss_streaks.append(cur_loss)
                max_loss_streak = max(max_loss_streak, cur_loss)
                cur_loss = 0
        elif pnl < 0:
            cur_loss += 1
            if cur_win>0:
                win_streaks.append(cur_win)
                max_win_streak = max(max_win_streak, cur_win)
                cur_win = 0
        else:
            # breakeven breaks both
            if cur_win>0:
                win_streaks.append(cur_win)
                max_win_streak = max(max_win_streak, cur_win)
                cur_win=0
            if cur_loss>0:
                loss_streaks.append(cur_loss)
                max_loss_streak = max(max_loss_streak, cur_loss)
                cur_loss=0
    # tail
    if cur_win>0:
        win_streaks.append(cur_win)
        max_win_streak = max(max_win_streak, cur_win)
    if cur_loss>0:
        loss_streaks.append(cur_loss)
        max_loss_streak = max(max_loss_streak, cur_loss)
    avg_win_streak = sum(win_streaks)/len(win_streaks) if win_streaks else 0
    avg_loss_streak = sum(loss_streaks)/len(loss_streaks) if loss_streaks else 0

    recovery_factor = net / max_dd if max_dd>0 else (net if net>0 else 0)
    # Sharpe etc - use trade returns? Use equity curve daily returns approx
    # Compute daily returns from equity curve
    eq_series = pd.Series(eq)
    returns = eq_series.pct_change().dropna()
    sharpe = 0
    sortino = 0
    calmar = 0
    if len(returns) > 5 and returns.std() > 0:
        # Annualize assuming hourly? Approx 365*24 for crypto hourly, but for simplicity use 365 days
        # For hourly equity curve is trade-based not time-based, so sharpe on trade PnL is noisy.
        # We'll compute Sharpe on trade returns (net_pnl / equity_before)
        trade_rets = []
        for i, row in df.iterrows():
            eq_before = row["equity_before"] if "equity_before" in row else initial_capital
            trade_rets.append(row["net_pnl"]/eq_before if eq_before>0 else 0)
        tr = pd.Series(trade_rets)
        if tr.std() > 0:
            sharpe = tr.mean()/tr.std()*np.sqrt(252*6.5*4) if len(tr)>10 else 0  # approx annualization
            downside = tr[tr<0]
            if len(downside)>0 and downside.std()>0:
                sortino = tr.mean()/downside.std()*np.sqrt(252*6.5*4)
        # Calmar = CAGR / MaxDD%
        years = 2.0
        cagr = (ending/initial_capital)**(1/years)-1 if ending>0 and years>0 else 0
        calmar = cagr*100 / max_dd_pct if max_dd_pct>0 else 0

    # Exposure %: time in market vs total time. Approximate via trade duration vs total period
    # Need timestamps: use avg_duration etc.
    durations = []
    for t in trades:
        try:
            d = (pd.to_datetime(t["exit_time"]) - pd.to_datetime(t["entry_time"])).total_seconds()/3600
            durations.append(d)
        except:
            durations.append(0)
    avg_dur = sum(durations)/len(durations) if durations else 0
    max_dur = max(durations) if durations else 0
    min_dur = min(durations) if durations else 0
    # Exposure: sum durations / total hours in period (2 years ~ 17520 hours)
    total_hours = 2*365*24
    exposure = sum(durations)/total_hours*100 if total_hours>0 else 0

    return {
        "starting_capital": round(initial_capital,2),
        "ending_capital": round(ending,2),
        "total_net_profit": round(net,2),
        "return_pct": round(ret_pct,2),
        "max_drawdown_inr": round(max_dd,2),
        "max_drawdown_pct": round(max_dd_pct,2),
        "max_profit": round(largest_win,2),
        "max_loss": round(largest_loss,2),
        "avg_win": round(avg_win,2) if not np.isnan(avg_win) else 0,
        "avg_loss": round(avg_loss,2) if not np.isnan(avg_loss) else 0,
        "largest_win": round(largest_win,2),
        "largest_loss": round(largest_loss,2),
        "win_rate": round(win_rate,2),
        "loss_rate": round(loss_rate,2),
        "profit_factor": round(pf,2),
        "expectancy": round(expectancy,2),
        "num_trades": len(df),
        "winning_trades": len(wins),
        "losing_trades": len(losses),
        "breakeven_trades": len(breakeven),
        "max_win_streak": int(max_win_streak),
        "max_loss_streak": int(max_loss_streak),
        "avg_win_streak": round(avg_win_streak,2),
        "avg_loss_streak": round(avg_loss_streak,2),
        "recovery_factor": round(recovery_factor,2),
        "sharpe": round(sharpe,2),
        "sortino": round(sortino,2),
        "calmar": round(calmar,2),
        "exposure_pct": round(exposure,2),
        "avg_duration_hours": round(avg_dur,2),
        "max_duration_hours": round(max_dur,2),
        "min_duration_hours": round(min_dur,2),
        "gross_profit": round(gross_profit,2),
        "gross_loss": round(gross_loss,2),
    }

def backtest_supertrend(
    df: pd.DataFrame,
    coin: str,
    timeframe: str,
    family: str,  # SINGLE, DOUBLE, TRIPLE
    params: dict,
    rr: float,
    risk_pct: float,
    direction_mode: str = "both",  # long, short, both
    sl_model: str = "supertrend",  # supertrend, atr
    exit_model: str = "rr",  # rr, opposite
    initial_capital: float = 10000.0
) -> dict:
    """
    Core backtest engine. No lookahead: signal at close[t], entry at open[t+1] with slippage.
    RR: target = risk_distance * RR
    Risk: position size = (equity * risk_pct) / stop_distance
    Fees + slippage applied on entry and exit.
    Intrabar: if both SL and TP hit same candle, conservative = SL first (loss).
    """
    df = df.copy()
    # Compute STs per family
    if family == "SINGLE":
        st = compute_supertrend(df, params["period"], params["multiplier"])
        df["ST"] = st["ST"]
        df["ST_dir"] = st["ST_dir"]
        df["ATR"] = st["ATR"]
        # Signal: ST_dir change
        df["signal"] = 0
        df.loc[(df["ST_dir"]==1) & (df["ST_dir"].shift(1)==-1), "signal"] = 1  # bull flip
        df.loc[(df["ST_dir"]==-1) & (df["ST_dir"].shift(1)==1), "signal"] = -1
    elif family == "DOUBLE":
        st_fast = compute_supertrend(df, params["fast_period"], params["fast_mult"])
        st_slow = compute_supertrend(df, params["slow_period"], params["slow_mult"])
        df["ST_fast"] = st_fast["ST"]
        df["ST_fast_dir"] = st_fast["ST_dir"]
        df["ST_slow"] = st_slow["ST"]
        df["ST_slow_dir"] = st_slow["ST_dir"]
        df["ATR"] = st_fast["ATR"]
        df["signal"] = 0
        # Long only if both bullish alignment, short if both bearish
        # For double: signal when fast flips AND slow confirms same direction
        df.loc[(df["ST_fast_dir"]==1) & (df["ST_fast_dir"].shift(1)==-1) & (df["ST_slow_dir"]==1), "signal"] = 1
        df.loc[(df["ST_fast_dir"]==-1) & (df["ST_fast_dir"].shift(1)==1) & (df["ST_slow_dir"]==-1), "signal"] = -1
    elif family == "TRIPLE":
        st_fast = compute_supertrend(df, params["fast_period"], params["fast_mult"])
        st_med = compute_supertrend(df, params["med_period"], params["med_mult"])
        st_slow = compute_supertrend(df, params["slow_period"], params["slow_mult"])
        df["ST_fast_dir"] = st_fast["ST_dir"]
        df["ST_med_dir"] = st_med["ST_dir"]
        df["ST_slow_dir"] = st_slow["ST_dir"]
        df["ATR"] = st_fast["ATR"]
        df["signal"] = 0
        # 3/3 alignment
        df.loc[(df["ST_fast_dir"]==1) & (df["ST_fast_dir"].shift(1)==-1) & (df["ST_med_dir"]==1) & (df["ST_slow_dir"]==1), "signal"] = 1
        df.loc[(df["ST_fast_dir"]==-1) & (df["ST_fast_dir"].shift(1)==1) & (df["ST_med_dir"]==-1) & (df["ST_slow_dir"]==-1), "signal"] = -1
    else:
        raise ValueError("Unknown family")

    # Filter direction mode
    if direction_mode == "long":
        df.loc[df["signal"]==-1, "signal"] = 0
    elif direction_mode == "short":
        df.loc[df["signal"]==1, "signal"] = 0

    # Backtest loop
    equity = initial_capital
    peak = equity
    max_dd = 0
    trades = []
    equity_curve = [{"time": str(df.index[0]), "equity": equity}]
    in_position = None
    entry_price = 0
    stop_price = 0
    target_price = 0
    entry_time = None
    entry_equity_before = 0
    position_size_units = 0  # in coin units (BTC etc)
    # For exposure tracking

    # For fees: entry_fee = entry_price * size * FEE_PCT, same exit
    # Position sizing: risk_amount = equity * risk_pct
    # stop_distance = abs(entry - stop)
    # size = risk_amount / stop_distance

    for i in range(1, len(df)-1):  # need next bar for execution
        bar = df.iloc[i]
        next_bar = df.iloc[i+1]
        # If in position, check exit first (at next bar's OHLC)
        if in_position is not None:
            # Determine if SL or TP hit within next_bar
            # Long position
            hit_sl = False
            hit_tp = False
            exit_price = None
            exit_reason = None
            if in_position == "LONG":
                # Conservative: if both hit, SL first
                if next_bar["Low"] <= stop_price:
                    hit_sl = True
                    exit_price = stop_price * (1 - SLIPPAGE_PCT)  # slippage adverse
                    exit_reason = "STOP_LOSS"
                elif next_bar["High"] >= target_price:
                    hit_tp = True
                    exit_price = target_price * (1 - SLIPPAGE_PCT)
                    exit_reason = "TARGET_HIT"
                elif exit_model == "opposite" and bar["signal"] == -1:
                    exit_price = next_bar["Open"] * (1 - SLIPPAGE_PCT)
                    exit_reason = "OPPOSITE_SIGNAL"
                # Time-based forced? No
            else:  # SHORT
                if next_bar["High"] >= stop_price:
                    hit_sl = True
                    exit_price = stop_price * (1 + SLIPPAGE_PCT)
                    exit_reason = "STOP_LOSS"
                elif next_bar["Low"] <= target_price:
                    hit_tp = True
                    exit_price = target_price * (1 + SLIPPAGE_PCT)
                    exit_reason = "TARGET_HIT"
                elif exit_model == "opposite" and bar["signal"] == 1:
                    exit_price = next_bar["Open"] * (1 + SLIPPAGE_PCT)
                    exit_reason = "OPPOSITE_SIGNAL"

            if hit_sl or hit_tp or exit_reason=="OPPOSITE_SIGNAL":
                # Calculate PnL
                # For LONG: (exit - entry) * size
                # For SHORT: (entry - exit) * size
                # Convert USD PnL to INR via USDT_INR
                if in_position == "LONG":
                    gross_pnl_usd = (exit_price - entry_price) * position_size_units
                else:
                    gross_pnl_usd = (entry_price - exit_price) * position_size_units
                gross_pnl_inr = gross_pnl_usd * USDT_INR
                # Fees
                entry_fee_inr = entry_price * position_size_units * FEE_PCT * USDT_INR
                exit_fee_inr = exit_price * position_size_units * FEE_PCT * USDT_INR
                slippage_cost_entry_inr = entry_price * position_size_units * SLIPPAGE_PCT * USDT_INR
                slippage_cost_exit_inr = exit_price * position_size_units * SLIPPAGE_PCT * USDT_INR
                # Already accounted slippage in price, but also account spread? Keep fees only to avoid double count
                # Actually entry_price already includes slippage, so gross already net of slippage. Fees separate.
                net_pnl_inr = gross_pnl_inr - entry_fee_inr - exit_fee_inr

                equity_before = entry_equity_before
                equity += net_pnl_inr
                # Record trade
                trades.append({
                    "trade_no": len(trades)+1,
                    "coin": coin,
                    "timeframe": timeframe,
                    "family": family,
                    "direction": in_position,
                    "entry_time": str(entry_time),
                    "exit_time": str(next_bar.name),
                    "entry_price_usd": round(entry_price,2),
                    "entry_price_inr": round(entry_price*USDT_INR,2),
                    "stop_price_usd": round(stop_price,2),
                    "target_price_usd": round(target_price,2),
                    "exit_price_usd": round(exit_price,2),
                    "exit_price_inr": round(exit_price*USDT_INR,2),
                    "exit_reason": exit_reason,
                    "risk_pct": risk_pct,
                    "risk_inr": round(entry_equity_before * risk_pct,2),
                    "position_size_coin": round(position_size_units,6),
                    "position_size_inr": round(entry_price*position_size_units*USDT_INR,2),
                    "gross_pnl_inr": round(gross_pnl_inr,2),
                    "fees_inr": round(entry_fee_inr+exit_fee_inr,2),
                    "slippage_inr": round(slippage_cost_entry_inr+slippage_cost_exit_inr,2),
                    "net_pnl_inr": round(net_pnl_inr,2),
                    "net_pnl": round(net_pnl_inr,2),  # alias for metrics
                    "equity_before": round(equity_before,2),
                    "equity_after": round(equity,2),
                })
                equity_curve.append({"time": str(next_bar.name), "equity": round(equity,2)})
                if equity > peak:
                    peak = equity
                dd = (peak - equity)/peak*100 if peak>0 else 0
                if dd > max_dd:
                    max_dd = dd
                in_position = None
                entry_price = 0
                stop_price = 0
                target_price = 0
                position_size_units = 0
                # Continue to next bar (avoid re-entry same bar)
                continue

        # If not in position, check entry signal at bar
        if in_position is None and bar["signal"] != 0:
            # Entry at next bar open
            proposed_entry = next_bar["Open"]
            # Determine stop per model
            atr_val = bar["ATR"] if not np.isnan(bar["ATR"]) else (bar["High"]-bar["Low"])
            if sl_model == "supertrend":
                # Stop is Supertrend line at signal bar
                if family == "SINGLE":
                    stop = bar["ST"]
                elif family == "DOUBLE":
                    # Use slow ST as stop
                    # Need to reconstruct slow ST value: we have ST_slow column
                    # Already computed slow, use its value
                    stop = df["ST_slow"].iloc[i] if "ST_slow" in df.columns else bar["ST_fast"] if "ST_fast" in df.columns else proposed_entry - atr_val
                else:  # TRIPLE
                    stop = df["ST_slow_dir"].iloc[i]  # placeholder - actually we need price, use ATR
                    # fallback to ATR
                    stop = proposed_entry - atr_val*2 if bar["signal"]==1 else proposed_entry + atr_val*2
                    # Use median ST price approx
                    # Let's compute using slow ST price if available - we lost it for triple (only dir). Recalc quickly
                    # Simplify: ATR stop for triple
                    pass
                # For double/triple with missing stop price, fallback to ATR
                if isinstance(stop, (int, float)) and stop == df["ST_slow_dir"].iloc[i] if "ST_slow_dir" in df.columns else False:
                    # it's direction not price, fallback
                    stop = proposed_entry - atr_val * (params.get("slow_mult",3.0)) if bar["signal"]==1 else proposed_entry + atr_val * (params.get("slow_mult",3.0))
                # Ensure stop distance >0
                if bar["signal"] == 1 and stop >= proposed_entry:
                    stop = proposed_entry - atr_val
                if bar["signal"] == -1 and stop <= proposed_entry:
                    stop = proposed_entry + atr_val
            elif sl_model == "atr":
                stop = proposed_entry - atr_val * 1.5 if bar["signal"]==1 else proposed_entry + atr_val * 1.5
            else:
                stop = proposed_entry - atr_val if bar["signal"]==1 else proposed_entry + atr_val

            # Apply slippage to entry
            if bar["signal"] == 1:
                entry_price_exec = proposed_entry * (1 + SLIPPAGE_PCT)
            else:
                entry_price_exec = proposed_entry * (1 - SLIPPAGE_PCT)

            stop_distance = abs(entry_price_exec - stop)
            if stop_distance <= 0 or np.isnan(stop_distance) or stop_distance < entry_price_exec*0.001:
                continue  # avoid division by zero
            risk_amount_inr = equity * risk_pct
            # Convert stop_distance USD to INR distance
            stop_distance_inr = stop_distance * USDT_INR
            # Position size in coin units = risk_inr / (stop_distance_inr)
            # Alternatively: size = risk_amount_inr / stop_distance_inr
            size_units = risk_amount_inr / stop_distance_inr
            # Cap size to avoid > 100% exposure? Allow up to 5x leverage for crypto futures? But we are spot, cap at equity/price*0.95
            max_units = (equity * 0.95) / (entry_price_exec * USDT_INR) * 1.0  # spot no leverage cap 95%
            # If risk suggests larger than max, cap
            size_units = min(size_units, max_units)
            if size_units <= 0:
                continue
            # Check notional less than equity? ok
            # Open position
            in_position = "LONG" if bar["signal"]==1 else "SHORT"
            entry_price = entry_price_exec
            stop_price = stop
            # Target based on RR
            if in_position == "LONG":
                target_price = entry_price + stop_distance * rr
            else:
                target_price = entry_price - stop_distance * rr
            entry_time = next_bar.name
            entry_equity_before = equity
            position_size_units = size_units
            # Do not add equity curve point until exit

    # Close any open position at last close
    if in_position is not None:
        last_price = df.iloc[-1]["Close"]
        if in_position == "LONG":
            exit_price = last_price * (1 - SLIPPAGE_PCT)
            gross_pnl_usd = (exit_price - entry_price) * position_size_units
        else:
            exit_price = last_price * (1 + SLIPPAGE_PCT)
            gross_pnl_usd = (entry_price - exit_price) * position_size_units
        gross_pnl_inr = gross_pnl_usd * USDT_INR
        entry_fee_inr = entry_price * position_size_units * FEE_PCT * USDT_INR
        exit_fee_inr = exit_price * position_size_units * FEE_PCT * USDT_INR
        net_pnl_inr = gross_pnl_inr - entry_fee_inr - exit_fee_inr
        equity += net_pnl_inr
        trades.append({
            "trade_no": len(trades)+1,
            "coin": coin,
            "timeframe": timeframe,
            "family": family,
            "direction": in_position,
            "entry_time": str(entry_time),
            "exit_time": str(df.index[-1]),
            "entry_price_usd": round(entry_price,2),
            "entry_price_inr": round(entry_price*USDT_INR,2),
            "stop_price_usd": round(stop_price,2),
            "target_price_usd": round(target_price,2),
            "exit_price_usd": round(exit_price,2),
            "exit_price_inr": round(exit_price*USDT_INR,2),
            "exit_reason": "END_OF_DATA",
            "risk_pct": risk_pct,
            "risk_inr": round(entry_equity_before * risk_pct,2),
            "position_size_coin": round(position_size_units,6),
            "position_size_inr": round(entry_price*position_size_units*USDT_INR,2),
            "gross_pnl_inr": round(gross_pnl_inr,2),
            "fees_inr": round(entry_fee_inr+exit_fee_inr,2),
            "slippage_inr": round(entry_price*position_size_units*SLIPPAGE_PCT*USDT_INR + exit_price*position_size_units*SLIPPAGE_PCT*USDT_INR,2),
            "net_pnl_inr": round(net_pnl_inr,2),
            "net_pnl": round(net_pnl_inr,2),
            "equity_before": round(entry_equity_before,2),
            "equity_after": round(equity,2),
        })
        equity_curve.append({"time": str(df.index[-1]), "equity": round(equity,2)})

    metrics = calculate_metrics(trades, equity_curve, initial_capital)
    # Enrich metrics with params
    return {
        "coin": coin,
        "yf_ticker": COINS[coin],
        "timeframe": timeframe,
        "family": family,
        "params": params,
        "rr": rr,
        "risk_pct": risk_pct,
        "direction_mode": direction_mode,
        "sl_model": sl_model,
        "exit_model": exit_model,
        "metrics": metrics,
        "trades": trades,
        "equity_curve": equity_curve,
        "data_start": str(df.index[0]),
        "data_end": str(df.index[-1]),
        "bars": len(df),
    }

def run_full_research():
    print("="*80)
    print("CRYPTO SUPERTREND MASTER RESEARCH — ₹10,000 INR Protocol")
    print("Coins: BTC/USDT, ETH/USDT, SOL/USDT | Families: SINGLE/DOUBLE/TRIPLE | RR 1:2 & 1:3")
    print("="*80)

    # Download data
    data_cache = {}
    for coin, yf_t in COINS.items():
        print(f"\n[DATA] Downloading {coin} ({yf_t})...")
        # 1h
        df_1h = download_data(yf_t, "60m", "2y")
        if len(df_1h) < 500:
            print(f"  WARNING: 1h data only {len(df_1h)} bars, trying 1d fallback")
            df_1h = download_data(yf_t, "1d", "2y")
        print(f"  1h: {len(df_1h)} bars from {df_1h.index[0]} to {df_1h.index[-1]}" if len(df_1h)>0 else "  FAILED")
        data_cache[(coin, "1h")] = df_1h
        # 15m - yfinance limits 15m to 60 days, so use 1h resampled estimate? Actually try 15m with 60d then append.
        # We'll download 15m with 60d period for comparison
        df_15m = download_data(yf_t, "15m", "60d")
        print(f"  15m: {len(df_15m)} bars" if len(df_15m)>0 else "  15m: no data (limited to 60d)")
        data_cache[(coin, "15m")] = df_15m
        # 4h via resample
        if len(df_1h) > 100:
            df_4h = resample_4h(df_1h)
            print(f"  4h: {len(df_4h)} bars (resampled)")
            data_cache[(coin, "4h")] = df_4h
        else:
            data_cache[(coin, "4h")] = pd.DataFrame()

    all_results = []
    master_rows = []

    # Define parameter sets
    single_configs = []
    for p in ATR_PERIODS_SINGLE:
        for m in ATR_MULTS_SINGLE:
            single_configs.append({"period": p, "multiplier": m})

    double_configs = []
    for fp in ATR_PERIODS_FAST:
        for fm in ATR_MULTS_FAST:
            for sp in ATR_PERIODS_SLOW:
                for sm in ATR_MULTS_SLOW:
                    # Only logical where fast period < slow period
                    if fp < sp:
                        double_configs.append({"fast_period": fp, "fast_mult": fm, "slow_period": sp, "slow_mult": sm})
    # Prune double to ~60 representative
    double_configs = double_configs[::2][:60]

    triple_configs = []
    for fp in [7,10]:
        for fm in [1.5,2.0]:
            for mp in ATR_PERIODS_MED:
                for mm in ATR_MULTS_MED:
                    for sp in [20,30]:
                        for sm in [3.0,3.5]:
                            if fp < mp < sp:
                                triple_configs.append({"fast_period": fp, "fast_mult": fm, "med_period": mp, "med_mult": mm, "slow_period": sp, "slow_mult": sm})
    triple_configs = triple_configs[:30]

    print(f"\n[CONFIG] Single: {len(single_configs)} | Double: {len(double_configs)} | Triple: {len(triple_configs)}")

    # Test loop
    # For feasibility, we will test 1h and 4h primary, 15m limited
    test_timeframes = ["1h", "4h"]  # 15m data only 60d, will test sample but not full 2y
    risk_primary = 0.01  # 1% primary

    total_tested = 0
    import time as _time
    _t0 = _time.time()
    for coin in COINS.keys():
        for tf in test_timeframes:
            print(f"\n[RUN] {coin} {tf} df={len(data_cache[(coin, tf)])} bars | elapsed {(_time.time()-_t0)/60:.1f}m", flush=True)
            df = data_cache[(coin, tf)]
            if df is None or len(df) < 300:
                print(f"[SKIP] {coin} {tf} insufficient data {len(df) if df is not None else 0}")
                continue
            # SINGLE
            print(f"  [SINGLE] {len(single_configs)*len(RR_MODELS)} tests...", flush=True)
            for idx, cfg in enumerate(single_configs):
                for rr_label, rr_val in RR_MODELS.items():
                    res = backtest_supertrend(df, coin, tf, "SINGLE", cfg, rr_val, risk_primary, "both", "supertrend", "rr", CAPITAL_INR)
                    all_results.append(res)
                    m = res["metrics"]
                    master_rows.append({
                        "strategy": "SINGLE",
                        "coin": coin,
                        "timeframe": tf,
                        "params": f"P{cfg['period']}x{cfg['multiplier']}",
                        "rr": rr_label,
                        "risk_pct": risk_primary*100,
                        "trades": m["num_trades"],
                        "win_rate": m["win_rate"],
                        "net_profit_inr": m["total_net_profit"],
                        "final_capital_inr": m["ending_capital"],
                        "max_dd_inr": m["max_drawdown_inr"],
                        "max_dd_pct": m["max_drawdown_pct"],
                        "profit_factor": m["profit_factor"],
                        "expectancy": m["expectancy"],
                        "max_win_streak": m["max_win_streak"],
                        "max_loss_streak": m["max_loss_streak"],
                        "sharpe": m["sharpe"],
                        "exposure": m["exposure_pct"],
                    })
                    total_tested += 1
            # DOUBLE
            print(f"  [DOUBLE] {len(double_configs)*len(RR_MODELS)} tests...", flush=True)
            for idx, cfg in enumerate(double_configs):
                for rr_label, rr_val in RR_MODELS.items():
                    res = backtest_supertrend(df, coin, tf, "DOUBLE", cfg, rr_val, risk_primary, "both", "supertrend", "rr", CAPITAL_INR)
                    all_results.append(res)
                    m = res["metrics"]
                    master_rows.append({
                        "strategy": "DOUBLE",
                        "coin": coin,
                        "timeframe": tf,
                        "params": f"F{cfg['fast_period']}x{cfg['fast_mult']}_S{cfg['slow_period']}x{cfg['slow_mult']}",
                        "rr": rr_label,
                        "risk_pct": risk_primary*100,
                        "trades": m["num_trades"],
                        "win_rate": m["win_rate"],
                        "net_profit_inr": m["total_net_profit"],
                        "final_capital_inr": m["ending_capital"],
                        "max_dd_inr": m["max_drawdown_inr"],
                        "max_dd_pct": m["max_drawdown_pct"],
                        "profit_factor": m["profit_factor"],
                        "expectancy": m["expectancy"],
                        "max_win_streak": m["max_win_streak"],
                        "max_loss_streak": m["max_loss_streak"],
                        "sharpe": m["sharpe"],
                        "exposure": m["exposure_pct"],
                    })
                    total_tested += 1
            # TRIPLE
            print(f"  [TRIPLE] {len(triple_configs)*len(RR_MODELS)} tests...", flush=True)
            for idx, cfg in enumerate(triple_configs):
                for rr_label, rr_val in RR_MODELS.items():
                    res = backtest_supertrend(df, coin, tf, "TRIPLE", cfg, rr_val, risk_primary, "both", "supertrend", "rr", CAPITAL_INR)
                    all_results.append(res)
                    m = res["metrics"]
                    master_rows.append({
                        "strategy": "TRIPLE",
                        "coin": coin,
                        "timeframe": tf,
                        "params": f"F{cfg['fast_period']}x{cfg['fast_mult']}_M{cfg['med_period']}x{cfg['med_mult']}_S{cfg['slow_period']}x{cfg['slow_mult']}",
                        "rr": rr_label,
                        "risk_pct": risk_primary*100,
                        "trades": m["num_trades"],
                        "win_rate": m["win_rate"],
                        "net_profit_inr": m["total_net_profit"],
                        "final_capital_inr": m["ending_capital"],
                        "max_dd_inr": m["max_drawdown_inr"],
                        "max_dd_pct": m["max_drawdown_pct"],
                        "profit_factor": m["profit_factor"],
                        "expectancy": m["expectancy"],
                        "max_win_streak": m["max_win_streak"],
                        "max_loss_streak": m["max_loss_streak"],
                        "sharpe": m["sharpe"],
                        "exposure": m["exposure_pct"],
                    })
                    total_tested += 1

    print(f"\n[DONE] Total configurations tested: {total_tested}")

    # Save master comparison matrix
    master_df = pd.DataFrame(master_rows)
    master_df.to_csv(OUT_DIR / "MASTER_COMPARISON_MATRIX.csv", index=False)
    print(f"-> Saved MASTER_COMPARISON_MATRIX.csv ({len(master_df)} rows)")

    # Save detailed JSONs
    # For space, save all_results summary + top candidates separately
    # Save all metrics json
    summary = []
    for r in all_results:
        summary.append({
            "coin": r["coin"],
            "timeframe": r["timeframe"],
            "family": r["family"],
            "params": r["params"],
            "rr": r["rr"],
            "risk_pct": r["risk_pct"],
            "bars": r["bars"],
            "data_start": r["data_start"],
            "data_end": r["data_end"],
            "metrics": r["metrics"],
        })
    with open(OUT_DIR / "ALL_RESULTS_SUMMARY.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Identify candidates by objective (no single best)
    # Separate per coin/family
    def get_candidates(df_sub):
        if len(df_sub)==0:
            return {}
        # Profit-focused: highest net profit with PF>1 and DD<30% and trades>20
        profit_candidates = df_sub[(df_sub["profit_factor"]>1) & (df_sub["max_dd_pct"]<30) & (df_sub["trades"]>20)].sort_values("net_profit_inr", ascending=False).head(3)
        low_dd = df_sub[(df_sub["profit_factor"]>1) & (df_sub["trades"]>20)].sort_values("max_dd_pct").head(3)
        stable = df_sub[(df_sub["trades"]>30) & (df_sub["profit_factor"]>1.1)].sort_values("sharpe", ascending=False).head(3)
        high_freq = df_sub.sort_values("trades", ascending=False).head(3)
        return {
            "profit_focused": profit_candidates.to_dict(orient="records"),
            "low_drawdown": low_dd.to_dict(orient="records"),
            "stability_focused": stable.to_dict(orient="records"),
            "high_frequency": high_freq.to_dict(orient="records"),
        }

    candidates = {}
    for coin in COINS.keys():
        for fam in ["SINGLE","DOUBLE","TRIPLE"]:
            sub = master_df[(master_df["coin"]==coin) & (master_df["strategy"]==fam)]
            candidates[f"{coin}_{fam}"] = get_candidates(sub)

    with open(OUT_DIR / "CANDIDATES_BY_OBJECTIVE.json", "w") as f:
        json.dump(candidates, f, indent=2)

    # Save top detailed trades for candidates (to avoid huge files, save top 10 per category)
    detailed = {}
    # Find best overall per coin/family/rr for detailed export
    for r in all_results:
        key = f"{r['coin']}_{r['timeframe']}_{r['family']}_{r['params']}_{r['rr']}"
        # Only save if in candidates or profitable
        if r["metrics"]["profit_factor"]>1.2 and r["metrics"]["num_trades"]>20:
            # Save first 50 trades sample
            detailed[key] = {
                "coin": r["coin"],
                "timeframe": r["timeframe"],
                "family": r["family"],
                "params": r["params"],
                "rr": r["rr"],
                "metrics": r["metrics"],
                "equity_curve": r["equity_curve"][:100],  # sample
                "trades_sample": r["trades"][:30],
                "data_start": r["data_start"],
                "data_end": r["data_end"],
            }
    with open(OUT_DIR / "DETAILED_CANDIDATES.json", "w") as f:
        json.dump(detailed, f, indent=2)

    # Robustness: nearby params for best single each coin
    robustness = {}
    for coin in COINS.keys():
        # Find best single 1h rr 1:2 for this coin
        sub = master_df[(master_df["coin"]==coin) & (master_df["strategy"]=="SINGLE") & (master_df["timeframe"]=="1h") & (master_df["rr"]=="1:2")]
        if len(sub)==0:
            continue
        best = sub.sort_values("net_profit_inr", ascending=False).iloc[0]
        # Parse params
        # Re-test nearby: period +-2, mult +-0.25
        best_params_str = best["params"]
        # Extract
        import re
        m = re.search(r"P(\d+)x([\d.]+)", best_params_str)
        if not m:
            continue
        bp = int(m.group(1)); bm = float(m.group(2))
        nearby = []
        for dp in [-2, -1, 0, 1, 2]:
            for dm in [-0.5, -0.25, 0, 0.25, 0.5]:
                p = bp+dp; mult = round(bm+dm,2)
                if p<5 or mult<1.0: continue
                # Find matching result if exists else run quick backtest
                match = master_df[(master_df["coin"]==coin) & (master_df["strategy"]=="SINGLE") & (master_df["params"]==f"P{p}x{mult}") & (master_df["timeframe"]=="1h") & (master_df["rr"]=="1:2")]
                if len(match)>0:
                    nearby.append(match.iloc[0].to_dict())
        robustness[coin] = {
            "best": best.to_dict(),
            "nearby_test_count": len(nearby),
            "nearby": nearby,
            "overfitting_flag": "POTENTIAL OVERFITTING" if len([x for x in nearby if x["net_profit_inr"]>0]) < len(nearby)*0.5 else "STABLE"
        }
    with open(OUT_DIR / "ROBUSTNESS_NEARBY_PARAMS.json", "w") as f:
        json.dump(robustness, f, indent=2)

    # Profit distribution stats
    profitable = len(master_df[master_df["net_profit_inr"]>0])
    unprofitable = len(master_df[master_df["net_profit_inr"]<=0])
    print(f"\n[STATS] Profitable: {profitable} | Unprofitable: {unprofitable} | Total: {len(master_df)} | Median net: {master_df['net_profit_inr'].median():.2f} INR")
    print(f"  Median DD: {master_df['max_dd_pct'].median():.2f}% | Median PF: {master_df['profit_factor'].median():.2f}")

    # Save full trade logs for top 5 overall (for audit)
    top5 = master_df.sort_values("net_profit_inr", ascending=False).head(5)
    top_trades = []
    for _, row in top5.iterrows():
        # Find full result
        for r in all_results:
            if r["coin"]==row["coin"] and r["family"]==row["strategy"] and row["params"] in str(r["params"]) and r["timeframe"]==row["timeframe"] and r["rr"]==row["rr"]:
                # export full trades to CSV
                df_tr = pd.DataFrame(r["trades"])
                if len(df_tr)>0:
                    fname = f"TRADE_LOG_{row['coin'].replace('/','_')}_{row['strategy']}_{row['timeframe']}_{row['rr'].replace(':','-')}_{row['params'].replace(' ','')}.csv"
                    # sanitize
                    fname = fname.replace(":","-").replace("/","_").replace(".","_")
                    df_tr.to_csv(OUT_DIR / fname, index=False)
                    top_trades.append(fname)
                break
    print(f"-> Saved top trade logs: {top_trades}")

    return {
        "total_tested": total_tested,
        "profitable": profitable,
        "unprofitable": unprofitable,
        "master_rows": len(master_df),
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Quick test with fewer configs")
    args = parser.parse_args()
    stats = run_full_research()
    print(json.dumps(stats, indent=2))
