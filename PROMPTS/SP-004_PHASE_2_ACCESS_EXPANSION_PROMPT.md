# SP-004 — Phase 2 — access expansion prompt

<!-- structured prompt entry | type: phase | verbatim: false | source: user structured prompt (conversation) — verbatim text repo me nahi tha | body_sha256_16: 13fc6c18b904ffe3 | added: 2026-09-23 -->
| field | value |
|---|---|
| Type | `phase` |
| Source | user structured prompt (conversation) — verbatim text repo me nahi tha |
| Verbatim user text? | nahi (reconstructed) |
| Applied in | 03_ACCESS_EXPANSION/, tools/access_routes.py, CONVERSATION/01_ACTION_LEDGER.md §D |

---

# Phase 2 (reconstructed)

User ka doosra structured phase prompt: jo targets blocked the, unke **legitimate routes** dhoondo
(jina reader, Wayback, public APIs) — bypass nahi, sirf legal/open raste.

**Kya apply hua:**
- 12 blocked targets me se 9 ke routes khule -> `03_ACCESS_EXPANSION/` (6 deliverables)
- `tools/access_routes.py` (demo|fetch|rss|so|paper|nse|wb), route_provenance.jsonl
- Boundary saaf likhi: auth/paywall/CAPTCHA bypass = NAHI (spec §24)

**Note:** verbatim text repo me nahi; user de de to yahi entry update ho jayegi.
