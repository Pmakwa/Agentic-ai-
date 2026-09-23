# UAI-COS v2.0 — EXTERNAL INTEGRATION (spec ko is chat se bahar le jaana)

> Spec khud kehta hai: memory ka faayda tab hai jab real storage **aur** retrieval ho [`V1 reality rule`, #86`].
> Ye file wahi layer deti hai — 3 raste, sab **ready**, sab is workspace me.

---

## Rastha 1 — SYSTEM PROMPT COMPILER (kisi bhi chatbot me paste karo) ✅ ready

```bash
cd /home/user/uai-cos
python3 tools/build_system_prompt.py -m compact     # ~6.3k chars — kisi bhi chat me paste
python3 tools/build_system_prompt.py -m standard    # ~7.5k chars — rules + LIVE MEMORY inline (default)
python3 tools/build_system_prompt.py -m full        # ~50k chars — poora spec + memory
python3 tools/build_system_prompt.py --memory-scope image-generation -o out.md   # domain-specific
```

Output files: `00_SYSTEM/UAI-COS_SYSTEM_PROMPT_{compact,standard,full}.md`

**Ye kyun important hai:** "standard" mode me spec ke core rules **aur** tumhari 26 live memories
inline aa jaati hain — matlab Gemini/Claude/ChatGPT me paste karte hi wo model tumhare rules ke saath
aur tumhari memory jaan kar jawab dega. Memory badlegi to prompt dobara build kar lena (ek command).

**Flow:**
```
memory store (jsonl) ──┐
spec (V2) ─────────────┼──▶ build_system_prompt.py ──▶ prompt file ──▶ kisi bhi LLM me paste
active preferences ────┘
```

---

## Rastha 2 — TELEGRAM BOT (mobile se memory console + LLM bridge) ✅ code ready

```bash
# 1) BotFather se token, phir:
export TELEGRAM_BOT_TOKEN="123456:ABC..."
export ALLOWED_CHAT_IDS="<tumhara chat id>"     # bot /id se batata hai
export LLM_PROVIDER="openai"                     # openai | anthropic | gemini | ollama
export LLM_API_KEY="sk-..."
export LLM_MODEL="gpt-4o-mini"

# 2) chalao (background me bhi chal sakta hai)
python3 tools/interfaces/telegram_bot.py
```

| Command | Kaam | Autonomy |
|---|---|---|
| `/mem <text>` | Memory capture → auto type classification (constraint > preference > error > project > working) | A4 (allowed, audit log) |
| `/list [type]`, `/search <q>` | Retrieval | A4 |
| `/audit` | Memory health score live | A4 |
| `/ask <question>` | UAI-COS system prompt + live memory ke saath LLM jawab | A3 (external API call) |
| `/status`, `/id`, `/dash` | Snapshot | A4 |
| delete/forget | **Bot me nahi hai** — irreversible = human approval [`#49`] | — |

Security (spec ke hisaab se): chat-id whitelist [`#68`], Telegram se aayi memory default `sensitivity=private` [`#70`],
LLM key na ho to bot degrade hota hai (memory console chalta rehta hai) [`#58`], har command audit log me [`#51`].

**Smoke test (aaj chalaya gaya):** `/mem "Hamesha client proposals me GST breakup dikhana hai"` →
`MEM-PREF-0001 (preference, candidate)`. `/mem "Kisi ko bhi mera API key mat bhejo"` → `MEM-CONS-0001 (constraint, candidate)`. ✅

---

## Rastha 3 — FILE / SHELL interface (aaj se chal raha hai) ✅ live

Is chat me jo main kar raha hoon wahi ye hai — `tools/uai_mem.py` CLI + workspace files:

```bash
python3 tools/uai_mem.py list --status active --status verified --wide   # boot read
python3 tools/uai_mem.py search "image"                                  # retrieval
python3 tools/uai_mem.py add --type decision --statement "..." --source user_instruction
python3 tools/uai_mem.py audit --log && python3 tools/uai_mem.py index && python3 tools/uai_mem.py dash
bash tests/test_memory_os.sh                                             # regression
```

Yahi interface Telegram/WhatsApp/API integrations ka **core** hai — koi bhi naya interface sirf iske upar
patli layer hai (single source of truth bana rehta hai).

---

## Aage ke integration options (priority order me)

| # | Integration | Kaam | Effort | Risk |
|---|---|---|---|---|
| 1 | WhatsApp Cloud API | wahi commands, WhatsApp par | medium | Meta business setup |
| 2 | Daily health cron | roz `expire` + `audit` + reminder message | low | very low |
| 3 | Web dashboard (live) | `DASHBOARD.html` ko device par refresh ke saath dekhna | low | very low |
| 4 | Voice interface | speech → `/mem` (voice notes se memory capture) | medium | low |
| 5 | Google Sheets mirror | memory ka human-readable backup sheet | medium | low |
| 6 | n8n / LangGraph orchestration | Phase 4 ke real parallel sub-agents | high | medium |
| 7 | Vector DB retrieval | Phase 2 ka semantic search (embeddings) | high | medium |

---

## Privacy & security checklist (kisi bhi naye interface ke liye)

- [ ] Whitelist / auth laga hai? [`#68`]
- [ ] Secrets env vars me hain (code/chat me nahi)? [`#69`]
- [ ] External bhejne se pehle `sensitivity` check hota hai? [`#70`]
- [ ] Irreversible commands ke liye confirmation flow hai? [`#49`]
- [ ] Interface ki har write action audit log me jaati hai? [`#51`, #61`]
- [ ] Interface fail hone par system degrade ho kar chalta rehta hai? [`#58`]
