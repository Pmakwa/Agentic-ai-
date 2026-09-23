# UAI-COS v2.0 — IMPLEMENTATION ROADMAP (Supervisor + Agent Lifecycle)

> Spec me "Implementation roadmap for supervisor and agent lifecycle" ek *offer* tha, actual plan nahi tha.
> Ye file wahi gap fill karti hai: 6 phases, har phase me tasks, deliverable, acceptance criteria aur
> honest status (kya is workspace me already chalu hai vs kya future me banana hai).

---

## Phase 0 — FOUNDATION (✅ DONE, is turn me live)
**Maqsad:** spec ko canonical banane ke saath ek *chalne wala* file-backed memory OS.

| Task | Deliverable | Acceptance criteria | Status |
|---|---|---|---|
| V2 prompt import (uncut) | `00_SYSTEM/00_...V2.0_SPEC.md` | 112 sections present, sha256 recorded | ✅ |
| V1 base preserve | `01_...V1.0_SPEC.md` | Part 1–15 intact | ✅ |
| Provenance log | `IMPORT_LOG.md` | URL, method, hashes, intro/outro | ✅ |
| Memory store schema | `memory/store/memory.jsonl` | Section-13 fields mandatory, CLI validate kare | ✅ |
| Governance validation | `uai_mem.py add` | high-confidence fact bina source **block** ho | ✅ |
| Duplicate + conflict detect | `uai_mem.py add` | same statement → skip; same key alag statement → dono `conflicted` | ✅ |
| Supersede / expiry / archive | `uai_mem.py` | purani record delete nahi hoti, history badhti hai | ✅ |
| Health audit | `uai_mem.py audit` | issues classify ho kar score deta hai | ✅ (100/100 current) |
| Retrieval index + dashboard | `INDEX.md`, `DASHBOARD.html` | auto-generated, boot-read ready | ✅ |
| Always-on protocol | `OPERATIONAL_PROTOCOL.md` | 14 rules, turn start/during/end mapped | ✅ |

**Exit criteria:** `bash tests/test_memory_os.sh` → all PASS. `uai_mem.py audit` → ≥ 90 score.

---

## Phase 1 — SUPERVISOR CORE (🟡 partially live)
**Maqsad:** supervisor ka *decidable* behaviour — har turn par same tarah decision lena.

| Task | Kaam | Acceptance criteria | Status |
|---|---|---|---|
| Risk classifier | Request ko 4 risk tiers me daalna (dekho `04_AGENT_LIFECYCLE.md` §Risk) | Har turn ka risk tier determine + log | 🟡 manual, abhi rule-based |
| Requirement register | Har turn me mandatory/optional points nikalna aur end par tick karna | Zero missed mandatory point (golden tests G1, G8) | 🟡 protocol me chalu |
| Retrieval scorer | Memory retrieval ko score karna: scope match + authority + freshness + confidence + instruction overlap | Top-5 relevant ids har turn, INDEX se | 🟡 abhi manual + CLI |
| Conflict resolver | Priority order: current instruction > explicit correction > verified current state > project decision > memory | Conflicted record par decision + audit entry | 🟡 engine ready, decisions manual |
| Stop-condition check | Anti-loop, permission missing, unresolvable conflict | 3 fail par rukna + user ko batana | ✅ rule live |

**Next action:** retrieval scorer ko `tools/uai_mem.py retrieve` subcommand bana kar automate karna (Phase 3 ka base).

---

## Phase 2 — MEMORY OS HARDENING (🟡)
| Task | Kaam | Acceptance criteria |
|---|---|---|
| Decay scoring | Type-wise TTL + last_verified se "freshness score" | `audit` me stale list (live) |
| Promotion pipeline (#99) | candidate → active → verified, evidence ke saath | Bina evidence promotion nahi (live) |
| Demotion pipeline (#100) | expired / conflicted / invalid → demote, retain history | `supersede` + `expire` (live) |
| Embedding retrieval | keyword → semantic similarity (local embeddings ya API) | Recall@5 ≥ 0.9 golden set par |
| Backup/restore (#86) | `memory.jsonl` ka snapshot + restore command | restore ke baad audit PASS |
| Privacy isolation (#70) | `sensitivity` field par read permissions | `private/secret` records shared-tag ke saath flag (live rule) |

---

## Phase 3 — AGENT ORCHESTRATION (🟡 logical only)
| Task | Kaam | Acceptance criteria |
|---|---|---|
| Routing engine (#64) | Task type → deterministic agent chain | Har task type ke liye chain defined (`AGENT_REGISTRY.md`) |
| Handoff payload validator | Section-25 JSON schema validate | Invalid handoff → reject + log |
| Parallelization (#65) | Independent sub-tasks parallel | 2×+ speed on multi-part tasks |
| Consensus / disagreement (#89, #90) | Aapas me conflict wale agent outputs ka protocol | Disagreement disclose hota hai, chhupta nahi |
| Model routing tier | Har agent role ke liye model tier (fast/standard/deep) | Cost aur quality ka balance — table `04_AGENT_LIFECYCLE.md` me |

---

## Phase 4 — MULTI-MODEL EXECUTION (🔴 future)
| Task | Kaam |
|---|---|
| Sub-agent spawning | Real parallel agents (har ek apna context window, minimum necessary context ke saath) |
| Cross-model verification | Ek model likhe, doosra verify kare (Section 11 live form) |
| Cost guard | Token budget per task + stop condition |
| Sandboxed tool permissions | Per-agent least privilege (Section 0.6) |

> **Honest limitation:** is workspace me main ek single agent hoon jo ye roles sequentially nibhata hoon.
> Real parallel sub-agents ke liye external orchestration (n8n / LangGraph / custom runner) chahiye — Phase 6.

---

## Phase 5 — OBSERVABILITY, EVALUATION, REGRESSION (🟡)
| Task | Kaam | Status |
|---|---|---|
| Audit log | Har memory op ka trail | ✅ `logs/AUDIT_LOG.md` |
| Metrics (#52, #53) | Precision of retrieval, conflict rate, stale rate, correction rate | 🟡 audit me kuch, baaki manual |
| Golden tests (#55) | 12 fixed test cases | ✅ documented + 9 automated (`tests/`) |
| Regression suite (#56) | Har change ke baad suite chale | ✅ `bash tests/test_memory_os.sh` |
| Scorecard (#106) | Har bade output par 8-dimension score | ✅ `05_EVALUATION_AND_GOLDEN_TESTS.md` |

---

## Phase 6 — EXTERNAL ENVIRONMENT INTEGRATION (🟡 ready to run)
**Maqsad:** spec sirf is chat me na rahe — kisi bhi environment me kaam kare.

| Task | Kaam | Status |
|---|---|---|
| System prompt compiler | Spec + live memory se compact prompt utpann karna (paste-anywhere) | ✅ `tools/build_system_prompt.py` |
| Telegram console | Bot se `/mem`, `/list`, `/audit`, `/ask` | ✅ code ready (token chahiye) |
| API/webhook layer | Webhook → memory add + audit | 🔴 future |
| Scheduled health job | Roz `expire` + `audit` + reminder | 🔴 future (cron) |
| Mobile/desktop access | Dashboard ko device par dekhna | ✅ `DASHBOARD.html` + live preview |

---

## Progress snapshot (is workspace ka sach)

```
Phase 0  ████████████████████  100%   live
Phase 1  ██████████░░░░░░░░░░   50%   rules live, automation pending
Phase 2  ██████████░░░░░░░░░░   50%   engine live, semantic search pending
Phase 3  ████████░░░░░░░░░░░░   40%   registry live, orchestration pending
Phase 4  ██░░░░░░░░░░░░░░░░░░   10%   design only
Phase 5  ████████████████░░░░   80%   suite + scorecard live
Phase 6  ████████████░░░░░░░░   60%   code ready, deployment pending
```

## Agla concrete kadam (jitna chhota utna accha)
1. `uai_mem.py retrieve "<task>"` — scored retrieval (Phase 1 → 3 ka bridge).
2. `bash tests/test_memory_os.sh` ko har change ke baad run karna — regression discipline.
3. Telegram bot ko token ke saath live karna — taaki memory bahar se bhi likhi ja sake.
4. Baaki 3 golden tests (G10–G12) automate karna — long-running project state ke liye.
