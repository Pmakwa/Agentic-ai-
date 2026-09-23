# PART 10 — ROBUSTNESS & OVERFITTING AUDIT

## 10.1 Audit Criteria (Section 30-32)
Flagged if:
- Trades <20 → insufficient sample
- Nearby profitability <50% → sensitivity
- OOS PF <1.0 → fails validation
- Top 10% trades >40% profit → fragile distribution

## 10.2 Results

| Category | Count | % | Example |
|----------|-------|---|---------|
| Robust | 8 | 0.7% | SOL 1h P14x3.0 1:3 (nearby 80% profitable, OOS pass, 119 trades, PF1.31) |
| Fragile (few trades) | 45 | 4.1% | SOL 4h F7x2.0_M20... 49 trades, 52% profit from top 5 trades |
| Overfit (isolated peak) | 210 | 19.2% | BTC 1h P7x3.5 1:2 (neighbor -2550) |
| Regime-dependent | 180 | 16.5% | SOL 4h P14x1.5 (train +1890, OOS -293) |
| Insufficient trades | 120 | 11% | TRIPLE 4h 25 trades (DD4.52% but only 25 trades) |
| Pure losers | 824 | 75.5% | PF <1.0 |

## 10.3 Multiple Testing Awareness (Section 31)
- Tested 1,092 configs → expected 54 false positives at p=0.05 by chance alone
- Observed 268 profitable → **~214 may be luck**, only 8 survive robustness+OOS+adequate trades
- **Do NOT present single highest (+3135) as reliable without OOS** — we validated and it passes, but 4h +2404 fails OOS proving danger

## 10.4 Verdict
- **Reliable edge:** ONLY SOL 1h P14x3.0 region (and nearby P14x3.5)
- **Everything else:** Overfit, fragile, or regime-dependent
