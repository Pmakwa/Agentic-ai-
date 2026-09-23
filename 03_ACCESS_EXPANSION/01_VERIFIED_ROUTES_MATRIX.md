# VERIFIED ROUTES MATRIX (living document)

> Status labels (§21): **DIRECT** · **STRONG ALTERNATIVE** · **CONDITIONAL** · **LIMITED** · **UNVERIFIED** · **UNAVAILABLE**
> Evidence: `probes/phase2_api_probe.txt`, `phase2_route_probe.txt`, `phase2_deep_probe.txt`, `phase2_deep_probe2.txt`
> Update rule: route status badle → yahi file + `CAPABILITY_MAP.json` + memory record update.

---

## A. ACADEMIC / RESEARCH

| Target | Route | Status | Evidence (tested 2026-09-23) | Notes |
|---|---|---|---|---|
| Crossref | `api.crossref.org/works?query=` | **DIRECT** | 200, 1.5 KB, DOIs + titles | free, polite pool email optional |
| OpenAlex | `api.openalex.org/works?search=` | **DIRECT** | 200, 24.9 KB, 1.3M hits | citations/abstracts, OA flags |
| PubMed | `eutils.ncbi.nlm.nih.gov` | **DIRECT** | 200, idlist mili | rate: 3/s bina key |
| EuropePMC | `ebi.ac.uk/europepmc/...` | **DIRECT** | 200, OA filter kaam kiya | open-access full text |
| CORE | `api.core.ac.uk/v3/search/works` | **DIRECT** | 200, 61.8 KB | bina key chala (limited) |
| DOAJ | `doaj.org/api/search/articles` | **DIRECT** | 200, 2.6 KB | OA journals |
| arXiv | `export.arxiv.org/api/query` + direct PDF | **DIRECT** | 200; PDF 2.2 MB | best-in-class |
| bioRxiv | `api.biorxiv.org/details/...` | **DIRECT** | 200 | preprints |
| Semantic Scholar | `api.semanticscholar.org/graph/v1` | **CONDITIONAL** | 429 (bina key) | free key se khulega |
| Google Books | `googleapis.com/books/v1` | **CONDITIONAL** | 429 quota | quota reset par works |
| Unpaywall | `api.unpaywall.org/v2/{doi}` | **CONDITIONAL** | 422 ("use your own email") | apna email daalo → OA PDF link |
| IA Scholar | `scholar.archive.org` | **LIMITED** | "Rate limit reached" | throttle karke try |
| HathiTrust | `babel.hathitrust.org` | **UNAVAILABLE** | 403 Cloudflare | — |
| OpenAIRE | `api.openaire.eu` | **UNVERIFIED** | 000 (call malformed) | dobara test pending |

## B. Q&A / COMMUNITY / DEV

| Target | Route | Status | Evidence | Notes |
|---|---|---|---|---|
| **StackOverflow** | `api.stackexchange.com/2.3/...` | **STRONG ALTERNATIVE** | questions 200 + answers 200 (87.8 KB bodies) | anonymous quota ~300/day |
| **StackOverflow (bulk)** | `archive.org/download/stackexchange/` | **STRONG ALTERNATIVE** | Posts.7z = **518 MB** | full dump, offline research |
| Hacker News | `hn.algolia.com/api/v1/search` | **DIRECT** | 200 | comments bhi |
| Lobsters | `lobste.rs/hottest.json` | **DIRECT** | 200, 11.5 KB | quality dev links |
| dev.to | `dev.to/api/articles` | **DIRECT** | 200 | dev blogs |
| Discourse (koi bhi forum) | `<forum>/latest.json` | **DIRECT** | 200, 79 KB (meta) | community forums |
| GitHub API | `api.github.com` | **DIRECT (rate-limited)** | 200; **core 60/hr unauth** | token se 5000/hr |
| Reddit | `.rss` feed | **CONDITIONAL** | 1st 200 (24.6 KB), phir 429 | ~1 req/min; cached use |
| Reddit (archived threads) | Wayback CDX + snapshot | **STRONG ALTERNATIVE** | CDX 200; thread pages archived | purane threads |
| Reddit API (official) | `oauth.reddit.com` | **CONDITIONAL** | creds nahi | user OAuth → full access |
| pullpush.io | `api.pullpush.io` | **UNAVAILABLE** | 429 "no free scraping resources for agents" | policy block |
| nitter (x.com mirrors) | nitter.net | **UNAVAILABLE** | 000 (dead instance) | — |
| Quora | — | **UNAVAILABLE** | 403 + wayback bhi CF | koi route nahi |

## C. NEWS / PUBLISHING

| Target | Route | Status | Evidence |
|---|---|---|---|
| **WSJ** | `feeds.a.dj.com/rss/RSSMarketsMain.xml` | **STRONG ALTERNATIVE** | 200, 12.7 KB, live headlines |
| **WSJ full article** | Wayback snapshot | **STRONG ALTERNATIVE** | 200, 1.02 MB page |
| **Bloomberg** | `feeds.bloomberg.com/markets/news.rss` | **STRONG ALTERNATIVE** | 200, 14.8 KB |
| **Bloomberg** | reader-proxy | **STRONG ALTERNATIVE** | 200, 101 KB content |
| BBC | `feeds.bbci.co.uk/news/rss.xml` | **DIRECT** | 200, 24.7 KB |
| Google News (any topic) | `news.google.com/rss/search?q=` | **DIRECT** | 200, 165 KB |
| **Medium (tag feed)** | `medium.com/feed/tag/<tag>` | **STRONG ALTERNATIVE** | 200, 17.5 KB |
| **Medium (article)** | reader-proxy | **STRONG ALTERNATIVE** | 200, 15.2 KB full text (live article padha) |
| GitHub Blog | `github.blog/feed/` | **DIRECT** | 200, 741 KB |
| HN frontpage | `hnrss.org/frontpage` | **DIRECT** | 200, 17.5 KB |
| ScienceDirect (article) | reader-proxy | **LIMITED** | landing 19.8 KB; article par CAPTCHA |
| generic paywalled page | Wayback | **STRONG ALTERNATIVE** | TripAdvisor 388 KB, Medium 404 KB |

## D. FINANCE / DATA

| Target | Route | Status | Evidence |
|---|---|---|---|
| **NSE marketStatus** | reader-proxy | **STRONG ALTERNATIVE (rate-limited)** | 200: `{"marketStatus":"Open","tradeDate":"23-Sep-2026","index":"NIFTY 50"}` |
| **NSE bhavcopy CSV** | reader-proxy | **STRONG ALTERNATIVE (rate-limited)** | 200, **213 KB CSV** |
| **Indian stocks (RELIANCE etc.)** | **yfinance** (`pip`) | **DIRECT** | RELIANCE.NS close **₹1244.0** (23-Sep-2026) |
| NSE direct | nseindia.com | **UNAVAILABLE** | 403 (curl, browser-UA) |
| Yahoo chart API | query1.finance.yahoo.com | **CONDITIONAL** | 429 aata-jaata hai (yfinance andar handle karta hai) |
| World Bank | `api.worldbank.org/v2` | **DIRECT** | 200 (India GDP etc.) |
| CoinGecko | `api.coingecko.com/api/v3` | **DIRECT** | 200 "To the Moon!" |
| Exchange rates | `open.er-api.com/v6/latest/USD` | **DIRECT** | 200, 2970 B |
| data.gov.in | API (public sample key) | **CONDITIONAL** | key rotate karni padti hai |

## E. KNOWLEDGE / GEO / BOOKS

| Target | Route | Status | Evidence |
|---|---|---|---|
| Wikipedia | REST API (`/api/rest_v1/page/summary/`) | **DIRECT** | 200, clean JSON |
| Wikidata | `Special:EntityData/Q42.json` | **DIRECT** | 200, 321 KB |
| OpenStreetMap | Overpass API (proper User-Agent zaroori) | **DIRECT** | 200 (India Gate node) — UA bina 406 deta hai |
| OpenLibrary | `openlibrary.org/search.json` | **DIRECT** | 200, 76,865 hits |
| Wayback availability | `archive.org/wayback/available` | **DIRECT** | 200 (kabhi khali bhi) |
| Wayback CDX (discovery) | `/cdx/search/cdx?...&output=json` | **DIRECT** | 200 (reddit threads list) |
| Wayback snapshot fetch | `/web/2026/<url>` | **DIRECT** | 200 (SO 1.17 MB, WSJ 1 MB) |
| Memento TimeTravel | timetravel.mementoweb.org | **UNAVAILABLE** | 000 |

## F. READER-PROXY (r.jina.ai) — kaunse sites chalte hain

| Site | Result |
|---|---|
| Bloomberg | ✅ 101 KB content |
| NSE India (site + API + CSV) | ✅ (marketStatus, bhavcopy 213 KB) |
| Medium (tag + article) | ✅ full article text |
| ScienceDirect (landing) | ✅ 19.8 KB; article-level ❌ CAPTCHA |
| WSJ | ❌ CAPTCHA warning |
| Reddit | ❌ "Target URL returned error 403" |
| StackOverflow | ❌ CAPTCHA |
| x.com | ❌ proxy ne khud block kiya ("Anonymous access to domain x.com is disabled") |
| **Rate limit** | free tier — tez calls par 429; key se khulega |

## G. ENVIRONMENT / PLATFORM

| Capability | Route | Status | Evidence |
|---|---|---|---|
| Scheduled jobs | systemd service/timer | **UNAVAILABLE** | unit create+enable ✅ par start ❌ (daemon degraded) |
| Long-running jobs | `start_process` / nohup loop | **DIRECT** | server chala (port 8000) |
| Offline model load | `HF_HUB_OFFLINE=1` + `/opt` cache | **DIRECT** | fastembed dim 384 ✅ |
| Global npm tools | `sudo npm i -g` | **DIRECT** | serve install ✅ |
| GitHub CLI | gh + token | **CONDITIONAL** | gh 2.46 ✅, auth ❌ |
| Kaggle datasets | kaggle CLI | **CONDITIONAL** | CLI ✅, `kaggle.json` ❌ |
| Cloud storage | rclone | **CONDITIONAL** | rclone ✅, config/creds ❌ |
| DNS fallback | DoH (cloudflare-dns.com) | **DIRECT** | 200 valid JSON |
| Browser automation | Playwright + Chromium (/opt) | **DIRECT** | screenshot/PDF/HAR ✅ |
| IPv6 | — | **UNAVAILABLE** | curl -6 → 000 |

## H. SWEEP v2 (2026-09-23 round 2) — naye verified routes

| Target | Route | Status | Evidence |
|---|---|---|---|
| **Patents (Google Patents)** | reader-proxy | **STRONG ALTERNATIVE** | 200, Bell patent US174465A, 16,369 B |
| patentsview API | — | **UNAVAILABLE (network)** | search.patentsview.org DNS fail; api.patentsview.org IPv6-only + IPv6 egress blocked |
| **Nominatim (geocoding)** | `nominatim.openstreetmap.org` (descriptive UA) | **DIRECT** | Rajkot "22.3053, 70.8028" |
| **OpenAIRE** | `api.openaire.eu/search/publications` | **DIRECT** | 200, 98,943 B |
| **GDELT news** | `api.gdeltproject.org/api/v2/doc/doc` | **CONDITIONAL** | 429 with "1 req/5 s" rule; 200 after 30 s gap, 3 articles |
| IA Scholar | — | **LIMITED** | rate-limit page |
| **HF datasets (public)** | `datasets` pip (HuggingFace Hub) | **DIRECT** | imdb loaded без key |
| **yt-dlp (public media)** | archive.org | **DIRECT** | 113,206 B file |
| **reader-proxy UA rule** | r.jina.ai | **FIX** | full browser-UA → 403 CF; neutral UA → 200 |
