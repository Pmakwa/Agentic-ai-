# UAI-COS v2.0 — MEMORY TYPES INTEGRATION

> Spec V2 #11–#23 (Memory Operating System → Knowledge Graph) ka practical integration guide:
> kaunsa type kidhar store hota hai, kaise retrieve hota hai, kab expire hota hai, kaun padh/likh sakta hai,
> aur is workspace me uska **live example** kya hai.
>
> Ye file source chat ke us "option 2" ka jawab hai: *integration of memory types in Advanced V2.0*.

---

## A. Taxonomy — V1 ke 12 types → V2 ke 15 types

| # | V2 Type (spec #12) | V1 me tha? | Storage | Retrieval weight | Default TTL | Live example (is workspace) |
|---|---|---|---|---|---|---|
| 1 | CORE | ✅ | jsonl (append-only) | Highest — har turn load | No expiry (review yearly) | `MEM-CORE-0001` user ka UAI-COS goal |
| 2 | PREFERENCE | ✅ | jsonl | High (style/language par veto) | No expiry, review 6 months | `MEM-PREF-0001` Roman Hindi |
| 3 | CONSTRAINT | ✅ | jsonl | **Veto power** — ignore nahi kar sakte | No expiry | `MEM-CONS-0003` high-risk par approval |
| 4 | SEMANTIC | ✅ | jsonl + knowledge graph node | High (facts) | 180 din par re-verify | (research tasks se bharega) |
| 5 | EPISODIC | ✅ | jsonl | Low-medium (context ke liye) | 12 months → archive | `MEM-EPI-0001` aaj ka milestone |
| 6 | PROCEDURAL | ✅ | jsonl | High (workflow maangne par) | Review 6 months | `MEM-PROC-0001` session boot protocol |
| 7 | WORKING | ✅ | jsonl (expires quickly) | Highest for current turn, phir drop | **7 din** (auto expiry) | `MEM-WORK-0001` current task |
| 8 | PROJECT | ✅ | jsonl | High jab us project par kaam ho | Project end tak | `MEM-PROJ-0001` UAI-COS workspace |
| 9 | DECISION | ✅ | jsonl + graph edge | High (rationale ke liye) | No expiry | `MEM-DEC-0001` V2 canonical |
| 10 | ERROR | ✅ | jsonl | Medium-high (repeat galti rokne ke liye) | No expiry, review 6 months | `MEM-ERR-0001` 403 → proxy fix |
| 11 | SOURCE | ✅ | jsonl (evidence layer) | High (fact verification par) | source type ke hisaab se | `MEM-SRC-0001` share chat URL |
| 12 | SHARED | ✅ | jsonl + permission check | Medium (multi-agent only) | Workflow end tak | (multi-agent phase me bharega) |
| 13 | **TEMPORAL** | ❌ new | jsonl with `expires_at` | High jab time-window relevant ho | Explicit `valid_from`/`valid_until` | `MEM-TEMP-0001` session validity |
| 14 | **RELATIONAL** | ❌ new | knowledge graph edges (abhi jsonl edge records) | Query-based (graph traversal) | Edges superede hote hain, delete nahi | `MEM-REL-0001` USER→PROJECT→MEMORY→SOURCE |
| 15 | **PROCEDURAL STATE** | ❌ new | jsonl (state snapshot + history) | High (resume karne ke liye) | Workflow end tak | `MEM-PSTATE-0001` Step1 done / Step2 live |

**Integration rule:** V1 ke 12 types *drop nahi* hui — unke upar 3 layer add hui: **temporal** (kab valid thi),
**relational** (kis se judi hai), **procedural state** (workflow kahan tak pahuncha). Isliye store backward-compatible hai.

---

## B. Record lifecycle (Spec #14 + #99 + #100)

```
        intake                  validation              use                    decay
  ┌───────────────┐      ┌──────────────────┐   ┌──────────────┐      ┌────────────────┐
  │  candidate    │ ───▶ │   unverified     │──▶│   verified   │ ───▶ │    active      │
  └───────────────┘      └──────────────────┘   └──────────────┘      └────────────────┘
        │                        │                     │                      │
        │                        │                     │                      ▼
        │                        │                     │              ┌────────────────┐
        │                        │                     │              │   expired      │
        │                        │                     │              └────────────────┘
        ▼                        ▼                     ▼                      ▼
   uncertain              conflicted             superseded              archived / deleted
   (kuch missing)      (do versions takraye)   (naya version aaya)     (history retain)
```

**Promotion ke liye evidence chahiye (#99):** user ka explicit statement, ya verified source, ya repeated observation.
**Demotion (#100):** expire, conflict, ya naya version — lekin record **delete nahi** hota; `history[]` aur `superseded_by` chain rehti hai.

---

## C. Confidence integration (Spec #15)

Confidence ek number nahi — 8 factors ka mixture:

| Factor | Is workspace me kaise capture hota hai |
|---|---|
| Source authority | `authority` field: user_explicit > user_correction > verified_source > user_implied > derived > agent_inference |
| Source recency | `source.observed_at` + `last_verified` |
| Direct user statement | `source.kind = user_instruction` |
| Independent verification | `last_verified` date + `source.kind = tool_result/url` |
| Consistency | Audit ka `open_conflict` check |
| Repeat observation | Same fingerprint dobara milna (dedupe log) |
| Context match | `applies_when` / `does_not_apply_when` / `scope.domains` |
| Conflict level | `status = conflicted` → confidence automatically suspect |

**Bands:** `very_high` (user ne 2+ baar kaha ya tool se verify) · `high` (explicit statement + verifiable source) ·
`medium` (ek baar kaha, ya context-specific) · `low` (inference, unverified) · `very_low` (guess — **isse avoid karo**).

---

## D. Retrieval pipeline (Spec #18) — is workspace ka actual filter order

```
1. SCOPE FILTER      : domain/project match? warna drop
2. CONSTRAINT LOCK   : saare matching constraints ko non-negotiable maano (veto)
3. AUTHORITY SORT    : user_explicit pehle, agent_inference sabse baad
4. FRESHNESS CHECK   : expired / stale → drop (ya "purana" label ke saath)
5. CONFIDENCE GATE   : low/very_low ko fact ki tarah mat use karo
6. CONFLICT CHECK    : conflicted record use karne se pehle resolve karo
7. INSTRUCTION OVERLAP: current instruction ke saath direct takraav? → current jeetega (#44)
8. TOP-K             : sirf minimum necessary context handoff (#0.5)
```

Is order ko **manual + CLI** (`list --status active --status verified`, `search`, `audit`) se implement kiya gaya hai;
Phase 2/3 me isko scored retrieval engine banega (dekho roadmap).

---

## E. Access control per type (Spec #70, #0.6)

| Type | Read | Write | Share (bahar) |
|---|---|---|---|
| core / preference / constraint | sab agents | supervisor only | allowed (non-sensitive part) |
| project / decision / procedural | relevant agents | supervisor + assigned agent | project ke andar |
| semantic / source / error | sab (verification ke liye) | assigned agent | URL/evidence share allowed |
| working / procedural_state | current task agents | current task agents | nahi |
| relational | graph queries | supervisor | restricted |
| **sensitivity=private/secret** | sirf task-relevant agent | supervisor | **never** (audit isko flag karta hai) |

---

## F. Knowledge graph (Spec #23) — is workspace ka minimal live version

```
        ┌──────┐  owns   ┌──────────────┐  contains  ┌──────────────┐  sourced_from  ┌──────────────┐
        │ USER │────────▶│ PROJECT      │───────────▶│ MEMORY STORE │───────────────▶│ SOURCE       │
        │      │         │ uai-cos      │            │ 25 records   │                │ shared chat  │
        └──┬───┘         └──────┬───────┘            └──────┬───────┘                └──────────────┘
           │ stated             │ governed by                │ resolved_by (conflict)
           ▼                    ▼                            ▼
     ┌───────────┐        ┌───────────┐                ┌───────────┐
     │PREFERENCE │        │ DECISION  │                │  ERROR    │
     │ +CONSTRAINT│       │ +PSTATE   │                │ → FIX     │
     └───────────┘        └───────────┘                └───────────┘
```

Edges aaj `relational` records ke roop me store hote hain (`MEM-REL-0001`) — Phase 2/3 me ye ek proper
edge table / graph index banega jisme traversal queries chalengi (`kaunsi memory kis decision se depend karti hai?`).

---

## G. Integration checklist (jab bhi naya info aaye)

- [ ] Type decide kiya? (`TYPES` list se, guess nahi)
- [ ] Scope likha? (`domain`, `project`, `applies_when`, `does_not_apply_when`)
- [ ] Source + authority + observed date diya?
- [ ] Confidence band honestly chuna (false precision nahi)?
- [ ] Sensitivity set ki (client data → private)?
- [ ] Duplicate/conflict check CLI ne chalaya?
- [ ] Status `candidate` rakha, seedha "fact" nahi banaya?
- [ ] Kya user ko batana chahiye ki ye memory **kahan** save hui (reality rule)?
- [ ] Index + dashboard + audit dobara chala?
