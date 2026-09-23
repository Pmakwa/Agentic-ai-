# START HERE 👋 (insaan ke liye — 2 minute me samajh lo)

## Ye repo kya hai?

Ye tumhara **UAI-COS v2.0** hai — ek personal AI operating system jo ek AI agent ke saath milkar bana hai.
Isme sab kuch hai jo hamari pooori baat-cheet me bana:

1. **System ka dimaag** — V1 + V2.0 spec (112 sections), operational protocol, system prompts
2. **Memory** — 71 live records (file-backed, verifiable, export hoti hai)
3. **Capability audit** — kya ho sakta hai, kya nahi, kis evidence ke saath (`CAPABILITY_MAP.json` v2.4)
4. **Access routes** — verified cheezein: social platforms, GitHub, research APIs, local AI, RSSHub
5. **Tools** — 8+ chalne wale scripts (memory engine, access routes, social unlock, GitHub unlock, local AI, monitor)
6. **Poora A-to-Z conversation log** — kaunsi baat kab hui, kya kiya, kaise kiya, kahan se kiya, kya result aaya
7. **Evidence** — har claim ke peeche raw log files (`probes/` folders me)

---

## Kisi bhi agent ke saath GitHub connect karke kya karna hai?

### Option 1 — Sabse aasan (recommended)
Agent ko ye ek line bolo:

> **"Is repo ko padho — `AGENTS.md` se shuru karo, phir `CONVERSATION/00_A_TO_Z_LOG.md` padho, boot-check chalao aur wahin se aage kaam continue karo."**

Bas. Agent khud: AGENTS.md padhega → spec + protocol + memory INDEX padhega → health check chalayega
(provenance 4/4, audit 100/100, tests 28/28, routes status) → phir `AGENTS.md` §5 me likhe **open threads**
se agla kaam khud utha ke karne lagega.

### Option 2 — Bina kuch bole
Bahut se agent platforms (Codex, Cursor, Claude Code, Windsurf, Devin-type) repo khulte hi **`AGENTS.md` / `README.md` khud padhte hain**.
Us case me bina kuch bole bhi agent start kar sakta hai — par ek line dena safest hai.

### Option 2.5 — Kya agent ko kuch batana padega? (seedha jawab)
| Cheez | Zaroori hai? | Kyun |
|---|---|---|
| Repo ka access | **Haan** | Agent ko code+docs padhne milenge |
| Ek line ka kickoff | **Recommended** | Warna agent sochega "kya karna hai?" — par AGENTS.md padhne ke baad ye bhi cover ho jata hai |
| Chalane ke liye environment | **Haan** | Agent ko ek sandbox/terminal chahiye (internet + python) — warna wo sirf padh sakta hai, chala nahi sakta |
| Credentials (API keys, tokens) | **Sirf advanced kaam ke liye** | 90% verified kaam bina kisi key ke chalta hai; bina token sirf GitHub **push** nahi ho sakta |
| Model/budget | Haan | Agent ke andar jo model use hoga |

### Option 3 — Zero-setup continuation
Agar tum bina setup ke continuation chahte ho: `PROMPTS` folder me compiled system prompt hai
(`00_SYSTEM/UAI-COS_SYSTEM_PROMPT_standard.md`) — usko kisi bhi chat me paste kar do, memory + protocol
inline aa jayega, aur wo agent wahi se kaam continue kar sakta hai.

---

## Pehli baar chalu karne ka exact tareeka (agent ke liye commands)

```bash
git clone <this-repo> && cd uai-cos
python3 tools/verify_provenance.py          # 4/4 PASS hona chahiye
python3 tools/uai_mem.py audit | tail -3    # 100/100
bash tests/test_memory_os.sh | tail -3      # 28 passed, 0 failed
python3 tools/social_unlock.py status       # verified routes ka live status
```
Agar env naya hai (fresh sandbox) to pehle:
```bash
bash tools/bootstrap_environment.sh         # packages, fonts, browser, model cache, PATH
```
RSSHub (social feeds ke liye) chahiye to: `RUNBOOK.md` §3 — 3 commands me live ho jata hai
(Node 22 + swap zaroori hai — reason bhi likha hai).

---

## Is repo me kya-kya folder hai?

| Folder | Andar kya |
|---|---|
| `00_SYSTEM/` | Canonical spec (never edit), protocol, system prompts, provenance hashes |
| `01_STEP2/` | Roadmap, scenarios, memory types, evaluation, external integration |
| `02_CAPABILITY_AUDIT/` | Capability map (v2.4), self-sweeps, evidence, probes |
| `03_ACCESS_EXPANSION/` | Blocked targets ke legitimate routes + blocker register + playbook |
| `04_GITHUB_UNLOCK/` | GitHub capability report (bina token kya-kya hota hai) |
| `05_SOCIAL_UNLOCK/` | Social platform unlock report (verified matrix) |
| `06_REPO_HUNT/` | **Latest:** 15 GitHub repos install + live-test → 7 naye platforms khule |
| `CONVERSATION/` | **Poora A-to-Z:** baat-cheet, action ledger, Q&A, decisions |
| `memory/` | Live memory (71 records) + INDEX + archive |
| `tools/` | Sab chalne wale scripts (social_unlock, uai_mem, access_routes, github_unlock, local_ai, monitor) |
| `agents/` | 40+ logical agent registry + handoff protocol |
| `tests/`, `logs/` | Regression suite (28 tests) + audit log + route health |

---

## Ek zaroori baat (security)

- Is repo me **koi password/token/API key nahi hai** (verified scan).
- Agar tum API keys daalna chaho (Discord bot, YouTube key, Reddit OAuth) — `.env` file banake `.gitignore`
  me daal do, warna GitHub par public ho jayengi.
- Login-wall / CAPTCHA / paywall todne wale kaam is system me **allowed nahi** hain (spec §24) — agent
  ko ye rule sikhaya gaya hai, wo khud enforce karega.
