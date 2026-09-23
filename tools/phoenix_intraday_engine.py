#!/usr/bin/env python3
"""
phoenix_intraday_engine.py — PHOENIX RISING V2.0 PURE INTRADAY QUANT ENGINE
Strictly Intraday: ZERO OVERNIGHT HOLDINGS. 100% Cash at market close.

Reference:
  - 00_SYSTEM/05_PHOENIX_RISING_V2_QUANT_SPEC.md
  - User Constraint: "tumhe sirf intraday hi allowed hai"

Components:
  1. Real Intraday Data Loader (2 years of 1h / 5m bars from yfinance)
  2. Opening Range Volatility Expansion Strategy (ORB-Intraday V2)
  3. Mandatory 15:30 Hard Auto-Squareoff (Zero gap risk)
  4. Commission ($0.005/share) and Slippage (0.03%) Modeling
  5. Live Intraday Execution Plan Generator
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
QUANT_DIR = ROOT / "09_QUANT_RESEARCH"
QUANT_DIR.mkdir(parents=True, exist_ok=True)


def load_intraday_data(ticker: str = "QQQ", period: str = "2y") -> pd.DataFrame:
    """
    Downloads 2 years of 1-hour intraday candles from official exchange data via yfinance.
    """
    df = yf.download(ticker, period=period, interval="1h", progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    df = df.dropna(subset=["Open", "High", "Low", "Close", "Volume"])
    
    # ATR(14) on hourly bars
    prev_close = df["Close"].shift(1)
    tr = pd.concat([df["High"] - df["Low"], (df["High"] - prev_close).abs(), (df["Low"] - prev_close).abs()], axis=1).max(axis=1)
    df["ATR_14"] = tr.rolling(14).mean()
    
    df["Date"] = pd.to_datetime(df.index.date)
    df["Hour"] = df.index.hour
    df["Minute"] = df.index.minute
    return df


def run_intraday_backtest(ticker: str = "QQQ") -> dict:
    """
    Backtests a disciplined, selective Intraday Volatility Breakout strategy.
    Rule: 100% intraday. All positions closed before market close.
    """
    df = load_intraday_data(ticker=ticker, period="2y")
    days = sorted(df["Date"].unique())
    
    equity = 10000.0
    peak = equity
    max_dd = 0.0
    trades = []
    daily_equity_curve = []
    
    commission_per_share = 0.005
    slippage_pct = 0.0003
    
    for d in days:
        day_bars = df[df["Date"] == d].sort_index()
        if len(day_bars) < 5:
            continue
            
        # Bar 0 is Opening Range (09:30 - 10:30)
        first_bar = day_bars.iloc[0]
        or_high = float(first_bar["High"])
        or_low = float(first_bar["Low"])
        or_range = or_high - or_low
        atr = float(first_bar["ATR_14"])
        if np.isnan(atr) or atr <= 0:
            continue
            
        # SELECTIVITY FILTER: Only trade if Opening Range is significant (volatility expansion)
        # Avoid low-volatility chop days
        if or_range < (0.6 * atr) or or_range > (2.5 * atr):
            continue
            
        pos = None  # None, 'LONG', 'SHORT'
        entry_price = 0.0
        shares = 0
        stop_loss = 0.0
        target = 0.0
        entry_time = None
        
        for idx, row in day_bars.iloc[1:].iterrows():
            c = float(row["Close"])
            h = float(row["High"])
            l = float(row["Low"])
            is_last = (idx == day_bars.index[-1]) or (row["Hour"] >= 15 and row["Minute"] >= 30)
            
            # Position management
            if pos == "LONG":
                if h >= target:
                    exit_price = target * (1.0 - slippage_pct)
                    pnl = (exit_price - entry_price) * shares - (commission_per_share * shares * 2)
                    equity += pnl
                    trades.append({"date": str(d.date()), "ticker": ticker, "type": "LONG",
                                   "entry_time": str(entry_time), "exit_time": str(idx),
                                   "entry": round(entry_price, 2), "exit": round(exit_price, 2),
                                   "shares": shares, "pnl": round(pnl, 2), "reason": "TARGET_HIT"})
                    pos = None
                    break
                elif l <= stop_loss:
                    exit_price = stop_loss * (1.0 - slippage_pct)
                    pnl = (exit_price - entry_price) * shares - (commission_per_share * shares * 2)
                    equity += pnl
                    trades.append({"date": str(d.date()), "ticker": ticker, "type": "LONG",
                                   "entry_time": str(entry_time), "exit_time": str(idx),
                                   "entry": round(entry_price, 2), "exit": round(exit_price, 2),
                                   "shares": shares, "pnl": round(pnl, 2), "reason": "STOP_LOSS"})
                    pos = None
                    break
                elif is_last:
                    exit_price = c * (1.0 - slippage_pct)
                    pnl = (exit_price - entry_price) * shares - (commission_per_share * shares * 2)
                    equity += pnl
                    trades.append({"date": str(d.date()), "ticker": ticker, "type": "LONG",
                                   "entry_time": str(entry_time), "exit_time": str(idx),
                                   "entry": round(entry_price, 2), "exit": round(exit_price, 2),
                                   "shares": shares, "pnl": round(pnl, 2), "reason": "MANDATORY_EOD_SQUAREOFF"})
                    pos = None
                    break
                    
            elif pos == "SHORT":
                if l <= target:
                    exit_price = target * (1.0 + slippage_pct)
                    pnl = (entry_price - exit_price) * shares - (commission_per_share * shares * 2)
                    equity += pnl
                    trades.append({"date": str(d.date()), "ticker": ticker, "type": "SHORT",
                                   "entry_time": str(entry_time), "exit_time": str(idx),
                                   "entry": round(entry_price, 2), "exit": round(exit_price, 2),
                                   "shares": shares, "pnl": round(pnl, 2), "reason": "TARGET_HIT"})
                    pos = None
                    break
                elif h >= stop_loss:
                    exit_price = stop_loss * (1.0 + slippage_pct)
                    pnl = (entry_price - exit_price) * shares - (commission_per_share * shares * 2)
                    equity += pnl
                    trades.append({"date": str(d.date()), "ticker": ticker, "type": "SHORT",
                                   "entry_time": str(entry_time), "exit_time": str(idx),
                                   "entry": round(entry_price, 2), "exit": round(exit_price, 2),
                                   "shares": shares, "pnl": round(pnl, 2), "reason": "STOP_LOSS"})
                    pos = None
                    break
                elif is_last:
                    exit_price = c * (1.0 + slippage_pct)
                    pnl = (entry_price - exit_price) * shares - (commission_per_share * shares * 2)
                    equity += pnl
                    trades.append({"date": str(d.date()), "ticker": ticker, "type": "SHORT",
                                   "entry_time": str(entry_time), "exit_time": str(idx),
                                   "entry": round(entry_price, 2), "exit": round(exit_price, 2),
                                   "shares": shares, "pnl": round(pnl, 2), "reason": "MANDATORY_EOD_SQUAREOFF"})
                    pos = None
                    break
                    
            # Entry Signal (Only before 13:00 to leave time for movement)
            if pos is None and not is_last and row["Hour"] <= 12:
                # Long Breakout
                if c > or_high:
                    pos = "LONG"
                    entry_price = c * (1.0 + slippage_pct)
                    entry_time = idx
                    risk_dist = 0.8 * atr
                    stop_loss = entry_price - risk_dist
                    target = entry_price + (1.25 * risk_dist)  # Realistic 1:1.25 Intraday Target
                    shares = int((equity * 0.015) / risk_dist) if risk_dist > 0 else 0
                    shares = min(shares, int((equity * 1.25) / entry_price))
                    if shares <= 0:
                        pos = None
                # Short Breakout
                elif c < or_low:
                    pos = "SHORT"
                    entry_price = c * (1.0 - slippage_pct)
                    entry_time = idx
                    risk_dist = 0.8 * atr
                    stop_loss = entry_price + risk_dist
                    target = entry_price - (1.25 * risk_dist)
                    shares = int((equity * 0.015) / risk_dist) if risk_dist > 0 else 0
                    shares = min(shares, int((equity * 1.25) / entry_price))
                    if shares <= 0:
                        pos = None

        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak if peak > 0 else 0.0
        if dd > max_dd:
            max_dd = dd

        daily_equity_curve.append({"date": str(d.date()), "equity": round(equity, 2), "drawdown_pct": round(dd * 100, 2)})

    tdf = pd.DataFrame(trades)
    if not trades:
        return {"error": "No trades executed"}

    wins = tdf[tdf["pnl"] > 0]
    losses = tdf[tdf["pnl"] <= 0]
    win_rate = round(len(wins) / len(tdf) * 100, 2)
    gross_profit = round(wins["pnl"].sum(), 2)
    gross_loss = round(abs(losses["pnl"].sum()), 2)
    profit_factor = round(gross_profit / gross_loss, 2) if gross_loss > 0 else 99.0
    total_ret = round(((equity - 10000.0) / 10000.0) * 100, 2)
    cagr = round(((equity / 10000.0) ** (1.0 / 2.0) - 1.0) * 100, 2)

    return {
        "strategy_name": f"Phoenix Intraday ORB-Volatility ({ticker})",
        "tested_period": "2 Years (Hourly bars from 2024 to 2026)",
        "total_intraday_trades": len(tdf),
        "ending_equity": round(equity, 2),
        "total_return_pct": total_ret,
        "cagr_pct": cagr,
        "max_drawdown_pct": round(max_dd * 100, 2),
        "profit_factor": profit_factor,
        "win_rate_pct": win_rate,
        "gross_profit_usd": gross_profit,
        "gross_loss_usd": gross_loss,
        "exit_reason_breakdown": tdf["reason"].value_counts().to_dict(),
        "trades": trades,
        "daily_equity_curve": daily_equity_curve
    }


def get_live_intraday_plan(ticker: str = "QQQ") -> dict:
    """
    Generates exact minute-by-minute execution levels for today's trading session.
    """
    df = load_intraday_data(ticker=ticker, period="5d")
    latest_bar = df.iloc[-1]
    last_price = float(latest_bar["Close"])
    atr = float(latest_bar["ATR_14"]) if not np.isnan(latest_bar["ATR_14"]) else 5.0
    
    return {
        "ticker": ticker,
        "current_market_price": round(last_price, 2),
        "hourly_atr_14": round(atr, 2),
        "intraday_rules": {
            "session_open": "09:30 EST (DO NOT TRADE first 30-60 minutes)",
            "opening_range_calculation": "Record High (OR_High) and Low (OR_Low) at 10:30 EST",
            "long_trigger": f"Buy if 5m/1h candle closes ABOVE OR_High. Stop: Entry - ${round(0.8*atr, 2)}. Target: Entry + ${round(1.0*atr, 2)}",
            "short_trigger": f"Short if 5m/1h candle closes BELOW OR_Low. Stop: Entry + ${round(0.8*atr, 2)}. Target: Entry - ${round(1.0*atr, 2)}",
            "position_size_formula": f"Shares = Floor( $150 / ${round(0.8*atr, 2)} ) -> Approx {int(150 / (0.8*atr))} shares (1.5% fixed risk on $10k)",
            "mandatory_squareoff": "15:30 EST -> Market Sell/Cover regardless of PnL. Strictly 100% Cash overnight!"
        }
    }


def main():
    parser = argparse.ArgumentParser(description="PHOENIX RISING V2.0 Pure Intraday Engine")
    parser.add_argument("--backtest", action="store_true", help="Run 2-year intraday backtest on QQQ")
    parser.add_argument("--live-plan", action="store_true", help="Generate today's minute-by-minute intraday execution plan")
    parser.add_argument("--verify", action="store_true", help="Quick verification check")

    args = parser.parse_args()

    if args.live_plan:
        plan = get_live_intraday_plan()
        print("\n" + "="*70)
        print("     PHOENIX RISING V2.0 — TODAY'S INTRADAY EXECUTION PLAN")
        print("="*70)
        print(f"  Instrument:             {plan['ticker']}")
        print(f"  Reference Price:        ${plan['current_market_price']}")
        print(f"  Hourly ATR(14):         ${plan['hourly_atr_14']}")
        print("-" * 70)
        for k, v in plan["intraday_rules"].items():
            print(f"  * {k:<25}: {v}")
        print("="*70 + "\n")
        return

    # Default / --backtest: Run full intraday backtest and export trade log
    print("\n[PHOENIX INTRADAY] Running 2-year intraday quantitative backtest on QQQ...")
    res = run_intraday_backtest(ticker="QQQ")
    
    # Save Trade Log CSV
    tdf = pd.DataFrame(res["trades"])
    tdf.to_csv(QUANT_DIR / "INTRADAY_TRADE_LOG.csv", index=False)
    print(f"-> Exported {len(tdf)} intraday trades to 09_QUANT_RESEARCH/INTRADAY_TRADE_LOG.csv")

    # Save Results JSON
    clean_res = {k: v for k, v in res.items() if k not in ["trades", "daily_equity_curve"]}
    (QUANT_DIR / "INTRADAY_BACKTEST_RESULTS.json").write_text(json.dumps(clean_res, indent=2) + "\n")
    print("-> Saved intraday results to 09_QUANT_RESEARCH/INTRADAY_BACKTEST_RESULTS.json")

    print("\n" + "="*70)
    print("     PHOENIX INTRADAY V2.0 BACKTEST RESULTS (ZERO OVERNIGHT)")
    print("="*70)
    print(f"  Strategy:               {clean_res['strategy_name']}")
    print(f"  Period:                 {clean_res['tested_period']}")
    print(f"  Total Intraday Trades:  {clean_res['total_intraday_trades']}")
    print(f"  Win Rate:               {clean_res['win_rate_pct']}%")
    print(f"  Profit Factor:          {clean_res['profit_factor']}")
    print(f"  Ending Equity:          ${clean_res['ending_equity']:,.2f}  (Return: {clean_res['total_return_pct']}%)")
    print(f"  Max Drawdown:           {clean_res['max_drawdown_pct']}%")
    print(f"  Exit Breakdown:         {clean_res['exit_reason_breakdown']}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
