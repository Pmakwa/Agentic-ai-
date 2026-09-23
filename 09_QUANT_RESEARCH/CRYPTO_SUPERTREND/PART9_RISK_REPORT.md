# PART 9 — RISK REPORT

## 9.1 Max Drawdown (Across 1,092 tests)
| Metric | Value |
|--------|-------|
| Worst DD | 79.04% (BTC 1h P10x1.5 1:2, ₹7,904) |
| Median DD | 18.68% (₹1,967) |
| Best DD among profitable | 3.21% (TRIPLE SOL 4h F7x2.5_M14...) but only 40 trades |
| Best robust DD | 9.67% (SOL 1h P14x3.0 1:3, ₹1,341) |

## 9.2 Losing Streak — SOL 1h P14x3.0 1:3
| Metric | Value |
|--------|-------|
| Max Loss Streak | 12 consecutive losses |
| Capital Lost in Streak | ₹1,340 (9.67% DD) |
| Max Win Streak | 4 |
| Avg Loss Streak | 3.16 |
| Avg Win Streak | 1.6 |
| Recovery Avg | 15 days |

## 9.3 Drawdown Periods (Best Config)
- **18 drawdowns** avg 4.2%, largest 5: 9.67%, 7.1%, 6.3%, 5.9%, 5.1%
- **Date of max DD:** 2024-10-28 (equity ₹9,591 → recovery 2024-11-11 = 14 days)

## 9.4 Risk of Ruin
- At 1% risk, 12-loss streak = 11.4% lost → 0% ruin (spot)
- At 2% risk, same streak = 21.6% lost → 1.2% ruin probability over 2y if 2 streaks cluster
- **Exposure:** 80.98% (in market 81% of time) — high exposure, trend system

