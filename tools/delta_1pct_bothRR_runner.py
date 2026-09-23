#!/usr/bin/env python3
"""
Delta India — 1% Risk, RR 1:2 vs 1:3 Separate, 5m/15m/30m/1h
24 configs: 3 coins × 4 TF × 2 RR
Capital ₹10,000 | Risk 1% (₹100 initial, compounding) | SL 8% | Delta fees 0.059%
"""
import sys
sys.path.insert(0, "/home/user/uai-cos/tools")
from delta_double_supertrend_intraday import download_delta_data, backtest_double_st_intraday
from pathlib import Path
import pandas as pd, json

ROOT=Path("/home/user/uai-cos")
OUT=ROOT/"09_QUANT_RESEARCH"/"DELTA_INTRADAY_1PCT"
OUT.mkdir(parents=True, exist_ok=True)

COINS={"BTC/INR":"BTC-USD","ETH/INR":"ETH-USD","SOL/INR":"SOL-USD"}
TIMEFRAMES={"5m":("5m","7d"), "15m":("15m","60d"), "30m":("30m","60d"), "1h":("60m","2y")}
RR_MAP={"1:2":2.0, "1:3":3.0}
RISK_PCT=0.01

# Cache data
cache={}
for coin,yft in COINS.items():
    for tf,(interval,period) in TIMEFRAMES.items():
        print(f"[DATA] {coin} {tf} ...", flush=True)
        df=download_delta_data(yft, interval, period)
        cache[(coin,tf)]=df
        print(f" -> {len(df)} bars", flush=True)

all_rows=[]
for coin in COINS:
    for tf in TIMEFRAMES:
        df=cache[(coin,tf)]
        if len(df)<100:
            continue
        for rr_label, rr_val in RR_MAP.items():
            print(f"\n[RUN] {coin} {tf} RR {rr_label} Risk 1% ...", flush=True)
            res=backtest_double_st_intraday(df, coin, tf, 10,3.0,10,4.0, 0.08, rr_val, RISK_PCT, True, risk_fixed=None)
            m=res["metrics"]
            print(f" => Trades {m['num_trades']} Win {m['win_rate']}% Net ₹{m['total_net_profit']} PF {m['profit_factor']} Final ₹{m['ending_capital']} DD {m['max_drawdown_pct']}%", flush=True)
            # Save
            pd.DataFrame(res["trades"]).to_csv(OUT / f"TRADE_LOG_{coin.replace('/','_')}_{tf}_{rr_label.replace(':','-')}_1pct.csv", index=False)
            with open(OUT / f"RESULT_{coin.replace('/','_')}_{tf}_{rr_label.replace(':','-')}_1pct.json","w") as f:
                json.dump({k:v for k,v in res.items() if k!="trades"}, f, indent=2, default=str)
            with open(OUT / f"TRADES_{coin.replace('/','_')}_{tf}_{rr_label.replace(':','-')}_1pct.json","w") as f:
                json.dump(res["trades"][:100], f, indent=2, default=str)
            all_rows.append({
                "coin":coin,"timeframe":tf,"bars":res["bars"],"data_start":res["data_start"],"data_end":res["data_end"],
                "rr":rr_label,"risk_pct":"1%","sl_pct":"8%","strategy":"Double ST 10x3+10x4",
                "starting_capital":m["starting_capital"],"ending_capital":m["ending_capital"],"total_net_profit":m["total_net_profit"],"return_pct":m["return_pct"],
                "max_drawdown_inr":m["max_drawdown_inr"],"max_drawdown_pct":m["max_drawdown_pct"],"max_profit":m["max_profit"],"max_loss":m["max_loss"],
                "avg_win":m["avg_win"],"avg_loss":m["avg_loss"],"largest_win":m["largest_win"],"largest_loss":m["largest_loss"],
                "win_rate":m["win_rate"],"loss_rate":m["loss_rate"],"profit_factor":m["profit_factor"],"expectancy":m["expectancy"],
                "num_trades":m["num_trades"],"winning_trades":m["winning_trades"],"losing_trades":m["losing_trades"],"breakeven_trades":m["breakeven_trades"],
                "max_win_streak":m["max_win_streak"],"max_loss_streak":m["max_loss_streak"],"avg_win_streak":m["avg_win_streak"],"avg_loss_streak":m["avg_loss_streak"],
                "recovery_factor":m["recovery_factor"],"sharpe":m["sharpe"],"sortino":m["sortino"],"calmar":m["calmar"],
                "exposure_pct":m["exposure_pct"],"avg_duration_hours":m["avg_duration_hours"],"max_duration_hours":m["max_duration_hours"],"min_duration_hours":m["min_duration_hours"],
                "gross_profit":m["gross_profit"],"gross_loss":m["gross_loss"],
            })

pd.DataFrame(all_rows).to_csv(OUT/"MASTER_DELTA_1PCT_1-2_1-3.csv", index=False)
with open(OUT/"SUMMARY_1PCT.json","w") as f: json.dump(all_rows,f,indent=2)
print(f"\n[DONE] {len(all_rows)} configs")
dfp=pd.DataFrame(all_rows)
print("\n=== RR 1:2 ===")
print(dfp[dfp["rr"]=="1:2"][["coin","timeframe","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct","ending_capital"]].to_string(index=False))
print("\n=== RR 1:3 ===")
print(dfp[dfp["rr"]=="1:3"][["coin","timeframe","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct","ending_capital"]].to_string(index=False))
