# RESEARCH EXECUTION PROTOCOL
## PHOENIX RISING V2.0 — Institutional Scientific Quant Standard

This protocol enforces strict research integrity (§0, §2, §20, §28, §45, §52). No strategy may be considered without traversing each sequential phase.

---

### Step 1: Hypothesis Formulation & Economic Rationale (§10)
- State the market inefficiency or structural behavioral bias.
- Why should this edge exist? (Liquidity provision, volatility risk premium, trend persistence, retail order flow imbalance).
- Does it require new indicators or can simple features capture it? (§11, §12).

### Step 2: Data Integrity & Cleanliness Gate (§19)
- Run timestamp and candle check (no future leakage, zero lookahead).
- Adjust for corporate actions, dividends, and splits.
- Verify survivorship bias status.

### Step 3: In-Sample Development (§20)
- Allocate 60% of data to in-sample development.
- Test baseline deterministic entry/exit rules (§13, §14).
- Log experiment in `RESEARCH_LEDGER.json` (§27).

### Step 4: Out-Of-Sample Validation & Walk-Forward Analysis (§21, §22)
- Allocate 20% to validation.
- Run rolling walk-forward optimization (e.g. 12-month train -> 3-month test -> roll).
- Verify performance decay is within acceptable bounds (<20% decay).

### Step 5: Stress Testing & Monte Carlo Simulation (§23, §24)
- 10,000 Monte Carlo permutations (randomizing trade sequence, execution delay, slippage shocks).
- Apply 3x fee shock and 2x slippage shock.
- Confirm probability of ruin is < 5%.

### Step 6: Adversarial Red-Team Audit (§28)
- Independent Agent 10 attempts to disprove the strategy.
- Checks: hidden leverage, parameter curve-fitting, regime dependence, over-optimization.

### Step 7: Final Holdout Lock & Deployment Consideration (§45, §46, §50)
- Lock final 20% holdout dataset.
- Run exactly ONE single pass. No parameter adjustments permitted after holdout exposure.
- If passed, proceed to paper/shadow mode ramp (§36, §37).
