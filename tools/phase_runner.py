#!/usr/bin/env python3
"""
phase_runner.py — UAI-COS ka phase engine.

Kya karta hai:
  status   : saare phases ka status table (done / active / next / waiting_user)
  next     : agla actionable phase + exact commands (agent isko utha ke kaam shuru karta hai)
  add      : naya phase add (user jab naya kaam/phase de) -> auto id + phases.json + PHASES.md update
  set      : phase ka status badlo (next -> active -> done)
  --md     : PROJECT_BOARD/PHASES.md ka table regenerate (phases.json se, drift khatam)

Files: PROJECT_BOARD/phases.json (source of truth) · PROJECT_BOARD/PHASES.md (human view)
"""
from __future__ import annotations
import argparse, json, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PJ = ROOT / "PROJECT_BOARD" / "phases.json"
MD = ROOT / "PROJECT_BOARD" / "PHASES.md"
STATUS_ORDER = {"active": 0, "next": 1, "waiting_user": 2, "done": 3}
ICON = {"done": "✅ DONE", "active": "🟢 ACTIVE", "next": "🟡 NEXT", "waiting_user": "⏸ WAITING"}


def load() -> dict:
    return json.loads(PJ.read_text(encoding="utf-8"))


def save(d: dict) -> None:
    d["updated"] = datetime.date.today().isoformat()
    PJ.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_table(d: dict) -> str:
    rows = ["| # | Phase | Status | Owner | Deliverable / Evidence | Next step |",
            "|---|---|---|---|---|---|"]
    for p in d["phases"]:
        rows.append(f"| {p['id']} | **{p['title']}** | {ICON.get(p['status'], p['status'])} | {p.get('owner','agent')} "
                    f"| {p.get('evidence','-')} | {p.get('next_step','-')} |")
    return "\n".join(rows)


def write_md(d: dict) -> str:
    """PHASES.md ke markers ke beech table update karo; markers na ho to file bana do."""
    tbl = render_table(d)
    if MD.exists():
        t = MD.read_text(encoding="utf-8")
        if "<!-- PHASES:START -->" in t and "<!-- PHASES:END -->" in t:
            pre, rest = t.split("<!-- PHASES:START -->", 1)
            _, post = rest.split("<!-- PHASES:END -->", 1)
            MD.write_text(pre + "<!-- PHASES:START -->\n" + tbl + "\n<!-- PHASES:END -->" + post, encoding="utf-8")
        else:
            MD.write_text("<!-- AUTO-GENERATED TABLE (phase_runner.py) -->\n\n"
                          "<!-- PHASES:START -->\n" + tbl + "\n<!-- PHASES:END -->\n\n" + t, encoding="utf-8")
    else:
        MD.write_text("# PHASES\n\n<!-- PHASES:START -->\n" + tbl + "\n<!-- PHASES:END -->\n", encoding="utf-8")
    return tbl


def cmd_status(a) -> int:
    d = load()
    ph = sorted(d["phases"], key=lambda p: (STATUS_ORDER.get(p["status"], 9), p["id"]))
    print(json.dumps({"updated": d.get("updated"), "phases": ph}, indent=2, ensure_ascii=False) if a.json else render_table(d))
    if not a.json:
        c = {}
        for p in d["phases"]:
            c[p["status"]] = c.get(p["status"], 0) + 1
        print("\nTOTAL:", len(d["phases"]), "|", " · ".join(f"{k}: {v}" for k, v in sorted(c.items())))
    return 0


def cmd_next(a) -> int:
    d = load()
    cand = [p for p in d["phases"] if p["status"] in ("active", "next")]
    if not cand:
        print("Koi pending phase nahi. Naya kaam = naya phase: python3 tools/phase_runner.py add --id P21 --title \"...\"")
        return 0
    cand.sort(key=lambda p: STATUS_ORDER[p["status"]])
    for p in cand[: a.count]:
        print(f"\n=== {p['id']} — {p['title']}  [{p['status']}]")
        print(f"    evidence : {p.get('evidence','-')}")
        print(f"    next step: {p.get('next_step','-')}")
    print("\nRule: kaam shuru karne se pehle BOOT karo (python3 tools/agent_boot.py) · kaam ke baad push karo (tools/sync_to_github.sh)")
    return 0


def cmd_add(a) -> int:
    d = load()
    pid = a.id
    if not pid:
        nums = [int(p["id"][1:]) for p in d["phases"] if p["id"][1:].isdigit()]
        pid = f"P{max(nums)+1}"
    if any(p["id"] == pid for p in d["phases"]):
        print(f"ERROR: {pid} pehle se hai."); return 1
    entry = {"id": pid, "title": a.title, "status": a.status, "owner": a.owner,
             "evidence": a.evidence or "-", "next_step": a.next_step or "kaam shuru karo + evidence add karo"}
    d["phases"].append(entry)
    save(d); tbl = write_md(d)
    print(f"[OK] phase {pid} add hua: {a.title}")
    print("PHASES.md table updated. Ab: boot -> kaam -> evidence -> CAPABILITY_MAP bump -> memory -> sync_to_github.sh")
    return 0


def cmd_set(a) -> int:
    d = load()
    for p in d["phases"]:
        if p["id"] == a.id:
            p["status"] = a.status
            if a.evidence: p["evidence"] = a.evidence
            if a.next_step is not None: p["next_step"] = a.next_step
            save(d); write_md(d)
            print(f"[OK] {a.id} -> {a.status}")
            return 0
    print(f"ERROR: {a.id} nahi mila."); return 1


def cmd_md(a) -> int:
    write_md(load()); print("[OK] PROJECT_BOARD/PHASES.md regenerate ho gaya"); return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="phase_runner.py", description="UAI-COS phase engine")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status"); s.add_argument("--json", action="store_true"); s.set_defaults(f=cmd_status)
    n = sub.add_parser("next"); n.add_argument("-n", "--count", type=int, default=3); n.set_defaults(f=cmd_next)
    ad = sub.add_parser("add"); ad.add_argument("--id"); ad.add_argument("--title", required=True)
    ad.add_argument("--status", default="next", choices=["next", "active", "done", "waiting_user"])
    ad.add_argument("--owner", default="agent"); ad.add_argument("--evidence"); ad.add_argument("--next-step")
    ad.set_defaults(f=cmd_add)
    st = sub.add_parser("set"); st.add_argument("--id", required=True)
    st.add_argument("--status", required=True, choices=["next", "active", "done", "waiting_user"])
    st.add_argument("--evidence"); st.add_argument("--next-step"); st.set_defaults(f=cmd_set)
    m = sub.add_parser("md"); m.set_defaults(f=cmd_md)
    a = ap.parse_args()
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
