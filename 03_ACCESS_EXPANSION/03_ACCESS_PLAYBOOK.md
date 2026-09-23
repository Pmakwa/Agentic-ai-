# ACCESS PLAYBOOK — verified routes ka daily use

> Ye recipes **actually chalayi gayi hain** (2026-09-23). Har recipe ke saath evidence ki wo live data deti hai.

---

## 0. Rule jo har route par lagti hai

1. **Order:** direct → official API → feed/RSS → reader-proxy → Wayback → user-provided file. (Blueprint §31 decision logic)
2. **Rate limits:** Reddit RSS = **60s gap**; reader-proxy free = tez calls par 429 → 10-15s gap; GitHub unauth = 60/hr.
3. **Provenance:** har call `03_ACCESS_EXPANSION/route_provenance.jsonl` me likhi jaati hai — success fabricate nahi hoti.
4. **Bypass nahi:** paywall/login/CAPTCHA par **ruk jao**, alternate source dhundo, ya user se maango. (§25)

---

## 1. StackOverflow Q&A (site 403 → API se full content)

```bash
python3 tools/access_routes.py so "python asyncio gather"
```
Output (live):
```
[   0] (Python) How to run tasks concurrently ... (ans=1)
[   5] Python asyncio gather dictionary (ans=1)
```
Answer body bhi milta hai (`so_answers(q_id)`), aur bulk chahiye to **SO data dump (518 MB)** archive.org par hai.

## 2. Paywalled news ki headlines (WSJ / Bloomberg)

```bash
python3 tools/access_routes.py rss https://feeds.a.dj.com/rss/RSSMarketsMain.xml
python3 tools/access_routes.py rss https://feeds.bloomberg.com/markets/news.rss
```
Live output:
```
WSJ      -> "Stocks Sink in Broad AI Rout Sparked by China's Deep..."
Bloomberg-> "CanSemi Tech Joins China Chip IPO Wave With $919 Mil..."
```

## 3. Blocked page ka poora content (smart fetch — fallback chain khud lagti hai)

```bash
python3 tools/access_routes.py fetch "https://medium.com/tag/programming"
# → status: PROXY ya WAYBACK (dono verified)
```
Chain: `direct (403) → reader-proxy (200, full text) → wayback (404 KB)` — jo pehle chalega wahi return hoga.

## 4. Academic research — 4 sources ek command me

```bash
python3 tools/access_routes.py paper "retrieval augmented generation"
```
Live output mein: Crossref DOI + OpenAlex (citations/OA flag) + EuropePMC (OA full-text flag) + PubMed IDs.
**Open-access PDF** ke liye Unpaywall: `oa_pdf(doi)` — bas apna email `access_routes.py` me daal dena (API test-email reject karti hai).

## 5. NSE / Indian stocks

```bash
python3 tools/access_routes.py nse marketStatus      # proxy route → marketState JSON
python3 tools/access_routes.py nse sec_bhavdata_full.csv   # bhavcopy CSV (~213 KB)
```
Aur stocks ke liye best route (direct, reliable):
```python
import yfinance as yf
yf.Ticker("RELIANCE.NS").history(period="5d")   # ✅ live: close ₹1244.0 (23-Sep-2026)
```

## 6. Purani/dead/blocked page (Wayback)

```bash
python3 tools/access_routes.py wb "https://stackoverflow.com/questions/11227809/"
# → available=True, 1,175,484 chars
```
Discovery ke liye CDX:
```python
from access_routes import wayback_find
wayback_find("reddit.com/r/programming/comments/*", limit=5)   # archived thread URLs + timestamps
```

## 7. Reddit (slow lane — rules respect karke)

```python
from access_routes import rss          # 60s gap built-in hai
rss("https://www.reddit.com/r/programming/.rss", limit=10)   # titles + links
```
Full API chahiye (fast + complete) → user Reddit app banaye → OAuth creds → tab ye route `DIRECT` ho jaayega.

## 8. Environment bootstrap (har session ke start me)

```bash
bash tools/bootstrap_environment.sh    # browser + fonts + model cache + packages + verify
python3 tools/access_routes.py demo    # saare routes ka health check
```

---

## Rate-limit cheat sheet

| Route | Limit | Rule |
|---|---|---|
| Reddit RSS | ~1/min | 60s gap (library me set hai) |
| reader-proxy (free) | burst par 429 | 10-15s gap, ya user ka Jina key |
| StackExchange (anonymous) | ~300/day/IP | batches me karo |
| GitHub (unauth) | 60/hr | token se 5000/hr |
| PubMed | 3/sec | bina key |
| Crossref/OpenAlex | polite pool | email bhejo (optional) |
| yfinance | unofficial | thoda gap, bulk par cached data |
| Wayback | soft limits | CDX queries sambhal kar |

## "Kya code se ho sakta hai?" — 10 sawal ka jawab (blueprint §19)

| Sawaal | Jawab |
|---|---|
| Documented interface? | ✅ StackExchange/Crossref/OpenAlex/Overpass/RSS sab documented |
| Authorized API? | ✅ (public), kuch key-based |
| Official SDK/CLI? | ✅ yfinance, kaggle, gh, rclone; SDKs pip se |
| Current env execute kar sakti hai? | ✅ Python + network verified |
| Credentials chahiye? | kuch routes par (user action listed) |
| Another env? | sirf user ke accounts (hard limit) |

**Conclusion:** jo bhi route "code se" possible hai, wo **likh diya gaya hai aur test bhi ho gaya** (`tools/access_routes.py`) —
aur jo permission ke bina possible nahi, wo **alag se listed** hai (bypass nahi).
