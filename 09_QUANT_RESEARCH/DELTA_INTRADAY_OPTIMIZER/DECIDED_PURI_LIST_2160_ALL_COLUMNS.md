# DECIDED FORMAT — PURI LIST (2160 ROWS) — JAISA PEHLE DECIDE KIYA THA, SAB COLUMNS KE SAATH

**Format: Coin → TF (5m→15m→30m) → Net Profit | Har Row Me SAB Columns: Coin, TF, Time Period, Bars, ST1 Period/Mult, ST2 Period/Mult, Settings, SL, RR, Target, Risk, Starting/Ending, Net, Return, DD INR/%, Max Profit/Loss, Avg Win/Loss, Largest, Win%/Loss%, PF, Expectancy, Trades (Win/Loss/BE), Streaks, Sharpe, Sortino, Calmar, Exposure, Duration, Gross Profit/Loss — SAB HAI**

**Puri 2160 rows ki CSV:** `DECIDED_FULL_2160_SETTINGS_PERIOD_COMPLETE.csv` — Excel me kholo, har column filter karo. Neeche 5 rows ka preview (all columns) + har TF ka summary:

### Preview — Pehle 5 Rows (All Columns — Horizontal Scroll)

| # | coin | timeframe | period | bars | st1_period | st1_mult | st2_period | st2_mult | settings | sl | rr | num_trades | win_rate | total_net_profit | ending_capital | return_pct | max_drawdown_pct | profit_factor | expectancy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BTC/INR | 5m | 2026-09-17 to 2026-09-24 (7D) | 1963 | 10 | 3.0 | 10 | 4.0 | ST1(10,3.0)+ST2(10,4.0) | 1.5% | 1:3 | 10 | 80.0 | 719.74 | 10719.74 | 7.2 | 1.11 | 6.72 | 71.97 |
| 2 | BTC/INR | 5m | 2026-09-17 to 2026-09-24 (7D) | 1963 | 10 | 3.0 | 12 | 4.0 | ST1(10,3.0)+ST2(12,4.0) | 1.5% | 1:3 | 10 | 80.0 | 719.74 | 10719.74 | 7.2 | 1.11 | 6.72 | 71.97 |
| 3 | BTC/INR | 5m | 2026-09-17 to 2026-09-24 (7D) | 1963 | 10 | 3.0 | 14 | 4.0 | ST1(10,3.0)+ST2(14,4.0) | 1.5% | 1:3 | 10 | 80.0 | 719.74 | 10719.74 | 7.2 | 1.11 | 6.72 | 71.97 |
| 4 | BTC/INR | 5m | 2026-09-17 to 2026-09-24 (7D) | 1963 | 10 | 4.0 | 10 | 3.0 | ST1(10,4.0)+ST2(10,3.0) | 1.5% | 1:3 | 10 | 80.0 | 719.74 | 10719.74 | 7.2 | 1.11 | 6.72 | 71.97 |
| 5 | BTC/INR | 5m | 2026-09-17 to 2026-09-24 (7D) | 1963 | 10 | 4.0 | 12 | 3.0 | ST1(10,4.0)+ST2(12,3.0) | 1.5% | 1:3 | 10 | 80.0 | 719.74 | 10719.74 | 7.2 | 1.11 | 6.72 | 71.97 |

*Note: CSV me uske alawa bhi **max_drawdown_inr, max_profit, max_loss, largest_win/loss, loss_rate, winning/losing/breakeven_trades, max_win/loss_streak, avg_win/loss_streak, recovery_factor, sharpe, sortino, calmar, exposure_pct, avg/max/min_duration_hours, gross_profit, gross_loss, starting_capital, sl_pct, rr_val, strategy** — sab columns hai jaise pehle decide kiya tha.*

---

### 5m / 15m / 30m — Har TF Ka Count (Puri List Me)

| TF | Coin | Tests | Period | Bars |
|---|---|---|---|---|
| 15m | BTC | 240 | 2026-07-25 to 2026-09-24 (60D) | 5742 |
| 15m | ETH | 240 | 2026-07-25 to 2026-09-24 (60D) | 5742 |
| 15m | SOL | 240 | 2026-07-25 to 2026-09-24 (60D) | 5742 |
| 30m | BTC | 240 | 2026-07-25 to 2026-09-24 (60D) | 2872 |
| 30m | ETH | 240 | 2026-07-25 to 2026-09-24 (60D) | 2872 |
| 30m | SOL | 240 | 2026-07-25 to 2026-09-24 (60D) | 2872 |
| 5m | BTC | 240 | 2026-09-17 to 2026-09-24 (7D) | 1963 |
| 5m | ETH | 240 | 2026-09-17 to 2026-09-24 (7D) | 1963 |
| 5m | SOL | 240 | 2026-09-17 to 2026-09-24 (7D) | 1963 |

- **Total: 2160 tests** (240 combos × 3 coins × 3 TFs)
- **Sorted as decided:** Coin (BTC→ETH→SOL) → TF (5m→15m→30m) → Net Profit High→Low
- **Har row me Settings + Period dono hai**

---

### ⏳ 1h (2Y) — 720 Tests Abhi Bhi Chal Raha Hai (Background PID 3812, ~15 min baaki)

Jaise hi 1h complete hoga, isi file me **720 rows aur add karke 2880 ki puri list** bana dunga, same decide format (Coin→TF→Settings→Period). Tab tak **5m/15m/30m ki puri 2160 rows yahi final hai.**
