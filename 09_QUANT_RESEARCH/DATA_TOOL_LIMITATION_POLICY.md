# LIVE-DATA AND TOOL LIMITATION POLICY
## PHOENIX RISING V2.0 — Truth in Execution & Capabilities

This policy governs the interaction between quantitative simulation and actual live environment tooling (§0, §18, §19, §34, §35).

---

### 1. Data Source Hierarchy & Quality Grading (§20)
| Tier | Source Class | Latency | Coverage | Survivorship Bias Mitigation |
|---|---|---|---|---|
| **Tier 1 (Authoritative)** | Official Exchange Historical Files / SEC EDGAR | End-of-Day / T+1 | Equities, Indices | Full point-in-time adjusted |
| **Tier 2 (Verified Public API)** | Yahoo Finance (`yfinance`), CoinGecko, AlphaVantage | Daily / 1-hour | Global stocks, crypto | Unadjusted intraday; requires verification |
| **Tier 3 (Local Middleware)** | Self-hosted RSSHub feeds (`:1200`) | Minutes | News, sentiment, public feeds | Read-only; proxy dependent |
| **Tier 4 (Scraped / Third-Party)** | Unofficial mirrors | Variable | Ad-hoc | Unreliable; forbidden for backtesting |

### 2. Execution Environment Reality (§6, §34, §35)
- **Account Capital**: Starting at $10,000 limits asset class suitability:
  - High-margin index futures (e.g. CME S&P 500 E-mini) require $12,000+ margin per contract -> **INCOMPATIBLE**.
  - Micro futures (MES), Liquid ETFs (SPY, QQQ), and Spot Equities (with fractional sizing) -> **COMPATIBLE**.
- **Execution Friction**:
  - Minimum modeled commission: $0.005/share or 0.05% per trade.
  - Modeled slippage: 1-2 ticks minimum on liquid instruments; wider during high-volatility regimes (§18).
  - Perfect fill assumptions are strictly prohibited.

### 3. Absolute False Claims Prohibition (§19)
- Never claim live trading execution when only simulated or paper backtesting occurred.
- If live broker API connection is unavailable, classify status as: `PAPER / BACKTEST ONLY — LIVE BROKER NOT CONNECTED`.
