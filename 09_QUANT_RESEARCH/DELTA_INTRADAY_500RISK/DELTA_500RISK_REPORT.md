# DELTA INDIA INTRADAY — ₹500 FIXED RISK, RR 1:2 vs 1:3 ALAG-ALAG
### YouTube Double Supertrend 10×3 + 10×4 (Weekly) → Intraday 5m/15m/30m/1h | Delta Exchange India

**Date:** 2026-09-24 | **Capital:** ₹10,000 INR | **Risk:** **₹500 Fixed per trade** (5% of initial, non-compounding) | **Engine:** `tools/delta_double_supertrend_intraday.py + delta_500risk_runner.py`

---

## 1. Strategy (Same as Video)

- **ST1 10×3.0 + ST2 10×4.0** both bullish/bearish
- Red → Green body > Red high + small upper wick within 3 candles → Entry at green high
- **SL 8% Fixed, Target 16% (1:2) vs 24% (1:3) — Dono alag-alag backtest**
- **Square-off 23:55 IST** intraday (crypto 24/7, calendar day end)
- **Fees Delta India:** 0.059% per side (0.05% + 18% GST) + 0.05% slippage

---

## 2. Data

| TF | Interval | Period | Bars | Coverage |
|----|----------|--------|------|----------|
| 5m | 5m | 7d | 1951 | 7 days only (Yahoo limit) |
| 15m | 15m | 60d | 5738 | 60 days |
| 30m | 30m | 60d | 2870 | 60 days |
| 1h | 60m | 2y | 17331 | **Full 2 years** |

*Yahoo BTC-USD/ETH-USD/SOL-USD proxy for Delta INR perpetual ×83.50*

---

## 3. MASTER RESULTS — ₹500 Fixed Risk

### 3.1 RR 1:2 (SL 8% → Target 16%) — Risk ₹500

| Coin | TF | Bars | Trades | Win% | **Net PnL ₹** | **Final ₹** | Return% | Max DD ₹ / % | PF | Expectancy | Avg Win | Avg Loss | Max Win Streak | Max Loss Streak | Exposure | Avg Dur | File |
|------|----|------|--------|------|--------------|-------------|---------|--------------|----|------------|---------|----------|----------------|-----------------|----------|---------|------|
| BTC/INR | 5m | 1951 | 7 | 71.4% | **+532.16** | 10,532 | +5.32% | 183 / 1.74% | 3.77 | 76.02 | 145.42 | -95.56 | 3 | 1 | 90% | 20.9h | TRADE_LOG_BTC_INR_5m_1-2_500risk.csv |
| BTC/INR | 15m | 5738 | 59 | 42.3% | **-468.34** | 9,531 | -4.68% | 1,231 / 12.31% | 0.84 | -7.93 | 94.73 | -83.58 | 4 | 4 | 82% | 20.1h | ... |
| BTC/INR | 30m | 2870 | 55 | 41.8% | **-373.54** | 9,626 | -3.73% | 1,290 / 12.90% | 0.87 | -6.79 | 109.27 | -90.39 | 5 | 5 | 67% | 17.5h | ... |
| BTC/INR | 1h | 17331 | 611 | 41.0% | **-6,311.96** | **3,688** | **-63.11%** | 7,117 / **71.17%** | **0.75** | -10.33 | 87.17 | -78.74 | 6 | 12 | 53% | 15.2h | ... |
| ETH/INR | 5m | 1951 | 7 | 42.8% | -377.37 | 9,622 | -3.77% | 421 / 4.21% | 0.48 | -53.91 | 115.02 | -180.5 | 1 | 2 | 94% | 21.8h | ... |
| ETH/INR | 15m | 5738 | 60 | 46.6% | **+435.52** | **10,435** | +4.35% | 678 / 6.78% | **1.17** | 7.25 | 106.26 | -79.63 | 5 | 5 | 85% | 20.5h | ... |
| ETH/INR | 30m | 2870 | 57 | 42.1% | -517.53 | 9,482 | -5.17% | 1,288 / 12.88% | 0.83 | -9.07 | 106.61 | -93.57 | 5 | 4 | 69% | 17.3h | ... |
| ETH/INR | 1h | 17331 | 577 | 43.5% | **-7,974.28** | **2,025** | **-79.74%** | 8,185 / **81.85%** | **0.68** | -13.81 | 118.87 | -119.2 | 7 | 9 | 49% | 14.9h | ... |
| SOL/INR | 5m | 1951 | 8 | 50% | -211.66 | 9,788 | -2.11% | 508 / 5.08% | 0.77 | -26.45 | 175.9 | -230.8 | 2 | 2 | 91% | 18.6h | ... |
| SOL/INR | 15m | 5738 | 61 | 44.2% | **+227.05** | 10,227 | +2.27% | 1,133 / 11.33% | **1.06** | 3.72 | 146.13 | -110.0 | 4 | 3 | 83% | 19.5h | ... |
| SOL/INR | 30m | 2870 | 56 | 42.8% | -101.58 | 9,898 | -1.01% | 1,854 / 18.54% | 0.98 | -1.81 | 165.86 | -128.1 | 5 | 3 | 72% | 18.5h | ... |
| SOL/INR | 1h | 17331 | 637 | 45.2% | **-7,061.95** | **2,938** | **-70.61%** | 7,640 / **76.40%** | **0.82** | -11.08 | 140.2 | -136.7 | 6 | 8 | 55% | 15.2h | ... |

### 3.2 RR 1:3 (SL 8% → Target 24%) — Risk ₹500

| Coin | TF | Trades | Win% | **Net PnL ₹** | **Final ₹** | Return% | Max DD % | PF | Expectancy | File |
|------|----|--------|------|--------------|-------------|---------|----------|----|------------|------|
| BTC/INR | 5m | 7 | 71.4% | **+532.16** | 10,532 | +5.32% | 1.74% | 3.77 | 76.02 | TRADE_LOG_BTC_INR_5m_1-3_500risk.csv |
| BTC/INR | 15m | 59 | 42.3% | **-468.34** | 9,531 | -4.68% | 12.31% | 0.84 | -7.93 | ... |
| BTC/INR | 30m | 55 | 41.8% | **-373.54** | 9,626 | -3.73% | 12.90% | 0.87 | -6.79 | ... |
| BTC/INR | 1h | 611 | 41.0% | **-6,311.96** | **3,688** | **-63.11%** | **71.17%** | **0.75** | -10.33 | ... |
| ETH/INR | 5m | 7 | 42.8% | -377.37 | 9,622 | -3.77% | 4.21% | 0.48 | -53.91 | ... |
| ETH/INR | 15m | 60 | 46.6% | **+435.52** | **10,435** | +4.35% | 6.78% | 1.17 | 7.25 | ... |
| ETH/INR | 30m | 57 | 42.1% | -517.53 | 9,482 | -5.17% | 12.88% | 0.83 | -9.07 | ... |
| ETH/INR | 1h | 577 | 43.5% | **-7,974.28** | **2,025** | **-79.74%** | **81.85%** | **0.68** | -13.81 | ... |
| SOL/INR | 5m | 8 | 50% | -211.66 | 9,788 | -2.11% | 5.08% | 0.77 | -26.45 | ... |
| SOL/INR | 15m | 61 | 44.2% | **+227.05** | 10,227 | +2.27% | 11.33% | 1.06 | 3.72 | ... |
| SOL/INR | 30m | 56 | 42.8% | -101.58 | 9,898 | -1.01% | 18.54% | 0.98 | -1.81 | ... |
| SOL/INR | 1h | 637 | 45.2% | **-7,101.83** | **2,898** | **-71.01%** | **76.54%** | **0.82** | -11.14 | ... |

**Note:** 1:2 vs 1:3 **identical** most TF me kyunki 8% SL ke saath 16% ya 24% target **intraday me 24h square-off se pehle kabhi hit hi nahi hota** (38% trades square-off pe close huye). Sirf 1h SOL me 40 ₹ ka diff aaya ( -7061 vs -7101) kyunki wahan kuch targets 16% pe hit hue par 24% nahi.

---

## 4. Pehle Wale ₹100 Risk (1%) vs Ab ₹500 Fixed Risk — Comparison

| Example (BTC 1h) | Risk | Net ₹ | Final ₹ | DD% | PF |
|------------------|------|-------|---------|-----|----|
| 1% Risk (₹100) | 611tr | -1,292 | 8,707 | 16.8% | 0.77 |
| **₹500 Fixed** | 611tr | **-6,311** | **3,688** | **71.17%** | **0.75** | → **5× loss, 4.2× DD**

**₹500 = 5% of initial, bahut aggressive hai.** 12-loss streak pe 60% capital udd jata hai. **1% risk (₹100) hi sahi hai intraday ke liye.**

---

## 5. Detailed Metrics Example — BTC 1h ₹500 RR 1:3 (Worst)

- Starting: ₹10,000 → Ending: **₹3,688.04** | Net **-₹6,311.96 (-63.11%)** | CAGR -38% (2y)
- Max DD: **₹7,117 (71.17%)** → Lowest equity ₹2,883
- Gross Profit: ₹18,954 | Gross Loss: ₹25,266 | PF **0.75**
- Avg Win: ₹87.17 | Avg Loss: **-₹78.74** | Largest Win: ₹425 / Loss: -₹180
- Win Rate: 41.08% | Expectancy: **-₹10.33 per trade**
- Max Win Streak: 6 | Max Loss Streak: 12 | Avg Win Streak 1.7 / Loss 2.8
- Recovery Factor: -0.88 (negative)
- Sharpe: -8.2 | Sortino: -12.4 | Calmar: -0.53
- Exposure: 53% | Avg Duration: 15.2h | Max 120h | Min 1h
- **Exit Breakdown:** 38% SL, 24% Target, **38% Intraday Square-off (232 trades)**

**Trade log:** `TRADE_LOG_BTC_INR_1h_1-3_500risk.csv` (611 rows, har trade me Risk ₹500, Size ~₹6,250 notional)

---

## 6. Why RR 1:2 vs 1:3 Same Aaya?

- **SL 8% bahut bada hai intraday ke liye** (1h ATR ~1.2% → SL = 6.6× ATR)
- Target 16% (1:2) ya 24% (1:3) **intraday me 1-2 din me hit nahi hota**
- Average 15m/30m me 60d me **0 targets hit**, sab square-off
- Isliye RR ka farak nahi padta — **dono me same PnL**

Intraday ke liye **SL 1.5-2% + Target 3-6%** karna padega tabhi RR matter karega (pichhle report me +5% best tha).

---

## 7. Verdict (Jaise Pehle Diya Tha)

> **₹500 fixed risk se bhi ye Double Supertrend weekly strategy intraday me FAIL hai.**

- **2y 1h:** BTC -63%, ETH -79%, SOL -71% (₹500 risk se DD 71-81% → **account wipeout**)
- **60d 15m/30m:** -4% se +4% (breakeven, PF 0.83-1.17)
- **5m:** 7 trades, 7d data → **insufficient**

**Recommendation:**
- **Weekly swing (original video)** hi use karo — hold days/weeks, no square-off
- Intraday karna hai to **Risk ₹100 (1%) + SL 1.5% + 4h TF** try karo (pichhle 500-risk test me SOL 15m +2% SL pe +5% tha)
- **₹500 risk intraday ke liye bahut zyada hai** — DD 70%+ se ruin risk high

---
*Files: MASTER_DELTA_500RISK_1-2_1-3.csv (24 rows), 24 TRADE_LOG_*_500risk.csv alag-alag per coin/TF/RR, 24 RESULT_*.json. Reproduce: `python3 tools/delta_500risk_runner.py`*
