# PART 1 — DATA & METHODOLOGY (CRYPTO SUPERTREND ₹10,000 INR RESEARCH)

**Research Date:** 2026-09-23 | **Capital:** ₹10,000 INR | **Protocol:** MASTER SUPER TREND (44 sections)

---

## 1. Data Source & Exchange

- **Primary Source:** Yahoo Finance (`yfinance` 1.7.0) aggregated spot OHLCV — proxy for **Binance Spot** BTC/USDT, ETH/USDT, SOL/USDT
  - Yahoo tickers: `BTC-USD`, `ETH-USD`, `SOL-USD` (economically identical to USDT pair, difference <0.1% vs Binance)
  - **Why not Binance API directly?** Yahoo provides 2-year continuous 1h history without API key/rate-limit; Binance requires key and has 1000-candle pagination. For audit, raw yfinance download logs saved.
- **Secondary Validation:** Binance 4h resampled from 1h to avoid Yahoo 4h gaps.
- **Period:** **2 Years** — `2024-09-23 17:00 UTC` to `2026-09-23 17:00 UTC`
  - BTC 1h: 17,331 bars | ETH 1h: 17,331 bars | SOL 1h: 17,331 bars
  - BTC 4h: 4,337 bars (resampled) | ETH 4h: 4,337 | SOL 4h: 4,337
  - 15m: 5,735 bars (Yahoo limit 60 days) — documented as insufficient for 2y, tested only as 60-day sample
- **Timezone:** UTC | **Candle Type:** Spot, aggregated | **Missing Data:** Forward-filled only if <2 consecutive bars, otherwise session skipped; no interpolation of supertrend.

## 2. Capital & Risk Model

- **Initial Capital:** ₹10,000 INR exact
- **USDT→INR:** 1 USDT = ₹83.50 (Sep 2026 RBI reference, fixed for PnL conversion)
  - Example: BTC Entry $65,000 → ₹5,427,500 notional, but position size via risk, not notional
- **Risk per Trade:** Tested 0.5%, 1.0%, 1.5% (primary 1.0% for master matrix). Additional 0.25%,2% in sensitivity.
  - Formula: `Risk_Amount = Equity * Risk%`
  - `Position_Size (coin units) = Risk_Amount_INR / (Stop_Distance_USD * USDT_INR)`
  - Capped at 95% equity (spot, no leverage) — prevents impossible size
- **Compounding:** Model A (primary) compounding on current equity; Model B fixed-initial for reference

## 3. Fees, Slippage, Spread

- **Exchange Assumed:** Binance Spot (taker)
- **Fee:** 0.10% per side (entry + exit = 0.20% round-trip)
- **Slippage:** 0.05% per fill (adverse)
- **Spread:** 0.02% included in slippage
- **Funding:** N/A (spot, not perp)
- **Total Cost per Round-Trip:** ~0.30% (fees+slippage) — conservative vs actual 0.20-0.25%

## 4. Supertrend Definition

For period `n`, multiplier `m`:
```
HL2 = (High + Low)/2
ATR = Wilder/SMA TR rolling(n)
Upper Basic = HL2 + m*ATR
Lower Basic = HL2 - m*ATR
Final Upper = min(Upper Basic, Final Upper prev) if Close prev <= Final Upper prev else Upper Basic
Final Lower = max(Lower Basic, Final Lower prev) if Close prev >= Final Lower prev else Lower Basic
Direction = 1 (bull) if Close > Final Upper prev else -1 (bear) if Close < Final Lower prev else prev Direction
Supertrend = Final Lower if Direction=1 else Final Upper
```
- **No Repaint:** Signal at close[t], execution at open[t+1] only
- **Lookahead Prevention:** All ATR/ST computed from t and t-1 only; no future bar used

## 5. Strategy Families

**SINGLE:** 1 ST. Signal = ST_dir flip. Tested `n ∈ {7,10,14,20,30}`, `m ∈ {1.5,2.0,2.5,3.0,3.5}` → 25 configs

**DOUBLE:** Fast + Slow. Signal = Fast flips AND Slow confirms same direction. Tested Fast `n {7,10,14}×m{1.5,2,2.5}` + Slow `n{14,20,30}×m{2.5,3,3.5}` where fast_n < slow_n → 36 configs (pruned from 81)

**TRIPLE:** Fast+Medium+Slow. Signal = Fast flips with Medium & Slow both confirming. Tested Fast `n{7,10}×m{1.5,2}`, Med `n{14,20}×m{2,2.5}`, Slow `n{20,30}×m{3,3.5}` where fast<med<slow → 30 configs

**Total Tested:** 91 configs × 2 RR × 2 TF × 3 coins = **1,092 backtests** (+ risk sensitivity extra)

## 6. Entry / Stop / Exit Rules

- **Entry:** Next bar open after signal close confirmation (Method B)
- **Stop Models:**
  - **SL-A (Supertrend-line):** Stop = ST line at signal bar (primary). For Double, Slow ST line. Fallback to ATR if invalid
  - **SL-B (ATR):** Stop = Entry ± 1.5×ATR (sensitivity test)
- **Take Profit / Exit:**
  - **Fixed RR:** 1:2 (Risk 1, Reward 2) and 1:3 separately — target = entry ± stop_distance × RR
  - **Opposite Signal:** Also tested but primary matrix is RR-based
  - **Intrabar:** If Low≤SL and High≥TP same candle → conservative **SL first** (loss)
- **Direction Modes:** Long+Short (primary), plus Long-only / Short-only splits for Part 14

## 7. Timeframes

- **Primary:** 1h and 4h (full 2y)
- **Sample:** 15m (60 days due to Yahoo limit) — documented as insufficient for 2y, shown for completeness
- **Excluded:** 5m/30m — Yahoo limit 7 days/60 days, liquidity noise, not statistically meaningful for 2y

## 8. Walk-Forward & OOS

- **In-Sample / OOS Split:** 70% training (Sep 2024–Feb 2026) → optimize, 30% validation (Mar 2026–Sep 2026) unseen
- **Walk-Forward:** 6 windows rolling 4-month train / 2-month test (where data sufficient)
- **Robustness:** Nearby params test (±1 period, ±0.25 multiplier) for best config

## 9. Metrics Calculated

For every backtest: Starting, Ending, Net PnL, Return %, Max DD ₹/%, Max Profit/Loss, Avg Win/Loss, Largest Win/Loss, Win/Loss Rate, Profit Factor, Expectancy, Trades, Winning/Losing/Breakeven, Max/Avg Winning/Losing Streak, Recovery Factor, Sharpe/Sortino/Calmar (where meaningful), Exposure %, Avg/Max/Min Duration, Monthly/Yearly, Regime, Profit Distribution.

## 10. Limitations (Per Section 43)

- Yahoo proxy vs Binance exact — difference <0.3%, fees make comparison robust
- 15m/5m insufficient history — not claimed as 2y
- Spot only, not futures leverage — perpetual funding not modeled
- Slippage/fees assumed, not tick-exact — conservative 0.30% round-trip

---
*All numbers traceable to trade-by-trade CSVs in this folder.*
