# RUNBOOK — har verified capability ko chalane / dobara banane ke exact commands

> Sab kuch is environment me **actually chala hua** hai. Jo command yahan hai, wo copy-paste chalegi.
> Jahan kuch extra chahiye (Node 22, swap, env var) wahan likha hai.

---

## 1. Pehla boot (fresh sandbox)

```bash
git clone <repo-url> uai-cos && cd uai-cos
bash tools/bootstrap_environment.sh     # apt/pip packages, fonts, playwright path, model cache, PATH
python3 tools/verify_provenance.py      # expect: 4/4 PASS
python3 tools/uai_mem.py audit | tail -3  # expect: 100/100
bash tests/test_memory_os.sh | tail -3    # expect: 28 passed, 0 failed
```

`bootstrap_environment.sh` ke andar jo set hota hai (kyunki `.cache` wipe ho jata hai):
```bash
export PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright      # browsers yahin persist karte hain
export FASTEMBED_CACHE_PATH=/opt/uai-cache/fastembed
export HF_HOME=/opt/uai-cache/hf
export PATH="$HOME/uai-cos/tools/bin:$PATH"             # yq, crane
```

---

## 2. Memory OS (roz ka kaam)

```bash
python3 tools/uai_mem.py add --type semantic --statement "..." --detail "..." \
        --source "..." --confidence very_high --status verified --authority verified_source --tag "x"
python3 tools/uai_mem.py search "instagram"     # dhoondo
python3 tools/uai_mem.py list --type constraint # filter
python3 tools/uai_mem.py audit                  # health (100/100 rakho)
python3 tools/uai_mem.py index && python3 tools/uai_mem.py dash   # regen INDEX + DASHBOARD
python3 tools/uai_mem.py export --format md > /tmp/memory_export.md
python3 tools/build_system_prompt.py            # system prompt me live memory inline
```
Rule: record add karne ke **baad** `index` + `dash` + `audit` chalana zaroori hai (warna dashboard stale ho jata hai).

---

## 3. RSSHub (self-hosted social feeds) — **sabse zyada setup wala hissa**

**Zaroorat:** Node **22+** (Node 20 par `undici@8` crash karta hai) aur **swap** (route build 2 GB RAM me OOM hota hai).

```bash
# (a) swap (ek baar)
sudo fallocate -l 4G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile

# (b) Node 22 (ek baar; /opt persist karta hai)
sudo mkdir -p /opt/uai-cache/node22
curl -sL -o /tmp/node22.tar.xz https://nodejs.org/dist/v22.23.2/node-v22.23.2-linux-x64.tar.xz
sudo tar -xJf /tmp/node22.tar.xz -C /opt/uai-cache/node22 --strip-components=1

# (c) repo + install
git clone --depth 1 https://github.com/DIYgod/RSSHub /opt/uai-cache/rsshub && cd /opt/uai-cache/rsshub
sudo npm i -g pnpm@9 tsx tsdown cross-env typescript     # global CLIs
export PATH="/opt/uai-cache/node22/bin:/usr/bin:$PATH"
pnpm install --reporter=append-only                       # ~914 MB node_modules

# (d) build (routes + bundle) — Node 22 se hi
NODE_ENV=dev NODE_OPTIONS=--max-old-space-size=1536 tsx scripts/workflow/build-routes.ts
NODE_OPTIONS=--max-old-space-size=1536 node node_modules/tsdown/dist/run.mjs   # local tsdown v0.23 use karo

# (e) run (background; 0.0.0.0 par bind hota hai)
NODE_ENV=production PORT=1200 PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright \
  NODE_OPTIONS="--max-old-space-size=1400" node dist/index.mjs
```

**Verified routes (13):** `/telegram/channel/<u>`, `/telegram/blog`, `/tiktok/user/<u>`, `/tiktok/live/<u>`,
`/threads/<user>`, `/threads/search/<kw>`, `/mastodon/acct/<user@instance>/statuses`, `/mastodon/tag/<site>/<tag>`,
`/youtube/user/<handle>`, `/pinterest/user/<u>`, `/weibo/user/<uid>`, `/weibo/search/hot`, `/zhihu/hot`.

**Config chahiye (in par mat atko):** `/twitter/*` (paid Twitter API), `/instagram/*` (cookie config),
`/tumblr/*` (client config), `/github/trending/*` (GitHub token).
**Upstream blocked:** `/bilibili/*` (412 risk control), `/linkedin/*` (empty), `/douyin/*` (browser fail).

---

## 4. Social unlock tool (repo-verified routes)

```bash
python3 tools/social_unlock.py status                                   # sab routes ka live check
python3 tools/social_unlock.py reddit programming -n 5 --threads 2      # redlib auto-fallback (safereddit → artemislena)
python3 tools/social_unlock.py rsshub /threads/zuck -n 3                # local RSSHub → JSON items
python3 tools/social_unlock.py gallery https://www.tiktok.com/@tiktok --limit 1
python3 tools/social_unlock.py gallery https://bsky.app/profile/bsky.app/media --meta-only
python3 tools/social_unlock.py pin "search:minimal desk setup" -n 2
python3 tools/social_unlock.py pin "url:https://www.pinterest.com/pinterest/official-news/" -n 2
python3 tools/social_unlock.py transcript <youtube-video-id> --chars 500
python3 tools/social_unlock.py comments <youtube-video-id> -n 10
python3 tools/social_unlock.py x jack                 # ya  x jack/status/20
python3 tools/social_unlock.py bsky bsky.app
```
Underlying CLIs: `gallery-dl` (pip), `pinterest-dl` (pip), `youtube-transcript-api`, `youtube-comment-downloader`.

---

## 5. General fetch / research routes

```bash
python3 tools/access_routes.py demo                        # saare routes ka smoke
python3 tools/access_routes.py fetch https://medium.com/@x/y   # direct → jina → wayback chain
python3 tools/access_routes.py rss https://feeds.bbci.co.uk/news/rss.xml
python3 tools/access_routes.py so "python asyncio"          # StackExchange API
python3 tools/access_routes.py paper "quantum error correction"
python3 tools/access_routes.py nse marketStatus
python3 tools/access_routes.py wb https://stackoverflow.com/questions/...
```
**Rules jo bhoolni nahi:**
- `r.jina.ai` par **full Chrome UA mat bhejo** (403) — neutral UA (`UAI-COS-research/1.0`) use karo.
- Reddit `.rss` ~60 s window; dobara hit → "Blocked".
- GDELT ≥30 s gap; GitHub search 10/min (bina token).
- IPv6 egress blocked — kuch hosts (patentsview) isliye unreachable hain.

---

## 6. GitHub (bina token)

```bash
python3 tools/github_unlock.py --help      # 12 commands
# Verified: repo/issues search, releases+assets, raw, codeload, clone, wiki, GH Archive, container images
# Token chahiye: code search (401), GraphQL, Actions, write/push
```
Container demo (bina Docker):
```bash
export PATH="$HOME/uai-cos/tools/bin:$PATH"
crane export alpine:latest /tmp/alpine.tar && tar -tf /tmp/alpine.tar | wc -l   # → 515 files
```

---

## 7. Local AI (bina internet, CPU)

```bash
python3 tools/local_ai.py status
python3 tools/local_ai.py chat "explain DNS in 3 lines"     # Qwen2.5-0.5B Q4, ~2-4s
python3 tools/local_ai.py say "namaste, ye hindi audio hai" --out /tmp/hi.mp3
python3 tools/local_ai.py transcribe /tmp/hi.mp3
```
Note: 0.5B model Hindi me weak hai; refusal par `--raw` flag. Model: `/opt/uai-cache/models_qwen05b.gguf`.

---

## 8. Monitoring (systemd, 30-min cycle)

```bash
systemctl status uai-cos-monitor.timer --no-pager      # active hona chahiye
sudo systemctl start uai-cos-monitor.service           # manual run
python3 tools/route_monitor.py                         # direct run → 6/6 routes
tail -5 logs/route_health.txt
```
**Important:** oneshot service chalne ke baad `inactive (dead)` dikhati hai — **ye success hai, failure nahi**.

---

## 9. Dashboards / servers

```bash
# control center (index.html dashboard)
cd /home/user/uai-cos && python3 -m http.server 8000 --bind 0.0.0.0
# RSSHub already :1200 par chalta hai (section 3e)
```
`index.html` ka title deliberately **"UAI-COS v2.0"** hai (system spec version) — use badalna nahi.

---

## 10. Naya capability add karne ka process (definition of done)

1. **Install/clone** karo → 2. **Live tokenless test** chalao (aur error text capture karo) →
3. Evidence file `probes/` me save karo → 4. Report ka section update karo →
5. `CAPABILITY_MAP.json` version bump + evidence path add → 6. `uai_mem.py add` se memory record →
7. `index` + `dash` + `audit` (100/100) → 8. `README.md` + `index.html` sync → 9. User ko Hindi summary + options.
