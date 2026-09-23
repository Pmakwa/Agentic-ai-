# HINDI SUMMARY — ek page me poori kahani (Roman Hindi)

## Shuruaat
Aapne ek V2 system prompt (ChatGPT share link) diya aur kaha: *"pura le lo, is environment me apply karo, aur step 2 bhi pura apply karo."*
Link direct blocked tha → `r.jina.ai` reader se poora text mila → **V1 (15 parts)** + **V2.0 (112 sections)** import hue, hash-verified.

## Kya bana (aur chala)
| # | Kaam | Natija |
|---|---|---|
| 1 | **Memory OS** | 71 live records, 13 commands, audit **100/100**, tests **28/28** |
| 2 | **Capability audit** | 29-site live matrix, secrets scan, `CAPABILITY_MAP.json` (**v2.4**) |
| 3 | **Phase 2 — access expansion** | 12 blocked targets ke legitimate routes (jina reader, Wayback, APIs), playbook + blocker register |
| 4 | **GitHub dig** | bina token 8 capabilities verified; `yq` + `crane` (Docker-free image extract) |
| 5 | **Social unlock** | tokenless matrix + kya credentials chahiye + kya legit nahi hai |
| 6 | **Repo hunt (latest)** | 15 repos install + live test → **Reddit, TikTok, Pinterest, Threads, Weibo, Tumblr naye khule** |
| 7 | **RSSHub self-host** | 2015 namespaces ka apna RSS server, **13 routes verified, :1200 par live** |
| 8 | **Tools** | `social_unlock.py`, `uai_mem.py`, `access_routes.py`, `github_unlock.py`, `local_ai.py`, `route_monitor.py` |
| 9 | **Local AI** | Qwen2.5-0.5B (CPU), edge-tts Hindi voice, whisper transcribe |
| 10 | **Monitoring** | systemd timer, har 30 min 6 routes ka health check |

## Kya band raha (honest)
Instagram (login wall + 429), Facebook (login redirect — proof hai), LinkedIn, Quora, Bilibili (412), X full API (paid),
Douyin (cookie chahiye → boundary me excluded), Invidious/Nitter (dead ya bot-check).
**Rule:** auth/paywall/CAPTCHA todna allowed nahi — isliye ye "jugaad" nahi ki gayi; sirf legit raste test kiye.

## Aaj ki state
- Servers: control-center **:8000**, RSSHub **:1200** — dono HTTP 200
- Memory 71 · CAPABILITY_MAP v2.4 · 60+ evidence files · 7 report folders
- Sab kuch `/opt` me persist: playwright browsers, model cache, Node 22, swap

## Naya agent is repo se kaise continue karega
1. `AGENTS.md` padhe → 2. `CONVERSATION/00_A_TO_Z_LOG.md` padhe → 3. boot-check chalaye
(provenance 4/4, audit 100/100, tests 28/28, `social_unlock.py status`) → 4. `AGENTS.md` §5 ke open threads se agla kaam uthaye.

**Aapko bas ek line bolni hai:**
> "AGENTS.md se start karo, A-to-Z log padho, boot-check chalao aur aage kaam continue karo."
