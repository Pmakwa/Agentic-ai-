# UNKNOWN CAPABILITY QUEUE + RECOMMENDED SAFE TESTS

> **⚠️ UPDATE (v1.1, same day):** U1, U2, U5, U10, U11, U12 mein se kai **resolve ho gaye** —
> poora result `06_DEEP_EXPLORATION_v1.1.md` me hai. Summary: ✳ U1 = `/home/user` files + `/usr` survive,
> `.cache/node_modules/.venv/out` wipe (browser+model cache **/opt** me shift kar diya);
> ✳ U2 = processes turn ke baad **mar jaate hain** → bootstrap script bani;
> ✳ U11 = ffmpeg ✅; ✳ U3/U4 = APIs ✅; ✳ U10 = systemd system-scope writable, --user nahi chalta;
> ✳ naye unknowns: `/opt` persistence (U1b), systemd service start (U2b), offline model load (U16).

> Blueprint Parts 14, 32, 33, 15 ka output.
> Rule: jo verified nahi, wo **POSSIBLE/CONDITIONAL/UNKNOWN** hi rahega. "Assume → fact" conversion **ban** hai (Part 14).

---

## 1. UNKNOWN CAPABILITY QUEUE (prioritized)

| ID | Unknown | Kyun matters | Discovery method | Safe test | Risk | Expected value | Status |
|---|---|---|---|---|---|---|---|
| **U1** | Cross-turn persistence: `/home/user` zinda rehta hai? `node_modules/.venv/out/.cache` volatile? | memory + installed tools + browser reusable honge ya nahi | stamp files agle turn me check | `ls _persist_test/*/stamp.txt` | none | **very high** (poora workflow plan isi par) | TEST SET UP (`_persist_test/`) |
| **U2** | Sandbox/process lifetime: http.server + bot chalu rehte hain? | Telegram bot aur preview ke liye critical | agle turn me process probe | `get_process_output` port check | none | high | PENDING |
| **U3** | Stack Exchange API (StackOverflow data bina scraping) | dev research ka bada gap bhar sakta hai | anonymous API call | `curl api.stackexchange.com/...?site=stackoverflow&intitle=python` | none | high | ✅ **VERIFIED — bina key chalta hai (200 JSON results)** |
| **U4** | archive.org / wayback availability | dead pages, historical research | direct fetch | `curl https://archive.org/wayback/available?url=reddit.com/r/programming` | none | high | ✅ **VERIFIED — snapshot available:true (blocked pages ka legitimate fallback)** |
| **U5** | DDG HTML endpoint se usable results? | search redundancy | follow redirect + parse | `curl -L "https://html.duckduckgo.com/html/?q=test"` | none | medium | PARTIAL — 202/302 milta hai, parse untested |
| **U6** | Google Scholar / Semantic Scholar API | academic research depth | API call | `curl api.semanticscholar.org/graph/v1/paper/search?query=...` | none | high | ⚠️ **CONDITIONAL — endpoint zinda hai, bina key 429 (rate limit) deta hai** |
| **U7** | patents view / lens.org API | patent research | API call | public endpoint test | none | medium | TEST PENDING |
| **U8** | Playwright: logged-out JS sites (x.com) ka real extraction ceiling | social research | DOM wait + selector test | script with wait_for_selector | low | medium | PARTIAL (title empty) |
| **U9** | Rate limits: pip/npm/apt/search bulk operations | automation scale | throttled loop | 30 requests with delay | low | medium | UNKNOWN |
| **U10** | systemd timer cron-replacement ke liye chalega? | scheduled memory expiry | systemctl probe | `systemctl list-timers` | none | medium | ✅ **VERIFIED — systemd timers chal rahe hain (apt-daily.timer, tmpfiles-clean.timer)** |
| **U11** | ffmpeg install ke baad video pipeline | media workflows | apt install test | install + `ffmpeg -version` | none | medium | INSTALL PENDING |
| **U12** | LibreOffice headless se docx→pdf conversion | document conversion | apt install test | `soffice --headless --convert-to pdf` | none | medium | INSTALL PENDING |
| **U13** | Voice audition ke baad speech quality | narration deliverable | add_voice + generate_speech | 15-sec audition | none | medium | CONDITIONAL (user) |
| **U14** | Cross-model verification (agar user key de) | high-stakes verification | API call | user key ke baad | cost | high | CONDITIONAL (user) |

---

## 2. RECOMMENDED SAFE TESTS (Part 27-L) — exact commands

```bash
# U1 — persistence (AGLE TURN me)
ls -la /home/user/uai-cos/_persist_test/*/stamp.txt && cat /home/user/uai-cos/_persist_test/normal/stamp.txt

# U2 — process lifetime
curl -s -o /dev/null -w "local server: %{http_code}\n" http://127.0.0.1:8000/ || echo "server gaya"

# U3 — Stack Exchange API (unauth, quota-safe)
curl -s -m 10 "https://api.stackexchange.com/2.3/search?order=desc&sort=relevance&intitle=python&site=stackoverflow" | head -c 300

# U4 — Wayback availability
curl -s -m 10 "https://archive.org/wayback/available?url=reddit.com/r/programming" | head -c 300

# U6 — Semantic Scholar (unauth tier)
curl -s -m 10 "https://api.semanticscholar.org/graph/v1/paper/search?query=transformer&limit=1" | head -c 300

# U10 — systemd timers scope
systemctl list-timers --all 2>&1 | head -5

# U11/U12 — media/document converters
sudo apt-get install -y ffmpeg libreoffice >/dev/null 2>&1 && ffmpeg -version | head -1 && soffice --version
```

**Safety rules for testing (Part 24 ke saath):** sirf read-only/public endpoints; koi auth bypass nahi; koi scraping storm nahi
(delay + respect robots/ToS); user ke accounts me kuch nahi.

---

## 3. CAPABILITY BOUNDARY TESTING (Part 15) — lower/upper/hard

| Capability | LOWER BOUND (definitely) | UPPER BOUND (possible, unverified) | HARD LIMIT (nahi hoga) |
|---|---|---|---|
| Web research | open sites + PDFs + repos | blocked sites ke snippets/mirrors | paywall/login/CF bypass |
| Automation | scripts, servers, loops, parallel processes | systemd timers, long crawls | true sub-agents |
| Data | CSV/JSON/PDF/HTML pipelines | streaming APIs (key ke saath) | private databases |
| Media | images gen/edit/OCR/screenshot | video (ffmpeg install), audio (TTS) | GPU inference/training |
| Communication | file deliverable + preview | Telegram/email (user creds ke baad) | anonymous mass messaging |
| Memory | file-backed, audited, versioned | vector retrieval (Phase 2) | infinite/permanent claim |

---

## 4. RECURSIVE SELF-AUDIT (Part 33) — jo abhi bhi check nahi hua

- [ ] `systemctl --user` scope me kya kya chalta hai? (U10)
- [ ] Playwright ke saath **network logging** (HAR capture) — research evidence ke liye
- [ ] `pip` ke against private index / offline wheel cache?
- [ ] Browser me **PDF generation** (print-to-pdf) ka quality check
- [ ] `sqlite3` + FTS5 full-text search (memory search upgrade ka candidate)
- [ ] `/dev/shm` size limits (heavy temporary processing)
- [ ] Parallel process count ka real ceiling (2 vCPU par practical limit)
- [ ] Kya koi **outbound port restriction** HTTP ke alawa? (jaise 8080, 25, 587 — 25 tested OK)
- [ ] **DNS-over-HTTPS** fallback agar koi host DNS block kare
- [ ] Kya user ke sandbox me **shared network** hai (kisi doosre sandbox se reach)?

---

## 5. STOP CONDITION (Part 34) — official wording

> **"Maximum capability audit jo is observable + authorized environment me possible tha, wo complete hai."**
> Findings: verified capabilities (Section F), unknowns (U1–U14), aur hard limits (H1–H6) ke saath.
> Ye map **versioned** hai — environment badlega to map badlega (`05_...MAINTENANCE.md` protocol).
