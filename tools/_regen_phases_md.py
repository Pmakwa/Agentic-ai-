#!/usr/bin/env python3
"""PHASES.md ko phases.json se clean regenerate karta hai (header + auto table + notes)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "PROJECT_BOARD" / "phases.json").read_text(encoding="utf-8"))
ICON = {"done": "✅ DONE", "active": "🟢 ACTIVE", "next": "🟡 NEXT", "waiting_user": "⏸ WAITING"}

rows = ["| # | Phase | Status | Owner | Deliverable / Evidence | Next step |", "|---|---|---|---|---|---|"]
for p in d["phases"]:
    rows.append(f"| {p['id']} | **{p['title']}** | {ICON[p['status']]} | {p.get('owner','agent')} "
                f"| {p.get('evidence','-')} | {p.get('next_step','-')} |")
table = "\n".join(rows)
checklist = "\n".join(f"{i+1}. {x}" for i, x in enumerate(d["recurring_checklist"]))

doc = f"""# PHASES — UAI-COS ka phase tracker

> **Source of truth:** `PROJECT_BOARD/phases.json` · **Engine:** `tools/phase_runner.py`
> (`status` · `next` · `add` · `set` · `md`). Neeche ka table auto-generated hai — haath se edit mat karo,
> sirf `python3 tools/phase_runner.py md` chalao.

<!-- PHASES:START -->
{table}
<!-- PHASES:END -->

**Total:** {len(d['phases'])} phases · **Updated:** {d.get('updated')}

## Recurring checklist (har naye kaam par — "definition of done")

{checklist}

## Naya phase kaise add hota hai

1. **User naya prompt/spec de** → `python3 tools/import_prompt.py --url/--file/--text ... --name "V3"`
   → file `00_SYSTEM/` me save + memory record + phase auto-add (status=next) → phir usko apply karo.
2. **User naya kaam bole** → `python3 tools/phase_runner.py add --title "..." --status next`
   → `python3 tools/phase_runner.py set --id P2x --status active` → kaam karo → `set --status done`.

## Environment me "applied" ka matlab (kya live hai + check kaise karein)

| Cheez | Live? | Check |
|---|---|---|
| Memory OS (73 records) | ✅ | `python3 tools/uai_mem.py audit` |
| Capability map v2.4 (20 evidence) | ✅ | `python3 tools/agent_boot.py --json` |
| Boot system (P12) | ✅ | `python3 tools/agent_boot.py --json` |
| Phase engine + prompt intake (P19/P20) | ✅ | `python3 tools/phase_runner.py next` |
| Social routes (P10) | ⚠️ instance-dependent | `python3 tools/social_unlock.py status` |
| RSSHub `:1200` | ⚠️ sandbox restart par band | `RUNBOOK.md` §3 |
| Control-center `:8000` | ⚠️ same | `RUNBOOK.md` §9 |
| systemd monitor (30 min) | ⚠️ timer dependency | `systemctl status uai-cos-monitor.timer` |
"""

(ROOT / "PROJECT_BOARD" / "PHASES.md").write_text(doc, encoding="utf-8")
print("PHASES.md rewritten:", len(doc), "chars, phases:", len(d["phases"]))
