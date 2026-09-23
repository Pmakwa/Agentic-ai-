#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/user/uai-cos/tools")
from delta_double_supertrend_intraday import download_delta_data, backtest_double_st_intraday
from pathlib import Path
import pandas as pd, itertools, time
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

ROOT=Path("/home/user/uai-cos")
OUT=ROOT/"09_QUANT_RESEARCH"/"DELTA_INTRADAY_OPTIMIZER"
OUT.mkdir(parents=True, exist_ok=True)

COINS={"BTC/INR":"BTC-USD","ETH/INR":"ETH-USD","SOL/INR":"SOL-USD"}
TIMEFRAMES={"5m":("5m","7d"), "15m":("15m","60d"), "30m":("30m","60d"), "1h":("60m","2y")}
PERIODS=[7,10,12,14]
MULTS=[2.0,3.0,3.5,4.0]
SL_VAL=0.015
RR_VAL=3.0

combos = [(p1,m1,p2,m2) for p1,m1,p2,m2 in itertools.product(PERIODS, MULTS, PERIODS, MULTS) if not (p1==p2 and m1==m2)]
print(f"[FAST] {len(combos)} combos per dataset × {len(COINS)*len(TIMEFRAMES)} datasets = {len(combos)*len(COINS)*len(TIMEFRAMES)} total")
print(f"[FAST] Using {mp.cpu_count()} cores parallel")

# Cache data in main process
cache={}
for coin,yft in COINS.items():
    for tf,(interval,period) in TIMEFRAMES.items():
        df=download_delta_data(yft, interval, period)
        cache[(coin,tf)]=df
        print(f"[DATA] {coin} {tf} {len(df)} bars", flush=True)

# Build tasks: list of (coin, tf, p1,m1,p2,m2, df_copy?) Need to pass df via shared? We'll pass coin/tf and cache will be rebuilt in worker via global? Simpler: pass df as pickled
tasks=[]
for coin in COINS:
    for tf in TIMEFRAMES:
        df=cache[(coin,tf)]
        period_label = {"5m":"2026-09-17 to 2026-09-24 (7D)","15m":"2026-07-25 to 2026-09-24 (60D)","30m":"2026-07-25 to 2026-09-24 (60D)","1h":"2024-09-24 to 2026-09-24 (2Y)"}[tf]
        for (p1,m1,p2,m2) in combos:
            tasks.append((coin, tf, period_label, len(df), df, p1,m1,p2,m2))

def worker(args):
    coin, tf, period_label, bars_len, df, p1,m1,p2,m2 = args
    res=backtest_double_st_intraday(df, coin, tf, p1,m1,p2,m2, SL_VAL, RR_VAL, 0.01, True, risk_fixed=None)
    m=res["metrics"]
    return {
        "coin":coin,"timeframe":tf,"period":period_label,"bars":res["bars"],
        "st1_period":p1,"st1_mult":m1,"st2_period":p2,"st2_mult":m2,
        "settings": f"ST1({p1},{m1})+ST2({p2},{m2})",
        "sl":"1.5%","rr":"1:3","target":"4.5%","risk":"1%",
        "num_trades":m["num_trades"],"win_rate":m["win_rate"],"total_net_profit":m["total_net_profit"],
        "ending_capital":m["ending_capital"],"return_pct":m["return_pct"],
        "max_drawdown_inr":m["max_drawdown_inr"],"max_drawdown_pct":m["max_drawdown_pct"],
        "profit_factor":m["profit_factor"],"expectancy":m["expectancy"],
        "avg_win":m["avg_win"],"avg_loss":m["avg_loss"],"gross_profit":m["gross_profit"],"gross_loss":m["gross_loss"],
        "sharpe":m["sharpe"],"exposure_pct":m["exposure_pct"]
    }

all_rows=[]
start=time.time()
with ProcessPoolExecutor(max_workers=4) as exe:
    futures={exe.submit(worker, t): t for t in tasks}
    done=0
    for fut in as_completed(futures):
        all_rows.append(fut.result())
        done+=1
        if done % 400 == 0:
            print(f"[PROG] {done}/{len(tasks)} done ({done/len(tasks)*100:.1f}%) elapsed {(time.time()-start)/60:.1f}m", flush=True)

print(f"[DONE] {len(all_rows)} in {(time.time()-start)/60:.1f} min")
df=pd.DataFrame(all_rows)
# Sort by net profit
df_sorted = df.sort_values("total_net_profit", ascending=False)
df_sorted.to_csv(OUT/"MASTER_OPTIMIZER_2688.csv", index=False)
# Top3 etc
top3 = df_sorted.head(3)
print("\n=== TOP 3 BY NET (overall) ===")
print(top3[["coin","timeframe","period","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))
prof = df[(df["total_net_profit"]>0) & (df["num_trades"]>=20)].sort_values("profit_factor", ascending=False).head(3)
print("\n=== TOP 3 BY PF (profitable >=20tr) ===")
if len(prof)>=3:
    print(prof[["coin","timeframe","period","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))
for tf in ["1h","15m","30m","5m"]:
    sub=df[df["timeframe"]==tf].sort_values("total_net_profit", ascending=False).head(3)
    print(f"\n=== TOP 3 {tf} ===")
    print(sub[["coin","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))
