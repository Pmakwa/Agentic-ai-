# CAPABILITY & ACCESS MAP (detail) — Agent Capability & Access Map v1.0

> Ye file blueprint ke **Phase 1, 2, 3, 4, 10** ka output hai: capability inventory, tool inventory,
> environment inventory, access/permission matrix — sab **verified reality** par.
> Confidence labels: `VERIFIED` / `STRONGLY SUPPORTED` / `POSSIBLE` / `CONDITIONAL` / `UNAVAILABLE` / `RESTRICTED` / `UNKNOWN`

---

## 1. COGNITIVE CAPABILITIES (Part 3-A)

| Capability | Status | Evidence / Note |
|---|---|---|
| Reasoning, planning, decomposition | `VERIFIED` | ye audit khud 15 phases me decompose hua |
| Synthesis, comparison, classification | `VERIFIED` | audit ke inventories |
| Extraction, summarization, transformation | `VERIFIED` | V1/V2 spec extraction + 28 memory records |
| Pattern detection, hypothesis generation/testing | `VERIFIED` | spec-drift gaps pakde (15 vs 12 memory types) |
| Error detection, contradiction detection | `VERIFIED` | stale count bug, audit false-positive fix |
| Uncertainty estimation | `VERIFIED` | har claim par confidence label |
| Self-critique, verification | `VERIFIED` | tests 28/28 pass, provenance hashes |
| Simulation / forecasting | `POSSIBLE` (simulation code likh sakta hoon; "forecast" = data-based inference) | — |
| Mathematical reasoning | `VERIFIED` | pandas/numpy/scipy available |
| Coding + debugging | `VERIFIED` | Python 3.13, Node 20, Java 11, gcc 14 |
| Research (multi-source) | `VERIFIED (coverage-limited)` | kuch sites 403 |
| Multimodal reasoning (image in) | `VERIFIED` | read_file image dikhata hai (test image dekhi) |
| Document understanding (PDF) | `VERIFIED` | arxiv paper parse |
| Long-context reasoning | `VERIFIED` | 44k char spec ek saath handle hua |
| Structured knowledge construction | `VERIFIED` | memory schema + knowledge graph notes |
| Iterative problem solving | `VERIFIED` | playwright gap → fix → re-test |

**Honest caveat:** "intrinsic" cognitive claims ka test = output quality check, na ki alag se measurable unit test.
Isliye inhe `VERIFIED` maana gaya hai kyunki **actual output** exist karta hai (file bani, test pass hua) — sirf dava nahi.

---

## 2. TOOL CAPABILITIES (Part 3-B + Part 12)

### 2.1 Native agent tools
| Tool | Purpose | Input | Output | Action type | External comms | Website interaction | Limitations |
|---|---|---|---|---|---|---|---|
| `bash` | shell execution | command | stdout/stderr/exit | read+write+execute | ✅ (network) | indirect (curl/git/pip) | sandbox boundaries, no host |
| `read_file` | file padhna | path | text / image / metadata | read | — | — | workspace-scoped paths |
| `write_file` | file banana | path+content | file | create/overwrite | — | — | overwrite warning |
| `edit_file` | targeted edit | old/new text | diff | modify | — | — | fuzzy match |
| `fetch_page` | URL → markdown | URL | page text (chunks) | read | ✅ | ✅ (static) | JS-heavy/Cloudflare fail; PDF 30-page limit |
| `web_search` | web search | query, depth | results + citations | search | ✅ | — | depth 1–3, result count limited |
| `image_search` | images dhoondhna | query, count | image files | search+download | ✅ | — | 1–5 per call |
| `generate_image` | image banana/edit | prompt, path | image file | create | ✅ | — | 1 image per call (options mode possible) |
| `add_voice`/`generate_speech` | spoken audio | text, voice_id | mp3/wav | create | — | — | **CONDITIONAL**: voice audition pehle |
| `start_process`/`get_process_output`/`stop_process` | long-running procs | command | logs + ports | execute+monitor | ✅ | — | process dies with sandbox |
| `present_file` | user viewer me file | path | — | UI action | — | — | one file at a time |
| `ask_user` | clarification | questions | user choices | interactive | — | — | pause turn |

**Tool chaining (Part 31) — VERIFIED example chains:**
```
SEARCH → FETCH → PARSE → DATA → CHART → DOC        (research report)
APT/SUDO → BROWSER INSTALL → LAUNCH → SCREENSHOT    (web evidence capture)
PIL → TESSERACT → TEXT → MEMORY                     (image → text pipeline)
GIT CLONE → TEST → BUILD → FILE                     (repo work)
SEARCH → FETCH → MEMORY(candidate) → INDEX          (knowledge capture)
```

### 2.2 System-level toolchain (apt/pip/npm ke baad)
`VERIFIED available`: curl, wget, git, zip/unzip, ssh/scp, ImageMagick (`convert`/`magick`), python3.13 + 19 libs
(pandas, numpy, scipy, sklearn, matplotlib, openpyxl, python-docx, PIL, cv2, requests, httpx, aiohttp, bs4, lxml, yaml, jsonschema, rich, tqdm),
node 20 + npm, java 11, gcc/g++/make, sqlite3 (install kiya), tesseract 5.5.0 (install kiya), Playwright+Chromium (install kiya),
systemd present (`systemctl` binary), `/dev/shm` present.
`MISSING but installable`: ffmpeg, pandoc, libreoffice, docker, gh, rsync, pdftotext, qpdf, chromium (system), torch/ML stack, OCR langs extra.
`UNAVAILABLE`: GPU, cron/at daemons.

---

## 3. ENVIRONMENT INVENTORY (Part 4)

| | E1 Sandbox | E2 Persistence layer | E3 User browser | E4 External web/APIs | E5 User's own systems |
|---|---|---|---|---|---|
| **Kya hai** | full Linux VM, 2 vCPU/2GB/25GB | `/home/user` snapshots | preview iframe (sandbox="allow-scripts") | internet | phone/laptop/accounts |
| **Mera access** | full (root) | read/write | sirf serve kar sakta hoon | HTTP(S), DNS, TCP | ❌ koi nahi |
| **Tools** | shell, pkg mgrs, browsers, libs | file I/O | live preview | curl/py/playwright | — |
| **Restrictions** | no GPU, no host, ephemeral risk | excluded dirs volatile | no external CDN in preview | 403/CAPTCHA/paywall; no keys | needs bridge (bot/token) |
| **Aur environments se alag** | execution + install | cross-turn memory | user-visible rendering | research scale | real-world identity/actions |
| **Transfer** | files → E2, HTTP → E3, net → E4 | files | URL | responses → files | user-mediated |

**Environment fallback (Part 5/25):** E1 me kuch na ho → E4 se lo → file bana kar E2 me rakho → E3 par dikhao →
agar real-world action chahiye → E5 ka bridge (bot token/API key) mango.

---

## 4. ACCESS MATRIX (Part 10) — full

| Resource | Exists | Discoverable | Readable | Searchable | Downloadable | Writable | Executable | Auth? | Current access | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| Workspace `/home/user` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | FULL `VERIFIED` | write tests |
| `/tmp` (tmpfs, 993MB) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | FULL `VERIFIED` | write test |
| `/` write | ✅ | ✅ | ✅ | — | — | ❌ | — | ❌ | DENIED | touch fail |
| System files `/etc /usr /var` | ✅ | ✅ | ✅ | ✅ | — | ✅ (sudo) | ✅ | ❌ | FULL `VERIFIED` | apt install |
| apt (Debian repos) | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | sudo | FULL `VERIFIED` | sqlite3, tesseract, libnspr4… |
| PyPI | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | ❌ | FULL `VERIFIED` | pip install ×3 |
| npm registry | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | ❌ | FULL `VERIFIED` | npm install |
| GitHub public | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ push | — | push ke liye | READ `VERIFIED`, WRITE `UNAVAILABLE` | git clone |
| GitHub raw / API (unauth) | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ❌ | `VERIFIED` (rate-limited) | api.github.com/zen 200 |
| Wikipedia / arXiv / data.gov | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ❌ | `VERIFIED` | HTTP 200 + PDF parse |
| Google web (search page) | ✅ | ✅ | ⚠️ | ⚠️ | — | — | — | — | `PARTIAL` (JS/consent; web_search tool better) | 200 par extraction unreliable |
| X/Twitter (public view) | ✅ | ✅ | ⚠️ shell | ❌ | — | — | — | login | `RESTRICTED` (JS/login) | curl 200 shell, playwright title empty |
| Instagram / LinkedIn | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | login | `RESTRICTED` | login wall / 403 |
| Reddit | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | CF challenge | `RESTRICTED` | 403 (curl + fetch_page + playwright) |
| StackOverflow / Medium / Quora | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | CF challenge | `RESTRICTED` | 403 "Just a moment..." |
| Bloomberg / WSJ / ScienceDirect | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | paid | `RESTRICTED` | 403 / 401 |
| TripAdvisor / NSE India | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | bot-wall | `RESTRICTED` | 403 / timeout |
| Finance data (Yahoo) | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ❌ | `VERIFIED` (HTTP 200) | probe |
| User's accounts / private data | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | yes | `REQUIRES USER` | — |

---

## 5. PERMISSION MATRIX (Part 11) — action-wise

| Action | Can do now | Tool | Permission | User step chahiye? | Alternative route | Verified |
|---|---|---|---|---|---|---|
| Web search | ✅ | web_search / curl | — | ❌ | DDG/Bing HTML, site APIs | ✅ |
| Open webpage | ✅ (static) | fetch_page / curl | — | ❌ | Playwright, reader proxy, cache | ✅ |
| PDF read | ✅ | fetch_page / pypdf (installable) | — | ❌ | download + parse with libs | ✅ |
| File create/modify | ✅ | write/edit/bash | — | ❌ | — | ✅ |
| Code execute | ✅ | bash | — | ❌ | venv isolation | ✅ |
| Install software | ✅ | apt/pip/npm | sudo (available) | ❌ | venv / npm local / compile | ✅ |
| API call | ✅ (public, no-key) | curl/python | — | key wale ke liye ✅ | public mirrors | ✅ |
| Access cloud storage | ❌ | — | credentials | ✅ | tum link/pre-signed URL do | `REQUIRES USER` |
| Send message (email/TG/WA) | ❌ (creds nahi) | smtplib/HTTP API | token/key | ✅ | bot token mango | `CONDITIONAL` |
| Publish content | ❌ (koi endpoint/platform cred nahi) | — | ✅ | ✅ | tum publish karo, main content banau | `REQUIRES USER` |
| Interact with website (logged-in) | ❌ | playwright | session | ✅ | tum export/screenshot do | `RESTRICTED` |
| Schedule automation (cron) | ❌ cron binary | — | — | ❌ | `start_process` + loop, ya systemd timer | `POSSIBLE` |
| Image generate | ✅ | generate_image | — | ❌ | PIL/cv2 programmatic | ✅ |
| Audio generate | ⚠️ | generate_speech | voice audition | ✅ | gTTS/espeak install karke (quality kam) | `CONDITIONAL` |
| Video process | ⚠️ | — | — | ❌ | ffmpeg apt se install → phir ✅ | `POSSIBLE` |
| Bypass paywall/auth | ❌ | — | — | — | **kabhi nahi (§24)** | `RESTRICTED` |

---

## 6. MULTI-AGENT DISCOVERY (Part 13) — honest

| Capability | Status | Note |
|---|---|---|
| Sub-agents create karna | `UNAVAILABLE` | platform me agent-spawn API nahi |
| Sub-agent call karna | `UNAVAILABLE` | — |
| Parallel **processes** | `VERIFIED` | background servers chale; parallel bash bhi |
| Roles (orchestrator/researcher/verifier/critic…) | `POSSIBLE (logical)` | main sequentially assume karta hoon; `agents/AGENT_REGISTRY.md` me registry maujood |
| Cross-check outputs | `VERIFIED` | main khud verifier/critic role nibha sakta hoon (tests + provenance iska proof) |
| Multi-model verification | `POSSIBLE` | **agar user API key de** (cross-model critique route) |

**Imaginary agents nahi banaye** — jo architecture actually support nahi karta, uske liye "haan" nahi kaha.
