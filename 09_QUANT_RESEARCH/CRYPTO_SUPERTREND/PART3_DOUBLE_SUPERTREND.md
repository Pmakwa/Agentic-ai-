# PART 3 — DOUBLE SUPERTREND (₹10,000 INR)

**Tested:** 36 configs × 2 RR × 2 TF × 3 coins = 432 tests

## 3.1 Logic
- Fast ST (7,10,14 × 1.5-2.5) + Slow ST (14,20,30 × 2.5-3.5)
- Signal only when Fast flips AND Slow confirms same direction
- Filters 40% of single signals

## 3.2 Best per Coin

### BTC/USDT Top 5
| Rank | Params | TF | RR | Final ₹ | Net ₹ | PF | Trades |
|------|--------|----|----|---------|-------|----|--------|
| 1 | F10x2.0_S30x3.5 | 1h | 1:3 | ₹11301 | ₹1301 | 1.15 | 111 |
| 2 | F10x2.0_S14x3.5 | 1h | 1:3 | ₹11297 | ₹1297 | 1.17 | 100 |
| 3 | F14x2.5_S20x2.5 | 4h | 1:3 | ₹11158 | ₹1158 | 1.37 | 43 |
| 4 | F14x2.5_S20x2.5 | 1h | 1:3 | ₹11083 | ₹1083 | 1.09 | 151 |
| 5 | F7x2.0_S14x3.0 | 1h | 1:3 | ₹10890 | ₹890 | 1.08 | 131 |

**Double vs Single best:** Double ₹1301 vs Single ₹1932 → SINGLE WINS

### ETH/USDT Top 5
| Rank | Params | TF | RR | Final ₹ | Net ₹ | PF | Trades |
|------|--------|----|----|---------|-------|----|--------|
| 1 | F14x1.5_S20x3.5 | 1h | 1:3 | ₹11632 | ₹1632 | 1.14 | 145 |
| 2 | F10x1.5_S20x3.5 | 4h | 1:3 | ₹11630 | ₹1630 | 1.58 | 40 |
| 3 | F10x1.5_S14x3.0 | 1h | 1:3 | ₹11567 | ₹1567 | 1.11 | 165 |
| 4 | F10x1.5_S20x3.5 | 4h | 1:2 | ₹11357 | ₹1357 | 1.45 | 49 |
| 5 | F10x2.0_S30x3.5 | 4h | 1:2 | ₹11321 | ₹1321 | 1.57 | 38 |

**Double vs Single best:** Double ₹1632 vs Single ₹2314 → SINGLE WINS

### SOL/USDT Top 5
| Rank | Params | TF | RR | Final ₹ | Net ₹ | PF | Trades |
|------|--------|----|----|---------|-------|----|--------|
| 1 | F10x2.0_S20x3.0 | 1h | 1:3 | ₹12625 | ₹2625 | 1.27 | 121 |
| 2 | F10x2.0_S30x3.5 | 4h | 1:2 | ₹11838 | ₹1838 | 1.76 | 41 |
| 3 | F10x1.5_S14x3.0 | 4h | 1:3 | ₹11703 | ₹1703 | 1.58 | 40 |
| 4 | F14x1.5_S20x3.5 | 1h | 1:3 | ₹11436 | ₹1436 | 1.1 | 172 |
| 5 | F14x1.5_S30x3.0 | 1h | 1:3 | ₹11414 | ₹1414 | 1.08 | 201 |

**Double vs Single best:** Double ₹2625 vs Single ₹3135 → SINGLE WINS

## 3.3 Verdict
- **Mean Double -1002 INR** vs Single -1580 INR → Double slightly better mean but still negative median (-905)
- **Only SOL benefits**; BTC Double best (+1356) < Single best (+1932)
