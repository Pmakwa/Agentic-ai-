# STEP 2 — MASTER PLAN: UAI-COS v2.0 ka LIVE implementation layer

> **Step 1 (done):** V2 prompt ko poora le liya, canonical spec bana liya, aur is environment me
> actually live kar diya — memory store + CLI + audit + dashboard + agent registry + operational protocol.
> **Step 2 (ye folder):** us spec ka *implementation layer* — roadmap, scenarios, memory-type integration,
> agent lifecycle, evaluation/regression, aur external-environment integration (bot/API interfaces).

## Step 1 ke asli deliverables (verify kar lo)

| # | File | Kya hai |
|---|---|---|
| 1 | `00_SYSTEM/00_UAI-COS_V2.0_SPEC.md` | V2 prompt ka **poora uncut text** (112 sections, ~44k chars, sha256 hash ke saath) |
| 2 | `00_SYSTEM/01_UAI-COS_V1.0_SPEC.md` | Base V1 system (Part 1–15) — intent disambiguation ke liye |
| 3 | `00_SYSTEM/IMPORT_LOG.md` | Provenance: source URL, import method (403 → reader proxy), hashes, intro/outro as-is |
| 4 | `memory/store/memory.jsonl` | **Live memory database** — 22 records, Section-13 schema par |
| 5 | `memory/INDEX.md` | Auto-generated retrieval index (boot par yahi padha jaata hai) |
| 6 | `DASHBOARD.html` | Offline memory dashboard (counts, types, statuses, table) |
| 7 | `tools/uai_mem.py` | Memory OS engine: governance validation, duplicate/conflict detect, supersede, expiry, audit, index, dash |
| 8 | `tools/seed_initial_memory.sh` | Bootstrap script (idempotent-ish, CLI ke through hi likhti hai) |
| 9 | `agents/AGENT_REGISTRY.md` | 40+ logical agents + handoff protocol + stop conditions |
| 10 | `00_SYSTEM/OPERATIONAL_PROTOCOL.md` | 14-rule always-on protocol (turn start / during / end) |
| 11 | `logs/AUDIT_LOG.md` | Har memory operation ka audit trail |

## Source chat me "next step" ke roop me 3 options offer hue the

1. **Detailed user scenarios** for Advanced V2.0
2. **Integration of memory types** in Advanced V2.0
3. **Implementation roadmap** for supervisor + agent lifecycle

Isliye Step 2 me wahi 3 cheezein *aadhi-aadhi* nahi, **poori** bana rahe hain — plus ek 4th layer jo source chat me missing tha:
**evaluation/regression + external environment integration** (kyunki spec khud kehta hai: verify before trust, aur
memory tabhi kaam ki jab real storage/retrieval ho).

## Step 2 ke deliverables

| # | File | Type | Kya dega |
|---|---|---|---|
| 1 | `01_IMPLEMENTATION_ROADMAP.md` | Roadmap | 6 phases, task-level breakdown, acceptance criteria, kya already done hai |
| 2 | `02_USER_SCENARIOS.md` | Scenarios | 8 end-to-end scenarios — request se memory update tak, actual expected behaviour ke saath |
| 3 | `03_MEMORY_TYPES_INTEGRATION.md` | Integration | V1 ke 12 types → V2 advanced taxonomy, storage/retrieval/expiry rules, is workspace ke live examples |
| 4 | `04_AGENT_LIFECYCLE.md` | Lifecycle | Agent states, model routing tiers, permission matrix, handoff payload rules |
| 5 | `05_EVALUATION_AND_GOLDEN_TESTS.md` | QA | 12 golden tests, metrics, regression policy, quality scorecard |
| 6 | `06_EXTERNAL_INTEGRATION.md` | Integration | Telegram bot + any-LLM system prompt compiler — taaki ye system is workspace se bahar bhi chale |
| 7 | `../tests/test_memory_os.sh` | Runnable | Live regression suite (ye actually chalti hai, PASS output deti hai) |
| 8 | `../tools/interfaces/telegram_bot.py` | Runnable | Telegram memory-console bot (token aapke env se) |
| 9 | `../tools/build_system_prompt.py` | Runnable | Compact, paste-anywhere system prompt generator (spec + live memory index se) |

## Guiding rule (spec se)
> "Har information ko store karna goal nahi hai. Sahi information ko sahi scope me, sahi time par,
> sahi agent ko, sahi permission ke saath, sahi tareeke se use karna goal hai."

Isliye Step 2 ka har deliverable ek hi sawal ka jawab deta hai: **spec ka kaun sa hissa, kab, kis
condition par, kaunse agent se, aur kis evidence par execute hoga?**
