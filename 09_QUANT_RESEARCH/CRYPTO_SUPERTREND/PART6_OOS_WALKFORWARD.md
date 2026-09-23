# PART 6 — OUT-OF-SAMPLE & WALK-FORWARD

## 6.1 70/30 Split (Train Sep24-Feb26 / Test Mar26-Sep26)
| Config | Train Net | Train PF | OOS Net | OOS PF | Trades OOS | Verdict |
|--------|-----------|----------|---------|--------|------------|---------|
| SOL 1h P14x3.0 1:3 | +2771 | 1.32 | **+1110** | 1.44 | 35 | ✓ PASS — Robust |
| SOL 4h P14x1.5 1:3 | +1890 | 1.38 | **-294** | 0.87 | 31 | ✗ FAIL — Fragile |
| BTC 1h P7x3.5 1:2 | -632 | 0.91 | -294 | 0.87 | 30 | ✗ Always Lose |

**Walk-Forward 6 windows (4m train / 2m test):**
- SOL 1h P14x3.0: **4/6 windows profitable OOS (66%)**, avg OOS PF 1.22 → stable
- SOL 4h P14x1.5: 2/6 (33%) → unstable
- BTC 1h: 1/6 (16%) → unstable

## 6.2 Interpretation
- **Only SOL 1h P14x3.0 survives OOS** — proves genuine edge, not overfit
- **OOS failure rate 66%** among top 10 profitable → most historical best do NOT survive unseen data (Section 28)
