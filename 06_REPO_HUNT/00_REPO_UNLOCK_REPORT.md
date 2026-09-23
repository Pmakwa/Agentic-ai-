# REPO UNLOCK REPORT — Agent-Accessible GitHub Repos: Discovered, Installed, Live-Tested

**Date:** 2026-09-23 · **Environment:** Debian 13, 2 vCPU / 2 GB RAM (+4 GB swap), Node 20 & 22, Python 3.13, no GPU, no credentials present
**Method:** GitHub search API (stars-sorted, unauth) → candidate shortlist → real install/clone → **live tokenless test in this environment** → per-platform verdict
**Evidence (raw):** `06_REPO_HUNT/probes/` (30 files) · **Tool:** `tools/social_unlock.py` (10 subcommands, all smoke-tested)
**Boundary (spec §24):** only public/authorized access routes. No login-wall, CAPTCHA, paywall or anti-bot bypass. Repos whose only working mode was **account-cookie / identity-pool based were excluded** and are marked so below.

---

## 1. Repos found & what actually happened with each

| # | Repo | ★ | What it is | Verdict in THIS environment |
|---|------|---|-----------|------------------------------|
| 1 | `mikf/gallery-dl` | 19.8k | Multi-platform media downloader (pip) | ✅ **VERIFIED — 4 platforms**: TikTok (@tiktok → 3 files / 19.4 MB), Bluesky (2 files / 3.4 MB), Pinterest (105 KB pin metadata incl. `i.pinimg.com/originals/...`), Tumblr (2 files / 530 KB). Reddit → blocked, X → AuthRequired, FB → AuthRequired, IG → 429, Weibo → 403 |
| 2 | `redlib-org/redlib` (+ public instances) | 3.8k | Reddit front-end (Rust) | ✅ **VERIFIED via 2 live instances** — `safereddit.com`, `red.artemislena.eu`: 25 titles + 25 scores + 50 thread links; single thread fetch → title + 6 comments. Self-hosting pointless here (same egress IP that Reddit blocks) |
| 3 | `sean1832/pinterest-dl` | 200 | Pinterest downloader (pip) | ✅ **VERIFIED** — `search "nature photography"` → 3 files / 8.5 MB; board scrape → 3 files / 3.0 MB. Tokenless |
| 4 | `DIYgod/RSSHub` | — | Self-hosted RSS for ~2,015 namespaces | ✅ **BUILT & RUNNING locally on :1200** — 13 live routes across 8 platforms (see §3) |
| 5 | `jdepoix/youtube-transcript-api` | 8.4k | YouTube transcripts (pip) | ✅ **VERIFIED** — 166 segments for Fireship video `TbkUKCm3CHQ` |
| 6 | `youtube-comment-downloader` | — | YouTube comments (pip) | ✅ **VERIFIED** — 5 real comments with authors |
| 7 | `vxtwitter` / `fxtwitter` bridges | — | Public X/Tweet data bridges | ✅ **VERIFIED** — `api.vxtwitter.com/jack` (356 B profile), `api.fxtwitter.com/jack/status/20` (1,246 B tweet) |
| 8 | `Evil0ctal/Douyin_TikTok_Download_API` | 20.3k | Self-host TikTok/Douyin data API | ⚠️ **CLONED, NOT DEPLOYED** — v5.1.0 requires Postgres + Redis + **account identity pool (cookies)** → excluded per boundary; infra-heavy. TikTok covered tokenless by gallery-dl/RSSHub instead |
| 9 | `JoeanAmier/TikTokDownloader` | 16.3k | TikTok/Douyin downloader | ⚠️ not deployed — same cookie/account class as #8 |
| 10 | `Johnserf-Seed/f2` | 2.7k | Async multi-platform downloader | ⚠️ **INSTALLED** (f2 0.0.1.7) but not needed — gallery-dl already covers TikTok/Pinterest/Bluesky tokenless |
| 11 | `kevinzg/facebook-scraper` | 3.3k | FB public-page scraper | ❌ **BLOCKED** — 0 posts (pages=1..3, allow_extra_requests=True); raw proof: `mbasic.facebook.com/bbcnews` and `m.facebook.com/bbcnews` both **302→login.php** |
| 12 | `zedeus/nitter` | 14.5k | Twitter front-end | ❌ **ARCHIVED** (2026-09-07) + every tested instance dead (nitter.net 000) |
| 13 | `instaloader/instaloader` | — | Instagram scraper (pip) | ❌ **BLOCKED** — `web_profile_info` returns empty body (login wall) |
| 14 | `mendel5/alternative-front-ends` | 9.2k | Front-end index (used for discovery) | ℹ️ Used to enumerate instances; most are dead: teddit 000, xeddit→parking 302, quetre **410**, proxitok 000, neuters 502, biblio 000, libremdb 500, pipedapi 526 |
| 15 | `pystardust/ytfzf` | 4.2k | YouTube search in terminal | ℹ️ not installed — yt-dlp + Invidious-class coverage already verified for YouTube |
| — | Invidious instances (`yewtu.be`, `inv.nadeko.net`) | — | YT front-end APIs | ❌ `yewtu.be` → HTML "Verifying your browser…" (bot check); `inv.nadeko.net` → "Endpoint disabled" (403). Not usable |

---

## 2. Per-platform verdict after the repo hunt

| Platform | Status | Route that works **now** (tokenless) | Evidence |
|---|---|---|---|
| **Reddit** | 🟢 **NEW — unlocked** | redlib instance (`safereddit.com`, `red.artemislena.eu`) — listings, scores, threads, comments | `probes/repo_test_batchH.txt` |
| **TikTok** | 🟢 **NEW — unlocked** | gallery-dl media download **+** RSSHub `/tiktok/user/:u`, `/tiktok/live/:u` (+ oEmbed from earlier work) | `repo_test_batchA3.txt`, `rsshub_test2.txt` |
| **Pinterest** | 🟢 **NEW — unlocked** | pinterest-dl search/board/pin **+** gallery-dl pin metadata **+** RSSHub `/pinterest/user/:u` | `repo_tool_smoke.txt` |
| **Threads** | 🟢 **NEW — unlocked** | RSSHub `/threads/:user` (7 posts of @zuck) and `/threads/search/:kw` (14 items) | `rsshub_routes_test.txt` |
| **Weibo** | 🟢 **NEW — unlocked** | RSSHub `/weibo/user/:uid` (31.8 KB), `/weibo/search/hot` — uses Weibo's own public visitor-cookie flow | `rsshub_test2.txt` |
| **Bluesky** | 🟢 unlocked (extended) | gallery-dl media (2 files) + public API (keyless) | `repo_test_batchA3.txt` |
| **Mastodon** | 🟢 unlocked (extended) | public API + RSSHub `/mastodon/acct/:acct`, `/mastodon/tag/:site/:tag` | `rsshub_test2.txt` |
| **Telegram** | 🟢 unlocked (extended) | RSSHub `/telegram/channel/:u` (20 items), `/telegram/blog` (287 KB) + `t.me/s/` scraping | `rsshub_errors.txt` |
| **YouTube** | 🟢 unlocked (extended) | yt-dlp + transcripts + comments + RSSHub `/youtube/user/:handle` (30 items) | `repo_tool_smoke.txt` |
| **Tumblr** | 🟢 **NEW — unlocked** | gallery-dl (2 files); RSSHub route exists but needs config | `repo_test_batchC.txt` |
| **X / Twitter** | 🟡 LIMITED | Only public bridges (`api.fxtwitter.com`, `api.vxtwitter.com`). gallery-dl wants cookies; RSSHub route → `ConfigNotFoundError: Twitter API is not configured` (paid) | `repo_test_batchA3.txt`, `rsshub_errors.txt` |
| **Instagram** | 🔴 BLOCKED here | gallery-dl → 429 loop; instaloader → empty JSON (login wall); instanavigation 000 / imginn 403 / picuki 522; homepage 302→login | `repo_test_batchA3.txt`, `repo_test_batchI.txt` |
| **Facebook** | 🔴 BLOCKED here | login redirect (proved), gallery-dl `AuthRequired`, scraper 0 posts; Graph API needs app ID | `repo_test_batchC.txt` |
| **LinkedIn** | 🔴 BLOCKED here | RSSHub route → "this route is empty" (login wall) | `rsshub_test2.txt` + server log |
| **Bilibili** | 🔴 BLOCKED here | API 412 risk-control, browser fallback also 412 | server log (`rsshub_errors.txt`) |
| **Douyin** | ⚪ UNKNOWN here | Playwright navigation to douyin.com failed (browser closed) | server log |
| **VK** | ⚪ LIMITED | gallery-dl ran but extracted 0 files | `repo_test_batchD.txt` |

---

## 3. RSSHub — self-hosted, live in this workspace

**What it took (all real, all recorded):**
1. `git clone` + `pnpm install` (914 MB `node_modules`; two optional native modules failed to compile — non-fatal)
2. **Node 22 required** — bundled `undici@8` needs `webidl.util.markAsUncloneable`; Node 20 crashed the route build → installed Node v22.23.2 to `/opt/uai-cache/node22`
3. Route build initially **OOM-killed (exit 137)** on 2 GB RAM → added a **4 GB swapfile** → routes built (`assets/build/routes.json`, 2,015 namespaces)
4. `tsdown` bundle (local v0.23.0 + local TS 6) → `dist/index.mjs`
5. Server needs `PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright` (browser-driven routes otherwise error)
6. **Running now:** `http://127.0.0.1:1200` (bound 0.0.0.0) — reachable from the workspace preview

**Route verdicts (tested live, `probes/rsshub_routes_test.txt` + `rsshub_test2.txt`):**

| Route | Result | Note |
|---|---|---|
| `/telegram/channel/telegram` | ✅ 200 · 20 items | also `/telegram/blog` 200 (287 KB) |
| `/tiktok/user/tiktok` | ✅ 200 · 10 items | also `/tiktok/live/tiktok` |
| `/threads/zuck` · `/threads/search/ai` | ✅ 200 · 7 and 14 items | **new platform** |
| `/mastodon/acct/kev@fosstodon.org/statuses` · `/mastodon/tag/fosstodon.org/linux` | ✅ 200 · 20 items | |
| `/youtube/user/Fireship` | ✅ 200 · 30 items | |
| `/pinterest/user/pinterest` | ✅ 200 · 15 items | |
| `/weibo/user/2803301701` · `/weibo/search/hot` | ✅ 200 · 31.8 KB / 25.2 KB | visitor-cookie flow |
| `/zhihu/hot` | ✅ 200 | control, non-social |
| `/twitter/...` | ❌ 503 | `ConfigNotFoundError: Twitter API is not configured` (paid API) |
| `/instagram/...` | ❌ 503 | `ConfigNotFoundError: Instagram RSS is disabled (needs cookie config)` |
| `/tumblr/posts/...` | ❌ 503 | needs Tumblr client config (gallery-dl covers Tumblr instead) |
| `/github/trending/daily/python` | ❌ 503 | needs `GITHUB_ACCESS_TOKEN` |
| `/bilibili/...` | ❌ 503 | upstream 412 risk-control |
| `/linkedin/company/.../posts` | ❌ 503 | upstream empty (login wall) |
| `/douyin/...` | ❌ 503 | Playwright navigation to douyin failed |

---

## 4. Working tool: `tools/social_unlock.py`

Wraps **only** routes verified above. All 10 subcommands smoke-tested (`probes/repo_tool_smoke.txt`):

```bash
python3 tools/social_unlock.py status                                  # live-check every route
python3 tools/social_unlock.py reddit programming -n 5 --threads 2     # redlib → JSON (titles/scores/comments)
python3 tools/social_unlock.py rsshub /threads/zuck -n 3               # local RSSHub → JSON items
python3 tools/social_unlock.py gallery https://www.tiktok.com/@tiktok --limit 1
python3 tools/social_unlock.py pin "search:minimal desk setup" -n 2    # 2 files / 1.2 MB
python3 tools/social_unlock.py pin "url:https://www.pinterest.com/pinterest/official-news/" -n 2
python3 tools/social_unlock.py transcript TbkUKCm3CHQ --chars 300      # 166 segments
python3 tools/social_unlock.py comments TbkUKCm3CHQ -n 3
python3 tools/social_unlock.py x jack                                  # vxtwitter/fxtwitter bridge
python3 tools/social_unlock.py bsky bsky.app
```

---

## 5. Provenance (per §28 format: ROUTE → SOURCE → EVIDENCE → REQUIREMENTS → TEST RESULT → STATUS)

| Route | Source | Evidence file | Requirements | Test result | Status |
|---|---|---|---|---|---|
| Reddit via redlib | safereddit.com, red.artemislena.eu | `repo_test_batchH.txt`, `redlib_working.txt` | none (public web) | 25 titles/scores, thread + 6 comments | **VERIFIED** |
| TikTok media | gallery-dl 1.32.13 | `repo_test_batchA3.txt` | none | 3 files / 19.4 MB | **VERIFIED** |
| TikTok feed | RSSHub local | `rsshub_errors.txt` | local server on :1200 | 10 items | **VERIFIED** |
| Pinterest media/search | pinterest-dl 1.3.0 | `repo_tool_smoke.txt` | none | 2–3 files per query | **VERIFIED** |
| Pinterest metadata | gallery-dl | `repo_test_batchA3.txt` | none | 105 KB JSON incl. orig image URL | **VERIFIED** |
| Threads posts/search | RSSHub local | `rsshub_routes_test.txt` | local server | 7 / 14 items | **VERIFIED** |
| Weibo user/hot | RSSHub local | `rsshub_test2.txt` | local server (visitor cookie) | 200, 31.8 KB | **VERIFIED** |
| Bluesky media/API | gallery-dl; public.api.bsky.app | `repo_test_batchA3.txt` | none | 2 files; profile 200 | **VERIFIED** |
| Mastodon acct/tag | RSSHub local; public API | `rsshub_test2.txt` | none | 20 items / 46.5 KB | **VERIFIED** |
| Tumblr media | gallery-dl | `repo_test_batchC.txt` | none | 2 files / 530 KB | **VERIFIED** |
| YouTube transcripts | youtube-transcript-api | `repo_tool_smoke.txt` | none | 166 segments | **VERIFIED** |
| YouTube comments | youtube-comment-downloader | `repo_test_batchD.txt` | none | 5 comments | **VERIFIED** |
| X public data | api.fxtwitter.com / api.vxtwitter.com | `repo_test_batchG.txt` | none | 200 + real payload | **LIMITED (third-party bridge, public data only)** |
| IG / FB / LinkedIn / Bilibili / Douyin | various | `repo_test_batchA3/C/I.txt`, server log | would need login/cookies/paid API | blocked | **UNAVAILABLE here** |
| X full timeline/API | X API | web fact-check | paid pay-per-use | n/a without credits | **UNAVAILABLE (unpaid)** |

---

## 6. Honest limits & next options

1. **Instagram/Facebook/LinkedIn/Bilibili** stay blocked — every tokenless repo route hit a login wall, a 429/412 risk-control, or a dead front-end. Only legitimate unlock left is **account/OAuth credentials** you supply (Meta app, LinkedIn app) — that's an authorization question, not a repo question.
2. **X** full API needs paid credits ($0.005/post read class pricing, 2026); public **bridges** (fxtwitter/vxtwitter) cover individual tweets/profiles tokenless.
3. **Reddit** redlib instances are third-party volunteers — they can rate-limit (catsarch 429) or die; the tool falls back between the two verified instances automatically.
4. **RSSHub** is running locally; if the sandbox restarts, restart with:
   `cd tools/rsshub && PATH=/opt/uai-cache/node22/bin:$PATH PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright NODE_ENV=production PORT=1200 node dist/index.mjs`
5. **Unknown-route queue:** Douyin browser mode, VK media extraction, Threads without RSSHub, Weibo long-term stability (visitor-cookie cooldowns), Instaloader with anonymous session ids.

*Stop condition (§34): this is the maximum repo-level unlock achievable within the currently observable and authorized environment.*
