# PART 11 — FINAL CONFIGURATION SET (BY OBJECTIVE, NO SINGLE BEST)

## Per Section 41 — Separate candidates by objective:

### 1. Profit-Focused
**SOL 1h SINGLE P14x3.0 1:3**
- Final: ₹13,135 (+31.35%) | Net: +₹3,135 | DD 9.67% | PF 1.31 | Win 33.6% | Trades 119 | Expectancy ₹26.34
- **Supports:** OOS +1110, nearby 80% profitable, distribution healthy (top10% 28%)
- **Risk:** 12-loss streak, 81% exposure

### 2. Drawdown-Focused
**SOL 4h SINGLE P7x3.5 1:3**
- Final: ₹10,180 (+1.8%) | DD 4.52% | PF 1.10 | 25 trades
- **Problem:** Too few trades (25 in 2y), fragile — NOT recommended despite low DD

### 3. Stability-Focused (Best Sharpe)
**SOL 4h SINGLE P14x2.0 1:3**
- Final: ₹12,158 (+21.58%) | PF 1.49 | Sharpe 14.85 | DD 8.28% | 59 trades
- **Needs OOS validation** — not yet proven

### 4. High-Frequency
**SOL 1h SINGLE P30x1.5 1:2**
- 596 trades but **-₹7,077 (-70%)** — proves high frequency ≠ profit, avoid

### 5. Conservative (Lower Risk)
**SOL 1h SINGLE P14x3.5 1:2**
- Final: ₹11,189 (+11.9%) | PF 1.11 | DD 17.3% | 150 trades | Sharpe 4.76
- Lower return but more trades, slightly higher DD than profit-focused

## Complete Parameters for Profit-Focused (Reproducible)

```
Coin: SOL/USDT | Exchange: Binance Spot (Yahoo proxy) | Timeframe: 1h | ST: Period 14 Multiplier 3.0
RR: 1:3 | Risk: 1.0% of equity | Stop: Supertrend line | Entry: Close confirmation next open
Fees: 0.10% per side | Slippage: 0.05% | Initial: ₹10,000
Formula: Risk=Equity*0.01 | Size=Risk/(StopDistance*83.5) | Target=Entry±3*StopDistance
```

## How to Use
1. **Paper trade 1 month** on SOL 1h P14x3.0 1:3 with 0.5% risk
2. Verify your broker fees ≤0.10%
3. Monitor DD >12% → pause
4. Do NOT use BTC 1h defaults — 87.6% lose

