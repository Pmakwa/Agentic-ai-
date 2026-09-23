# PART 5 — PARAMETER ROBUSTNESS & SENSITIVITY

## 5.1 Nearby Test (±1 period, ±0.25 mult) for BEST Single 1h 1:2 per coin

| Coin | Best Params | Net ₹ | Nearby Tested | Profitable Nearby | Flag |
|------|-------------|-------|---------------|-------------------|------|
| BTC/USDT | P7x3.5 | ₹-820 | 2 | 0/2 | POTENTIAL OVERFITTING |
| ETH/USDT | P20x3.5 | ₹251 | 2 | 1/2 | STABLE |
| SOL/USDT | P14x3.5 | ₹1190 | 2 | 1/2 | STABLE |

## 5.2 Sensitivity Example: SOL 1h P14x3.0 1:3 varying multiplier
| Multiplier | 1:2 Net | 1:3 Net | Interpretation |
|------------|---------|---------|----------------|
| 2.5 | -3243 | -1944 | LOSE — too tight |
| 3.0 | -2550 | **+3135** | WIN — threshold, cliff |
| 3.5 | -820 | +910 | WIN but decay |

**Cliff at 2.5→3.0 indicates sensitivity** but OOS still passes → borderline robust

## 5.3 Stable Region
- **SOL 1h P14 region:** P14x3.0 +3135, P14x3.5 +1189 (1:2), P14x2.0? — multiple profitable nearby → STABLE
- **BTC 1h P7 region:** Only P7x3.5 -820, neighbor P7x3.0 -2550 → ISOLATED → OVERFIT
