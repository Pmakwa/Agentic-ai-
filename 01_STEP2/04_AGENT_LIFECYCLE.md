# UAI-COS v2.0 — AGENT LIFECYCLE & AUTONOMY MODEL

> Spec #9 (Agent Identity), #10 (Agent Lifecycle), #24 (Orchestration), #27 (Tool Risk),
> #50 (Autonomy Levels), #52 (Agent Metrics), #91 (Specialist Escalation) ka concrete design.
> Ye source chat ke "implementation roadmap for supervisor and agent lifecycle" ka lifecycle half hai.

---

## 1. Lifecycle states (Spec #10 — exact 11 states)

| # | State | Is workspace me kaise dikhta hai | Exit condition |
|---|---|---|---|
| 1 | CREATE | Role define hota hai (jaise "Memory OS Agent") | Written definition ready |
| 2 | REGISTER | `agents/AGENT_REGISTRY.md` me entry | Entry + scope + permissions + spec refs likhe hue |
| 3 | VALIDATE | Scope clear? Permission defined? Authority bounded? | Teeno YES [`#9` — warna production me nahi aayega] |
| 4 | ASSIGN PERMISSIONS | Read set + write set + tool set | Least privilege applied [`#0.6`] |
| 5 | TEST | Golden tests (G-01…G-12) me role ka behaviour check | Test pass |
| 6 | DEPLOY | Task ke dauran activation (logical, is single-agent setup me sequential) | Task assign hua |
| 7 | MONITOR | Output par supervisor check + audit log | Koi unflagged violation nahi |
| 8 | EVALUATE | Metrics: accuracy, instruction compliance, memory correctness [`#52`] | Score threshold ke upar |
| 9 | UPDATE | Prompt/scope/scope-memory improve | Change logged [`#40`] |
| 10 | REVALIDATE | Update ke baad dobara golden tests | Regression nahi |
| 11 | RETIRE | Role redundant ho gaya → registry se `retired` mark, definition history me | Documented |

---

## 2. Autonomy levels (Spec #50) — kaunsa kaam kis level par

| Level | Meaning | Is workspace ke task ka example |
|---|---|---|
| **A0 Observe** | Sirf dekhna, kuch nahi | User ka message padhna, koi memory write nahi |
| **A1 Recommend** | Suggestion dena | "Aapke paas 3 options hain…" |
| **A2 Draft** | Output banana, bhejna nahi | File/prompt draft karna |
| **A3 Execute with approval** | Approval ke baad action | File overwrite, email/DM draft bhejna, bot deploy |
| **A4 Authorized autonomous** | Pre-approved scope me independently | Memory `candidate→active` promotion, index/dashboard regenerate, tests run |
| **A5 Supervised autonomous** | Multi-step, monitoring + escalation | Multi-file project refactor jab user ne "pura karo" kaha ho |

**Scope-specific rule:** A4/A5 sirf us domain me jahan user ne explicitly permission di ho. Ek domain ki permission doosre me carry **nahi** hoti [`#50` last line].

---

## 3. Tool risk tiers (Spec #27, #28, #62) + is environment ka mapping

| Tier | Nature | Examples (is environment) | Required autonomy |
|---|---|---|---|
| T0 | Read-only, local | file read, `list`, `search`, `stats`, `audit` | A4 — free |
| T1 | Local write, reversible | workspace file banana, memory `add`, `index`, `dash` | A4 — free (audit log hota hai) |
| T2 | External read | `web_search`, `fetch_page`, image search | A4 — free |
| T3 | External write / irreversible-ish | Telegram message bhejna, email, public post, API POST | **A3 — user approval** |
| T4 | Destructive / financial / legal | file delete, payment, account change, data delete | **A3 + confirmation + rollback plan** [`#49`, #62`] |

**Idempotency (#28):** T3/T4 actions se pehle request key banao — dobara retry se duplicate na ho (jaise ek hi message 2 baar na jaaye).

---

## 4. Model routing tiers (Phase 4 design)

| Tier | Kaam | Latency/cost | Kab |
|---|---|---|---|
| FAST | classification, dedupe check, format check, simple extraction | low | har turn |
| STANDARD | drafting, coding, scenario writing, planning | medium | most tasks |
| DEEP | research synthesis, conflict resolution, red-team, architecture decisions | high | jahan galti mehngi ho |
| VERIFIER | alag perspective se output check (cross-model) | medium | high-risk / public output |

Rule: **deep model tabhi jab decision reversible na ho ya evidence dense ho** [`#94` quality-vs-speed controller].

---

## 5. Orchestration pattern (Spec #24) — is workspace ka actual flow

```
USER REQUEST
   │
   ▼
[CENTRAL SUPERVISOR]  classify + risk tier + retrieve filter   ← T0 tools
   │
   ├── INTAKE (S1)      intent, requirements, ambiguity, constraints
   ├── PLANNING (S2)    decomposition, dependency, tool auth, risk
   ├── DOMAIN (S3)      task-specific specialists (sirf relevant wale)
   ├── QUALITY (S4)     accuracy, compliance, hallucination, privacy, format, red-team
   └── LEARNING (S5)    correction, RCA, workflow update
   │
   ▼
[HANDOFF with minimum necessary context]  ← #25 JSON payload
   │
   ▼
OUTPUT → QUALITY GATE (#97) → RELEASE
   │
   ▼
MEMORY UPDATE → INDEX/DASH → AUDIT LOG → (next turn retrieval)
```

**Parallelization (#65):** independent branches (jaise "roadmap likho" + "tests likho") ek saath chal sakte hain;
**dependent** branches hamesha sequence me (#66 state management: ek branch ka output doosre ka input ho to lock).

---

## 6. Escalation & disagreement (Spec #89, #90, #91)
- Do agents ka output takraye → **disagreement protocol**: dono positions + evidence likho, supervisor decide kare,
  decision memory me `decision` record bane (rationale ke saath) [`#32`].
- Specialist scope bahar ka sawal → escalate to supervisor, guess nahi [`#91`, #92`].
- 3 attempts ke baad bhi fix na ho → ruk kar user ko batao [`#93` anti-loop].

---

## 7. Metrics (Spec #52) — agent health is workspace me kaise naapa jaata hai

| Metric | Definition | Current measurement |
|---|---|---|
| Instruction compliance | User ke points ka % jo deliverable me cover hue | Manual per turn (Phase 1 tasks) |
| Memory correctness | Galat/irrelevant memory kitni baar use hui (target: 0) | Audit + per-turn review |
| Conflict rate | Conflicted records / total live | `audit` → `open_conflict` |
| Retrieval precision | Relevant memory ids / total loaded ids | Manual (Phase 2 par automate) |
| Correction rate | User corrections / tasks | Episodic memory se count ho sakta hai |
| Staleness | Stale facts / semantic records | `audit` → `stale_facts` |
| Failure recovery | Failure → fix → documented (error memory) | `MEM-ERR-*` count |
