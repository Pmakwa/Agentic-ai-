# PROMPTS/REGISTRY.md — structured prompts ka index (auto-generated)

> Source of truth: `PROMPTS/registry.json` · regenerate: `python3 tools/prompt_registry.py md`
> Naya structured prompt aaye (V3 / Phase 4 / naya rules-pack) -> `prompt_registry.py add ...` phir usko apply karke
> `apply --id SP-xxx --where '...'` chalao. Rule: **koi structured prompt bina apply ke nahi chhodna.**

| ID | Type | Prompt | Verbatim | Body hash | Applied in | File |
|---|---|---|---|---|---|---|
| SP-001 | `spec` | **V1.0 structured spec (Parts 1-15)** | ✅ | `456102f91c061b6e` | AGENTS.md §1, tools/agent_boot.py, 00_SYSTEM/OPERATIONAL_PROTOCOL.md | `00_SYSTEM/01_UAI-COS_V1.0_SPEC.md` |
| SP-002 | `spec` | **V2.0 structured spec (112 sections)** | ✅ | `4aa1c6a1f872a3f3` | AGENTS.md §1-§4, UAI-COS_BOOT_PROMPT.md, tools/agent_boot.py (SPEC MAP), memory/, tests/boot_attestation.md | `00_SYSTEM/00_UAI-COS_V2.0_SPEC.md` |
| SP-003 | `phase` | **Phase 1 — capability baseline + audit prompt** | ◐ recon | `688ae5921d0637fd` | 02_CAPABILITY_AUDIT/, ENVIRONMENT.md, AGENTS.md §4 | `PROMPTS/SP-003_PHASE_1_CAPABILITY_BASELINE_AUDIT_PROMPT.md` |
| SP-004 | `phase` | **Phase 2 — access expansion prompt** | ◐ recon | `13fc6c18b904ffe3` | 03_ACCESS_EXPANSION/, tools/access_routes.py, CONVERSATION/01_ACTION_LEDGER.md §D | `PROMPTS/SP-004_PHASE_2_ACCESS_EXPANSION_PROMPT.md` |
| SP-005 | `phase` | **Phase 3 — repo hunt + apply (GitHub repos ko capability me badlo)** | ◐ recon | `1fb384c1d6e99c2e` | 06_REPO_HUNT/, 05_SOCIAL_UNLOCK/, tools/social_unlock.py, PROJECT_BOARD/phases.json | `PROMPTS/SP-005_PHASE_3_REPO_HUNT_APPLY_GITHUB_REPOS_KO_CAPABILITY_ME_BADLO.md` |
| SP-006 | `rules` | **Standing instructions pack (user rules — always apply)** | ✅ | `431aebffb78beab2` | AGENTS.md §5,§9, UAI-COS_BOOT_PROMPT.md, PHASE_PROTOCOL.md §5, tests/ci_extra.py (boot freshness) | `CONVERSATION/04_STANDING_INSTRUCTIONS.md` |
| SP-007 | `boot` | **Boot prompt (paste-ready, generated)** | ◐ recon | `20114d89d0d32809` | CLAUDE.md, GEMINI.md, .windsurfrules, .cursor/rules/uai-cos.mdc, .github/copilot-instructions.md, START_HERE.md | `UAI-COS_BOOT_PROMPT.md` |
| SP-008 | `rules` | **Workspace hygiene + recurring cleanup rule** | ✅ | `4ef4f0d96b4b55ae` | AGENTS.md §12, PHASE_PROTOCOL.md §7, PROJECT_BOARD/phases.json (recurring_checklist), tools/cleanup_workspace.py | `PROMPTS/SP-008_WORKSPACE_HYGIENE_RECURRING_CLEANUP_RULE.md` |
| SP-009 | `rules` | **Structured-prompt apply rule (V2 / Phase-1 / Phase-2 / aage jo bhi)** | ✅ | `42eccd5c4aec6052` | PROMPTS/registry.json, PROMPTS/REGISTRY.md, AGENTS.md §13, PHASE_PROTOCOL.md §8, tests/ci_extra.py | `PROMPTS/SP-009_STRUCTURED_PROMPT_APPLY_RULE_V2_PHASE_1_PHASE_2_AAGE_JO_BHI.md` |
| SP-010 | `rules` | **Cleanup safety lesson (node_modules dedupe incident)** | ◐ recon | `dd670d171c8892ec` | tools/cleanup_workspace.py (PROTECTED/HEAVY_SKIP/DELETE_CAP), AGENTS.md §12, PHASE_PROTOCOL.md §7, tests/ci_extra.py | `PROMPTS/SP-010_CLEANUP_SAFETY_LESSON_NODE_MODULES_DEDUPE_INCIDENT.md` |

**Total:** 10 structured prompts · updated 2026-09-23 06:53:28

## Naya structured prompt add karne ka tareeka

```bash
python3 tools/prompt_registry.py add --file /tmp/new_prompt.txt --title "Phase 4 — X" --type phase \
    --source "user message 2026-09-24" --verbatim
python3 tools/prompt_registry.py apply --id SP-009 --where 'AGENTS.md §9, UAI-COS_BOOT_PROMPT.md'
python3 tools/prompt_registry.py verify && python3 tools/agent_boot.py --write
```
