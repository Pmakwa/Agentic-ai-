# ACCESS UNKNOWN QUEUE + HARD LIMITS

> Blueprint §26 (unknown queue) + §24 (4 states) + §27 (no-false-access).
> **Rule:** jo test nahi hua wo UNVERIFIED likha hai — "kaam karta hoga" jaisa dava kahin nahi.

---

## 1. ACCESS UNKNOWN QUEUE (test pending, priority order me)

| # | Target | Desired capability | Known blocker | Possible routes | Next safe test | Priority |
|---|---|---|---|---|---|---|
| AQ-01 | Patents | patent search + PDFs | patents.google.com timeout | patentsview API, EPO OPS, USPTO PatentsView, Lens.org (key) | `curl api.patentsview.org` basic query | **high** |
| AQ-02 | OpenAIRE | EU research aggregator | call malformed tha | `api.openaire.eu/search/publications?format=json` | corrected call | medium |
| AQ-03 | IA Scholar | academic PDF archive | "rate limit reached" | throttle + retry; direct `scholar.archive.org/search?q=` slow | 30s gap ke saath 3 tries | medium |
| AQ-04 | data.gov.in | India gov datasets | sample key rotate | apna key register (free), ya data.gov (US) verified | user key | medium |
| AQ-05 | Kaggle datasets | ML datasets | kaggle.json missing | kaggle API (user key), ya HF datasets public | user key ya `datasets` pip | **high** |
| AQ-06 | Reddit OAuth | fast/complete reddit | creds | reddit app (script type) | user se client_id/secret | **high** |
| AQ-07 | Jina key | proxy rate-limit khatam | free tier limit | jina.ai API key (free tier bhi badhta hai) | user key | medium |
| AQ-08 | Semantic Scholar key | academic search rate | 429 | free API key form | user key | medium |
| AQ-09 | Unpaywall | OA PDF links | apna email chahiye | email param | user email (ya generic) | low |
| AQ-10 | X/IG/LinkedIn API | social content | paid/login | official APIs (paid/partner) | user decision | low |
| AQ-11 | Telegram bridge | mobile memory console | bot token | BotFather token | user token | **high** |
| AQ-12 | LLM keys | /ask, embeddings-API, cross-check | keys missing | OpenAI/Anthropic/Gemini keys | user key | **high** |
| AQ-13 | systemd service execution | real daemons | sandbox systemd degraded | process-loop (fallback chalu hai) | docker/podman? (test) | low |
| AQ-14 | WhatsApp Cloud API | WA messaging | Meta business setup | Cloud API | user setup | low |
| AQ-15 | Cloud storage | Drive/S3 files | creds | rclone (installed) + user config | user config | medium |

**Prioritization logic (§26):** wo unknowns pehle jo **kai capabilities unlock karte hain** —
isliye AQ-05 (Kaggle), AQ-06 (Reddit), AQ-11 (Telegram), AQ-12 (LLM) top par hain.

---

## 2. HARD LIMITS (jo legitimately possible nahi — aur bypass nahi karenge)

| # | Hard limit | Kyun | Honest status |
|---|---|---|---|
| HL-01 | Paywall/content bypass | Security & legality boundary (§25) | **kanooni route hi nahi — user ke subscription/PDF se hi ho sakta hai** |
| HL-02 | Login-wall content (x.com, IG, LinkedIn) anonymous access | Auth required | user creds/API ke bina **possible nahi** |
| HL-03 | Private user data (email inbox, personal drive, bank) | Authorization | user ke bina **koi route nahi** |
| HL-04 | CAPTCHA/bot-wall defeating | Security control | **kabhi nahi** |
| HL-05 | Host machine / sandbox escape | Architecture | possible nahi |
| HL-06 | GPU training in-sandbox | No GPU | hosted (Colab/Kaggle) user route |
| HL-07 | Real parallel sub-agents | Platform me nahi | Phase 4 design only |
| HL-08 | Cross-turn live processes | Sandbox lifecycle | files me state rakho |
| HL-09 | Quora content | koi legitimate route nahi mila | **UNAVAILABLE** (bina bypass) |
| HL-10 | Fresh paywalled article full-text | paywall | headline RSS + archive tak hi |

---

## 3. FOUR STATES — final classification (§24)

| State | Targets |
|---|---|
| **"Directly accessible"** | GitHub, arXiv, Wikipedia/Wikidata, OSM, World Bank, OpenLibrary, CoinGecko, ExchangeRate, BBC/GoogleNews RSS, HN, Lobsters, dev.to, Discourse, yfinance, data.gov |
| **"Accessible elsewhere (alternative route)"** | StackOverflow (API+archive), Medium (RSS+proxy), WSJ/Bloomberg (RSS+archive), NSE (proxy+yfinance), TripAdvisor (Wayback+OSM), ScienceDirect OA (Crossref/OpenAlex/PubMed/Unpaywall), Reddit archives (CDX) |
| **"Accessible with authorization"** | Reddit full API · Kaggle · gh · cloud storage (rclone) · Telegram · LLM APIs · WhatsApp · Semantic Scholar key · Jina key · paywalled journals (institutional) |
| **"Cannot legitimately be accessed"** | Quora · x.com/IG/LinkedIn private content · HathiTrust · private data · CAPTCHA/paywall bypass |

---

## 4. NO-FALSE-ACCESS AUDIT (§27 self-check)

Har claim ke saath: kya test actually chala tha?

| Claim | Actually tested? | Evidence file |
|---|---|---|
| SO API se answers mile | ✅ | phase2_api_probe + demo output (87,856 B payload) |
| Reddit RSS chalta hai | ✅ (1 request, phir 429) | final retest output |
| WSJ/Bloomberg RSS live | ✅ | demo output me titles |
| Medium article text mila | ✅ | 15,158 B, article title live |
| NSE marketStatus JSON | ✅ | 2,135 B payload dekha |
| yfinance RELIANCE price | ✅ | ₹1244.0 print hua |
| Wayback SO page | ✅ | 1,175,484 bytes |
| OSM Overpass | ✅ (UA ke saath) | India Gate node |
| systemd service start | ✅ (test kiya — fail hua) | "inactive (dead)" |
| Offline model load | ✅ | dim 384 |
| Google Books 429 | ✅ | error body |
| Quora no-route | ✅ (403 + wayback 403) | probe |

**Koi bhi route "verified" nahi likha gaya jise test nahi kiya.**

---

## 5. NEXT SAFE TESTS (blueprint §30-13)

1. `patentsview` API basic query (AQ-01) — public, no key.
2. Kaggle/HF datasets route (AQ-05) — `pip install datasets` se public HF datasets bina key test.
3. Reddit RSS ko **60s gap** ke saath 3 subs par test (rate-limit window confirm).
4. OpenAIRE corrected call (AQ-02).
5. IA Scholar throttled retry (AQ-03).
6. reader-proxy ke saath **bhavcopy CSV ka daily snapshot** (evidence + reuse ke liye cache).

Ye sab **read-only, public, rate-respecting** tests hain — koi boundary nahi todte.
---

## 6. SWEEP v2 UPDATE (2026-09-23, round 2) — queue revision

| Item | Pehle | Ab |
|---|---|---|
| AQ-01 Patents | UNVERIFIED | ✅ **SOLVED via reader-proxy** (Google Patents page, 16,369 B). patentsview API unreachable (IPv6-only DNS + IPv6 egress blocked) — alternative route use karo |
| AQ-02 OpenAIRE | call malformed | ✅ **CLEARED** (200, 98,943 B) |
| AQ-03 IA Scholar | rate limit | ⚠️ abhi bhi limited (rate-limit page) — throttle + retry chahiye |
| AQ-05 Kaggle/HF datasets | key chahiye | ✅ **HF `datasets` public route CLEARED** (imdb bina key load hua); Kaggle API key abhi bhi optional |
| NEW: GDELT | — | ⚠️ CONDITIONAL — 5 s+ gap zaroori (30 s gap par 200) |
| HL: scheduled automation | listed as UNAVAILABLE (systemd dead) | ✅ **CORRECTED — systemd timers WORK** (15 s test 3/3; route monitor har 30 min chal raha hai). Hard limit nahi hai |

**Naya route: Nominatim geocoding** ✅ verified (Rajkot → 22.3053, 70.8028).
**Proxy UA rule:** r.jina.ai par full browser-UA → Cloudflare 403; neutral UA (`UAI-COS-research/1.0`) → 200.
