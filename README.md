# UAI-COS v2.0 — Universal AI Cognitive Operating System (live workspace)

> 🚀 **Naya agent? pehle [`AGENTS.md`](AGENTS.md) padho, phir [`START_HERE.md`](START_HERE.md).**
> Poori baat-cheet ka A-to-Z record [`CONVERSATION/`](CONVERSATION/00_A_TO_Z_LOG.md) me · chalane ke commands [`RUNBOOK.md`](RUNBOOK.md) ·
> environment ki haqeeqat [`ENVIRONMENT.md`](ENVIRONMENT.md) · machine-readable truth [`CAPABILITY_MAP.json`](02_CAPABILITY_AUDIT/CAPABILITY_MAP.json) (v2.6).

Ye tumhare **V2 prompt** ka poora implementation hai — spec sirf text me nahi, chalne wale system me.

> **LANGUAGE RULE:** user se Hindi, English alphabet/spelling me (Roman Hindi) — jab tak user Devanagari/other na maange.
> **REALITY RULE:** "permanent/unlimited memory" ka jhootha claim nahi — jo is workspace me disk par save hai, wahi persistent hai.

---

## 1. Kya-kya bana hai (Step 1 + Step 2)

```
uai-cos/
├── 00_SYSTEM/                              ← SPEC LAYER
│   ├── 00_UAI-COS_V2.0_SPEC.md             ✅ V2 prompt — poora, uncut (112 sections, sha256 hash ke saath)
│   ├── 01_UAI-COS_V1.0_SPEC.md             ✅ base V1 (Part 1–15) — history + intent disambiguation
│   ├── IMPORT_LOG.md                       ✅ provenance: source URL, 403→proxy method, hashes
│   ├── provenance.json                     ✅ machine-readable hashes (verifier ka input)
│   ├── _raw/                               ✅ raw extraction backup (hash-verified)
│   ├── OPERATIONAL_PROTOCOL.md             ✅ 14-rule always-on protocol (turn start / during / end)
│   └── UAI-COS_SYSTEM_PROMPT_{compact,standard,full}.md   ✅ paste-anywhere compiled prompts (live memory inline)
│
├── memory/                                 ← MEMORY OS (live data)
│   ├── store/memory.jsonl                  ✅ 82 records — Section-13 schema par
│   ├── INDEX.md                            ✅ auto-generated retrieval index (boot-read)
│   └── store/archive.jsonl                 ✅ archive (delete nahi, retire)
│
├── tools/
│   ├── uai_mem.py                          ✅ memory engine (13 subcommands)
│   ├── seed_initial_memory.sh              ✅ memory bootstrap script
│   ├── bootstrap_environment.sh            ✅ session start: apt/pip/browser/fonts/model-cache + verify
│   ├── build_system_prompt.py              ✅ system prompt compiler
│   ├── verify_provenance.py                ✅ spec files ka hash IMPORT se match hai ya nahi
│   └── interfaces/telegram_bot.py          ✅ Telegram console + LLM bridge
│
├── agents/AGENT_REGISTRY.md                ✅ 40+ logical agents + handoff protocol + stop conditions
├── tests/test_memory_os.sh                 ✅ regression suite — 28 tests, 28 pass
├── logs/AUDIT_LOG.md                       ✅ har operation ka audit trail
├── DASHBOARD.html                          ✅ offline memory dashboard

├── 03_ACCESS_EXPANSION/                    ← PHASE 2: ACCESS EXPANSION (blocked targets ke legitimate raste)
│   ├── 00_PHASE2_MASTER_REPORT.md          ✅ 12 blocked targets → 9 verified routes (evidence ke saath)
│   ├── 01_VERIFIED_ROUTES_MATRIX.md        ✅ har route ka status/label + proof (living document)
│   ├── 02_BLOCKER_ANALYSIS_REGISTER.md     ✅ §22 format: TARGET…HARD LIMIT (14 targets, 24 blocker types)
│   ├── 03_ACCESS_PLAYBOOK.md               ✅ chalne wali recipes + rate-limit rules
│   ├── 04_ACCESS_UNKNOWN_QUEUE_AND_HARD_LIMITS.md  ✅ AQ-01..15 + HL-01..10 + 4-state classification
│   ├── 05_EXPANSION_GRAPH_AND_USER_ACTIONS.md      ✅ capability multiplier graph + 8 user actions
│   ├── route_provenance.jsonl              ✅ har route test ka ROUTE→…→STATUS record
│   └── probes/                             ✅ 5 raw evidence files (koi claim bina proof nahi)
│
├── 06_REPO_HUNT/                          ← REPO UNLOCK (GitHub se platform access, live-tested)
│   ├── 00_REPO_UNLOCK_REPORT.md            ✅ 15 repos tested → 7 platforms naye khule (Reddit/TikTok/Pinterest/Threads/Weibo/Tumblr/…)
│   └── probes/                             ✅ 30 raw evidence files (install + test logs)
│
├── 05_SOCIAL_UNLOCK/                      ← SOCIAL PLATFORM UNLOCK (verified matrix)
│   ├── 00_SOCIAL_PLATFORM_UNLOCK_REPORT.md ✅ kaunse platforms bina creds khule (Reddit/Telegram/Bluesky/Mastodon/TikTok/YouTube)
│   └── probes/                             ✅ raw evidence
│
├── 04_GITHUB_UNLOCK/                       ← GITHUB KHANGAL (24 probes, sab verified)
│   ├── 00_GITHUB_CAPABILITY_REPORT.md      ✅ 7 capability categories (binaries/code/data/packages/containers/intel/discovery)
│   └── probes/                             ✅ raw evidence (2 probe files)
│
├── tools/github_unlock.py                  ✅ GitHub toolkit (12 commands, bina token)
├── PROMPTS/registry.json + REGISTRY.md     ✅ structured prompts (V1/V2/Phase-1/2/3/rules) + kahan apply hue
├── tools/prompt_registry.py                ✅ structured prompt add/apply/verify engine
├── tools/cleanup_workspace.py              ✅ workspace hygiene (junk/duplicate cleanup, time-to-time)
├── PHASE_PROTOCOL.md                       ✅ naye phase/prompt apply karne ka contract (boot → phase → evidence → push)
├── UAI-COS_BOOT_PROMPT.md                  ✅ paste-ready boot prompt (chat-only agents, auto-generated)
├── CLAUDE.md / GEMINI.md / .windsurfrules  ✅ har agent-platform ke liye boot pointers (same system apply)
├── .cursor/rules/uai-cos.mdc               ✅ Cursor rule (always apply)
├── .github/copilot-instructions.md         ✅ Copilot instructions
├── PROJECT_BOARD/phases.json               ✅ machine-readable phase source of truth (21 phases)
├── tools/phase_runner.py                   ✅ phase engine (status/next/add/set/md)
├── tools/import_prompt.py                  ✅ naya V2-type prompt import (hash + memory + auto phase)
├── tools/sync_to_github.sh                 ✅ ek command me commit + push (secret-scan ke saath)
├── tests/boot_attestation.md               ✅ 12-sawal boot test + scoring
├── tests/ci_extra.py                       ✅ CI checks: phases/prompt-hash/boot-freshness
├── tools/social_unlock.py                  ✅ repo-verified platform layer (10 commands, smoke-tested)
├── tools/agent_boot.py                     ✅ V2 boot payload generator (agent isse boot hota hai)
├── UAI-COS_BOOT_PROMPT.md                  ✅ paste-ready boot prompt (chat-only agents ke liye, 14 KB)
├── tests/boot_attestation.md               ✅ 12-sawal boot test + scoring (booted / partial / not booted)
├── /opt/uai-cache/rsshub                   ✅ self-hosted RSSHub (2015 namespaces, :1200) — heavy deps workspace ke bahar
├── /opt/uai-cache/bin/{yq,crane}           ✅ GitHub release se aaye binaries (persist, workspace ke bahar)
├── tools/access_routes.py                  ✅ WORKING route library (fetch/rss/so/papers/nse/wayback + demo)
├── 02_CAPABILITY_AUDIT/                    ← SELF-AUDIT (blueprint Phase 1–15)
│   ├── 00_EXECUTIVE_SUMMARY.md             ✅ asli discovery: kya possible hai, kya nahi (evidence ke saath)
│   ├── 01_CAPABILITY_AND_ACCESS_MAP.md     ✅ capability + tool + environment + access + permission matrices
│   ├── 02_RESEARCH_CAPABILITY_MAP.md       ✅ web matrix, 25 research methods, source-quality rubric
│   ├── 03_FALLBACK_ROUTE_GRAPH.md          ✅ 10-question protocol, route graph, 15 failure classes
│   ├── 04_UNKNOWN_QUEUE_AND_TESTS.md       ✅ U1–U14 unknowns + safe test commands
│   ├── 05_EXPANSION_ROADMAP_AND_MAINTENANCE.md ✅ capability expansion + versioning protocol
│   ├── 06_DEEP_EXPLORATION_v2.1.md         ✅ 2nd pass: persistence solved, 13+ naye capabilities, naye limits
│   ├── CAPABILITY_MAP.json                 ✅ machine-readable, versioned (v1.0)
│   └── probes/                             ✅ rerunnable probes + raw evidence (env + site matrix)
│
└── 01_STEP2/                               ← STEP 2 (implementation layer)
    ├── 00_STEP2_MASTER_PLAN.md             ✅ plan + deliverables map
    ├── 01_IMPLEMENTATION_ROADMAP.md        ✅ 6 phases, honest status (kya live, kya future)
    ├── 02_USER_SCENARIOS.md                ✅ 9 end-to-end scenarios (real memory IDs ke saath)
    ├── 03_MEMORY_TYPES_INTEGRATION.md      ✅ 15 types, lifecycle, confidence, retrieval, ACL, graph
    ├── 04_AGENT_LIFECYCLE.md               ✅ 11 lifecycle states, 6 autonomy levels, tool risk tiers
    ├── 05_EVALUATION_AND_GOLDEN_TESTS.md   ✅ 12 golden tests, metrics, scorecard, real audit numbers
    └── 06_EXTERNAL_INTEGRATION.md          ✅ Telegram bot + prompt compiler + privacy checklist
```

## 2. Abhi ka system status (2026-09-23, asli numbers)

| Metric | Value | Command |
|---|---|---|
| Live memory records | **82** | `python3 tools/uai_mem.py stats` |
| Memory health score | **100/100** | `python3 tools/uai_mem.py audit` |
| Golden tests | **28/28 pass** | `bash tests/test_memory_os.sh` |
| Open conflicts | 0 | audit |
| Duplicates | 0 | audit |
| Schema violations | 0 | audit |
| Provenance coverage | 26/26 | audit |
| Spec compliance | V2 ke 112 sections mapped | `01_STEP2/` docs |
| Provenance integrity | 4/4 files PASS | `python3 tools/verify_provenance.py` |
| Capability audit | **v2.1** — persistence solved, browser+model cache /opt me | `02_CAPABILITY_AUDIT/` |

## 3. Quick start

```bash
cd /home/user/uai-cos

# (a) system boot read — sirf relevant memory
python3 tools/uai_mem.py list --status active --status verified --wide

# (b) naya info capture karo (governance validate karega)
python3 tools/uai_mem.py add --type preference --status candidate --confidence medium \
        --authority user_explicit --source user_instruction \
        --statement "Proposals me GST breakup hamesha dikhana hai" --domain billing

# (c) health check + artifacts refresh
python3 tools/uai_mem.py audit --log && python3 tools/uai_mem.py index && python3 tools/uai_mem.py dash

# (d) regression suite (koi bhi change ke baad)
bash tests/test_memory_os.sh

# (e) kisi bhi chatbot ke liye prompt banao (live memory ke saath)
python3 tools/build_system_prompt.py -m standard -o /tmp/uai_prompt.md
```

## 4. Memory engine ke 13 subcommands

`add` · `list` · `search` · `show` · `update` · `supersede` · `expire` · `archive` · `audit` · `stats` · `index` · `dash` · `export`

**Governance jo engine khud enforce karta hai:**
- High-confidence fact bina verifiable source → **block** [`#0.7`, #13`]
- Same statement dobara → **duplicate skip**; same conflict-key par alag statement → dono **`conflicted`** [`#19`, #21`]
- Delete nahi — **supersede** (bidirectional link + history intact) [`#39`, #87`]
- Past `expires_at` → auto **expired** [`#20`]
- `audit` 9 tarah ke issues pakadta hai: stale working memory, unscoped rules, verified-but-low-confidence,
  privacy leak risk, inference-promoted-to-fact, dangling supersede, duplicates, open conflicts, stale facts [`#79`, #80`]

## 5. Har turn ka rule (short version)

```
READ   → INDEX/active memory → task classify → sirf relevant filter (scope+authority+freshness+confidence)
PLAN   → decomposition → constraint lock → risk tier → tool permission
EXECUTE→ tool se pehle verify → irreversible ho to approval → result verify
RELEASE→ quality gate (intent, coverage, memory correctness, safety, format) → phir answer
WRITE  → memory update (candidate → verified) → index/dash → audit log
```

## 6. Limits (honest disclosure — spec #0.4, #59)

- Ye memory **is workspace ke andar** persist hoti hai. Doosre chat/product me apne aap nahi jaati —
  uske liye `build_system_prompt.py` ka output paste karo, ya Telegram bot chalao.
- Semantic/embedding retrieval abhi nahi hai (Phase 2) — abhi keyword + filters + manual scoring.
- Parallel sub-agents (Phase 4) design-only hain — is setup me roles sequentially nibhaye jaate hain.
- Telegram bot ko chalane ke liye token chahiye (aapke env se) — bina token wo sirf instructions deta hai.
