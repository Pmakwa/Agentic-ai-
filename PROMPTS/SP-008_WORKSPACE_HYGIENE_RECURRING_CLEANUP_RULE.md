# SP-008 — Workspace hygiene + recurring cleanup rule

<!-- structured prompt entry | type: rules | verbatim: true | source: user instruction 2026-09-23: 'faltu/bekar/duplicate cheezein delete karo, time to time karte rehna' | body_sha256_16: 4ef4f0d96b4b55ae | added: 2026-09-23 -->
| field | value |
|---|---|
| Type | `rules` |
| Source | user instruction 2026-09-23: 'faltu/bekar/duplicate cheezein delete karo, time to time karte rehna' |
| Verbatim user text? | haan |
| Applied in | AGENTS.md §12, PHASE_PROTOCOL.md §7, PROJECT_BOARD/phases.json (recurring_checklist), tools/cleanup_workspace.py |

---

# Workspace hygiene (recurring)

1. Naya prompt/phase aaye -> registry me entry (`prompt_registry.py add ...`) + apply + boot regenerate.
2. Har kaam ke baad: evidence rakho, kachra delete karo.
3. **Time-to-time cleanup:** `python3 tools/cleanup_workspace.py` (report) -> `--apply` (safe junk delete).
   Cadence: har 3-5 turn ya jab workspace > 1.2 GB, phir bhi har push se pehle ek report.
4. Duplicates: exact-duplicate files ko rakho ek copy me; obsolete files (superseded scripts/docs) delete karo
   aur REASON `logs/cleanup_*.md` me likho.
5. Heavy deps (node_modules, RSSHub) workspace ke andar nahi — `/opt/uai-cache/` me rakho.
