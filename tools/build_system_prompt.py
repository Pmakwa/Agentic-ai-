#!/usr/bin/env python3
"""
build_system_prompt.py — UAI-COS v2.0 ka compact, paste-anywhere System Prompt compiler.

Problem: poora V2 spec ~44k chars hai — kuch environments me mehnga/lamba hai.
Solution: spec + live memory se ek **operational** prompt banao jo:
  - core 12 principles + supervisor loop + hard rules rakhe
  - active/verified memory ko INLINE kar de (taaki model ko memory pata ho)
  - baaki spec ko "on-demand reference" bana de (bina token kharch)

Modes:
  --mode compact   (~2-3k chars)  chat platforms, quick paste
  --mode standard  (~8-12k chars) full rules + memory inline  (default)
  --mode full      (~50k chars)   spec + memory poora (~paste only where supported)

Usage:
  python3 tools/build_system_prompt.py                  # standard, stdout
  python3 tools/build_system_prompt.py -m compact -o out.md
  python3 tools/build_system_prompt.py --with-spec      # spec text bhi inline
  python3 tools/build_system_prompt.py --memory-scope image-generation   # sirf ek domain ki memory
"""

from __future__ import annotations
import argparse
import os
import re
import sys
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec_path = os.path.join(ROOT, "00_SYSTEM", "00_UAI-COS_V2.0_SPEC.md")
store_path = os.path.join(ROOT, "memory", "store", "memory.jsonl")

sys.path.insert(0, os.path.join(ROOT, "tools"))
try:
    from uai_mem import load  # reuse loader (single source of truth)
except Exception:  # pragma: no cover
    def load(path=store_path):
        import json
        out = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out

COMPACT = """## SYSTEM: UAI-COS v2.0 (Universal AI Cognitive Operating System)

LANGUAGE: User se Hindi bolo, English alphabet/spelling (Roman Hindi) me — jab tak user Devanagari ya doosri script na maange.
TONE: Detailed, master-level, practical. Generic/basic answer nahi.

GOVERNANCE (12 absolute principles):
1) User intent pehle — keyword matching kaafi nahi.
2) Current explicit instruction > purani preference/memory.
3) Memory = evidence, automatic truth nahi (source, date, scope, confidence dekho).
4) Bina support assumption nahi: Know → Verify → Ask → Clearly Assume.
5) Minimum necessary context — poora memory dump nahi.
6) Least privilege — sirf jitni permission chahiye.
7) Provenance hamesha — important info ka origin traceable.
8) Temporal awareness — kab valid thi / kab expire hui.
9) Conflict = signal — detect → classify → resolve → record (chhupao nahi).
10) Reversibility — high-risk/irreversible action se pehle approval.
11) Verify before trust — kisi output ko andhadhundh truth na maano.
12) Continuous learning, blind learning nahi — permanent rule tabhi jab user clearly kahe.

SUPERVISOR LOOP: UNDERSTAND → CLASSIFY → RETRIEVE → FILTER → PLAN → ASSIGN → VERIFY → EXECUTE → AUDIT → CORRECT → APPROVE → RESPOND → LEARN

HARD RULES:
- "Permanent/unlimited memory" ka jhootha claim nahi — jo actually save hai wahi persistent hai.
- Memory ko keyword match par use nahi karna; scope + authority + freshness + confidence dekho.
- Missing info par guess nahi — verify, clarify, ya clearly labeled assumption.
- Delete/publish/payment/external-send = pehle confirmation.
- Internal agent/audit complexity user ko tabhi dikhao jab user maange.
"""

STANDARD_EXTRA = """
## MEMORY TYPES (15) aur unka behaviour
core, preference, constraint, semantic, episodic, procedural, working, project, decision,
error, source, shared, temporal, relational, procedural_state

LIFECYCLE: candidate → unverified → verified → active  |  side states: uncertain, conflicted,
expired, superseded, archived, deleted, quarantined. Delete nahi — supersede karo.

CONFIDENCE BANDS: very_high, high, medium, low, very_low  (false precision avoid karo)
AUTHORITY ORDER: user_explicit > user_correction > verified_source > user_implied > derived > agent_inference

RETRIEVAL PIPELINE (order matters):
scope filter → constraint lock (veto) → authority sort → freshness check → confidence gate →
conflict check → current-instruction overlap → top-k (minimum necessary)

TOOL RISK: T0 read → A4 free | T1 local write → A4 free | T2 external read → A4 free |
T3 external write → USER APPROVAL | T4 destructive/financial/legal → APPROVAL + rollback plan
STOP CONDITIONS: request badal gaya → re-plan | 3 baar same step fail → user ko batao |
conflict resolve na ho → dono versions disclose karo | permission missing → ruk jao
"""


def read_spec() -> str:
    try:
        with open(spec_path, encoding="utf-8") as f:
            txt = f.read()
        # html comment header hata do (build metadata, prompt me nahi chahiye)
        return re.sub(r"<!--.*?-->", "", txt, flags=re.S).strip()
    except FileNotFoundError:
        return "[spec file missing]"


def memory_lines(scope: str | None, include_status=("active", "verified", "conflicted")) -> str:
    rows = [r for r in load() if r["status"] in include_status]
    if scope:
        rows = [r for r in rows
                if scope in ((r.get("scope") or {}).get("domains") or [])
                or scope in (r.get("tags") or [])
                or scope in r["statement"].lower()
                or not (r.get("scope") or {}).get("domains")]  # global rules always included
    order = ["core", "constraint", "preference", "procedural", "project", "decision",
             "semantic", "episodic", "error", "source", "temporal", "relational",
             "procedural_state", "working", "shared"]
    rows.sort(key=lambda r: (order.index(r["type"]) if r["type"] in order else 99, r["id"]))
    out = []
    for r in rows:
        mark = {"verified": "V", "active": "A", "conflicted": "!"}.get(r["status"], "?")
        apply_txt = f" | applies: {r['applies_when']}" if r.get("applies_when") else ""
        skip_txt = f" | NOT for: {r['does_not_apply_when']}" if r.get("does_not_apply_when") else ""
        out.append(f"- [{r['id']}·{mark}] {r['statement']}{apply_txt}{skip_txt}")
    return "\n".join(out)


def build(mode: str, scope: str | None, with_spec: bool) -> str:
    parts = [COMPACT]
    if mode in ("standard", "full"):
        parts.append(STANDARD_EXTRA)
    if mode == "full":
        parts.append("\n## FULL SPEC (reference)\n\n" + read_spec())
    if with_spec and mode != "full":
        parts.append("\n## SPEC REFERENCE (reference section, on-demand)\n\n" + read_spec()[:12000] + "\n\n[...spec truncated — full file: 00_SYSTEM/00_UAI-COS_V2.0_SPEC.md]")
    mem = memory_lines(scope)
    if mem:
        parts.append("\n## LIVE MEMORY (is workspace ke memory store se inject hui)\n"
                     "Mark: V = verified, A = active, ! = conflicted (conflict resolve hone tak use na karo)\n\n" + mem)
        parts.append("\n## MEMORY WRITE PROTOCOL\n"
                     "Naya stable info mile to candidate memory banao; user confirm kare to verified. "
                     "Purani memory supersede karo, delete nahi. Har record me source + scope + confidence + authority zaroori.\n"
                     f"CLI: python3 tools/uai_mem.py (root: {ROOT})")
    return "\n".join(parts).strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="UAI-COS system prompt compiler")
    ap.add_argument("-m", "--mode", choices=["compact", "standard", "full"], default="standard")
    ap.add_argument("--memory-scope", default=None, help="sirf is domain/tag ki memory inline karo")
    ap.add_argument("--with-spec", action="store_true", help="spec ka trimmed reference bhi jodo")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()

    prompt = build(a.mode, a.memory_scope, a.with_spec)
    target = a.out or os.path.join(ROOT, "00_SYSTEM", f"UAI-COS_SYSTEM_PROMPT_{a.mode}.md")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"[OK] {target}  ({len(prompt):,} chars, mode={a.mode}"
          f"{', scope=' + a.memory_scope if a.memory_scope else ''})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
