# PHASES — UAI-COS ka poora phase tracker (status + evidence + next)

> Ye file **canonical progress tracker** hai. Har phase: kya hua, evidence kahan hai, status kya hai.
> Naya phase add karte waqt yahan entry karo + `CAPABILITY_MAP.json` / memory / README sync karo + push karo.

| # | Phase | Status | Deliverable / Evidence |
|---|---|---|---|
| P0 | **Spec import (Step 1)** — V1 + V2.0 (112 sections) hash-verified | ✅ DONE | `00_SYSTEM/00_UAI-COS_V2.0_SPEC.md` (42,743 chars · `4aa1c6a1f872a3f3`), `01_UAI-COS_V1.0_SPEC.md`, `provenance.json`, verifier 4/4 |
| P1 | **Step 2 implementation** — poora system apply | ✅ DONE | `01_STEP2/` (9 docs), `tools/uai_mem.py` (13 cmds), `OPERATIONAL_PROTOCOL.md`, `agents/AGENT_REGISTRY.md`, tests 28/28 |
| P2 | **Capability audit** — 29-site matrix, secrets scan, map v1.0 | ✅ DONE | `02_CAPABILITY_AUDIT/` + `probes/site_matrix.csv` |
| P3 | **Deep exploration #1** — persistence, /opt caches, probes, bug fixes | ✅ DONE | `02_CAPABILITY_AUDIT/07…`, `/opt/ms-playwright`, `/opt/uai-cache`, map v1.1 |
| P4 | **Access Expansion (Phase 2)** — 12 blocked targets → legitimate routes | ✅ DONE | `03_ACCESS_EXPANSION/` (6 deliverables + `route_provenance.jsonl`) |
| P5 | **Sweep #1** — systemd correction + proxy UA fix + monitor | ✅ DONE | `tools/route_monitor.py`, `logs/route_health*.txt`, systemd units (30-min cycle) |
| P6 | **Installs + Local AI** | ✅ DONE | `tools/local_ai.py` (Qwen2.5-0.5B, edge-tts, whisper), `/opt/uai-cache/models_qwen05b.gguf` |
| P7 | **Self-Sweep v2 → map v2.1** | ✅ DONE | `07_SELF_SWEEP_v2.md`, MEM-SEM-0017..0024, Hindi mp3 summary |
| P8 | **GitHub dig** ("barikhi se khangalo") | ✅ DONE | `04_GITHUB_UNLOCK/` report + `tools/github_unlock.py` (12 cmds) + yq/crane |
| P9 | **Social unlock** | ✅ DONE | `05_SOCIAL_UNLOCK/00_SOCIAL_PLATFORM_UNLOCK_REPORT.md`, SDKs (praw/tweepy/atproto), map v2.3 |
| P10 | **Repo hunt** — 15 repos install + live tests + RSSHub self-host | ✅ DONE | `06_REPO_HUNT/` report + 30 evidence files + `tools/social_unlock.py` (10 cmds), map v2.4 |
| P11 | **GitHub handover + push** | ✅ DONE | Repo live: `Pmakwa/Agentic-ai-` (158+ files), CI "UAI-COS smoke checks" green, tag `v2.0.0` |
| P12 | **Boot mechanism** — V2 ko agent ke environment me apply karna | ✅ DONE | `tools/agent_boot.py`, `UAI-COS_BOOT_PROMPT.md`, `AGENTS.md` STEP 0, `tests/boot_attestation.md` |
| P13 | **Sync + standing rules** — har baat-cheet repo me, phases live rahenge | ✅ DONE (isse chalta rahega) | `tools/sync_to_github.sh`, `CONVERSATION/04_STANDING_INSTRUCTIONS.md`, ye file |
| P14 | **RSSHub route expansion** — 2015 namespaces me se aur verify | 🟡 NEXT | `/vimeo`, `/spotify`, `/hackernews`, regional news; phir `route_monitor.py` me add |
| P15 | **Monitoring integration** — naye routes 30-min health cycle me | 🟡 NEXT | `tools/route_monitor.py` + systemd timer |
| P16 | **Naye public endpoints** — Discord invite, Spotify oEmbed, pullpush archive | 🟡 NEXT | test → evidence → `social_unlock.py` me add |
| P17 | **Keyed APIs (jab user creds de)** — Reddit OAuth, YouTube Data, Telegram bot, Discord bot, Meta app | ⏸ WAITING ON USER | `.env` (gitignored) → live test → map update |
| P18 | **Board cards** — GitHub Project me cards paste karna | ⏸ USER ACTION | `PROJECT_BOARD/CARDS.md` (12 cards) |

## Recurring (har naye kaam par)

1. Live test + evidence → 2. Report update → 3. `CAPABILITY_MAP.json` bump → 4. memory add →
5. `index`+`dash`+`audit` 100/100 → 6. README/index sync → 7. **`tools/sync_to_github.sh` se push** → 8. CI green check → 9. Hindi summary + options.

## Environment me "applied" ka matlab (kya live hai)

| Cheez | Live? | Kaise check karein |
|---|---|---|
| Memory OS (73 records) | ✅ | `python3 tools/uai_mem.py audit` |
| Capability map v2.4 (20 evidence) | ✅ | `python3 -c "import json;print(json.load(open('02_CAPABILITY_AUDIT/CAPABILITY_MAP.json'))['map_version'])"` |
| Boot system (P12) | ✅ | `python3 tools/agent_boot.py --json` |
| Social routes (P10) | ⚠️ instance-dependent | `python3 tools/social_unlock.py status` |
| RSSHub `:1200` | ⚠️ sandbox restart par band ho jata hai | `RUNBOOK.md` §3 se dobara start |
| Control-center `:8000` | ⚠️ same | `python3 -m http.server 8000 --bind 0.0.0.0` |
| systemd monitor (30 min) | ⚠️ sandbox me timer chalna depend karta hai | `systemctl status uai-cos-monitor.timer` |
