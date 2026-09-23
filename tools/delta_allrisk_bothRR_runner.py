#!/usr/bin/env python3
"""
Delta India — Full Grid: Risk 1% / 1.5% / 2% × RR 1:2 / 1:3 × 5m/15m/30m/1h × 3 coins = 72 backtests
Capital ₹10,000 | SL 8% | Double ST 10x3+10x4 | Delta fees 0.059% per side
"""
import sys
sys.path.insert(0, "/home/user/uai-cos/tools")
from delta_double_supertrend_intraday import download_delta_data, backtest_double_st_intraday
from pathlib import Path
import pandas as pd, json

ROOT=Path("/home/user/uai-cos")
OUT=ROOT/"09_QUANT_RESEARCH"/"DELTA_INTRADAY_ALLRISK"
OUT.mkdir(parents=True, exist_ok=True)

COINS={"BTC/INR":"BTC-USD","ETH/INR":"ETH-USD","SOL/INR":"SOL-USD"}
TIMEFRAMES={"5m":("5m","7d"), "15m":("15m","60d"), "30m":("30m","60d"), "1h":("60m","2y")}
RISK_LEVELS={"1%":0.01, "1.5%":0.015, "2%":0.02}
RR_MAP={"1:2":2.0, "1:3":3.0}

# Cache data
cache={}
for coin,yft in COINS.items():
    for tf,(interval,period) in TIMEFRAMES.items():
        print(f"[DATA] {coin} {tf} ...", flush=True)
        df=download_delta_data(yft, interval, period)
        cache[(coin,tf)]=df
        print(f" -> {len(df)} bars {df.index[0].date() if len(df)>0 else 'none'} to {df.index[-1].date() if len(df)>0 else 'none'}", flush=True)

all_rows=[]
for coin in COINS:
    for tf in TIMEFRAMES:
        df=cache[(coin,tf)]
        if len(df)<100:
            continue
        for risk_label, risk_val in RISK_LEVELS.items():
            for rr_label, rr_val in RR_MAP.items():
                print(f"\n[RUN] {coin} {tf} Risk {risk_label} RR {rr_label} ...", flush=True)
                res=backtest_double_st_intraday(df, coin, tf, 10,3.0,10,4.0, 0.08, rr_val, risk_val, True, risk_fixed=None)
                m=res["metrics"]
                print(f" => Trades {m['num_trades']} Win {m['win_rate']}% Net ₹{m['total_net_profit']} PF {m['profit_factor']} Final ₹{m['ending_capital']} DD {m['max_drawdown_pct']}%", flush=True)
                # Save trade log with full naming
                fname=f"TRADE_LOG_{coin.replace('/','_')}_{tf}_{risk_label.replace('%','pct')}_{rr_label.replace(':','-')}.csv"
                pd.DataFrame(res["trades"]).to_csv(OUT / fname, index=False)
                # Result json
                with open(OUT / f"RESULT_{coin.replace('/','_')}_{tf}_{risk_label.replace('%','pct')}_{rr_label.replace(':','-')}.json","w") as f:
                    json.dump({k:v for k,v in res.items() if k!="trades"}, f, indent=2, default=str)
                all_rows.append({
                    "coin":coin,"timeframe":tf,"bars":res["bars"],"risk":risk_label,"rr":rr_label,
                    "risk_pct":risk_val*100,"rr_val":rr_val,"sl_pct":"8%","strategy":"Double ST 10x3+10x4",
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

# Save master
pd.DataFrame(all_rows).to_csv(OUT/"MASTER_DELTA_ALLRISK_72.csv", index=False)
with open(OUT/"SUMMARY_ALLRISK.json","w") as f: json.dump(all_rows,f,indent=2)
print(f"\n[DONE] {len(all_rows)} configs")
# Print pivot summaries
df=pd.DataFrame(all_rows)
for risk in ["1%","1.5%","2%"]:
    print(f"\n=== RISK {risk} ===")
    sub=df[df["risk"]==risk]
    for rr in ["1:2","1:3"]:
        print(f" RR {rr}:")
        print(sub[sub["rr"]==rr][["coin","timeframe","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))
