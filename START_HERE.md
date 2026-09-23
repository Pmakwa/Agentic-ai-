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

## 🔴 SABSE PEHLE — agent ko "boot" karana zaroori hai (ye hi asli problem hai)

Agent ke paas do cheezein alag hoti hain: **files padhna** (knowledge) aur **system me boot hona** (behaviour).
Sirf files padhne se agent normal assistant ki tarah jawab de deta hai — Hindi rule, boundary rule, evidence rule,
"kaam beech me nahi rokna" — kuch apply nahi hota. Isliye **boot karna zaroori hai**:

### Tareeka A — Terminal/Repo access wale agent ke liye (best)
Agent ko bas ye bolo:
> **"`python3 tools/agent_boot.py` chalao — wo poora UAI-COS system boot payload dega. Phir health check chalao
> (`verify_provenance.py`, `uai_mem.py audit`, `tests/test_memory_os.sh`) aur BOOT ATTESTATION bhar ke dikhao.
> Uske baad `AGENTS.md` §5 se agla kaam continue karo."**

`agent_boot.py` ek hi output me de deta hai: identity + rules + spec map (42k chars ka index, hash ke saath) +
14-rule protocol + memory snapshot (71 records) + capability truth (kya verified, kya blocked) + current status +
open threads + attestation template. Agent ko alag-alag 10 files padhne ki zaroorat nahi.

### Tareeka B — Sirf chat wale agent ke liye (ChatGPT/Claude/Gemini web)
`UAI-COS_BOOT_PROMPT.md` file ka **poora content** agent ko pehle message me paste karo (14 KB), saath me ye line:
> **"Tum ab UAI-COS v2.0 ho. System padho, BOOT ATTESTATION bharo, uske baad hi kaam karo."**

*(Paste-ready template `tests/boot_attestation.md` ke end me bhi hai.)*

### Boot hua ya nahi — CHECK kaise karo
`tests/boot_attestation.md` me **12 sawaal + scoring** hai. Agent se wo sawaal poocho:
- **10–12 sahi** → ✅ boot ho gaya, kaam karwao
- **6–9 sahi** → ⚠️ partial — `agent_boot.py` chala ke dobara bolo
- **0–5 sahi** → ❌ boot nahi hua — `UAI-COS_BOOT_PROMPT.md` paste karo

### Boot ke baad agent khud kya karega
Health check (provenance 4/4, audit 100/100, tests 28/28) → `AGENTS.md` §5 ke open threads se agla kaam
uthayega → aur har naya finding evidence + capability map + memory me daalega.

---

## Baaki (boot ke baad ke options)

### Option 1 — Sabse aasan
Agent ko ye line bolo: **"`AGENTS.md` se shuru karo, phir `CONVERSATION/00_A_TO_Z_LOG.md` padho aur aage kaam continue karo."**

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
