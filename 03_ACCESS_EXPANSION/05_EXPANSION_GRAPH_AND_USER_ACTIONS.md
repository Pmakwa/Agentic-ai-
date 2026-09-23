# CAPABILITY EXPANSION GRAPH + USER-ACTION SHORTLIST (§29, §30)

> "Ek nayi capability kitni aur capabilities unlock karti hai?" — yahi sawal is file ka core hai.

---

## 1. EXPANSION GRAPH (target → resources → routes → dependencies → result)

```
                          ┌─────────────────────────────┐
                          │  TARGET: full research ops  │
                          └──────────────┬──────────────┘
        ┌───────────────────────────────┼────────────────────────────────┐
        ▼                               ▼                                ▼
┌───────────────┐              ┌────────────────┐              ┌──────────────────┐
│ Academic      │              │ Q&A / Community│              │ News / Finance   │
│ (Crossref,    │              │ (SO API, HN,   │              │ (WSJ/Bloomberg   │
│ OpenAlex,     │              │ Lobsters,      │              │ RSS, NSE proxy,  │
│ PubMed, arXiv)│              │ dev.to)        │              │ yfinance)        │
└───────┬───────┘              └───────┬────────┘              └────────┬─────────┘
        │  ✅ VERIFIED (no key)         │ ✅ VERIFIED                   │ ✅ VERIFIED
        └───────────────┬───────────────┴──────────────┬────────────────┘
                        ▼                              ▼
              ┌────────────────────┐        ┌──────────────────────┐
              │ access_routes.py   │        │ route_provenance.jsonl│
              │ (working library)  │◄──────►│ (evidence trail)      │
              └─────────┬──────────┘        └──────────────────────┘
                        ▼
        ┌───────────────────────────────────────────────┐
        │ UAI-COS MEMORY + REPORTS (quality gate ke saath) │
        └───────────────────────────────────────────────┘
```

**Ek nayi capability = kitne unlock? (multiplier table)**

| Naya unlock | Kitni capabilities khulti hain |
|---|---|
| **Jina reader-proxy key** (free tier+) | rate-limit khatam → NSE daily data, Medium batch, Bloomberg batch, proxy-dependent sab routes *n×* tez |
| **Reddit OAuth app** | Reddit full search + comments + subreddit data (research, sentiment, communities) |
| **LLM API key** | `/ask`, cross-model verification, auto-summaries, embedding-API (better retrieval), research drafting |
| **Kaggle key / HF datasets** | ML datasets, competitions data, model demos (bina GPU bhi inference ONNX se) |
| **gh token** | 60/hr → 5000/hr GitHub (repo research, issue mining, CI) |
| **Telegram bot token** | mobile memory console + daily reports + reminders |
| **Institutional library access** | paywalled journal full text (legal, user ke through) |
| **Hosted GPU (Colab/Kaggle)** | fine-tuning, heavy ML, embeddings at scale |

## 2. USER-ACTION SHORTLIST (sabse chhoti mehnat, sabse bada faayda)

| Priority | Action | Kahan se | Time | Kya khulega |
|---|---|---|---|---|
| **P1** | Telegram bot token | @BotFather → `/newbot` | 2 min | mobile console + reports + reminders |
| **P1** | LLM API key | koi bhi provider (OpenAI/Anthropic/Gemini) | 5 min | `/ask`, auto-research, verification |
| **P2** | Jina reader key | jina.ai (free tier) | 5 min | proxy rate-limits gone → NSE/news batch |
| **P2** | Kaggle API key | kaggle.com → Account → Create token | 3 min | datasets, competitions |
| **P3** | Reddit app creds | reddit.com/prefs/apps (script type) | 10 min | full Reddit access |
| **P3** | gh token | github.com → Settings → tokens | 3 min | 5000 req/hr + gist/repo actions |
| **P4** | rclone cloud config | `rclone config` (Drive/S3) | 10 min | cloud files read/write |
| **P4** | WhatsApp Cloud API | Meta developer setup | 30 min | WhatsApp commands |

**Ye 8 actions = Phase 2 ke saare remaining "CONDITIONAL" items → "DIRECT" ban jaate hain.** (Hard limits nahi bante.)

## 3. JO ABHI BHI USER KE BINA NAHI HO SAKTA (honest list)

- Tumhare private accounts/data ka access
- Paywalled content (subscription ke bina)
- Real-world publish/payment/legal actions
- Hosted GPU (account chahiye)
- WhatsApp/Meta business verification

## 4. NEXT STEPS (Phase 2 ke baad, priority order me)

1. **Verified routes ko memory me daalna + daily-use scripts me convert karna** ✅ (ho gaya: `access_routes.py`)
2. **Phase 2 ke routes par ek asli research task end-to-end** karna (proof of value)
3. **P1 user actions** (Telegram + LLM key) → capability doubling
4. **AQ-01/AQ-02/AQ-05 unknowns** clear karna (patents, OpenAIRE, Kaggle/HF datasets)
5. **Route health monitor** — `access_routes.py demo` ko roz/weekly chalana (routes toot sakte hain)

## 5. PHASE 2 KA BOTTOM LINE

> Phase 1 me humne map banaya tha: **"kya available hai"**.
> Phase 2 me humne wo cheez ki jo blueprint maangta tha: **"jo available nahi hai, uske legitimate raste dhundho"** —
> aur **12 blocked targets me 9 ke liye working route** mil gaya, jo ab code me hai, test kiya hua hai, aur evidence ke saath document hai.
> Jo nahi mila (Quora, login-walled social, paywalled full-text) — wo **saaf-saaf HARD LIMIT** likha hai, aur unhe bypass nahi kiya jayega.

## 6. SWEEP v2 CORRECTION (2026-09-23)

**systemd scheduled automation UNAVAILABLE nahi hai — WORKING hai.** Live proof: `uai-cos-monitor.timer` har 30 min par `tools/route_monitor.py` chalata hai → `logs/route_health.jsonl` (pehla run 6/6 routes pass). Iska matlab recurring kaam (memory housekeeping, backups, health checks, daily reports) ab scheduler par daale ja sakte hain — sirf session ke andar hi nahi.

**Bonus unlock (no API key):** local LLM (Qwen2.5-0.5B), edge-tts Hindi voice, whisper STT — sab `tools/local_ai.py` me. Isse "LLM key chahiye" wali CONDITIONAL list chhoti ho gayi (quality-limited fallback available hai).
