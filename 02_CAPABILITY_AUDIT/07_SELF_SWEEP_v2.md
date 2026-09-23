# SELF-SWEEP v2 — "kuch baki to nahi reh jata na?" (2026-09-23, round 2)

> Method: 3 disciplines — (1) workspace consistency/stale-check, (2) **nayi capabilities jo kabhi test nahi hui**, (3) bache hue unknowns.
> Har claim ke saath live test ka output. Jo nahi chala wo bhi saaf likha hai.

---

## 1. SABSE BADA CORRECTION — systemd timers actually kaam karte hain ⚠️→✅

Pichhle sweep me likha tha: *"sandbox me systemd service start nahi chalti — process-loop hi viable route hai"*. **Ye GALAT tha.**

Kya hua: workspace me ek root-owned `logs/heartbeat.log` mila jo **har 2 min me badh raha tha**. Investigation:

| Test | Result |
|---|---|
| `uai-cos-heartbeat.timer` status | **active (waiting)** — 04:31 se chal raha hai, 04:50 par fire hua, next 04:52 |
| Fire history (log) | 04:45:44, 04:47:54, 04:50:04 — har 2 min |
| Service result | `Result=success`, `ExecMainStatus=0` |
| **Direct start** (`systemctl start`) | ✅ line append hui (3→4) |
| **Fast timer test** (15 s interval) | ✅ 3/3 fires — 04:52:40, 04:52:55, 04:53:11 |
| Root service /home/user me likh sakti hai? | ✅ haan |
| Turn-boundary survival | ✅ timer 20+ min dauraan zinda raha |

**Nateeja:** scheduled/recurring automation ka **real route systemd timers hain** — process-loop ki zaroorat nahi. Galat memory record `MEM-SEM-0014` **supersede** kar diya (`MEM-SEM-0017`).

**Iski turant practical value:** naya service bana diya — `uai-cos-monitor.timer` = har 30 min par route-health check:
```
tools/route_monitor.py  →  logs/route_health.jsonl (history) + logs/route_health.txt (latest)
```
Pehla run: **5/6 routes OK** (reader-proxy fail hua — dekho #2).

## 2. Reader-proxy ka UA-trap (aur fix) 🐛→✅

Monitor ne `reader_proxy` par **403 "Just a moment..." (Cloudflare)** dikhaya, jabki manual curl 200 de raha tha. A/B test:

| UA | Result |
|---|---|
| `Mozilla/5.0 Chrome/124` (short) | **200** |
| full Chrome UA (`...Safari/537.36`) | **403 Cloudflare challenge** |
| koi UA nahi | **200** |

**Matlab:** r.jina.ai apne Cloudflare par full browser-UA + non-browser TLS ko suspicious maankar challenge karta hai. **Fix:** proxy ke liye alag neutral UA (`UAI-COS-research/1.0`) — `access_routes.py` aur `route_monitor.py` dono me. Post-fix: **6/6 routes pass**, aur NSE (marketStatus + bhavcopy) + Medium phir se chalne lage.

## 3. NAYI VERIFIED CAPABILITIES (jo pehle kabhi test nahi hui thi)

### 3a. Local AI — bina kisi API key 🔥
| Capability | Evidence |
|---|---|
| **Local LLM** (Qwen2.5-0.5B-Instruct, GGUF Q4, llama.cpp, CPU) | load 0.6 s, reply ~2 s, English answers sahi ("What is 2+2?" → "The answer is 4."); model 491 MB `/opt/uai-cache` me |
| Hindi accuracy (0.5B par) | weak — behtar ke liye bada model chahiye (slow on 2 vCPU). Honest limitation. |
| **edge-tts** (high-quality neural voice, Hindi) | `hi-IN-SwaraNeural` → 28,944 B mp3; natural voice (espeak se **bahut** behtar) |
| **faster-whisper STT** (offline, CPU) | base model ne apni Hindi TTS ko transcribe kiya: *"Namaste Bhai, ya UAI course ki nein aawaz hai"* — lang=hi p=1.00 |
| Wrapper | **`tools/local_ai.py`** — `chat` / `say` / `transcribe` / `status` (sab verified) |

### 3b. Document toolchain 📄
| Tool | Test result |
|---|---|
| **pandoc 3.1.11** | md → docx (10,014 B) + html ✅ |
| **pdflatex** (TeX Live) | PDF 22,098 B ✅ |
| **graphviz** | PNG 12,103 B ✅ |
| **ImageMagick 7.1.1** | annotate PNG ✅ |
| **ocrmypdf 16.7** | scanned PDF → PDF/A (searchable) ✅ |
| **sox 14.4** | wav → ogg (14,899 B) / flac (42,501 B) ✅ |
| **aria2 1.37** | multi-connection download ✅ |
| jq / ripgrep / fd / python-barcode / qrcode | ✅ sab chal gaye |

### 3c. Data stack 📊
| Tool | Test result |
|---|---|
| **duckdb 1.5** | SQL over CSV ✅ |
| **polars + pyarrow** | parquet write/read round-trip ✅ |
| **HF `datasets`** (public, **bina key**) | `stanfordnlp/imdb` load ✅ (AQ-05 clear) |
| **trafilatura 2.2** | article extraction — Wikipedia RAG page se 15,399 chars clean text ✅ |
| **feedparser** | WSJ feed → 20 entries ✅ |

### 3d. Media retrieval 🎬
| Tool | Test result |
|---|---|
| **yt-dlp** | archive.org (public-domain) se download ✅ 113,206 B |
| Note | Sirf public-domain/authorized sources — ToS ka khayal |

### 3e. Naye/cleared API routes 🌐
| Route | Result |
|---|---|
| **Google Patents via reader-proxy** | ✅ 200 — Bell telephone patent (US174465A), 16,369 B *(AQ-01 solved via different route)* |
| patentsview API | ❌ **unreachable** — `search.patentsview.org` DNS nahi resolve hota; `api.patentsview.org` **sirf IPv6** deta hai aur IPv6 egress blocked hai → precise blocker diagnose |
| **Nominatim (geocoding)** | ✅ 200 — "Rajkot, Gujarat" → 22.3053, 70.8028 |
| **OpenAIRE** | ✅ 200 (98,943 B) — AQ-02 **clear** |
| **GDELT news API** | ⚠️ 429 par "1 request / 5 s" rule; 30 s gap ke baad **200** (3 articles) → CONDITIONAL |
| IA Scholar | ⚠️ 200 par rate-limit page hi aata hai (throttle zaroori) |
| Reddit RSS | ⚠️ wahi 60 s window — koi badlav nahi |

---

## 4. Workspace consistency fixes (discipline 1)

| Finding | Fix |
|---|---|
| `logs/heartbeat.log` root-owned stray | ✅ Explain hua (systemd timer) → heartbeat units retire, jagah **route_monitor** ne li |
| `uai-fast-test.service/.timer` (test ke baad chhoot gaya) | ✅ disable + delete; `logs/fast_test.log` bhi clean |
| README.md stale: "v1.1" ×2, "45", "26 records" | ✅ 65 records + v2.1 numbers |
| index.html stale: "v1.1" ×2, "45", "56" | ✅ sync |
| `CAPABILITY_MAP.json` ke 4 `evidence_files` bina `02_CAPABILITY_AUDIT/` prefix ke | ✅ paths normalize |
| markdown link regex ne 0 links pakde | ⚠️ tool limitation (docs me links kam hain) — manual check kiya, sab fine |

## 5. Jo abhi bhi UNKNOWN / LIMITED hai (honest list)

| Item | Status |
|---|---|
| IA Scholar | LIMITED — rate limit page (throttle karke try karna hai) |
| GDELT | CONDITIONAL — 5 s+ gap zaroori |
| Reddit full access | OAuth creds chahiye (user) |
| Quora / x.com / IG / LinkedIn | UNAVAILABLE (no legitimate route) |
| Paywalled full-text | HARD LIMIT (no bypass) |
| Hindi quality (local 0.5B LLM) | weak — bada model chahiye (slow CPU) |
| /opt + /var/tmp persistence | ✅ confirmed isi sweep me |

## 6. Naya CLI summary
```bash
python3 tools/local_ai.py status              # kya ready hai
python3 tools/local_ai.py chat "question"     # local LLM (no key)
python3 tools/local_ai.py say "नमस्ते" -o a.mp3  # natural Hindi TTS
python3 tools/local_ai.py transcribe a.mp3    # STT (offline)
python3 tools/route_monitor.py                # route health (systemd se har 30 min auto)
systemctl list-timers | grep uai              # scheduled jobs dekho
```

**Verdict:** iss sweep me **17 nayi verified capabilities**, **1 bada correction** (systemd), **1 bug fix** (proxy UA), aur **workspace ke saare stale items** clear hue. Jo bacha hai wo upar §5 me saaf likha hai — koi cheez "ho sakta hai" ke bharose nahi chhodi.
