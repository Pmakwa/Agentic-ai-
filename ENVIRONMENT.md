# ENVIRONMENT — is sandbox ki asli haqeeqat (verified)

> Ye file ChatGPT/agent ke liye hai: **kya available hai, kya nahi, kya persist karta hai.**
> Jo yahan nahi likha, wo assume mat karo — pehle test karo (spec §2 zero-assumption).

## 1. Hardware / OS
| Cheez | Value |
|---|---|
| OS | Debian 13 (kernel 6.1.x) |
| CPU/RAM | 2 vCPU / **1984 MB RAM** (+ `/swapfile` 4 GB **added** by us) |
| Disk | ~25 GB root (≈14 GB free) |
| GPU | ❌ none (CPU-only inference) |
| User | `user`, **sudo root available** |
| Timezone | host UTC; user Asia/Calcutta |

## 2. Runtimes & toolchain (verified)
- Python **3.13**, Node **20.20.2** + **22.23.2** (`/opt/uai-cache/node22` — RSSHub ke liye zaroori)
- pnpm 9.15.9, tsx, tsdown 0.23 (local in rsshub), cross-env, typescript (global)
- ffmpeg, sox (**mp3 encoder nahi**, ogg/flac), pandoc 3.1.11.1, pdflatex, graphviz, ImageMagick 7, ocrmypdf 16.7
- aria2, jq, ripgrep, fd, duckdb 1.5.5, polars, pyarrow, trafilatura, feedparser, pypdf/pdfplumber
- yt-dlp, gallery-dl 1.32.13, pinterest-dl 1.3.0, youtube-transcript-api, youtube-comment-downloader, f2 0.0.1.7
- praw 8.0.3, tweepy 4.17.0, atproto 0.0.72, instaloader 4.15.3, facebook-scraper
- `tools/bin/`: `yq` (14.2 MB), `crane` (11.9 MB) — GitHub releases se, persist karte hain

## 3. Persistence model (bahut important)
| Path | Persist? |
|---|---|
| `/home/user/**` (regular files) | ✅ turns ke beech |
| `/opt/ms-playwright` (657 MB browsers) | ✅ |
| `/opt/uai-cache/{fastembed,hf,models_qwen05b.gguf}` | ✅ |
| `/swapfile` | ✅ (session ke andar; reboot par dobara banana pad sakta hai) |
| `/home/user/.cache`, `node_modules`, `.venv`, `dist`, `build` | ❌ wipe |
| Running processes / ports / systemd state | ❌ die ho jate hain |

## 4. Credentials — **NONE**
12 environment variables probed (Telegram token, LLM keys, GitHub token, AWS, HF, Reddit, Twitter...) → **sab absent**.
`gh` CLI installed hai par **logged out**: `gh auth status` → "You are not logged into any GitHub hosts".
No `~/.ssh`, no `~/.git-credentials`, no `~/.config/gh`.

**Iska matlab:** GitHub par **push** karne ke liye, aur saare keyed APIs (Reddit OAuth, YouTube key, Meta app, Pinterest app,
X pay-per-use) ke liye **user ko credential dena padega**. Local tool (`git init`, `git commit`, `git bundle`) bina token chal jata hai.

## 5. Network
- HTTP/HTTPS outbound ✅ · **IPv6 egress blocked** (patentsview jaise IPv6-only hosts unreachable)
- Kuch hosts **is IP ko block karte hain**: reddit (direct), medium, stackoverflow, nseindia, quora, sciencedirect, tripadvisor
- Isliye fallbacks: `r.jina.ai` reader, Wayback, official/RSS APIs, redlib instances (third-party IPs se reddit padhte hain)
- **UA sensitivity (seekha hua):** `r.jina.ai` aur Bluesky public API par **full Chrome UA → 403**; neutral `UAI-COS-research/1.0` → 200

## 6. Playwright / browser
- Browsers `/opt/ms-playwright` me: `chromium-1243`, `chromium_headless_shell-1243`, `ffmpeg-1011`
- **`PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright` set karna zaroori** (warna default `.cache` path dhoondhta hai jo wipe hota hai)
- x.com aur reddit extraction playwright se **nahi hoti** (blocked) — screen scraping ke bharose mat raho

## 7. Servers jo chal rahe hain (last verified)
| Server | Port | Status | Restart command |
|---|---|---|---|
| UAI-COS control center | 8000 | HTTP 200 | `cd uai-cos && python3 -m http.server 8000 --bind 0.0.0.0` |
| RSSHub (self-hosted) | 1200 | HTTP 200 | RUNBOOK §3(e) |

## 8. Systemd
`uai-cos-monitor.{service,timer}` installed aur live (30-min cycle, oneshot).
Purane heartbeat/fast-test units **remove** kiye gaye; `uai-test.service` dead hai.
Oneshot ka `inactive (dead)` = **success**, failure nahi.

## 9. Limits (hard)
- 2 GB RAM (swap ke bina bade Node builds OOM hote hain)
- No GPU → local LLM sirf 0.5B class
- No credentials → keyed APIs/push blocked
- IPv6 blocked, kuch hosts egress-IP block karte hain
- CAPTCHA/login-wall/paywall bypass **allowed nahi** (spec §24) — chahe tool available ho

## ⚠️ Persistence reality (2026-09-23 update)

**/opt reset hua mila** ek fresh sandbox me (RSSHub, node22, yq/crane gaye; pip tools bhi). Workspace `/home/user` safe tha.
**Recovery:** `bash tools/bootstrap_environment.sh` — apt+pip+yq+crane+node22 ~60s, RSSHub rebuild ~2min (VERIFIED).
Isliye rule: **/opt ko permanent maan kar mat chalo** — har session start par `python3 tools/self_audit.py` chalao (stamp + services check),
aur zaroorat par bootstrap.

## Persisted heavy artifacts (2026-09-23 — workspace lean rakhne ke liye /opt me)

| Path | Size | Kya |
|---|---|---|
| `/opt/uai-cache/rsshub` | ~996 MB | RSSHub self-host (2015 namespaces) — clone + `pnpm install` + `pnpm build`; chalao: `cd /opt/uai-cache/rsshub && PATH=/opt/uai-cache/node22/bin:$PATH NODE_ENV=production PORT=1200 node dist/index.mjs` |
| `/opt/uai-cache/bin` | 25 MB | `yq` + `crane` (tools/fetch_binaries.sh) — `export PATH=/opt/uai-cache/bin:$PATH` |
| `/opt/uai-cache/node22` | 200 MB | Node 22 (RSSHub ke liye) |
| `/opt/uai-cache/models_qwen05b.gguf` | 469 MB | local_ai.py (Qwen2.5-0.5B) |
| `/opt/ms-playwright` | — | Playwright browsers (`PLAYWRIGHT_BROWSERS_PATH`) |

**Rule:** `node_modules`/`.pnpm`/`dist` type cheezein workspace ke andar nahi rakhte (snapshot 128 MB cap + hygiene).
