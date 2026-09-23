# ENVIRONMENT FALLBACK MAP + FAILURE ANALYSIS

> Blueprint Parts 5, 16, 23, 25, 30 ka output. Rule: **"I cannot do this"** par rukna nahi —
> pehle 10 sawal poocho, phir route do. Fallback ko **verified** ya **hypothetical** label karo.

---

## 1. The 10 Questions (Part 5) — har block par

| # | Sawaal | Is environment ka jawab |
|---|---|---|
| Q1 | Capability genuinely impossible? | Sirf ~5 cheezein: host access, sandbox escape, GPU training, auth bypass, real agent-spawning |
| Q2 | Ya sirf *current environment* me unavailable? | Zyadatar cheezein yahi case hai (creds, connectors, private data) |
| Q3 | Doosra available tool kar sakta hai? | ✅ aksar — jaise curl→fetch_page→playwright, ya OCR, ya reader proxy |
| Q4 | Doosra environment kar sakta hai? | ✅ user ka system (bot/API bridge), ya koi hosted service |
| Q5 | External API kar sakta hai? | ✅ (public APIs ready; key wale user ke baad) |
| Q6 | Connector/plugin kar sakta hai? | ❌ currently koi connector installed nahi (platform support ho sakta hai) |
| Q7 | User ek authorization/file/credential/URL de sakta hai? | ✅ **sabse fast route** — token/key/file/link |
| Q8 | Task ko available operations me todna possible? | ✅ humesha try karo — 90% cases yahin solve hote hain |
| Q9 | Ek step human kare, baaki main? | ✅ publish, login, payment, hot-line steps |
| Q10 | Doosra agent kar ke result de? | ⚠️ `POSSIBLE` sirf agar user koi model/API de |

**Verified fallback examples (is audit me actually use hue):**
- Cloudflare-blocked chatgpt share link → direct curl **403** → **reader proxy** → content mila ✅
- Playwright launch fail (`libnspr4.so`) → `apt install` libs → launch **OK** ✅
- `sqlite3` CLI missing → `sudo apt install sqlite3` → **OK** ✅
- OCR module missing → `apt install tesseract-ocr` → **OK** ✅
- Blocked page (reddit/instagram) → `web_search` snippets + alternate sources → **partial**, honestly disclosed ⚠️

---

## 2. FALLBACK ROUTE GRAPH (Part 5 ka chain, is environment ke liye instantiated)

```
TASK
 │
 ├─(1) DIRECT METHOD ................ bash / tools / network — 85% kaam yahin
 │
 ├─(2) ALTERNATIVE TOOL ............. curl ↔ fetch_page ↔ playwright ↔ git ↔ API
 │        └─ e.g. fetch_page 403 → curl → playwright → reader proxy
 │
 ├─(3) ALTERNATIVE ENVIRONMENT ...... /tmp ↔ workspace ↔ venv ↔ container-like isolation
 │        └─ e.g. conflicting deps → python venv / npm local / apt isolated
 │
 ├─(4) EXTERNAL API / CONNECTOR ..... public APIs ✅ | key-wale → user se
 │        └─ e.g. LLM call → user ka key; cloud files → user ka link
 │
 ├─(5) HUMAN-IN-THE-LOOP ............ login, publish, payment, KYC, "mujhe ye file do"
 │        └─ main checklist/steps deta hoon, tum 1 step karte ho
 │
 ├─(6) MULTI-AGENT DELEGATION ....... ❌ real agents nahi | ⚠️ user ka koi model ho to possible
 │
 └─(7) SAFE MANUAL WORKFLOW ......... main script/instructions/template banata hoon, execution tumhara
```

**Rule:** route claim karne se pehle label lagta hai — `VERIFIED` (test kiya), `POSSIBLE` (architecture me ho sakta),
`HYPOTHETICAL` (sirf soch, test nahi). Is file me jo bhi `VERIFIED` hai, uska evidence `probes/` me hai.

---

## 3. "CAN I DO IT SOMEWHERE ELSE?" — concrete task examples

| Task | Direct | Alternative | Environment change | External dep. | Human step | Final verdict |
|---|---|---|---|---|---|---|
| Paywalled article padhna | ❌ | — | — | — | user PDF bhej de | **HUMAN STEP** (bypass ❌) |
| Reddit discussion ka content | ❌ 403 | search snippets | — | Reddit API key (user) | — | **PARTIAL / HUMAN** |
| StackOverflow answer | ❌ 403 | docs/gh issues/local install | — | StackExchange API | — | **ALTERNATIVE** (API untested → U-item) |
| Instagram post reading | ❌ | — | — | Graph API (business) | screenshot do | **HUMAN STEP** |
| Video edit/convert | ⚠️ | ffmpeg apt install | — | — | — | **ALTERNATIVE (install)** |
| Voiceover | ⚠️ | voice audition → generate_speech | — | — | ek baar voice choose | **HUMAN STEP (1 baar)** |
| Email bhejna | ❌ creds | SMTP creds do | — | user SMTP app-password | — | **EXTERNAL DEP (user)** |
| Telegram bot live | ⚠️ code ready | BotFather token | — | token | 2 min setup | **HUMAN STEP** |
| Bulk website scraping | ✅ | polite crawl + rate limit | — | — | — | **DIRECT** (robots/ToS ka lihaz) |
| Private DB query | ❌ | schema+query likh du | — | creds/connection | tum chalao | **HUMAN STEP** |
| GPU model training | ❌ | Colab/Kaggle (user) | — | hosted GPU | notebook do | **ENV CHANGE (user)** |

---

## 4. FAILURE ANALYSIS (Part 23) — failure classes + remedy

| # | Failure class | Is environment me kaise dikhi | Remedy (verified) |
|---|---|---|---|
| 1 | Reasoning failure | (self-caught) spec drift: 15 vs 12 types | self-audit + tests |
| 2 | Tool failure | Playwright launch (`libnspr4.so`) | apt deps install ✅ |
| 3 | Access failure | reddit/instagram 403 | alternate source / disclose |
| 4 | Permission failure | `/` write denied | /home/user, /tmp use karo |
| 5 | Authentication failure | keine keys | user se maango |
| 6 | Environment limitation | no GPU | hosted option |
| 7 | Data limitation | portal 403 | alternate dataset |
| 8 | Source limitation | paywall | preprint/author copy |
| 9 | Network limitation | (none found — egress open) | — |
| 10 | API limitation | unauth rate limits | backoff, key |
| 11 | Rate limit | (not hit yet) | throttle + retry |
| 12 | Format incompatibility | binary formats | libs install / convert |
| 13 | Missing dependency | tesseract, sqlite3, browser libs | apt/pip install ✅ |
| 14 | Safety/policy restriction | CF bypass, paywall | **nahi karta — disclose** |
| 15 | Unknown | NSE timeout, patents timeout | re-test (U-items) |

**Anti-pattern jo main nahi karunga:** same failed operation ko baar-baar retry karna (Part 23 ki warning).
Max 2 attempts → phir route badlo ya user ko batao.

---

## 5. ENVIRONMENT MIGRATION MODEL (Part 25) — authorized path

```
Aaj ka environment (E1 sandbox)
   │  missing: LLM keys, TG token, GPU, private data, real-world publish
   ▼
required capability identify → required tool identify → required permission identify
   ▼
setup dependency (user ke paas) → USER/ADMIN AUTHORIZATION
   ▼
naya capability live (bot / API bridge / hosted GPU / private export)
   ▼
verify + memory me record + capability map v2 me update
```

**Migration ka jhootha claim nahi:** jab tak actual setup nahi hua, status `POSSIBLE` ya `CONDITIONAL` hi rahega —
"ho gaya" nahi likhunga (Part 25 ka explicit rule).

---

## 6. MAXIMUM LEGITIMATE UTILIZATION (Part 30) — combinations jo single tool nahi de sakta

| Combination | Naya capability jo akele me nahi hai |
|---|---|
| `shell + apt + browser + OCR` | JS site ka screenshot → text → structured data |
| `search + fetch(PDF) + pandas + chart` | source-backed data report (citation ke saath) |
| `git clone + tests + patch + diff` | third-party repo ka verified fix |
| `memory + audit + prompt compiler` | cross-session/cross-model persistent behaviour |
| `process + HTTP server + present_file` | user ko live, interactive artifact |
| `image gen + image search + PIL` | product-style visuals + reference-based edits |
| `Playwright + screenshot + memory` | web evidence trail (URL + timestamp + image) |

**Rule:** capability ko individually nahi, **combination me** evaluate kiya — kyunki asli power wahi se aati hai.
