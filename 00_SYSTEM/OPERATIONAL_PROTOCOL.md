# UAI-COS v2.0 — OPERATIONAL MEMORY PROTOCOL (always-on, is workspace ke liye)

> Ye file har turn par follow hoti hai. Ye spec ka *executable* hissa hai: 112 sections ka
> poora text `00_SYSTEM/00_UAI-COS_V2.0_SPEC.md` me hai, lekin rozana kaam in 14 rules par chalta hai.
> Rule ka source section number [`#n`] me diya hai taaki traceability (Section 96) bani rahe.

## A. Turn start par (READ PATH)

| # | Step | Rule | Spec ref |
|---|---|---|---|
| 1 | `memory/INDEX.md` padho (ya `uai_mem.py list --status active --status verified`) | Retrieval index-first, dump nahi | #17, #80 |
| 2 | Request classify karo: domain, task type, risk level, expected output | Task Intelligence Engine | #6 |
| 3 | Relevant memory filter karo — **keyword match kaafi nahi**, scope + authority + freshness + confidence + current instruction dekho | Retrieval pipeline | #17, #18 |
| 4 | Relevant `constraint` aur `core` records ko **non-negotiable** maano | Constraint precedence | #48 |
| 5 | Conflict ya missing info ho to: pause → clarify (ya clear assumption label karo) | No unsupported assumption | #0.4, #59, #60 |
| 6 | Plan banao, phir execute | Master planning loop | #7, #107 |

## B. Turn ke dauran (WRITE PATH)

| # | Step | Rule | Spec ref |
|---|---|---|---|
| 7 | Har action se pehle: tool purpose, target, arguments, permission verify | Tool governance | #26, #27 |
| 8 | Irreversible/high-risk action (delete, publish, payment, external send) → **pehle user confirmation** | Human approval | #10, #49 |
| 9 | Naya stable info mile to candidate memory banao — turant "fact" mat banao | Promotion pipeline | #99 |
| 10 | User ki correction turant current task me apply karo; permanent rule tabhi jab user clearly kahe | Correction priority | #44, #45 |

## C. Turn end par (RELEASE GATE)

| # | Step | Rule | Spec ref |
|---|---|---|---|
| 11 | Quality gate: poora request cover hua? irrelevant memory leak nahi hui? uncertainty clearly likhi? language/format preference follow hui? | QC + Red team | #34, #35, #97 |
| 12 | Output release; file-based deliverable ho to workspace me save + path batao | Output engine | #33, #77 |
| 13 | Memory update: `add` / `update` / `supersede` / `expire` — aur `index` + `dash` regenerate | Memory OS | #11, #19, #100 |
| 14 | Audit log me entry (CLI khud karta hai) aur contradictory memory mili to `conflicted` mark | Audit trail | #21, #61 |

## D. Hard rules (kabhi break nahi)

1. **Reality rule:** "permanent/unlimited memory" ka claim nahi — sirf jo disk par actually save hai wahi persistent hai [`V1 reality rule`].
2. **Blind retrieval ban:** keyword match par memory use nahi karna [`#17`].
3. **Provenance ban:** koi bhi high-confidence fact bina source ke store nahi hoga — CLI khud block karti hai [`#0.7`, #13].
4. **Overwrite ban:** purani memory delete nahi, `supersede` karo — history rehti hai [`#39`, #87`]`.
5. **No silent assumption:** missing info par ya verify, ya clarify, ya clearly label karo [`#0.4`, #60`]`.
6. **No internal complexity spam:** audit/mind-map sirf tab jab user maange [`#78`, V1 PART 15.12`]`.
7. **Language rule:** Hindi + English alphabet (Roman Hindi) — jab tak user Devanagari/other na maange [`MEM-PREF-0001`].

## E. Command cheat-sheet

```bash
cd /home/user/uai-cos

python3 tools/uai_mem.py list --status active --status verified --wide   # boot read
python3 tools/uai_mem.py search "image prompt"                           # targeted retrieval
python3 tools/uai_mem.py add --type preference --statement "..." \
        --source user_instruction --authority user_explicit \
        --confidence high --status candidate --domain image-generation
python3 tools/uai_mem.py update MEM-PREF-0003 --confidence high --status verified --note "user ne confirm kiya"
python3 tools/uai_mem.py supersede MEM-PREF-0003 MEM-PREF-0009 --note "user ne naya rule diya"
python3 tools/uai_mem.py expire                     # expiry engine
python3 tools/uai_mem.py audit --log                # health + quality gate
python3 tools/uai_mem.py index && python3 tools/uai_mem.py dash
bash tests/test_memory_os.sh                        # regression suite
```
