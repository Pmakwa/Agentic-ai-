# SP-003 — Phase 1 — capability baseline + audit prompt

<!-- structured prompt entry | type: phase | verbatim: false | source: user structured prompt (conversation) — verbatim text repo me nahi tha | body_sha256_16: 688ae5921d0637fd | added: 2026-09-23 -->
| field | value |
|---|---|
| Type | `phase` |
| Source | user structured prompt (conversation) — verbatim text repo me nahi tha |
| Verbatim user text? | nahi (reconstructed) |
| Applied in | 02_CAPABILITY_AUDIT/, ENVIRONMENT.md, AGENTS.md §4 |

---

# Phase 1 (reconstructed)

User ka pehla structured phase prompt: system ko *imandaari se* samjho — kya kya capability hai, kya nahi.

**Kya apply hua:**
- 29-site capability matrix + secrets scan -> `02_CAPABILITY_AUDIT/CAPABILITY_MAP.json` (v1.x)
- Evidence-only claiming (No-False-Access), status labels (VERIFIED/POSSIBLE/BLOCKED…)
- Environment reality doc -> `ENVIRONMENT.md`

**Note:** verbatim user text repo me nahi mila (share-link extraction me sirf assistant text tha). Jab user verbatim de de -> `python3 tools/prompt_registry.py add --file <file> --title 'Phase 1 (verbatim)' --eid` se replace karo.
