# PHASES — UAI-COS ka phase tracker

> **Source of truth:** `PROJECT_BOARD/phases.json` · **Engine:** `tools/phase_runner.py`
> (`status` · `next` · `add` · `set` · `md`). Neeche ka table auto-generated hai — haath se edit mat karo,
> sirf `python3 tools/phase_runner.py md` chalao.

<!-- PHASES:START -->
| # | Phase | Status | Owner | Deliverable / Evidence | Next step |
|---|---|---|---|---|---|
| P0 | **Spec import (Step 1): V1 + V2.0 hash-verified** | ✅ DONE | agent | 00_SYSTEM/00_UAI-COS_V2.0_SPEC.md (4aa1c6a1f872a3f3) | - |
| P1 | **Step 2 implementation: memory OS + protocol + tests** | ✅ DONE | agent | 01_STEP2/, tools/uai_mem.py, tests/test_memory_os.sh (28/28) | - |
| P2 | **Capability audit: 29-site matrix + secrets scan + map v1.0** | ✅ DONE | agent | 02_CAPABILITY_AUDIT/ | - |
| P3 | **Deep exploration #1: persistence, /opt caches, bug fixes** | ✅ DONE | agent | 02_CAPABILITY_AUDIT/07_SELF_SWEEP_v2.md, /opt/ms-playwright | - |
| P4 | **Access Expansion (Phase 2): blocked targets -> legitimate routes** | ✅ DONE | agent | 03_ACCESS_EXPANSION/ (6 deliverables + route_provenance.jsonl) | - |
| P5 | **Sweep #1: systemd correction + proxy UA fix + route monitor** | ✅ DONE | agent | tools/route_monitor.py, logs/route_health*.txt | - |
| P6 | **Installs + Local AI (Qwen 0.5B, edge-tts, whisper)** | ✅ DONE | agent | tools/local_ai.py, /opt/uai-cache/models_qwen05b.gguf | - |
| P7 | **Self-Sweep v2 -> capability map v2.1** | ✅ DONE | agent | 07_SELF_SWEEP_v2.md, MEM-SEM-0017..0024 | - |
| P8 | **GitHub dig (tokenless capability report)** | ✅ DONE | agent | 04_GITHUB_UNLOCK/, tools/github_unlock.py (12 cmds) | - |
| P9 | **Social unlock matrix (tokenless / needs-creds / no-route)** | ✅ DONE | agent | 05_SOCIAL_UNLOCK/00_SOCIAL_PLATFORM_UNLOCK_REPORT.md | - |
| P10 | **Repo hunt: 15 repos live-tested + RSSHub self-host** | ✅ DONE | agent | 06_REPO_HUNT/ (30 evidence files), tools/social_unlock.py | - |
| P11 | **GitHub handover + push (repo live, CI green)** | ✅ DONE | agent | Pmakwa/Agentic-ai- · PUSH_LOG.md | - |
| P12 | **Boot mechanism: V2 apply karna (agent_boot.py + attestation)** | ✅ DONE | agent | tools/agent_boot.py, UAI-COS_BOOT_PROMPT.md, tests/boot_attestation.md | - |
| P13 | **Sync + standing rules (har baat-cheet repo me)** | 🟢 ACTIVE | agent | tools/sync_to_github.sh, CONVERSATION/04_STANDING_INSTRUCTIONS.md | har kaam ke baad push + PUSH_LOG entry |
| P14 | **RSSHub route expansion (baaki namespaces verify)** | ✅ DONE | agent | tools/rsshub_verify.py: 28 curated routes + 120/250 namespace sweep (rsshub_routes_test2.txt + rsshub_routes_sweep.txt) | RSSHub start karo (RUNBOOK §3) -> /vimeo, /spotify, /hackernews, regional test -> report + push |
| P15 | **Monitoring integration (naye verified routes 30-min cycle me)** | ✅ DONE | agent | route_monitor.py 11/11 PASS (logs/route_health.txt, logs/route_health.jsonl) | P14 ke verified routes add karo -> manual run -> logs |
| P16 | **Naye public endpoints (Discord invite, Spotify oEmbed, pullpush)** | ✅ DONE | agent | discord invite + spotify oembed + pullpush reddit (social_unlock.py invite|spotify|pullpush) | test -> evidence -> social_unlock.py me subcommand |
| P17 | **Keyed APIs (Reddit OAuth, YouTube Data, Telegram bot, Meta app)** | ⏸ WAITING | user+agent | target: .env (gitignored) + live tests | user creds de -> live test -> map update |
| P18 | **Project board cards paste karna** | ⏸ WAITING | user | PROJECT_BOARD/CARDS.md | GitHub Project -> Add item -> paste |
| P19 | **Prompt intake system (naya V2-type prompt aaye to apply karna)** | ✅ DONE | agent | tools/import_prompt.py + 00_SYSTEM/prompts_index.json | user naya prompt de -> import_prompt.py -> phase auto-add -> apply -> push |
| P20 | **Multi-platform agent pointers (sab agents same system apply karein)** | ✅ DONE | agent | CLAUDE.md, GEMINI.md, .windsurfrules, .cursor/rules/uai-cos.mdc, .github/copilot-instructions.md | - |
| P21 | **Repo unlock sweep (30+ starred repos) — test karo, verified tools lock karo** | 🟡 NEXT | agent | target: 06_REPO_HUNT/probes/repo_sweep_starred.txt + CAPABILITY_MAP bump + social_unlock subcommands | kaam shuru karo + evidence add karo |
| P22 | **Structured prompt registry + apply (V2/Phase-1/2/3 jaise saare prompts)** | ✅ DONE | agent | tools/prompt_registry.py + PROMPTS/registry.json (10 entries, SP-001..SP-010) + boot payload §4b + AGENTS §13 + PHASE_PROTOCOL §8 | - |
| P23 | **Workspace hygiene: junk/duplicate cleanup + heavy deps /opt me** | ✅ DONE | agent | tools/cleanup_workspace.py (protected heavy dirs) + logs/cleanup_2026-09-23.md + workspace 1.1GB->8.1MB + RSSHub /opt/uai-cache/rsshub | - |
| P24 | **MASTER SELF-AUDIT blueprint apply (original Phase 1 + Phase 2 prompt)** | ✅ DONE | agent | 00_SYSTEM/02_UAI-COS_MASTER_SELF_AUDIT_SPEC.md (hash e8d8620d378adc48) + 07_SELF_AUDIT/ (4 maps + report + roadmap) + tools/apply_phase.py (v2 6/6, self_audit 9/9, phase1 6/6, phase2 7/7) | kaam shuru karo + evidence add karo |
| P25 | **Fresh-sandbox recovery + continuous self-audit tooling** | ✅ DONE | agent | tools/bootstrap_environment.sh (apt+pip+yq+crane+node22+RSSHub, aaj verify) + tools/self_audit.py (env probe v1.2) + RSSHub 3 routes 200 + social status 11/11 | kaam shuru karo + evidence add karo |
<!-- PHASES:END -->

**Total:** 21 phases · **Updated:** 2026-09-23

## Recurring checklist (har naye kaam par — "definition of done")

1. live test + evidence probes/ me
2. report update
3. CAPABILITY_MAP.json version bump
4. uai_mem.py add (memory)
5. index + dash + audit (100/100)
6. README/index sync
7. GITHUB_TOKEN=<token> bash tools/sync_to_github.sh "message"
8. CI green verify + PUSH_LOG entry
9. Hindi summary + options (a/b/c)

## Naya phase kaise add hota hai

1. **User naya prompt/spec de** → `python3 tools/import_prompt.py --url/--file/--text ... --name "V3"`
   → file `00_SYSTEM/` me save + memory record + phase auto-add (status=next) → phir usko apply karo.
2. **User naya kaam bole** → `python3 tools/phase_runner.py add --title "..." --status next`
   → `python3 tools/phase_runner.py set --id P2x --status active` → kaam karo → `set --status done`.

## Environment me "applied" ka matlab (kya live hai + check kaise karein)

| Cheez | Live? | Check |
|---|---|---|
| Memory OS (73 records) | ✅ | `python3 tools/uai_mem.py audit` |
| Capability map v2.4 (20 evidence) | ✅ | `python3 tools/agent_boot.py --json` |
| Boot system (P12) | ✅ | `python3 tools/agent_boot.py --json` |
| Phase engine + prompt intake (P19/P20) | ✅ | `python3 tools/phase_runner.py next` |
| Social routes (P10) | ⚠️ instance-dependent | `python3 tools/social_unlock.py status` |
| RSSHub `:1200` | ⚠️ sandbox restart par band | `RUNBOOK.md` §3 |
| Control-center `:8000` | ⚠️ same | `RUNBOOK.md` §9 |
| systemd monitor (30 min) | ⚠️ timer dependency | `systemctl status uai-cos-monitor.timer` |
