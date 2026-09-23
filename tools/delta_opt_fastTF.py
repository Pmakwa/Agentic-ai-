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
TIMEFRAMES={"5m":("5m","7d"), "15m":("15m","60d"), "30m":("30m","60d")}
PERIODS=[7,10,12,14]
MULTS=[2.0,3.0,3.5,4.0]
SL_VAL=0.015
RR_VAL=3.0

combos = [(p1,m1,p2,m2) for p1,m1,p2,m2 in itertools.product(PERIODS, MULTS, PERIODS, MULTS) if not (p1==p2 and m1==m2)]
print(f"[OPT-FAST] {len(combos)} combos per dataset × {len(COINS)*len(TIMEFRAMES)} datasets = {len(combos)*len(COINS)*len(TIMEFRAMES)} tests (5m 7D, 15m/30m 60D)")
print(f"[OPT-FAST] Fix Risk 1%, SL 1.5% RR 1:3, Fees 0.059% — Settings in every row")

cache={}
for coin,yft in COINS.items():
    for tf,(interval,period) in TIMEFRAMES.items():
        df=download_delta_data(yft, interval, period)
        cache[(coin,tf)]=df
        print(f"[DATA] {coin} {tf} {len(df)} bars", flush=True)

all_rows=[]
start=time.time()
total=len(combos)*len(COINS)*len(TIMEFRAMES)
done=0
for coin in COINS:
    for tf in TIMEFRAMES:
        df=cache[(coin,tf)]
        period_label = {"5m":"2026-09-17 to 2026-09-24 (7D)","15m":"2026-07-25 to 2026-09-24 (60D)","30m":"2026-07-25 to 2026-09-24 (60D)"}[tf]
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
            if done % 200 == 0:
                print(f"[PROG-FAST] {done}/{total} done ({done/total*100:.1f}%) elapsed {(time.time()-start)/60:.1f}m", flush=True)

df=pd.DataFrame(all_rows)
df.to_csv(OUT/"MASTER_OPT_FAST_2160.csv", index=False)
print(f"[DONE-FAST] {len(df)} tests in {(time.time()-start)/60:.1f} min")

# Top overall
top = df.sort_values("total_net_profit", ascending=False).head(50)
top.to_csv(OUT/"TOP50_FAST_BY_NET.csv", index=False)
print("\n=== TOP 15 FAST BY NET (5m/15m/30m) ===")
print(top.head(15)[["coin","timeframe","period","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))

prof = df[(df["total_net_profit"]>0) & (df["num_trades"]>=10)].sort_values("profit_factor", ascending=False).head(50)
prof.to_csv(OUT/"TOP50_FAST_BY_PF.csv", index=False)
print("\n=== TOP 15 FAST BY PF (profitable >=10tr) ===")
if len(prof)>=15:
    print(prof.head(15)[["coin","timeframe","period","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))
else:
    print(df.sort_values("profit_factor", ascending=False).head(15)[["coin","timeframe","period","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))

for tf in ["15m","30m","5m"]:
    sub=df[df["timeframe"]==tf]
    t=sub.sort_values("total_net_profit", ascending=False).head(5)
    print(f"\n=== TOP 5 {tf} BY NET ===")
    print(t[["coin","settings","num_trades","win_rate","total_net_profit","profit_factor","max_drawdown_pct"]].to_string(index=False))

# Now build CLEAN list with settings + period for TOP 3
top3 = df.sort_values("total_net_profit", ascending=False).head(3)
# Create list for user as requested: rows with settings params
import json
with open(OUT/"TOP3_FAST_SUMMARY.json","w") as f:
    json.dump(top3.to_dict(orient="records"), f, indent=2, default=str)

# Create markdown report
md = """# DELTA INTRADAY — FAST TF OPTIMIZER (5m/15m/30m) — 2160 BACKTESTS
## 240 Double ST combos per dataset × 9 datasets = 2160 tests
**Fix: Risk 1% (₹100) | SL 1.5% | RR 1:3 → Target 4.5% | Fees Delta 0.059% | Square-off 23:55 IST**

### Settings Grid: ST1 Period {7,10,12,14} × Mult {2,3,3.5,4}  +  ST2 same = 240 combos (excl. identical)

| # | Coin | TF | Time Period | Bars | ST1 (P,Mult) | ST2 (P,Mult) | Settings | SL | RR | Target | Trades | Win% | Net PnL ₹ | Final ₹ | Return% | Max DD % | PF | Expectancy |
|---|------|----|-------------|------|--------------|--------------|----------|----|----|--------|--------|------|-----------|---------|---------|----------|----|------------|
"""
for idx, r in enumerate(top.head(15).itertuples(), 1):
    md += f"| {idx} | {r.coin.split('/')[0]} | {r.timeframe} | {r.period} | {r.bars} | {r.st1_period},{r.st1_mult} | {r.st2_period},{r.st2_mult} | {r.settings} | {r.sl} | {r.rr} | {r.target} | {r.num_trades} | {r.win_rate:.1f}% | **{r.total_net_profit:+.0f}** | {r.ending_capital:.0f} | {r.return_pct:+.1f}% | {r.max_drawdown_pct:.1f}% | {r.profit_factor:.2f} | {r.expectancy:.1f} |\n"

Path(OUT/"CLEAN_TOP15_FAST_WITH_SETTINGS.md").write_text(md)
print(f"\nWrote CLEAN_TOP15_FAST_WITH_SETTINGS.md")

# Also full sorted CSV for user
df_sorted = df.sort_values("total_net_profit", ascending=False)
df_sorted.to_csv(OUT/"MASTER_FAST_SORTED_BY_NET.csv", index=False)
print(f"Saved sorted full to MASTER_FAST_SORTED_BY_NET.csv")

print("\n[NOTE] 1h 2Y (720 tests, ~31 min) will run next as separate stage as you requested")
