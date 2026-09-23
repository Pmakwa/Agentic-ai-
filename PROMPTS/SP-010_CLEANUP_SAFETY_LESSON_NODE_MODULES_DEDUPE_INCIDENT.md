# SP-010 — Cleanup safety lesson (node_modules dedupe incident)

<!-- structured prompt entry | type: rules | verbatim: false | source: agent incident 2026-09-23 + user instruction 'time to time cleanup karte rehna' | body_sha256_16: dd670d171c8892ec | added: 2026-09-23 -->
| field | value |
|---|---|
| Type | `rules` |
| Source | agent incident 2026-09-23 + user instruction 'time to time cleanup karte rehna' |
| Verbatim user text? | nahi (reconstructed) |
| Applied in | tools/cleanup_workspace.py (PROTECTED/HEAVY_SKIP/DELETE_CAP), AGENTS.md §12, PHASE_PROTOCOL.md §7, tests/ci_extra.py |

---

# Cleanup safety (2026-09-23 ka incident)

Pehle cleanup run ne node_modules + `lib/` ke andar 'duplicates' delete kar diye (7959 files) → RSSHub toot gaya. Recovery: fresh clone + `pnpm install` + build → `/opt/uai-cache/rsshub`.

**Isliye permanent rules:**
1. HEAVY dirs (`node_modules`, `.pnpm`, `dist`, `build`, `.venv`, `lib` of vendored deps) никогда scan/delete nahi — protected.
2. Duplicate delete sirf `--dedupe` flag se (default `--apply` me nahi).
3. 500+ deletions ke liye `--force`, warna tool khud ruk jata hai.
4. Delete se pehle `--check`/report padho; reason `logs/cleanup_*.md` me likho.
5. Heavy deps workspace me hi nahi rakhte — `/opt/uai-cache/`.
