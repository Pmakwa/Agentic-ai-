# UAI-COS v2.0 — EVALUATION, GOLDEN TESTS & QUALITY SCORECARD

> Spec #54 (Evaluation Engine), #55 (Golden Test Cases), #56 (Regression Prevention),
> #106 (Universal Quality Scorecard), #53 (Memory Quality Metrics) ka working setup.
> Sabse important baat: **ye sirf design nahi hai — suite actually chalti hai.**

```
$ bash tests/test_memory_os.sh
  TOTAL: 28 passed, 0 failed      ← ye asli output hai (2026-09-23)
```

---

## 1. Golden test cases (Spec #55) — 12 cases, 9 automated

| ID | Test case | Kya verify hota hai | Automated? |
|---|---|---|---|
| G-01 | High-confidence fact bina source | Governance block (exit 2) | ✅ |
| G-01b | High-confidence fact verified source ke saath | Allowed | ✅ |
| G-01c | Invalid confidence band | Schema reject | ✅ |
| G-02 | Same statement dobara | Duplicate detect + skip (exit 3) | ✅ |
| G-03 | Same conflict-key, alag statement | Dono records `conflicted` | ✅ |
| G-04 | Supersede chain | Purani record `superseded`, bidirectional link, history intact, **koi data loss nahi** | ✅ |
| G-05 | Past `expires_at` | Auto `expired` | ✅ |
| G-06 | Stale working memory / unscoped preference / verified-but-low-confidence / privacy-leak-risk | Audit chaaron detect kare | ✅ |
| G-07 | Retrieval + artifacts | `search`, `index`, `dash`, `audit log` sab kaam karein | ✅ |
| G-08 | Command surface | 12 subcommands available | ✅ |
| G-09 | Scope discipline | `global` tag wali preference ko **galti se flag na karna** (false positive test) | ✅ |
| G-10 | Long-running project resume | Naye turn par sirf project + state memory load ho, purani episodic detail nahi | ⏳ manual (Phase 1) |
| G-11 | High-risk action gate | Delete/publish/payment bina confirmation **block** | ⏳ manual (Phase 1) |
| G-12 | Language preference compliance | Roman Hindi + English alphabet, bina user ke Devanagari nahi | ⏳ manual (Phase 1) |

**Regression policy (Spec #56):** koi bhi change `tools/uai_mem.py` ya store schema me →
suite dobara chale → 28/28 pass → tabhi "approved" [`#84` change approval]. Fail ho to change reject/revert [`#85`].

---

## 2. Memory quality metrics (Spec #53) — is workspace ke actual numbers

| Metric | Current value (2026-09-23) | Target | Kaise naapa |
|---|---|---|---|
| Total live records | 25 | — | `uai_mem.py stats` |
| Memory health score | **100/100** | ≥ 90 | `uai_mem.py audit` |
| Schema compliance | 100% (0 issues) | 100% | audit `[schema]` |
| Open conflicts | 0 | 0 | audit `[open_conflict]` |
| Expired-but-active | 0 | 0 | audit `[expired_but_active]` |
| Inference-promoted-to-fact | 0 | 0 | audit `[inference_promoted_to_fact]` |
| Unscoped preference/constraint | 0 | 0 | audit `[unscoped_preference]` |
| Privacy leak risk | 0 | 0 | audit `[privacy_leak_risk]` |
| Duplicates | 0 | 0 | audit `[duplicate]` |
| Provenance coverage | 25/25 (100%) | 100% | har record me `source.kind` |
| High-confidence records with source | 21/21 | 100% | audit rule |
| Automation coverage (golden tests) | 9/12 (75%) | 100% | ye file |

**Honest note:** "retrieval precision", "correction rate" jaise metrics ke liye real usage data chahiye —
abhi store chhota hai. Ye Phase 2 me automate honge (roadmap dekho).

---

## 3. Quality scorecard (Spec #106) — internal diagnostic, user ko thopa nahi jaata

| Dimension | Sawaal | Is workspace ke liye evidence |
|---|---|---|
| Intent match | User ka actual goal mila? | V2 prompt *poora* import hua + apply hua (V1 ke saath) |
| Requirement coverage | Saare mandatory points cover? | Step-1 deliverables table + Step-2 9 files |
| Factual reliability | Claims verify hue? | 403 episode documented, hashes, actual test output |
| Memory correctness | Sahi memory use hui, galat nahi? | Sirf V1/V2 ke extracted rules se records bane, fabricate nahi kiya |
| Source quality | Provenance clean? | `MEM-SRC-0001` + `IMPORT_LOG.md` |
| Completeness | Kuch chhoota nahi? | Chat ke 3 offered options + 4th layer sab cover |
| Relevance | Bakwaas bhara nahi? | Har doc ka apna kaam, no duplicate text |
| Consistency | Aapas me contradiction? | Audit 100/100, conflicts 0 |
| Format compliance | Language + structure preference follow? | Roman Hindi, headings + tables |
| Safety | Bounded actions? | Koi T3/T4 action bina approval nahi |
| Privacy | Sensitive data leak nahi? | Sab records `normal` sensitivity, client data nahi |
| Action correctness | Tools sahi chale? | 28/28 tests, index/dash regenerate |

**Rule [Spec #106]:** numeric score user-facing output me **nahi** thopa jaata — sirf tab dikhata hai jab user audit maange.

---

## 4. Evaluation workflow (Spec #54) — har system change par

```
SYSTEM CHANGE (naya memory type / rule / tool)
        ↓
GOLDEN SUITE RUN      bash tests/test_memory_os.sh
        ↓
LIVE AUDIT            python3 tools/uai_mem.py audit --log
        ↓
COMPARE with baseline (28/28 + score ≥ 90)
        ↓
REGRESSION?  ── haan ──▶ REVERT + error memory banao (MEM-ERR-*)
        │
        nahi
        ↓
APPROVE + audit log entry + decision memory (#32)
```

---

## 5. Ye setup kaunsi galti pakadta hai (real examples from aaj)

| Galti ka type | Kaise pakdi gayi | Fix |
|---|---|---|
| Spec drift | V2 #12 me 15 memory types the, tool me sirf 12 → gap mila | `temporal`, `relational`, `procedural_state` add kiye |
| Status model gap | V2 #14 me `unverified/uncertain/quarantined` bhi hain | STATUSES 11 values kiye |
| Confidence bands | V2 #15 me 5 bands (very_low…very_high) | CLI me 5 bands |
| False positive in audit | 3 constraints "unscoped" flag hue, jabki wo genuinely global the | Rule refine + explicit `global` tag |
| Silent single point of failure | Direct fetch 403 | Reader proxy fallback + error memory + prevention rule |
