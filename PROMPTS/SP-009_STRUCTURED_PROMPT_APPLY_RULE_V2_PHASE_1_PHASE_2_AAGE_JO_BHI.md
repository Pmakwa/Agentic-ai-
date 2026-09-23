# SP-009 — Structured-prompt apply rule (V2 / Phase-1 / Phase-2 / aage jo bhi)

<!-- structured prompt entry | type: rules | verbatim: true | source: user instruction 2026-09-23: 'jo jo structured prompt dunga (V2, Phase 1, Phase 2...) wo sab apply karna chahiye' | body_sha256_16: 42eccd5c4aec6052 | added: 2026-09-23 -->
| field | value |
|---|---|
| Type | `rules` |
| Source | user instruction 2026-09-23: 'jo jo structured prompt dunga (V2, Phase 1, Phase 2...) wo sab apply karna chahiye' |
| Verbatim user text? | haan |
| Applied in | PROMPTS/registry.json, PROMPTS/REGISTRY.md, AGENTS.md §13, PHASE_PROTOCOL.md §8, tests/ci_extra.py |

---

# Structured prompts — apply rule

User ke **saare structured prompts** (V1, V2, Phase 1, Phase 2, Phase 3, aur aage jo bhi aayega) repo me register honge aur **environment me apply** honge.

1. Entry banao: `python3 tools/prompt_registry.py add --file/--text --title ... --type phase|spec|rules`
2. Apply karo, phir likho kahan apply hua: `prompt_registry.py apply --id SP-xxx --where 'AGENTS.md §9, <script>'`
3. Boot payload me lao: `python3 tools/agent_boot.py --write` (taaki har naya agent ye rules padhe)
4. Verify: `python3 tools/prompt_registry.py verify` (hash + applied) — CI bhi ye chalata hai.
5. Jo prompt sirf conversation me tha (verbatim repo me nahi) — entry me `verbatim: recon` likho aur user se
   verbatim maang kar update karo.

**Rule: koi structured prompt bina apply + bina REGISTRY entry ke nahi chhodna.**
