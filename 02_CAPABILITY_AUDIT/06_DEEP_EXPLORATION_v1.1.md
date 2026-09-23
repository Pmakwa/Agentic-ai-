# DEEP EXPLORATION — SECOND PASS (Capability Map v1.1)

> Blueprint ka Part 33 (Recursive Self-Audit: *"kya maine sab check kar liya?"*) chala kar jo naya nikla.
> Har line ka evidence `probes/` me ya neeche command output me hai. **v1.0 ke baad ka sach:**

---

## 1. ⭐ SABSE BADA FINDING — Persistence ka asli pattern (U1 ka jawab)

v1.0 me maine 4 stamp files likhi thin. Aaj ka result:

| Path | v1.0 prediction | **v1.1 asli result** |
|---|---|---|
| `/home/user/uai-cos/.../normal/stamp.txt` | survive | ✅ **SURVIVED** |
| `.../node_modules/stamp.txt` | volatile | ❌ **GONE** (confirm) |
| `.../.venv/stamp.txt` | volatile | ❌ **GONE** (confirm) |
| `.../out/stamp.txt` | volatile | ❌ **GONE** (confirm) |

**Aur do cheezein jo maine soch ke test ki:**

| Cheez | Result |
|---|---|
| `/usr` me apt installs (sqlite3, tesseract, jq) | ✅ **STILL INSTALLED** |
| pip packages (playwright, humanize, tabulate) | ✅ **STILL INSTALLED** |
| `/home/user/.cache/ms-playwright` (114 MB Chromium) | ❌ **GONE** → browser dobara install karna pada |
| `/home/user/.cache/huggingface` (embedding model) | ❌ **GONE/volatile** |
| http.server process (port 8000) + `get_process_output` | ❌ **DEAD / not_found** — processes session ke saath marte hain |
| memory store (`memory.jsonl`) | ✅ **SURVIVED — 37 records intact** ✅ |

### Iska practical matlab (ye rules ab permanent)

1. **System layer (`/usr`, apt, pip) persistent hai** — dobara install karne ki zarurat nahi.
2. **`/home/user/.cache` volatile hai** — Playwright ka 114 MB browser aur embedding models **wahan mat rakho**.
3. **Fix jo maine aaj kar diya:** browser → `/opt/ms-playwright` (657 MB, sudo ke saath, user-owned) + model cache → `/opt/uai-cache`.
   Agle turn me verify hoga ki `/opt` survive karta hai (stamp file laga di hai: `/opt/uai-cache/PERSIST_STAMP.txt`, `/var/tmp/uai-persist/stamp.txt`).
4. **Processes turn ke baad zinda nahi rehte** → server/bot **har session me dobara start** karna hai (`tools/bootstrap_environment.sh` isi liye banayi).
5. **`tests/test_memory_os.sh` ki value aur badh gayi** — kyunki system state badalta rehta hai, regression suite har session chalanai chahiye.

---

## 2. Naye VERIFIED capabilities (v1.0 me nahi the)

| Capability | Evidence | Status |
|---|---|---|
| **Outbound WRITE (POST/PUT/DELETE)** | `httpbin.org` pe POST/PUT/DELETE → 200, JSON echo match | ✅ VERIFIED (auth wale services ke liye creds chahiye) |
| **Video processing** (U11 close) | ffmpeg 7.1.5: video create (10.9 KB), resize/convert, **frames extract (4 PNG)** | ✅ VERIFIED |
| **Offline Hindi TTS** | espeak-ng 1.52 → Hindi wav 95.8 KB ("नमस्ते, यह एक परीक्षण है") | ✅ VERIFIED (robotic; accha voice ke liye voice audition) |
| **Text-based PDF generation** | fpdf2 → 1 KB PDF; matplotlib → chart PDF | ✅ VERIFIED |
| **PPTX generation** | python-pptx → 28.2 KB deck | ✅ VERIFIED |
| **DOCX + XLSX round-trip** | docx create+re-read (36.8 KB), xlsx create + pandas read back | ✅ VERIFIED |
| **Web API server banane ki capability** | flask 3.1.3 → `/health` aur `/mem` endpoints live, memory store JSON serve hua (`{"count":37}`) | ✅ VERIFIED |
| **Local embeddings (bina torch)** | onnxruntime 1.30 + fastembed → 384-dim vectors **CPU par** | ✅ VERIFIED |
| **Semantic memory search (asli demo)** | 37 memories par: "browser se website kholna" → `MEM-PROC-0004` (fallback chain) top hit | ✅ VERIFIED |
| **Hindi OCR** | `tesseract-ocr-hin` → rendered image se **"सदासुहागिन" sahi padha** | ✅ VERIFIED |
| **Fonts (416 total)** | `fonts-noto-core` + `fonts-noto-color-emoji` → 4 Devanagari + 1 emoji font, **system-wide** | ✅ VERIFIED |
| **DNS-over-HTTPS fallback** | `cloudflare-dns.com/dns-query` → valid JSON answer | ✅ VERIFIED |
| **SQLite FTS5** | FTS5 virtual table + MATCH query chala | ✅ VERIFIED (memory search upgrade ka rasta khula) |
| **12 parallel processes** | 12 sleepers ek saath alive | ✅ VERIFIED |
| **systemd (system scope)** | `/etc/systemd/system` **writable**; is-system-running = degraded | ✅ writable (daemon par depend) |
| **Git local commit** | local repo + commit (`40cd0b4`) | ✅ VERIFIED (push → token chahiye) |

## 3. Naye limits jo milnay (v1.0 me miss the)

| Limit | Evidence | Status |
|---|---|---|
| **IPv6 egress band** | `curl -6` → HTTP 000 | ❌ UNAVAILABLE (IPv4 only) |
| **systemd --user scope nahi chalta** | "$DBUS_SESSION_BUS_ADDRESS undefined" | ❌ UNAVAILABLE → cron alternative = process loop / system service (test pending) |
| **`fonts-noto-devanagari` package exist nahi karta** Debian 13 me | `E: Unable to locate package` (sahi naam: `fonts-noto-core`) | ⚠️ naming trap — error memory me daala |
| **`/opt` write bina sudo nahi** | `EACCES` → `sudo mkdir + chown` se fix | ⚠️ workaround documented |
| **matplotlib Devanagari shaping** | "सदासुहागिन" → galat matra order ("सदासुहागनि") render hua | ⚠️ **PIL (Raqm=True) sahi karta hai, matplotlib nahi** — rule banaya |
| **Devnagari font me Latin glyphs nahi** | latin text boxes ban gaye → fallback font list lagani padi | ⚠️ fix: `font.family = ['Noto Sans Devanagari', 'DejaVu Sans']` |
| **`pkill -f <pattern>` khud ko bhi maarta hai** | mera hi shell mar gaya (pattern self-match) | ⚠️ safety rule |

---

## 4. Rules jo is exploration se nikle (aur memory me daale)

1. **Persistent vs volatile rule:** durable cheezein `/home/user` (excluded dirs chhod kar) + system path (`/usr`) me; caches `/opt` me (sudo se), warna `/home/user/.cache` use **na karo**.
2. **Session-start protocol:** `bash tools/bootstrap_environment.sh` (browser + model cache + missing packages) — phir `tests/test_memory_os.sh` + `uai_mem.py audit`.
3. **Devanagari rendering rule:** image me Hindi text → **PIL** (Raqm) use karo, matplotlib nahi; matplotlib me fallback font list zaroori.
4. **Query tool rule (U8/U9/POST):** outbound POST/GET/DELETE available hai, lekin **auth required services** ke liye user creds — bypass nahi.
5. **Process lifecycle rule:** server/bot har session me restart; state **files** me rakho, process memory me nahi.
6. **Tool kill safety:** `pkill -f` se pehle pattern check karo, warna apna shell mar sakta hai.
7. **Semantic search ab possible hai** (fastembed) → Phase 2 ka pehla step **aaj hi** ho sakta hai (FTS5 + embeddings dono available).

---

## 5. Ab bhi UNKNOWN (isliye honest)

| ID | Unknown | Kab / kaise test |
|---|---|---|
| U1b | `/opt` aur `/var/tmp` cross-turn survive karte hain? | **agle turn me** stamp files |
| U2b | systemd **service** sandbox me actually start hoti hai? (`systemctl start`) | chhota test service (pending) |
| U16 | model cache (fastembed) `/opt/uai-cache` se sach me load hua (network ke bina)? | next turn (offline test) |
| U9 | bulk rate limits (pip/npm/search) | load test (optional) |
| U7 | patents APIs (patentsview/lens) | endpoint test (pending) |
| U15 | Kaggle/Colab style hosted GPU — sirf user ke account se | user action |

---

## 6. Second-pass ka nichod (ek paragraph)

Pehle pass me maine "kya kya available hai" map kiya tha; is pass me **"kya cheez tik-ti hai"** aur **"kahan chhupti hui takat hai"** dono mil gayi:
system-level installs zinda rehte hain, caches mar jaate hain — isliye aaj maine browser + embedding cache ko `/opt` me shift kiya aur
bootstrap script likhi. Aur do bade unlocks mile jo v1.0 me sirf "POSSIBLE" the: **local embeddings (384-dim, CPU, bina torch)** aur
**web API server** — matlab semantic memory search aur external interface dono **aaj hi ban sakte hain**, sirf decision chahiye.
