# PART 4 — TRIPLE SUPERTREND (₹10,000 INR)

**Tested:** 30 configs × 2 RR × 2 TF × 3 coins = 360 tests
- Fast (7,10×1.5-2) + Medium (14,20×2-2.5) + Slow (20,30×3-3.5)
- Signal: Fast flips with Medium & Slow both confirming (3/3 alignment)

## 4.1 Best per Coin

### BTC/USDT Top 5
| Rank | Params | TF | RR | Final ₹ | Net ₹ | PF | Trades |
|------|--------|----|----|---------|-------|----|--------|
| 1 | F7x2.0_M20x2.5_S30x3.5 | 4h | 1:2 | ₹11702 | ₹1702 | 1.53 | 50 |
| 2 | F7x2.0_M14x2.5_S30x3.5 | 4h | 1:2 | ₹11674 | ₹1674 | 1.48 | 53 |
| 3 | F7x2.0_M14x2.5_S20x3.0 | 4h | 1:2 | ₹11315 | ₹1315 | 1.29 | 65 |
| 4 | F7x2.0_M20x2.0_S30x3.5 | 4h | 1:2 | ₹11282 | ₹1282 | 1.43 | 46 |
| 5 | F7x1.5_M20x2.5_S30x3.5 | 4h | 1:3 | ₹10839 | ₹839 | 1.17 | 59 |

### ETH/USDT Top 5
| Rank | Params | TF | RR | Final ₹ | Net ₹ | PF | Trades |
|------|--------|----|----|---------|-------|----|--------|
| 1 | F7x2.0_M14x2.0_S30x3.5 | 4h | 1:3 | ₹11713 | ₹1713 | 1.48 | 49 |
| 2 | F7x1.5_M20x2.0_S30x3.5 | 4h | 1:2 | ₹11256 | ₹1256 | 1.32 | 61 |
| 3 | F7x2.0_M20x2.0_S30x3.5 | 4h | 1:3 | ₹11190 | ₹1190 | 1.36 | 46 |
| 4 | F7x2.0_M14x2.0_S20x3.5 | 4h | 1:3 | ₹11092 | ₹1092 | 1.26 | 54 |
| 5 | F7x1.5_M20x2.0_S30x3.0 | 4h | 1:2 | ₹11065 | ₹1065 | 1.22 | 72 |

### SOL/USDT Top 5
| Rank | Params | TF | RR | Final ₹ | Net ₹ | PF | Trades |
|------|--------|----|----|---------|-------|----|--------|
| 1 | F7x2.0_M20x2.0_S30x3.0 | 4h | 1:3 | ₹12067 | ₹2067 | 1.51 | 49 |
| 2 | F7x2.0_M14x2.5_S30x3.0 | 4h | 1:3 | ₹11929 | ₹1929 | 1.47 | 50 |
| 3 | F7x2.0_M20x2.0_S30x3.5 | 4h | 1:3 | ₹11894 | ₹1894 | 1.55 | 43 |
| 4 | F7x2.0_M14x2.0_S30x3.0 | 4h | 1:3 | ₹11812 | ₹1812 | 1.43 | 51 |
| 5 | F7x2.0_M14x2.5_S30x3.5 | 4h | 1:3 | ₹11753 | ₹1753 | 1.49 | 44 |

## 4.2 Verdict
- **Mean Triple -2186 INR WORST** — adding 3rd ST hurts profitability
- Avg trades 86 vs Single 150 — reduces opportunity, not risk
- **Fragile:** Best Triple SOL 4h F7x2.0_M20x2.0_S30x3.0 49 trades → top 10% trades 52% of profit (depends on few 2024 trades)
