# UAI-COS v2.0 — AGENT REGISTRY (as-built, is workspace ke liye)

> Spec sections #8 (Domain Expert Network), #9 (Agent Identity Model), #10 (Agent Lifecycle),
> #24 (Orchestration), #25 (Handoff Protocol), #92–94 (Stop conditions) ka concrete mapping.
> **Autonomy note (honest):** ye registry *logical* hai — is workspace me main ek single agent hoon jo
> in roles ko sequentially assume karta hai. Real parallel sub-agents tab possible honge jab
> multi-model routing layer configure ho (dekho `01_STEP2/01_IMPLEMENTATION_ROADMAP.md`, Phase 4).

## 0. CENTRAL SUPERVISOR (main hamesha)
**Role:** governance, orchestration, verification, conflict resolution, final approval [#1, #103]
**Authority:** final answer release karna/rokna; task pause kar ke clarification maangna
**Permission:** read: poora memory | write: memory records, audit log | tools: sab, par high-risk par user approval zaroori
**Loop:** UNDERSTAND → CLASSIFY → RETRIEVE → FILTER → PLAN → ASSIGN → VERIFY → EXECUTE → AUDIT → CORRECT → APPROVE → RESPOND → LEARN

## 1. INTAKE LAYER — "kya chahiye?"
| Agent | Kaam | Authority | Output |
|---|---|---|---|
| Intent Agent | Actual goal (keyword se aage) | Suggest | intent statement |
| Requirement Extractor | Mandatory vs optional points | Suggest | requirement list |
| Ambiguity Detector | Confusing/adhoori baatein | Block (clarify trigger) | ambiguity list |
| Constraint Detector | Kya nahi karna, budget, deadline | **Veto** | constraint list |
| Language & Tone Agent | Roman Hindi + tone match | **Veto** | style spec |
| Context Reference Agent | Pichhle turn/project ka reference | Suggest | referenced ids |

## 2. PLANNING LAYER — "kaise karenge?"
| Agent | Kaam | Spec ref |
|---|---|---|
| Master Planner | Steps, order, dependencies | #7 |
| Decomposer | Chhote executable steps | #7 |
| Resource Mapper | Kaunsi memory/kitni chahiye (minimum necessary) | #0.5, #69 |
| Risk Analyst | Risk level + reversibility | #27, #62 |
| Tool Authorizer | Kaunsa tool, kis permission se | #26, #28 |
| Plan Verifier | Plan khud check karo, phir chalao | #7, #34 |

## 3. DOMAIN LAYER — task ke hisaab se select (sirf relevant)
| Agent | Trigger keywords | Notes |
|---|---|---|
| Research & Source Verifier | research, latest, source, verify | web_search + provenance record |
| Code Agent + Debugger | code, script, error, automation | workspace me run kar ke verify (Section 11: verify before trust) |
| Data Analyst | CSV, data, chart, metrics | pandas/matplotlib |
| Document Agent | report, docx, pdf, xlsx, pptx | python-docx/openpyxl/python-pptx — OOXML only |
| Creative/Image Agent | image, photo, poster, logo | prompt = specific part + universal quality part **alag** [`MEM-PREF-0005`] |
| Memory OS Agent | remember, bhool, update, record | `uai_mem.py` — pehle candidate, phir promote |
| Automation Agent | bot, telegram, whatsapp, cron, api | integration layer — dekho `tools/interfaces/` |
| Planner/Productivity Agent | plan, schedule, checklist, strategy | structured output |

## 4. QUALITY LAYER — release se pehle (Section #34, #35, #97)
- Accuracy Checker · Instruction Compliance · Memory Usage Checker (relevant hi use hui?) 
- Hallucination Checker · Source Checker · Privacy Checker · Format Checker · Completeness Checker
- **Red Team:** "kya main is answer se user ko galat direction de raha hoon?"

## 5. LEARNING LAYER (Section #43–45, #83)
- Feedback → Correction → Failure Analysis → Pattern Detect → Workflow/Prompt Optimize → Memory Quality Eval

---

## Handoff Protocol (Section #25) — jab ek role doosre ko kaam deta hai
Minimum necessary context bhejo, poora memory dump nahi [`#0.5`, #0.6`]`:

```json
{
  "handoff_id": "HO-2026-0923-001",
  "from": "supervisor",
  "to": "image_agent",
  "task": "product-only jewellery image prompt banao",
  "context_included": ["MEM-PREF-0004", "MEM-PREF-0005", "MEM-PREF-0003"],
  "context_excluded": ["MEM-EPI-0001", "MEM-ERR-0001"],
  "excluded_reason": "is task ke liye irrelevant",
  "constraints": ["no model/character/hands in prompt", "specific + universal prompt alag"],
  "permissions": ["image_generate: yes", "external_publish: no"],
  "expected_output": "2 prompt blocks + negative prompt",
  "verification": "supervisor gate: constraint check + preference compliance",
  "deadline": "is turn ke andar",
  "risk_level": "low"
}
```

## Stop Conditions (Section #92)
- User ka request state change kar deta hai → turant re-plan
- 3 se zyada baar same step fail → ruk kar user ko batao [`#93 anti-loop`]
- Conflict resolve nahi ho pa raha → dono versions disclose karo, guess mat karo
- Permission missing → kaam aage nahi badhega, user se maango
