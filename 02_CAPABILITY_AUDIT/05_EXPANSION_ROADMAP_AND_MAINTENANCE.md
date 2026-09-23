# CAPABILITY EXPANSION ROADMAP + MAINTENANCE PROTOCOL

> Blueprint Parts 22, 27-M, 33, 35 ka output. Do hisse: (1) capability kaise badhegi, (2) map kaise zinda rahega.

---

## 1. CAPABILITY EXPANSION ROADMAP — impact × effort ke hisaab se

### Tier 1 — Chhota kaam, bada unlock (aaj/parso possible)

| # | Expansion | Kya unlock karega | Kaun karega | Effort | User chahiye? |
|---|---|---|---|---|---|
| E1 | **Telegram bot live** (token) | mobile se memory console + LLM bridge; sandbox se bahar ka communication | main code ready, tum token do | 5 min | ✅ token |
| E2 | **LLM API key** (`LLM_API_KEY`) | `/ask`, cross-model verification, summaries, embeddings | tum key do | 5 min | ✅ key |
| E3 | **ffmpeg + libreoffice install** | video process, docx↔pdf conversion | main (apt) | 5 min | ❌ |
| E4 | **search upgrade**: StackExchange/Semantic Scholar/Wayback API test + wrapper | dev/academic research ka gap bhar jayega | main | 30 min | ❌ |
| E5 | **memory search upgrade**: SQLite FTS5 + scored retrieval | retrieval precision (Phase 2 ka pehla step) | main | 1–2 hrs | ❌ |

### Tier 2 — Medium (structural gains)

| # | Expansion | Unlock | Effort |
|---|---|---|---|
| E6 | **Vector/embedding memory search** (local sentence-transformers ya API embeddings) | semantic recall, "similar meaning" retrieval | half day |
| E7 | **Evidence vault**: har research task ka snapshot (HTML/PDF/screenshot + hash + URL) | citation-grade provenance | 2–3 hrs |
| E8 | **Scheduled maintenance job** (systemd timer ya process loop): roz expire+audit+reminder | memory hygiene khud-ba-khud | 1 hr |
| E9 | **WhatsApp Cloud API** (user ka Meta setup) | WhatsApp par wahi commands | user-dependent |
| E10 | **Playwright research agent**: JS sites, HAR capture, form-fill (authorized) | deep web research + evidence | 3–4 hrs |

### Tier 3 — Bada (architecture-level, sirf agar user chahe)

| # | Expansion | Unlock | Effort/Note |
|---|---|---|---|
| E11 | **Multi-model routing** (fast/standard/deep tiers) | cost-quality balance, cross-verification | user keys + orchestration |
| E12 | **Real orchestration** (n8n/LangGraph/custom runner) | actual parallel sub-agents | infra setup |
| E13 | **Hosted GPU channel** (Colab/Kaggle/Modal) | heavy ML tasks | user account |
| E14 | **Connectors** (Drive/Slack/Notion/GitHub app) | direct cloud data access | platform + auth |
| E15 | **Public API server** (workspace HTTP + webhook) | bahar se memory read/write | port exposure + auth design |

**Recommendation (Part 30-style):** E1+E2+E3+E4 = **aaj hi** capability ko 2× kar dete hain, aur inme sirf 2 cheezein tumse chahiye (token + key).
E5+E8 = system ko "self-maintaining" bana dete hain — bina user ke chalte rehte hain.

---

## 2. CONTINUOUS CAPABILITY UPDATE (Part 22) — versioning protocol

**Current:** `CAPABILITY-MAP v1.0` (2026-09-23, is audit se)

Map update **kab** hoga:
- naya tool/connector/API available ho
- permission badle (naya token/key)
- environment badle (OS, installs, GPU)
- koi previously-blocked operation possible ho jaye
- koi previously-working operation toot jaye
- naya data source accessible ho

**Har update me record hoga:**

| Field | Example |
|---|---|
| version | v1.0 → v1.1 |
| date/time | 2026-09-24 10:00 |
| what changed | "Telegram bot live ho gaya — external messaging ab `CONDITIONAL` se `AVAILABLE`" |
| why | user ne token diya |
| evidence | bot log + audit log entry |
| affected workflows | memory capture, /ask |
| rollback | token hatane par wapas CONDITIONAL |

**Files jo update honge:**
1. `CAPABILITY_MAP.json` (machine-readable — memory system isi se records banata hai)
2. Ye 6 docs (human-readable)
3. UAI-COS memory store (`uai_mem.py`) — `capability` facts `source` type me
4. `probes/` — naye test evidence

---

## 3. SELF-EXPLORATION LOOP (Part 14) — har session/phase par

```
OBSERVE    → environment state dekho (env probe script)
INVENTORY  → tools/packages/sites ki list refresh karo
TEST       → U-queue me se safe test chalao
VERIFY     → result ko evidence ke saath confirm karo
MAP        → CAPABILITY_MAP.json + docs update karo
DOCUMENT   → memory record + audit log entry
IMPROVE    → jo capability missing thi, uska expansion item banao
RE-TEST    → verify ki change ne kuch toda nahi (regression)
```

**Chalane ke commands:**
```bash
bash  02_CAPABILITY_AUDIT/probes/run_environment_probe.sh     # inventory refresh
bash  02_CAPABILITY_AUDIT/probes/run_site_matrix.sh           # access refresh
python3 02_CAPABILITY_AUDIT/probes/update_map.py              # JSON + version bump + memory sync
python3 tools/uai_mem.py audit --log                          # system health
bash  tests/test_memory_os.sh                                 # regression
```

---

## 4. FINAL OPERATING PRINCIPLE (Part 35) — is audit ka commitment

**DISCOVER → VERIFY → MAP → CONNECT → RESEARCH → CROSS-CHECK → EXECUTE → AUDIT → UPDATE**

- Har boundary par pehle poocho: *missing capability? missing tool? missing permission? missing environment?
  missing dependency? temporary failure? ya genuine hard limit?*
- Sirf **wo** kehna jo evidence se supported hai.
- `POSSIBLE`/`CONDITIONAL`/`UNKNOWN` ko kabhi `VERIFIED` ki tarah pesh nahi karna.
- Power dikhane ke liye nahi, **exactly kitne powerful hoon** ye jaanne ke liye — Part 29.

**Aur ek line jo is audit ka nichod hai:**
> Is environment me main **computer + browser + research layer + memory** ke saath ek kaam karne wala agent hoon —
> tumhari **credentials, private data, aur authorized bridges** ke bina aage nahi badh sakta, aur bypass **kabhi nahi** karunga.
