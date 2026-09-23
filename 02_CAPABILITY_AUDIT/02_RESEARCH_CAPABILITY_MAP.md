# RESEARCH CAPABILITY MAP — web, data sources, methods, depth

> Blueprint Phase 5 + Parts 6, 7, 8, 9, 17, 18, 19 ka output.
> Har row ka status: `VERIFIED` / `PARTIAL` / `UNAVAILABLE` / `UNKNOWN`
> Raw evidence: `probes/probe_results_2026-09-23.txt` + `probes/site_matrix.csv`

---

## 1. WEB DISCOVERY — actual results (curl, browser UA, 8s timeout, 2026-09-23)

| Site / category | HTTP | Content mila? | Classification | Fallback |
|---|---|---|---|---|
| example.com | 200 | ✅ | `VERIFIED` readable | — |
| github.com (public) | 200 | ✅ | `VERIFIED` readable | API/raw |
| api.github.com | 200 | ✅ | `VERIFIED` API open (unauth) | rate-limit handling |
| raw.githubusercontent.com | 200 | ✅ | `VERIFIED` | — |
| pypi.org | 200 | ✅ | `VERIFIED` | — |
| registry.npmjs.org | 200 | ✅ | `VERIFIED` | — |
| en.wikipedia.org | 200 | ✅ | `VERIFIED` | API, dumps |
| arxiv.org (+PDF) | 200 | ✅ (full text) | `VERIFIED` (best-in-class) | — |
| data.gov | 200 | ✅ | `VERIFIED` portal | dataset APIs |
| finance.yahoo.com | 200 | ✅ | `VERIFIED` | yfinance lib |
| google.com | 200 | ⚠️ JS/consent | `PARTIAL` | `web_search` tool, DDG |
| x.com (public view) | 200 | ❌ shell only | `RESTRICTED` | search snippets, news |
| instagram.com | 200 | ❌ login wall | `RESTRICTED` | press/news mentions |
| linkedin.com | 200 | ❌ login wall | `RESTRICTED` | company site, news |
| amazon.in | 200 | ⚠️ tiny response | `PARTIAL` | other retailers, APIs |
| reddit.com | **403** | ❌ | `RESTRICTED` (Cloudflare) | old.reddit? (untested), search snippets, mirrors |
| stackoverflow.com | **403** | ❌ | `RESTRICTED` (CF "Just a moment") | **Stack Exchange API** (untested → U-item), docs, local repos |
| medium.com | **403** | ❌ | `RESTRICTED` | author's own blog, archive |
| quora.com | **403** | ❌ | `RESTRICTED` | — |
| bloomberg.com | **403** | ❌ | `RESTRICTED` | Reuters, official filings |
| wsj.com | **401** | ❌ | `RESTRICTED` (paywall) | — |
| sciencedirect.com | **403** | ❌ | `RESTRICTED` (paywall) | arXiv, PubMed, preprints, author copies |
| tripadvisor.com | **403** | ❌ | `RESTRICTED` | official sites, maps |
| nseindia.com | **403** | ❌ | `RESTRICTED` | yahoo finance, other exchanges |
| patents.google.com | timeout | ❌ | `UNKNOWN` (test fail) | patentsview API (untested) |
| jstor.org | 200 | ⚠️ home only | `PARTIAL` | open-access mirrors |

**Reading of this table (honest):**
- **Open web ki poori read-layer available hai** — docs, code, papers, data portals, news sites (jo bina block ke hain).
- **Cloudflare/bot-walls** ek real, systematic limit hain (reddit, SO, medium, quora, sciencedirect, tripadvisor, NSE).
  Ye "internet nahi hai" nahi hai — ye "kuch specific publishers ne automation block kiya hai" hai.
- **Search-tool layer** (`web_search`) aksar in blocked sites ka content **snippet-level** de deta hai — matlab
  information mil sakti hai, par **page-level deep extraction** nahi. Isliye claim: `PARTIAL access to blocked sources`.

---

## 2. RESEARCH METHODS — available matrix (Part 7 ka 25-point list)

| # | Method | Status | Kaise |
|---|---|---|---|
| 1 | Keyword search | `VERIFIED` | `web_search` |
| 2 | Semantic search | `VERIFIED` (tool-level) | `web_search` natural language |
| 3 | Exact phrase search | `PARTIAL` | query me quotes; engine support tool-dependent |
| 4 | Domain-restricted search | `PARTIAL` | query me `site:` likhna; reliability untested → U-item |
| 5 | Source-specific search | `VERIFIED` | direct URL fetch (arxiv, github, wikipedia API) |
| 6 | Multi-query research | `VERIFIED` | parallel searches (is audit me kiya) |
| 7 | Iterative search | `VERIFIED` | follow-up queries |
| 8 | Citation chaining | `PARTIAL` | references padh sakta hoon; citation graph API untested |
| 9 | Primary-source search | `VERIFIED` | arxiv PDF, GitHub repo, official sites |
| 10 | Secondary-source search | `VERIFIED` | news/blogs |
| 11 | Document search | `VERIFIED` | HTML + PDF parse |
| 12 | PDF research | `VERIFIED` | fetch_page (30-page limit), pypdf installable |
| 13 | Dataset research | `PARTIAL` | data.gov ✅; kuch portals 403 |
| 14 | Technical documentation | `VERIFIED` | docs sites open |
| 15 | Repository research | `VERIFIED` | clone + grep + run |
| 16 | Historical research | `VERIFIED` | archives (jstor home, wikipedia, archive.org untested) |
| 17 | Current-event research | `VERIFIED` | news search |
| 18 | Comparative research | `VERIFIED` | multi-source |
| 19 | Contradiction search | `VERIFIED` (method) | deliberately opposing queries |
| 20 | Claim verification | `VERIFIED` (partial coverage) | do source mila kar; blocked source par limited |
| 21 | Source triangulation | `VERIFIED` | 3+ sources checklist |
| 22 | Timeline reconstruction | `VERIFIED` | dated sources |
| 23 | Entity identification | `VERIFIED` | — |
| 24 | Cross-source consistency | `PARTIAL` | automated diff script likh sakta hoon |
| 25 | Evidence-gap analysis | `VERIFIED` | yehi audit ka output hai |

---

## 3. DATA COLLECTION METHODS (Part 8)

| Source | Access method | Data type | Retrieval | Parsing | Validation | Storage | Citation | Update freq |
|---|---|---|---|---|---|---|---|---|
| User input | chat / `ask_user` | text | direct | — | user_explicit authority | memory | user ref | on input |
| Uploaded files | workspace | any | `read_file`/bash | lib-wise | hash + size | workspace | file path | manual |
| Web pages | curl / fetch_page | HTML | HTTP | bs4/lxml/markdown | source record | memory + files | URL + date | re-fetch |
| PDFs | fetch_page / pypdf | text | HTTP/download | pypdf | quote check | files | URL + page | re-fetch |
| Search results | web_search | snippets | API | — | cross-check | notes | URL | — |
| Public APIs (no key) | curl/requests | JSON | HTTP | json | schema check | files/DB | endpoint | rate-aware |
| Datasets | data.gov / direct | CSV/JSON | HTTP | pandas | schema + nulls | files | portal + license | as published |
| Repos | git clone | code | git/HTTPS | grep/exec | tests run | workspace | repo + commit | on demand |
| Images | image_search / generate | pixels | tool | PIL/cv2 | visual check | workspace | source URL | — |
| Screenshots | Playwright | PNG/PDF | browser | — | visual | workspace | URL + time | on demand |
| Audio | generate_speech | audio | tool | — | listen (user) | workspace | — | — |
| Agent-to-agent | **`UNAVAILABLE`** | — | — | — | — | — | — | — |
| Cloud files (Drive/S3) | **`REQUIRES USER`** | — | — | — | — | — | — | — |

**Pipeline (Part 8 ka required chain):** `SOURCE → ACCESS → TYPE → RETRIEVAL → PARSING → VALIDATION → STORAGE → CITATION → UPDATE`
— sab steps ka tool maujood hai, **except** cloud/app connectors aur agent-to-agent.

---

## 4. SOURCE QUALITY ENGINE (Part 9) — meri scoring rubric

| Factor | Weight | Kaise check karta hoon |
|---|---|---|
| Primary vs secondary | high | original paper/official doc vs blog summary |
| Official vs unofficial | high | domain + author |
| Original vs derivative | medium | "according to X" chains avoid |
| Publication + update date | high | page metadata |
| Methodological quality | high | sample size, method section |
| Evidence quality | high | data vs opinion |
| Corroboration | high | 2+ independent sources |
| Conflict of interest | medium | vendor/promotional content |
| Transparency | medium | author, funding, sources |
| Reproducibility | medium | code/data available? |
| Directness | high | primary claim vs third-hand |
| Completeness | medium | partial quote vs full context |

**Conflict protocol (Part 9):** claim-level table banao → dono side ka exact wording → evidence quality compare → unresolved
uncertainty **dikhao** (merge karke "average" nahi karna). Live demo: research tasks me main recency+authority likhta hoon,
aur conflict ko memory me `conflicted` mark karta hoon (§21 conflict engine).

---

## 5. RESEARCH DEPTH ENGINE (Part 17) — operations me kaise lagta hai

| Level | Kya hota hai | Is workspace me tool |
|---|---|---|
| L1 Discovery | queries + result scan | `web_search` |
| L2 Primary sources | paper/doc/repo fetch | `fetch_page`, `git clone` |
| L3 Cross-verification | independent 2nd/3rd source | multi-search |
| L4 Contradiction search | "X galat kyun hai" queries | `web_search` (deliberate) |
| L5 Context | history/legal/economic context | search + docs |
| L6 Gap analysis | kya missing hai likhna | main (reasoning) |
| L7 Confidence scoring | evidence strength labels | memory `confidence` field |
| L8 Synthesis | sirf supported conclusions | output + quality gate |

**Rule jo main follow karta hoon (Part 18):** ek search par rukna nahi; snippet ko evidence nahi manna; popular ≠ reliable;
generated summary ko primary source nahi manna; uncertainty chhupana nahi.

---

## 6. RESEARCH TOOL-CHAINING (Part 31) — verified chains

```
CHAIN A: SEARCH → FETCH(HTML/PDF) → EXTRACT → PANDAS → CHART → DOCX/XLSX → VERIFY/CITE
   stage failures: fetch 403 → fallback (reader proxy / alternate source) → agar phir fail → user-provided file

CHAIN B: CLONE → GREP/READ → RUN TESTS → PATCH → RE-RUN → DIFF REPORT
   stage failures: deps missing → pip/npm/apt install → agar network fail → local vendoring

CHAIN C: BROWSER → SCREENSHOT → OCR → TEXT → CLASSIFY → MEMORY
   stage failures: browser libs → apt deps; OCR accuracy → preprocess (upscale/threshold)

CHAIN D: SEARCH RESULTS (blocked sites) → SNIPPET TRIAGE → ALTERNATE PRIMARY SOURCE → CROSS-CHECK
   stage failures: no alternate source → disclose gap (never fabricate)
```

Har chain me **evidence preserve hota hai**: URL, fetch time, file path, hash — memory aur audit log me.

---

## 7. Access matrix → classified buckets (Part 1 ke 10 categories)

1. **AVAILABLE NOW:** open web + PDFs + repos + public APIs; shell + packages; browser; docs/data/image/OCR/media libs; memory.
2. **AVAILABLE WITH USER ACTION:** LLM API keys, Telegram token, cloud file links, private exports, voice audition.
3. **AVAILABLE THROUGH ANOTHER TOOL:** blocked site ka snippet (search tool), page→PDF (browser), OCR (tesseract),
   video processing (ffmpeg install), audio (gTTS/espeak install).
4. **AVAILABLE IN ANOTHER ENVIRONMENT:** tumhara phone/laptop (main nahi pahunch sakta) → bot/API bridge banega.
5. **POSSIBLE IN PRINCIPLE, NOT EXPOSED:** real parallel sub-agents, cross-model verification, connector plugins (Drive/Slack).
6. **REQUIRES EXTERNAL SERVICE/API/CONNECTOR:** WhatsApp, email sending, cloud storage, payments, e-sign.
7. **REQUIRES HUMAN AUTHORIZATION:** account actions, publishing, financial/legal steps, sensitive personal data.
8. **RESTRICTED:** paywalls, login walls, Cloudflare/CAPTCHA — bypass **nahi** karunga (§24).
9. **IMPOSSIBLE UNDER CURRENT ARCHITECTURE:** host access, sandbox escape, GPU training, unlimited credentials.
10. **UNKNOWN — TESTING REQUIRED:** cross-turn persistence, Stack Exchange API, archive.org, patents API, rate limits — `04_UNKNOWN_QUEUE_AND_TESTS.md`.
