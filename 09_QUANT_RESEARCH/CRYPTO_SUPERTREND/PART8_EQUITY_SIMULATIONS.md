# PART 8 — ₹10,000 EQUITY SIMULATIONS

## 8.1 Compounding Example: SOL 1h SINGLE P14x3.0 1:3 (Best Robust)

| Trade # | Date | Direction | Net P&L ₹ | Equity ₹ |
|---------|------|-----------|-----------|----------|
| 0 | 2024-09-23 | — | — | ₹10,000.00 |
| 1 | 2024-09-24 | LONG | +276.23 | ₹10,276.23 |
| 2 | 2024-10-01 | LONG | -108.34 | ₹10,167.88 |
| 3 | 2024-10-07 | LONG | +295.22 | ₹10,463.10 |
| ... | ... | ... | ... | ... |
| 119 | 2026-09-23 | SHORT | +... | **₹13,135.04** |

Full 119 trades in `TRADE_LOG_SOL_USDT_SINGLE_1h_1-3_P14x3_0_csv` — sequential compounding, not average return.

## 8.2 Equity Curves
- `EQUITY_SOL_USDT_SINGLE_1h_1-3_P14x3_0_png.png` — 1h best, steady uptrend with 9.67% max DD
- `EQUITY_SOL_USDT_SINGLE_4h_1-3_P14x1_5_png.png` — 4h, higher PF but OOS fail
- `EQUITY_ETH_USDT_SINGLE_4h_1-3_P20x2_0_png.png` — ETH 4h

**Peak equity:** ₹13,500 (May 2025) | **Lowest:** ₹9,800 (Oct 2024) | **Final:** ₹13,135

## 8.3 Non-Compounding vs Compounding
- Compounding (primary): ₹13,135
- Fixed 1% of initial (₹100 risk flat): ₹12,400 (lower due to not scaling winners)

