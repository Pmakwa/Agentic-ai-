# PART 7 — COMPLETE TRADE DATABASE

## 7.1 Separation Guarantee (Section 35)
Every test combination has SEPARATE dataset:
- BTC vs ETH vs SOL — NEVER merged
- SINGLE vs DOUBLE vs TRIPLE — separate
- 1:2 vs 1:3 — separate
- 1h vs 4h — separate
- Example: `TRADE_LOG_SOL_USDT_SINGLE_1h_1-3_P14x3_0_csv` is **strictly** SOL 1h Single P14x3.0 1:3 1% risk

## 7.2 Files Provided
| File | Description | Trades | Rows |
|------|-------------|--------|------|

## 7.3 Full Database
- `MASTER_COMPARISON_MATRIX.csv` — 1,092 rows, all configs, all metrics
- `ALL_RESULTS_SUMMARY.json` — full metrics per config (1.5 MB)
- `DETAILED_CANDIDATES.json` — 103 profitable PF>1.2 configs with equity curves + 30-trade samples (3.1 MB)
- **Reproduce all 1,092 logs:** `python3 tools/crypto_supertrend_engine.py` (with --quick for sample)

## 7.4 Trade Columns (Per Section 20)
Trade # | Date Time | Coin | Direction | Entry | Stop | Target | Exit | Exit Reason | Risk ₹ | Position Size | Gross P&L | Fees | Slippage | Net P&L | Equity

**Conservative intrabar rule:** If SL & TP same candle → SL first (loss) documented per trade.
