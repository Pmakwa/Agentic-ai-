# ACTION LEDGER — sab kuch jo actually kiya gaya (ordered)

Har line = ek executed action. Format: `# | kya kiya → natija`.
Narrative version: `00_A_TO_Z_LOG.md` · Raw evidence: respective `probes/` folders.

## A. Foundation (setup → step 2)
1–44 · Setup batch
- V2 spec link → direct fetch **403 (Cloudflare)** → `r.jina.ai` reader se poora text mila → `00_SYSTEM/_raw/` me saved
- V2.0 spec (112 sections, 42,743 chars, `4aa1c6a1f872a3f3`) + V1.0 spec (21,302 chars, `456102f91c061b6e`) import
- `provenance.json` + `verify_provenance.py` → **4/4 PASS**
- `uai_mem.py` (13 subcommands) + seed memory records
- `OPERATIONAL_PROTOCOL.md` (14 rules) + `AGENT_REGISTRY.md` (40+ agents) + `01_STEP2/` ke 9 documents
- `telegram_bot.py` (Telegram console + LLM bridge) likha (creds ke bina inert — verify kiya)
- `index.html` + `DASHBOARD.html` + `SAMJHO.html` + Hindi font asset
- `tests/test_memory_os.sh` → **28 tests, 0 fail**

## B. Capability audit (phase 1)
45–58
- 29-site live matrix (curl + real UA) → `site_matrix.csv`
- Secrets scan (12 vars) → **koi cred nahi** (documented)
- Browser-lib fix (playwright persistence path `/opt/ms-playwright`)
- Audit docs `00–05` + `CAPABILITY_MAP v1.0` + 9 memory adds (→ 37 records)

## C. Deep exploration #1
59–70
- Persistence mapping → `/home/user/.cache` wipe hota hai, `/opt/*` survive karta hai
- `/opt` me shift: playwright 657 MB, fonts, model caches
- Probes: DDG, `systemd --user` (dead), ffmpeg, docx/xlsx/pptx, fastembed, Hindi OCR, espeak
- Bug fix: `pkill` self-match → PID-only kill
- `CAPABILITY_MAP v1.1` (45 capabilities) + `bootstrap_environment.sh` + control-center server `:8000`

## D. Phase 2 — Access Expansion
71–90
- 4 probe batches → `03_ACCESS_EXPANSION/probes/phase2_*.txt`
- `tools/access_routes.py` (demo/fetch/rss/so/paper/nse/wb) + provenance jsonl
- Verified: Medium via jina 15,158 B · Wayback SO 1,175,484 B · Reddit CDX 3 threads · yfinance RELIANCE.NS ₹1244.0 · NSE via jina · OpenAIRE 98,943 B · Google Patents (Bell 1876) · Nominatim · GDELT (30s gap) · IA Scholar (limited)
- 6 deliverables likhe (master report, routes matrix, blocker register, playbook, unknown queue, expansion graph)
- `CAPABILITY_MAP v2.0` + MEM-SEM-0007..0016 (→ 57) + README/index patches + master report present kiya

## E. Sweep #1 (corrections)
91–100
- systemd oneshot `inactive(dead)` = **success** (pehla assumption galat tha — correct kiya)
- `route_monitor.py` + `uai-cos-monitor.{service,timer}` live (30-min cycle) → 6/6 routes 200
- UA fix: full Chrome UA → 403 (jina + monitor) → neutral `UAI-COS-research/1.0`

## F. Installs + Local AI
101–105
- apt/pip batch; unknowns clear (OpenAIRE/Nominatim/GDELT/patents/IA Scholar)
- Qwen2.5-0.5B GGUF → `/opt/uai-cache/models_qwen05b.gguf` (491 MB); `local_ai.py` (chat/say/transcribe/status) verified
- `MEM-SEM-0017..0024` + 1 supersede (→ 65) + `07_SELF_SWEEP_v2.md` + `v2.1` sync + Hindi mp3 (175,536 B)

## G. GitHub dig ("barikhi se khangalo")
109–116
- 2 probe batches (24 probes) → `04_GITHUB_UNLOCK/probes/phase_gh_probe*.txt`
- Tokenless verified: repo/issues search, releases/assets, raw, codeload, clone, wiki, GH Archive, containers
- Live: `yq` release binary install; `crane` se alpine image export (8.7 MB / 515 files, bina Docker)
- `github_unlock.py` (12 commands) smoke OK + report + `v2.2` + MEM-SEM-0025/0026 (→ 67) + README/index + Hindi summary

## H. Social unlock
117–123
- Batch 1 probes (Chrome UA) → `05_SOCIAL_UNLOCK/probes/phase_social_probe.txt`
- Batch 2 inline: Bluesky UA sensitivity, YouTube RSS 404, Mastodon instance variance, fxtwitter 200, `npx rsshub` fail
- SDKs: atproto, praw 8.0.3, tweepy 4.17.0 (installed + tested)
- Fact-check: X 2026 pay-per-use pricing; Reddit API free tier + manual approval
- Report `05_SOCIAL_UNLOCK/00_SOCIAL_PLATFORM_UNLOCK_REPORT.md` + `CAPABILITY_MAP v2.3` + MEM-SEM-0027/0028 (→ 69) + INDEX/DASH + README/index + live demo + Hindi summary

## I. Repo hunt (latest, 2026-09-23)
- GitHub search API (unauth, stars-sorted) — 10+ queries per platform → `06_REPO_HUNT/probes/repo_discovery.txt`
- Install: `gallery-dl 1.32.13`, `pinterest-dl 1.3.0`, `youtube-transcript-api`, `youtube-comment-downloader`, `instaloader 4.15.3`, `facebook-scraper`, `f2 0.0.1.7`
- Live tests (batch A–I, 9 evidence files):
  - gallery-dl ✅ TikTok 19.4 MB, Bluesky 3.4 MB, Pinterest metadata, Tumblr 530 KB
  - gallery-dl ❌ Reddit "blocked by network security", X `AuthRequired`, FB `AuthRequired`, IG 429 loop, Weibo 403
  - redlib instances ✅ safereddit.com + red.artemislena.eu (25 titles/scores, thread + comments)
  - pinterest-dl ✅ search 8.5 MB + board 3.0 MB
  - youtube-transcript-api ✅ 166 segments; youtube-comment-downloader ✅
  - fxtwitter ✅ + vxtwitter ✅ · Bluesky public API ✅
  - facebook-scraper ❌ 0 posts; raw proof: mbasic/m → `login.php` (302)
  - instaloader ❌ empty `web_profile_info`; IG viewers: imginn 403, picuki 522, instanavigation 000
  - Invidious: yewtu.be browser-verification gate; inv.nadeko.net endpoints disabled
  - dead front-ends: teddit 000, xeddit parking, quetre 410, proxitok 000, neuters 502, libremdb 500, piped 526, biblio 000
- **RSSHub self-host (bada kaam):**
  - clone + `pnpm install` (914 MB) → 2 optional native modules fail (non-fatal)
  - route build → **OOM kill (137)** → 4 GB swapfile add → build ✅ (Node 22 zaroori: undici@8 `markAsUncloneable` crash on Node 20) → `/opt/uai-cache/node22` install
  - global CLIs: pnpm 9.15.9, tsx, tsdown, cross-env, typescript
  - bundle: local `tsdown v0.23.0` ✅ → `dist/index.mjs`
  - server run `:1200` with `PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright` → **LIVE**
  - 13 routes ✅ (telegram, tiktok, threads, mastodon, youtube, pinterest, weibo, zhihu) · 4 need config (twitter/instagram/tumblr/github) · 3 upstream blocked (bilibili 412, linkedin empty, douyin browser fail)
- `tools/social_unlock.py` (10 subcommands) — full smoke test pass
- Report `06_REPO_HUNT/00_REPO_UNLOCK_REPORT.md` + `CAPABILITY_MAP v2.4` (22,914 B, `aef4a0c1a7bd36e9`, 20 evidence) + MEM-SEM-0029/0030 (**→ 71**) + INDEX/DASH + README/index + 30 evidence files

## J. Repo packaging (ab)
- `AGENTS.md` (agent manual) + `START_HERE.md` (human quick-start) likhe
- `CONVERSATION/` folder (ye log + ledger + Q&A + Hindi summary)
- `RUNBOOK.md` + `ENVIRONMENT.md` + `.gitignore` + CI smoke workflow + push helper script
- `git init` + commits + `git bundle` (offline transfer) — push tab jab user token/repo de
