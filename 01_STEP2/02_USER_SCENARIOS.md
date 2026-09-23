# UAI-COS v2.0 — USER SCENARIOS (detailed, end-to-end)

> Ye scenarios spec ke flow ko *sach me* chala kar dikhate hain: request → classification → retrieval →
> plan → execution → quality gate → memory update. Har scenario me **real memory IDs** use hue hain jo
> is workspace ke live store (`memory/store/memory.jsonl`) me maujood hain.
>
> Notation: `R#` = scenario ka step, `MEM-*` = live memory record, `[#n]` = spec section.

---

## S1 — Image prompt task (product-only jewellery shot)
**Request:** "Is haar ka product-only catalogue image prompt banao."

| Step | Kya hota hai |
|---|---|
| R1 Classify | domain = image-generation, type = creative prompt, risk = low, output = 2 prompt blocks |
| R2 Retrieve | `MEM-PREF-0003` (photorealism, pro finishing), `MEM-PREF-0004` (**no model/character/hands**), `MEM-PREF-0005` (specific vs universal prompt **alag**) |
| R3 Filter out | `MEM-EPI-0001`, `MEM-ERR-0001` — is task ke liye irrelevant |
| R4 Constraint gate | Prompt me human element add karna **blocked** [`MEM-PREF-0004`] |
| R5 Plan | (a) specific prompt: product, metal/stone details, lighting, lens, background (b) universal quality block: photorealism, detail, finish, resolution, colour accuracy (c) negative prompt |
| R6 Execute | Image generation **nahi** maangi gayi (sirf prompt) → sirf text deliverable [`#33` output engine] |
| R7 Quality gate | Model/hands present? → NO ✓ | Specific/universal mixed? → NO ✓ | Photorealism words present? → YES ✓ |
| R8 Memory update | Naya stable preference nahi mila → **koi record nahi** (jhoothi memory na banao) [`#45`] |
| R9 Output | Roman Hindi me 2 blocks + negative prompt, chat me hi (file ki zaroorat nahi) |

**Wisdom:** `MEM-PREF-0004` medium confidence hai — agar user lifestyle shot maange to `does_not_apply_when` trigger hota hai aur constraint **lagu nahi** hota. Yehi Section 17 ka core hai: scope pehle, keyword baad me.

---

## S2 — Coding / automation task
**Request:** "Email attachment se data nikaal kar Excel banane ka script likho."

| Step | Kya hota hai |
|---|---|
| R1 Classify | domain = coding+data, risk = low (read-only script), output = file + run proof |
| R2 Retrieve | `MEM-PROC-0003` (bada output workspace me file bana kar save karo), `MEM-CORE-0001` (quality bar), `MEM-CONS-0002` (blind memory use nahi) |
| R3 Plan | script → sample data par run → verify output → file save → path do |
| R4 Execute | workspace me `.py` + generated `.xlsx`; `verify before trust` [#11] → script ko actually chala kar output check karo |
| R5 Quality gate | Assumption (attachment format) clearly likhi? → YES (ya clarify maango [`#0.4`]) |
| R6 Memory update | Naya procedural memory candidate: "email→excel pipeline me openpyxl use karo" — `status=candidate`, phir user confirm kare to `verified` [`#99`] |

---

## S3 — Research task with conflicting sources (conflict engine live)
**Request:** "2026 me XYZ ka latest data kya hai?"

| Step | Kya hota hai |
|---|---|
| R1 Classify | domain = research, risk = medium (public claim), output = sourced answer |
| R2 Source check | do sources aapas me takra rahe hain → **conflict** [`#21`] |
| R3 Conflict protocol | detect → classify (data vs interpretation) → investigate (recency + authority) → resolve (jo jeete) → **record** |
| R4 Memory write | Dono records `source` type me; jeetne wale ko `verified` + `last_verified=today`, haarne wale ko `superseded` (delete **nahi**) [`#39`] |
| R5 Output | Answer me recency aur uncertainty clearly likhi: "X source (Sep 2026) kehta hai A; Y source (Mar 2026) kehta hai B — main A maan raha hoon kyunki newer." |
| R6 Gate | Uncertainty chhupai nahi gayi ✓ | Source URL diya ✓ |

---

## S4 — User correction mid-task (correction priority)
**Request (turn 1):** "Report me 5 points daalo." → **(turn 2)** "Nahi, 3 points chahiye the."

| Step | Kya hota hai |
|---|---|
| R1 Detect | correction = explicit user statement [`#44`] |
| R2 Apply | Current task me **turant** 3 points; 5 wala version discard |
| R3 Memory decision | Correction ko permanent rule banane se pehle poocho: "Ye sirf is report ka tha ya future reports ka default?" |
| R4 If durable | `MEM-PREF-000X` candidate → user confirm → `verified`. Purana genuine conflict ho to `supersede` (history rahegi) |
| R5 Anti-pattern | Correction ko chhupa kar purana output repeat karna = **banned** [`#36`, #111`] |

---

## S5 — "Ye yaad rakho" request (memory intake)
**Request:** "Yaad rakhna: mere client ka naam Rajesh hai, GST billing chahiye."

| Step | Kya hota hai |
|---|---|
| R1 Type decide | client info → `project` ya `core`; billing preference → `preference` |
| R2 Schema fill | source=user_instruction, authority=user_explicit, scope={domain: billing, project: <client>}, sensitivity=**private** [`#70`] |
| R3 Status | `candidate` → user ek baar confirm kare → `verified` |
| R4 Reality disclosure | "Ye memory is workspace ki file me persist hui hai (`memory/store/memory.jsonl`) — chat ke bahar chat me automatic nahi jaati." (jhootha "permanent memory" claim **nahi**) [`MEM-CONS-0001`] |
| R5 Audit | `uai_mem.py audit` → privacy check pass (private record shared-tag ke saath nahi) |

---

## S6 — High-risk / irreversible action (approval engine)
**Request:** "Purana data delete kar do" / "Ye post publish kar do" / "Payment kar do"

| Step | Kya hota hai |
|---|---|
| R1 Risk tier | irreversible / external impact → **Tier 3–4** [`#27`, #62`] |
| R2 Kaam rukta hai | Bina confirmation execute **nahi** [`MEM-CONS-0003`, #49`] |
| R3 Confirmation format | "Exactly ye 3 files delete hongi: … Confirm karo? Alternative: archive (reversible)." |
| R4 Safer path pehle | Rollback plan batao [`#62` reversibility], backup/archive option offer karo |
| R5 Execute + verify | Confirmation ke baad action → result verify → audit log entry [`#28`, #67`] |

---

## S7 — Long-running project across turns (project + working memory)
| Step | Kya hota hai |
|---|---|
| R1 Project memory | `MEM-PROJ-0001` (project state) + `MEM-PSTATE-0001` (workflow state) + `MEM-WORK-0001` (aktuell task, `expires_at` 2026-09-30) |
| R2 Naye turn par | INDEX se sirf project + current state load hota hai; purani episodic detail load **nahi** hoti [`#0.5` minimum context] |
| R3 Har milestone | `procedural_state` update (history badhti hai, statement replace) |
| R4 Expiry | Working memory `expire` command se `expired` — uske baad retrieve nahi hoti [`#20`] |
| R5 Handover | "Kal se continue karna hai" → state memory + INDEX padh kar exact point se resume |

---

## S8 — Failure & recovery (live example: is hi task ka 403 error)
| Step | Kya hota hai |
|---|---|
| R1 Fail | `chatgpt.com` share link direct fetch → **HTTP 403 (Cloudflare)** |
| R2 Detect + isolate | Failure record banao, guess mat karo [`#36`, #37`] |
| R3 Fallback | Reader proxy try → 200 OK [`#57` fallback architecture] |
| R4 Error memory | `MEM-ERR-0001`: failure + reason + fix + prevention |
| R5 Root cause | Share link = JS-heavy protected page → static fetch fail. Prevention: pehle proxy, 403 ko "content nahi mila" na maano |
| R6 User ko batana | Output me honestly likha: "direct fetch 403 tha, proxy se liya" — chhupaya nahi [`#1.14`, #35`] |

---

## S9 — "System dikhao" request (audit mode)
**Request:** "Mujhe mind-map / agent architecture / audit dikhao."

| Step | Kya hota hai |
|---|---|
| R1 Mode switch | Normally internal complexity **nahi** dikhate [`MEM-PREF-0007`, #78`], **lekin** user ne explicitly maanga → audit mode ON [V1 PART 15.13] |
| R2 Deliverable | Memory counts (type/status/confidence), audit score, conflicts, expired, agent registry, handoff example |
| R3 Evidence | Files: `memory/INDEX.md`, `logs/AUDIT_LOG.md`, `DASHBOARD.html` — sab actual output, made-up numbers nahi |

---

## Scenario-to-spec traceability (Section #96 form)

| Scenario | Trigger | Agents involved | Memories used | Spec refs |
|---|---|---|---|---|
| S1 image | image/prompt | Creative + Constraint + QC | PREF-0003/0004/0005 | #17, #34, #76 |
| S2 code | script/automation | Code + Debugger + Document | PROC-0003, CONS-0002 | #11, #73 |
| S3 research | latest/source | Research + Source Verifier + Conflict | dynamic | #21, #30, #71 |
| S4 correction | user correction | Supervisor + Learning | dynamic | #44, #45, #36 |
| S5 remember | "yaad rakho" | Memory OS + Privacy | new | #13, #70, #99 |
| S6 high-risk | delete/publish/pay | Permission + Approval + Audit | CONS-0003 | #10, #49, #62 |
| S7 long project | across turns | Project State + Memory OS | PROJ-0001, PSTATE-0001, WORK-0001 | #41, #42, #20 |
| S8 failure | tool error | Failure + RCA + Error memory | ERR-0001 | #36, #37, #57 |
| S9 audit | "dikhao" | Observability + Audit | PREF-0007 | #51, #78, #79 |
