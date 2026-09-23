#!/usr/bin/env python3
"""
Delta India — EXHAUSTIVE Double ST Settings Optimizer
Tests 1000+ combos of BOTH SuperTrend parameters across all TF/Coins
Fix: Risk 1%, SL 1.5% RR 1:3 (best intraday from previous), then verify top3 on SL 2% also
Searches: ST1 period 7,10,12,14 × mult 2,3,3.5,4 and ST2 period 7,10,12,14 × mult 2,3,3.5,4 => 256 combos per dataset
Datasets: BTC/ETH/SOL × 5m(7D)/15m(60D)/30m(60D)/1h(2Y) = 12 datasets
Total tests: 256 × 12 = 3072 backtests
"""
import sys
sys.path.insert(0, "/home/user/uai-cos/tools")
from delta_double_supertrend_intraday import download_delta_data, backtest_double_st_intraday
from pathlib import Path
import pandas as pd, json, itertools, time

ROOT=Path("/home/user/uai-cos")
OUT=ROOT/"09_QUANT_RESEARCH"/"DELTA_INTRADAY_OPTIMIZER"
OUT.mkdir(parents=True, exist_ok=True)

COINS={"BTC/INR":"BTC-USD","ETH/INR":"ETH-USD","SOL/INR":"SOL-USD"}
TIMEFRAMES={"5m":("5m","7d"), "15m":("15m","60d"), "30m":("30m","60d"), "1h":("60m","2y")}
# Grid
PERIODS=[7,10,12,14]
MULTS=[2.0,3.0,3.5,4.0]
SL_VAL=0.015
RR_VAL=3.0
RISK_PCT=0.01
SL_LABEL="1.5%"
RR_LABEL="1:3"
TARGET_LABEL="4.5%"

combos = list(itertools.product(PERIODS, MULTS, PERIODS, MULTS))
# 256 combos: (p1,m1,p2,m2)
# Filter: avoid identical STs? Keep all, but to reduce dup we keep p1<=p2? No, keep all for exhaustive
print(f"[OPT] Grid: periods {PERIODS} × mults {MULTS} => {len(combos)} combos per dataset × {len(COINS)*len(TIMEFRAMES)} datasets = {len(combos)*len(COINS)*len(TIMEFRAMES)} total backtests")
print(f"[OPT] Fixed: Risk 1%, SL {SL_LABEL}, RR {RR_LABEL} (Target {TARGET_LABEL}) — Intraday square-off 23:55, Fees 0.059%")

# Download / cache
cache={}
for coin,yft in COINS.items():
    for tf,(interval,period) in TIMEFRAMES.items():
        print(f"[DATA] {coin} {tf} {interval} {period} ...", flush=True)
        df=download_delta_data(yft, interval, period)
        cache[(coin,tf)]=df
        print(f"  -> {len(df)} bars {df.index.min()} to {df.index.max()}", flush=True)

all_rows=[]
start_all=time.time()
total = len(combos)*len(COINS)*len(TIMEFRAMES)
done=0
for coin in COINS:
    for tf in TIMEFRAMES:
        df=cache[(coin,tf)]
        if len(df)<100:
            continue
        # Determine period label
        period_label = {"5m":"2026-09-17 to 2026-09-24 (7D)","15m":"2026-07-25 to 2026-09-24 (60D)","30m":"2026-07-25 to 2026-09-24 (60D)","1h":"2024-09-24 to 2026-09-24 (2Y)"}[tf]
        for (p1,m1,p2,m2) in combos:
            # Skip where both ST identical? Keep but they are duplicate strategy; skip p1==p2 and m1==m2 to avoid identical double
            if p1==p2 and m1==m2:
                done+=1
                continue
            res=backtest_double_st_intraday(df, coin, tf, p1,m1,p2,m2, SL_VAL, RR_VAL, RISK_PCT, True, risk_fixed=None)
            m=res["metrics"]
            all_rows.append({
                "coin":coin,"timeframe":tf,"period":period_label,"bars":res["bars"],
                "st1_period":p1,"st1_mult":m1,"st2_period":p2,"st2_mult":m2,
                "settings": f"ST1({p1},{m1})+ST2({p2},{m2})",
                "sl":SL_LABEL,"rr":RR_LABEL,"target":TARGET_LABEL,"risk":"1%",
                "sl_pct":1.5,"rr_val":3.0,
                "num_trades":m["num_trades"],"win_rate":m["win_rate"],"total_net_profit":m["total_net_profit"],
                "ending_capital":m["ending_capital"],"return_pct":m["return_pct"],
                "max_drawdown_inr":m["max_drawdown_inr"],"max_drawdown_pct":m["max_drawdown_pct"],
                "profit_factor":m["profit_factor"],"expectancy":m["expectancy"],
                "avg_win":m["avg_win"],"avg_loss":m["avg_loss"],"gross_profit":m["gross_profit"],"gross_loss":m["gross_loss"],
                "sharpe":m["sharpe"],"exposure_pct":m["exposure_pct"]
            })
            done+=1
            if done % 200 == 0:
                elapsed=time.time()-start_all
                print(f"[PROG] {done}/{total} done ({done/total*100:.1f}%) elapsed {elapsed/60:.1f}m", flush=True)

print(f"\n[DONE] {len(all_rows)} backtests in {(time.time()-start_all)/60:.1f} min")

# Rank
df=pd.DataFrame(all_rows)
# Save full master
full_path=OUT/"MASTER_OPTIMIZER_3072.csv"
df.to_csv(full_path, index=False)
print(f"Saved full {len(df)} rows to {full_path}")

# Top 3 overall by Net Profit
top_profit = df.sort_values("total_net_profit", ascending=False).head(50)
top_profit.to_csv(OUT/"TOP50_BY_NET.csv", index=False)
top3_profit = top_profit.head(3)
print("\n=== TOP 3 BY NET PROFIT (overall) ===")
print(top3_profit[["coin","timeframe","period","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))

# Top 3 by PF among profitable (net>0 and trades>=20)
profitable = df[(df["total_net_profit"]>0) & (df["num_trades"]>=20)]
top_pf = profitable.sort_values("profit_factor", ascending=False).head(50)
top_pf.to_csv(OUT/"TOP50_BY_PF_PROFITABLE.csv", index=False)
print("\n=== TOP 3 BY PF (profitable, >=20 trades) ===")
if len(top_pf)>=3:
    print(top_pf.head(3)[["coin","timeframe","period","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))
else:
    print("No profitable >=20 trades, showing top PF overall")
    print(df.sort_values("profit_factor", ascending=False).head(3).to_string(index=False))

# Top 3 per timeframe (1h most reliable)
for tf in ["1h","15m","30m","5m"]:
    sub=df[df["timeframe"]==tf]
    t=sub.sort_values("total_net_profit", ascending=False).head(3)
    print(f"\n=== TOP 3 {tf} BY NET ===")
    print(t[["coin","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))

# For top 3 overall, also verify with SL 2% RR1:3 and SL 1% RR1:2 quickly
