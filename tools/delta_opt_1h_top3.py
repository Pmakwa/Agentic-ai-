#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/user/uai-cos/tools")
from delta_double_supertrend_intraday import download_delta_data, backtest_double_st_intraday
from pathlib import Path
import pandas as pd, itertools, time

ROOT=Path("/home/user/uai-cos")
OUT=ROOT/"09_QUANT_RESEARCH"/"DELTA_INTRADAY_OPTIMIZER"
OUT.mkdir(parents=True, exist_ok=True)

COINS={"BTC/INR":"BTC-USD","ETH/INR":"ETH-USD","SOL/INR":"SOL-USD"}
TIMEFRAMES={"1h":("60m","2y")}  # Start with 1h most reliable, then expand to 15m/30m/5m
PERIODS=[7,10,12,14]
MULTS=[2.0,3.0,3.5,4.0]
SL_VAL=0.015
RR_VAL=3.0

combos = [(p1,m1,p2,m2) for p1,m1,p2,m2 in itertools.product(PERIODS, MULTS, PERIODS, MULTS) if not (p1==p2 and m1==m2)]
print(f"[OPT-1h] {len(combos)} combos per dataset × {len(COINS)} coins = {len(combos)*len(COINS)} tests (1h 2Y only, most reliable)")
print(f"[OPT-1h] Will also do 15m/30m/5m after 1h top3 — full will be 2880 total, doing in stages for speed")

cache={}
for coin,yft in COINS.items():
    for tf,(interval,period) in TIMEFRAMES.items():
        df=download_delta_data(yft, interval, period)
        cache[(coin,tf)]=df
        print(f"[DATA] {coin} {tf} {len(df)} bars {df.index.min().date()} to {df.index.max().date()}")

all_rows=[]
start=time.time()
total=len(combos)*len(COINS)
done=0
for coin in COINS:
    for tf in TIMEFRAMES:
        df=cache[(coin,tf)]
        period_label="2024-09-24 to 2026-09-24 (2Y)"
        for (p1,m1,p2,m2) in combos:
            res=backtest_double_st_intraday(df, coin, tf, p1,m1,p2,m2, SL_VAL, RR_VAL, 0.01, True, risk_fixed=None)
            m=res["metrics"]
            all_rows.append({
                "coin":coin,"timeframe":tf,"period":period_label,"bars":res["bars"],
                "st1_period":p1,"st1_mult":m1,"st2_period":p2,"st2_mult":m2,
                "settings": f"ST1({p1},{m1})+ST2({p2},{m2})",
                "sl":"1.5%","rr":"1:3","target":"4.5%","risk":"1%",
                "num_trades":m["num_trades"],"win_rate":m["win_rate"],"total_net_profit":m["total_net_profit"],
                "ending_capital":m["ending_capital"],"return_pct":m["return_pct"],
                "max_drawdown_pct":m["max_drawdown_pct"],"profit_factor":m["profit_factor"],"expectancy":m["expectancy"],
                "avg_win":m["avg_win"],"avg_loss":m["avg_loss"],"exposure_pct":m["exposure_pct"]
            })
            done+=1
            if done % 100 == 0:
                print(f"[PROG-1h] {done}/{total} done ({done/total*100:.1f}%) elapsed {(time.time()-start)/60:.1f}m", flush=True)

df=pd.DataFrame(all_rows)
df.to_csv(OUT/"MASTER_OPT_1h_720.csv", index=False)
print(f"[DONE-1h] {len(df)} tests in {(time.time()-start)/60:.1f} min")
# Show top 15
top = df.sort_values("total_net_profit", ascending=False).head(15)
print("\n=== TOP 15 1h BY NET (SL 1.5% RR1:3) ===")
print(top[["coin","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))
# Also PF
prof = df[(df["total_net_profit"]>0) & (df["num_trades"]>=20)].sort_values("profit_factor", ascending=False).head(15)
print("\n=== TOP 15 1h BY PF (profitable >=20tr) ===")
if len(prof)>0:
    print(prof[["coin","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))
else:
    print("No profitable >=20tr, top PF overall:")
    print(df.sort_values("profit_factor", ascending=False).head(15)[["coin","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))
