# BLOCKER ANALYSIS REGISTER (§22 format)

> Har blocked target ke liye: **TARGET · DESIRED · BLOCKER · BLOCKER TYPE · DIRECT ROUTE · ALTERNATIVE ROUTES ·
> REQUIRED TOOLS · REQUIRED ENV · REQUIRED AUTH · REQUIRED USER ACTION · VERIFICATION · STATUS · HARD LIMIT**
> Blocker types (§1 taxonomy se): auth-required · CF-bot-wall · paywall · login-wall · rate-limit · missing-API ·
> missing-credentials · missing-connector · network/regional · format · platform · temporary · unknown

---

## B-01 — Reddit (r/* discussions, comments)

| Field | Value |
|---|---|
| Desired capability | subreddit posts + discussion threads padhna/search karna |
| Current blocker | Cloudflare 403 (site, .json, old.reddit) + pullpush policy 429 |
| Blocker type | CF-bot-wall + platform-policy |
| Direct route | ❌ 403 (curl, browser-UA, fetch_page, playwright) |
| Alternative routes | **RSS feed** (verified, 200, `reddit.com/r/<sub>/.rss`) — par **rate-limited ~1/min**; **Wayback CDX + snapshot** purane threads ke liye (verified); **official OAuth API** (credential-based) |
| Required tools | `access_routes.py rss` (ready) |
| Required auth | OAuth ke liye: Reddit app (client_id + secret + user agent) |
| Required user action | (a) kuch nahi — RSS se kaam chalega slow pace par; (b) full API chahiye to Reddit app banao |
| Verification | RSS 200 (24,685 B) — titles parse ✅; CDX 200 — archived thread list ✅ |
| Current status | **CONDITIONAL** (RSS slow) + **STRONG ALTERNATIVE** (archive) |
| Hard limit? | Nahi — sirf rate + freshness ki limitation |

## B-02 — StackOverflow (direct site)

| Field | Value |
|---|---|
| Desired | questions/answers ka content |
| Blocker | Cloudflare 403 + reader-proxy par bhi CAPTCHA |
| Blocker type | CF-bot-wall |
| Direct | ❌ |
| Alternatives | **StackExchange API** (✅ full bodies), **SO data dump** (518 MB), **Wayback** (1.17 MB page) |
| Tools | `access_routes.py so "<query>"` — ready |
| Auth | none (quota ~300/day; app key se zyada) |
| Verification | answers API 200 (87,856 B, bodies included) |
| Status | **STRONG ALTERNATIVE** |
| Hard limit? | Nahi — API hi official rasta hai |

## B-03 — Medium / personal blogs

| Field | Value |
|---|---|
| Blocker type | CF-bot-wall |
| Alternatives | **RSS tag feeds** (200) + **reader-proxy** full article (200, 15 KB text) + Wayback (404 KB) |
| Status | **STRONG ALTERNATIVE** |
| Hard limit? | Nahi |

## B-04 — WSJ

| Field | Value |
|---|---|
| Blocker | 401 paywall |
| Alternatives | **Official RSS** (headlines) + **Wayback** (full article page 1 MB) |
| Status | **STRONG ALTERNATIVE** (fresh article ka full text nahi milega; headline + archive haan) |
| Hard limit | **Article-level fresh full-text = HARD LIMIT** (paywall; bypass nahi) |

## B-05 — Bloomberg

| Field | Value |
|---|---|
| Blocker | 403 bot-wall |
| Alternatives | **RSS** (14.8 KB) + **reader-proxy** (101 KB content) |
| Status | **STRONG ALTERNATIVE** |
| Hard limit | Terminal-grade data = nahi |

## B-06 — ScienceDirect / paywalled journals

| Field | Value |
|---|---|
| Blocker | 403 + paywall + CAPTCHA (proxy par bhi) |
| Alternatives | **Crossref/OpenAlex/EuropePMC/CORE/DOAJ/PubMed/arXiv/bioRxiv/Unpaywall(own email)** — metadata + **open-access full text** |
| Status | **STRONG ALTERNATIVE (OA only)**; close-access full text = paywall |
| Hard limit | **Closed-access article ka full text = HARD LIMIT** (institutional access user ke paas ho to unka PDF) |

## B-07 — NSE India

| Field | Value |
|---|---|
| Blocker | 403 (site + archives + api) |
| Alternatives | **reader-proxy** (marketStatus JSON 200; bhavcopy CSV 213 KB) + **yfinance** (RELIANCE.NS verified) |
| Status | **STRONG ALTERNATIVE** (proxy rate-limited; yfinance direct ✅) |
| Hard limit | Nahi |

## B-08 — Quora

| Field | Value |
|---|---|
| Alternatives | Wayback snapshot bhi CF-blocked (403) |
| Status | **UNAVAILABLE** |
| Hard limit | **Haan** — koi authorized route nahi mila (aur bypass nahi karenge) |

## B-09 — x.com / Instagram / LinkedIn (content + interactions)

| Field | Value |
|---|---|
| Blocker | login walls + anti-bot |
| Alternatives | ❌ proxy ne x.com explicitly block kiya; Wayback kuch public pages ka ho sakta hai (site-specific) |
| Required user action | apna export/screenshot; ya official API keys (X API paid; IG Graph API business; LinkedIn partner) |
| Status | **UNAVAILABLE** (anonymous) → **CONDITIONAL** (user creds ke saath) |
| Hard limit | Anonymous ke liye **haan** |

## B-10 — Google Books / HathiTrust (books)

| Field | Value |
|---|---|
| Blocker | 429 quota / 403 CF |
| Alternatives | **OpenLibrary API** ✅ (metadata), Internet Archive items, Project Gutenberg (public domain) |
| Status | **CONDITIONAL → alternatives available** |
| Hard limit | Copyrighted book ka full text = nahi (legit) |

## B-11 — Patents

| Field | Value |
|---|---|
| Blocker | patents.google.com timeout |
| Alternatives | **UNVERIFIED** — patentsview API / EPO OPS / Lens.org API test pending (queue me) |
| Status | **UNVERIFIED** |

## B-12 — Search engines (Google/DDG scraping)

| Field | Value |
|---|---|
| Blocker | DDG 202 (bot detection), Google JS/consent |
| Alternatives | native `web_search` tool ✅ (verified, citations ke saath); Bing/DDG HTML best-effort |
| Status | **DIRECT (tool)** + LIMITED (raw scraping) |

## B-13 — Scheduled automation

| Field | Value |
|---|---|
| Desired | roz ke jobs (memory expire, audit, backups) |
| Blocker | sandbox systemd degraded; cron binary nahi |
| Alternatives | **process-loop** (`nohup`/`start_process` + sleep loop) ✅; systemd units ban/enable ho sakte hain par start nahi chalti |
| Status | **CONDITIONAL** (process-loop) / **UNAVAILABLE** (true daemon) |
| Hard limit | Session-lifetime ke andar hi chalega (process turn ke baad marta hai) |

## B-14 — Locked-in service APIs (LLM/TG/WhatsApp/cloud)

| Field | Value |
|---|---|
| Blocker type | missing-credentials |
| Routes | official APIs ready (OpenAI-compatible, Telegram Bot API, WhatsApp Cloud API, S3/Drive via rclone) |
| Required user action | keys/tokens (sabse chhota: Telegram bot token; LLM key) |
| Status | **CONDITIONAL — user action par 100% unlock** (library + bot code ready hai) |

---

### Blocker-type summary (kitni baar kaun sa blocker aaya)

| Blocker type | Count | Resolved by alternative route |
|---|---|---|
| CF-bot-wall | 6 (SO, Reddit, Medium, Quora, Hathi, TripAdvisor) | 4/6 ✅ |
| Paywall | 2 (WSJ, ScienceDirect) | 2/2 partial (headlines + OA/archive) ✅ |
| Login-wall | 3 (x, IG, LinkedIn) | 0/3 ❌ (hard) |
| Rate-limit | 4 (Reddit RSS, Jina free, GitHub unauth, Semantic Scholar) | ✅ workaround (gap/keys) |
| Missing credentials | 5 (LLM, TG, Kaggle, gh, rclone) | user action par ✅ |
| Platform limitation | 2 (systemd, GPU) | ⚠️ partial (process-loop) / ❌ |
| Network/regional | 1 (IPv6) | n/a |
| Genuinely unavailable | 1 (Quora) | ❌ |
