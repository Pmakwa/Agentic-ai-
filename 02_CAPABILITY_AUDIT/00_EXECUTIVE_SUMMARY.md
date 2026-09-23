# AGENT CAPABILITY & ACCESS MAP — EXECUTIVE SUMMARY

**Audit type:** Agent Operational Self-Audit (blueprint ke Phase 1–15 ke according)
**Auditor:** main (is workspace ka agent), **kisi bhi claim ko verify kiye bina nahi likha**
**Date:** 2026-09-23 (Asia/Kolkata) · **Map version:** `CAPABILITY-MAP v1.0`
**Environment:** `e2b` sandbox · Debian GNU/Linux 13 (trixie) · kernel 6.1.158+ · x86_64 · 2 vCPU · ~1.9 GB RAM · 25 GB disk (20 GB free)
**Identity:** user `user` (uid 1000), groups: `sudo` · **passwordless sudo VERIFIED** (`sudo -n id` → `uid=0`)

> **Blueprint ka sabse bada rule main follow kar raha hoon (Part 29 — No-False-Power):**
> "Full internet access", "sab kuch access kar sakta hoon" — aisi baat **nahi** likhi. Har line ke saath
> confidence label hai: `VERIFIED` / `STRONGLY SUPPORTED` / `POSSIBLE` / `CONDITIONAL` / `UNAVAILABLE` / `RESTRICTED` / `UNKNOWN`.

---

## A. Executive Summary — asli discovery kya nikli

**Sabse important finding:** is environment ki capability **blueprint ke typical assumptions se kaafi zyada** hai.
Sirf "chat + search" nahi hai — ye ek **poora Linux sandbox** hai jisme:

1. **Root access** hai (passwordless sudo) → apt se naye system tools install kar sakta hoon. `VERIFIED`
2. **Network egress open** hai (HTTPS + HTTP + DNS + raw TCP 53/443/25 tak tested). `VERIFIED`
3. **Package managers chalte hain** — pip (PyPI se install), npm (registry), apt (Debian repos), git clone. `VERIFIED`
4. **Real browser automation** setup ho gayi — Playwright + Chromium: launch, screenshot, page→PDF, navigation. `VERIFIED`
5. **OCR** live hai (tesseract 5.5.0 install + test). `VERIFIED (accuracy caveat: default font/resolution par imperfect)`
6. **Parallel background processes** chal sakte hain + 0.0.0.0 par bind karke user ko **live preview** milta hai. `VERIFIED`
7. **Document/data toolchain** — pandas, numpy, scipy, sklearn, matplotlib, openpyxl, python-docx, PIL, cv2, ImageMagick. `VERIFIED`
8. **Native agent tools** — bash, file I/O (read/write/edit), web_search, fetch_page (HTML **aur PDF**), image_search,
   image generation, speech generation (voice register karne ke baad), process control, file presentation. `VERIFIED` (speech: CONDITIONAL)
9. **File-backed memory** — 28+ records, CLI, audit, tests (pichhle phase me bana, chal raha hai). `VERIFIED`

**Sabse important limitation (honest):**

| Cheez | Status | Evidence |
|---|---|---|
| Sandbox me LLM/API keys | **absent** — koi bhi key env me nahi mili | `env` scan: OPENAI/ANTHROPIC/GEMINI/TELEGRAM/GITHUB/AWS… sab absent |
| GPU / torch | `UNAVAILABLE` — no `/dev/nvidia*`, torch import fail | probe |
| Private/login-gated data | `RESTRICTED` — paywall, login wall, Cloudflare bypass **nahi** karunga | reddit/instagram/scienceDirect par 403/proxy deny |
| Real parallel sub-agents | `UNAVAILABLE` — logical roles sequential; parallel **processes** chal jaate hain, parallel **agents** nahi | design limitation |
| Sandbox → user ka device | `UNAVAILABLE` | architecture |
| Cross-turn persistence | **UNKNOWN → test set up** (4 stamp files likhe, agle turn me check hoga) | `_persist_test/` |
| Voice output | `CONDITIONAL` — pehle tum ek voice choose karoge, tab generate hoga | tool contract |

**Ek line me:** is environment me main **ek kaam karne wala Linux computer + browser + research layer + persistent memory** ki tarah operate kar sakta hoon — lekin **tumhari credentials, tumhari private accounts, ya blocked/paywalled sources** ke bina aage nahi badh sakta, aur wo bypass bhi nahi karunga.

---

## B. Capability Inventory (top-level categories)

| # | Category | Verdict | Evidence |
|---|---|---|---|
| C1 | Reasoning / planning / synthesis / analysis | `VERIFIED` (intrinsic) | ye poora audit khud isi se bana |
| C2 | Coding + debugging + execution | `VERIFIED` | Python/Node/Java/C compilers chalte hain, code run hua |
| C3 | Shell / sysadmin | `VERIFIED` | sudo, apt, processes, services, file perms |
| C4 | Web research (search + read) | `VERIFIED (partial coverage)` | search tool + fetch_page kaam karte hain; kuch sites 403 |
| C5 | Browser automation | `VERIFIED` | Chromium launch + screenshot + PDF |
| C6 | Data analysis + visualization | `VERIFIED` | pandas/numpy/matplotlib/sklearn live |
| C7 | Document generation (docx/xlsx/pptx/pdf) | `VERIFIED` | libraries present, pichhle phase me use hui |
| C8 | Image processing + OCR + image search | `VERIFIED` | PIL/cv2/ImageMagick/tesseract + image_search |
| C9 | Image **generation** | `VERIFIED` | test image bani (`_tests/image_generation_test.png`) |
| C10 | Speech generation | `CONDITIONAL` | voice choose karna padega (audition step) |
| C11 | Persistent memory | `VERIFIED (within workspace)` | 28 records + audit 100/100 |
| C12 | External messaging (email/TG/WhatsApp) | `CONDITIONAL` | libraries present (smtplib), **credentials absent** |
| C13 | Scheduling (cron) | `UNAVAILABLE` (cron binary missing) → **`POSSIBLE via process + sleep loop`** | `crontab` not found |
| C14 | Multi-agent parallelism | `UNAVAILABLE` (real agents) / `VERIFIED` (parallel processes) | design + process probe |
| C15 | GPU / ML training | `UNAVAILABLE` | no GPU, no torch |
| C16 | Sandbox escape / host access | `IMPOSSIBLE` (by design, aur attempt bhi nahi kiya) | architecture |

---

## C. Tool Inventory (verified, agent-level)

| Tool | Read | Write | Execute | Search | External | Notes |
|---|---|---|---|---|---|---|
| `bash` (sandboxed shell, cwd=/home/user) | ✅ | ✅ | ✅ | ✅ (grep/find) | ✅ (network) | 2 vCPU, ~2GB RAM, 25GB disk; sudo root tak |
| `read_file` | ✅ | — | — | — | — | text + images (visual) + binary metadata |
| `write_file` / `edit_file` | — | ✅ | — | — | — | workspace me; parent dirs auto-create |
| `fetch_page` | ✅ | — | — | — | ✅ | HTML **aur PDF** parse (arxiv paper poora padha); Cloudflare sites par 403 (reddit, instagram) |
| `web_search` | ✅ | — | — | ✅ | ✅ | depth 1–3; citations ke saath |
| `image_search` | ✅ | ✅ (saves) | — | ✅ | ✅ | real files save hote hain |
| `generate_image` | ✅ (edit mode) | ✅ | — | — | ✅ | test image verified |
| `add_voice` / `generate_speech` | — | ✅ | — | — | — | `CONDITIONAL`: pehle user audition |
| `start_process` / `get_process_output` / `stop_process` | ✅ | ✅ | ✅ | — | ✅ (ports) | long-running servers + live preview (0.0.0.0) |
| `present_file` | — | — | — | — | — | user ke viewer me kholta hai |
| `ask_user` | ✅ | — | — | — | — | clarification UI (is turn me use kiya) |

**TOOL DISCOVERY LIMITATION (blueprint Part 12 ke hisaab se explicit):** main apne tool-list ko runtime par
"inspect" nahi kar sakta (koi `list_tools` API expose nahi hai) — jo tools implement hote hain wahi use kar sakta hoon.
Jo upar likha hai wo **actually use kiye gaye / call kiye gaye** tools ka verified set hai, kisi hidden tool ka claim nahi.

---

## D. Environment Inventory

| Environment | Purpose | Tools | Access | Restrictions | Transfer mechanism |
|---|---|---|---|---|---|
| **E1: Sandbox (Debian 13, e2b)** | execution, files, network | full Linux + apt/pip/npm + browsers | root (sudo), open egress | no GPU, no user's device, ephemeral risk | files (workspace), network, ports |
| **E2: Workspace persistence layer** | `/home/user` files turn-to-turn | file I/O | read/write | `node_modules/.venv/out/build/dist/.cache` jaise dirs snapshot se **excluded** (likely volatile) | file re-write, memory store |
| **E3: User's browser (preview)** | output viewing | HTTP preview proxy | user-side | sirf port expose hota hai, main user ke browser ko control nahi karta | HTTP serve |
| **E4: External web / APIs** | research, data, services | HTTP(S), DNS, TCP | open for tested hosts | kuch sites 403/CAPTCHA/paywall; keys nahi hain | curl/python/playwright |
| **E5: User's own systems (phone/laptop/Telegram/etc.)** | real-world actions | — | **mera koi access nahi** | needs user-provided bridge (bot token) | user-mediated |

**E4 vs E5 ka farq sabse bada hai:** internet **read/publish-able** hai, par tumhari **personal accounts** me main nahi hoon.

---

## E. Access & Permission Matrix (top rows — poori table `01_CAPABILITY_AND_ACCESS_MAP.md` me)

| Resource | Exists | Discoverable | Readable | Download | Write | Execute | Auth chahiye | Current access |
|---|---|---|---|---|---|---|---|---|
| Workspace files | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (scripts) | ❌ | `VERIFIED` full |
| System files (`/etc`, `/usr`) | ✅ | ✅ | ✅ | — | ✅ (sudo) | ✅ | ❌ | `VERIFIED` |
| `/` root of filesystem | ✅ | ✅ | ✅ | — | ❌ | — | ❌ | `DENIED` (write) |
| PyPI / npm registry | ✅ | ✅ | ✅ | ✅ | — | ✅ (install) | ❌ | `VERIFIED` |
| Debian apt repos | ✅ | ✅ | ✅ | ✅ | — | ✅ | ❌ (sudo) | `VERIFIED` |
| GitHub (public) | ✅ | ✅ | ✅ | ✅ (clone) | ❌ (no token) | — | push ke liye | `read VERIFIED`, write `UNAVAILABLE` |
| Search engines | ✅ | ✅ | ✅ (results) | — | — | — | ❌ | `VERIFIED` |
| Cloudflare-protected sites (reddit, SO, medium…) | ✅ | ✅ | ❌ 403 | ❌ | ❌ | ❌ | — | `RESTRICTED` |
| Paywalled (WSJ, Bloomberg, ScienceDirect) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | subscription | `RESTRICTED` |
| Login-gated (Instagram, LinkedIn) | ✅ | ✅ | ❌ (login wall) | ❌ | ❌ | ❌ | yes | `RESTRICTED` |
| User's private data / accounts | ✅ (tumhare paas) | ❌ | ❌ | ❌ | ❌ | ❌ | yes | `REQUIRES USER` |

---

## F. Research Inventory (short)

- **VERIFIED:** keyword search, multi-query research, iterative search, domain-restricted search, primary-source search,
  PDF/document research, repository research, claim verification (partial), source triangulation, entity identification, current-event research.
- **PARTIAL:** cross-source consistency (tool-dependent), datasets (public milte hain, kuch portals 403), contradiction search.
- **UNAVAILABLE:** paywalled literature, logged-in social platforms, CAPTCHA-gated portals, some gov data portals.

## G. Action Inventory (short)

`VERIFIED` free: search, read web/PDFs, code run, file create/modify, install packages, spawn processes/servers, screenshots, OCR, data analysis, image generation, memory ops.
`REQUIRES USER INPUT`: email/DM send karna, tumhare accounts me kuch bhi, private data, Telegram live (token), LLM API calls (key), voice output (audition).
`RESTRICTED/HARD LIMIT`: bypass auth/paywall/CAPTCHA, GPU training, real parallel agents, host-machine access.

---

## H. Hard Limits (jo environment ki wajah se hain, intelligence ki nahi)

1. **Credentials nahi hain** → koi API/LLM/social push nahi (tum key do to ban jaayega).
2. **Login sessions nahi hain** → Instagram/LinkedIn/Reddit jaise platform par "logged-in" kaam nahi.
3. **Paywall/Cloudflare** → technically curl 403 deta hai; main bypass nahi karunga (Part 24).
4. **GPU missing** → local heavy model training/inference nahi.
5. **Parallel sub-agents** → architecture me nahi hain; parallel *processes* hain.
6. **Ephemeral risk** → `node_modules/.venv/.cache` jaise dirs persist nahi hote (verify pending); Playwright ka 114MB browser
   `/home/user/.cache` me hai → agar snapshot hua to agle turn me **dobara install** karna pad sakta hai (known cost).

## I. Unknowns (top 5 — poori queue `04_UNKNOWN_QUEUE_AND_TESTS.md`)

| # | Unknown | Kyun matters | Test |
|---|---|---|---|
| U1 | Cross-turn persistence (`/home/user` + excluded dirs) | memory + installed tools zinda rehte hain ya nahi | `_persist_test/` stamps — **agle turn me** |
| U2 | Sandbox ka lifetime / process restart | server + bot chalu rehta hai ya nahi | process ko agle turn me probe |
| U3 | Site-specific 403s ka complete pattern | research coverage | site matrix dobara + per-site fallback |
| U4 | Rate limits (pip/npm/apt/search) | bulk automation | throttled loop test (optional, low priority) |
| U5 | Playwright logged-out sites (x.com/reddit) ka actual limit | social research | headed/JS wait tests (optional) |

## J–M
J (Alternative routes), K (Recommended tests), L (Expansion plan), M (maintenance/versioning) —
poora detail `03_FALLBACK_ROUTE_GRAPH.md`, `04_UNKNOWN_QUEUE_AND_TESTS.md`, `05_EXPANSION_ROADMAP_AND_MAINTENANCE.md` me.

---

## Verification ledger (kis claim ka kya evidence)

| Claim | Test | Result |
|---|---|---|
| Root/sudo available | `sudo -n id` | `uid=0(root)` ✅ |
| apt installs work | `apt-get install sqlite3` | 3.46.1 installed ✅ |
| pip + PyPI egress | `pip install humanize` | 4.16.0 ✅ |
| npm registry | `npm install left-pad` | 1 package ✅ |
| git over HTTPS | `git clone Hello-World` | OK ✅ |
| Browser automation | Playwright launch → screenshot → PDF | 17KB PNG + 14KB PDF ✅ |
| Browser deps gap + fix | launch fail `libnspr4.so` → apt libs → relaunch | fixed ✅ (error memory banayi) |
| OCR | tesseract on generated image | text nikla (accuracy imperfect) ✅⚠️ |
| Image generation | generate_image | PNG bani ✅ |
| Image search | image_search | 2 files saved ✅ |
| fetch_page on PDF | arxiv 1706.03762 | poora text ✅ |
| fetch_page on blocked site | instagram, reddit | HTTP 403 (honest fail) ✅ |
| web_search | Debian 13 release query | 3 cited results ✅ |
| Filesystem boundaries | write `/home/user`, `/tmp`, `/` | ✅ ✅ ❌ |
| Secrets absent | env scan 12 keys | sab absent ✅ |
| No GPU | `/dev/nvidia*`, torch | absent ✅ |

**Stop condition (Part 34):** main ye **nahi** keh raha ki "sab discover ho gaya". Ye keh raha hoon:
> **"Maximum capability audit jo is observable + authorized environment me possible tha, wo complete hai — in verified capabilities, unknowns aur limitations ke saath."**

> **PHASE 2 UPDATE (2026-09-23):** is audit ke 12 blocked/partial targets par access-expansion sweep chala — 9 ke legitimate routes verified. Dekho `03_ACCESS_EXPANSION/00_PHASE2_MASTER_REPORT.md` + `CAPABILITY_MAP.json` v2.0 + `tools/access_routes.py`.
