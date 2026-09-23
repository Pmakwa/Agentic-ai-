# PART 2 — SINGLE SUPERTREND (₹10,000 INR)

**Tested:** 25 params × 2 RR × 2 TF × 3 coins = 300 tests

## 2.1 Best per Coin

### BTC/USDT
| Rank | Params | TF | RR | Final ₹ | Net ₹ | DD% | PF | Win% | Trades |
|------|--------|----|----|---------|-------|-----|----|------|--------|
| 1 | P14x1.5 | 4h | 1:3 | ₹11932 | ₹1932 | 13.3% | 1.26 | 33.0% | 88 |
| 2 | P20x1.5 | 4h | 1:3 | ₹11537 | ₹1537 | 11.6% | 1.27 | 33.3% | 66 |
| 3 | P10x2.5 | 1h | 1:3 | ₹10916 | ₹916 | 14.2% | 1.06 | 31.1% | 177 |
| 4 | P7x3.5 | 1h | 1:3 | ₹10911 | ₹911 | 10.7% | 1.13 | 30.1% | 93 |
| 5 | P20x2.0 | 4h | 1:2 | ₹10792 | ₹792 | 6.8% | 1.14 | 39.0% | 82 |

**Worst BTC/USDT:** P10x1.5 1h 1:2 → ₹2176 (-78.2%)
**Median PF BTC/USDT:** 0.77 | **Profitable:** 8/100

### ETH/USDT
| Rank | Params | TF | RR | Final ₹ | Net ₹ | DD% | PF | Win% | Trades |
|------|--------|----|----|---------|-------|-----|----|------|--------|
| 1 | P20x2.0 | 4h | 1:3 | ₹12314 | ₹2314 | 8.7% | 1.43 | 34.3% | 67 |
| 2 | P7x1.5 | 4h | 1:3 | ₹11947 | ₹1947 | 16.0% | 1.27 | 31.6% | 95 |
| 3 | P14x1.5 | 4h | 1:2 | ₹11750 | ₹1750 | 10.7% | 1.21 | 40.9% | 115 |
| 4 | P20x1.5 | 4h | 1:2 | ₹11549 | ₹1549 | 17.2% | 1.16 | 39.7% | 126 |
| 5 | P10x2.0 | 4h | 1:3 | ₹11425 | ₹1425 | 10.5% | 1.32 | 32.2% | 59 |

**Worst ETH/USDT:** P7x1.5 1h 1:2 → ₹2808 (-71.9%)
**Median PF ETH/USDT:** 0.81 | **Profitable:** 19/100

### SOL/USDT
| Rank | Params | TF | RR | Final ₹ | Net ₹ | DD% | PF | Win% | Trades |
|------|--------|----|----|---------|-------|-----|----|------|--------|
| 1 | P14x3.0 | 1h | 1:3 | ₹13135 | ₹3135 | 9.7% | 1.31 | 33.6% | 119 |
| 2 | P14x1.5 | 4h | 1:3 | ₹12404 | ₹2404 | 8.7% | 1.4 | 34.2% | 79 |
| 3 | P20x1.5 | 4h | 1:3 | ₹12270 | ₹2270 | 13.2% | 1.3 | 32.6% | 95 |
| 4 | P14x2.0 | 4h | 1:3 | ₹12159 | ₹2159 | 8.3% | 1.49 | 35.6% | 59 |
| 5 | P7x3.0 | 1h | 1:3 | ₹11769 | ₹1769 | 23.2% | 1.16 | 30.6% | 147 |

**Worst SOL/USDT:** P7x1.5 1h 1:2 → ₹2411 (-75.9%)
**Median PF SOL/USDT:** 0.94 | **Profitable:** 39/100

## 2.2 Entry/Exit Detail (Example SOL 1h P14x3.0 1:3)
- **Entry:** Supertrend flip bullish/bearish at close, entry next open
- **Stop:** Supertrend line (ATR-based)
- **Target:** 3× stop distance (1:3)
- **Trade Sample:** See `TRADE_LOG_SOL_USDT_SINGLE_1h_1-3_P14x3_0_csv` first 5 lines shown in MASTER_REPORT
- **Equity Curve:** `EQUITY_SOL_USDT_SINGLE_1h_1-3_P14x3_0_png.png`
