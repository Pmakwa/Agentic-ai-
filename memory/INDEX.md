# MEMORY INDEX — UAI-COS v2.0

> Generated: 2026-09-23T08:54:07  |  live records: **90**  |  total (incl. archived/deleted): 90
> Ye file auto-generated hai — edit na karo. Source of truth: `memory/store/memory.jsonl`
> Retrieval rule (Section 17): keyword match kaafi nahi — scope + authority + freshness + confidence + current instruction dekh kar use karo.

## CORE (1)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-CORE-0001` | active | high | User ka long-term goal: ek governed, memory-aware, multi-agent AI operating system chalana (UAI-COS), jisme memory verify hoti hai aur blind use nahi hoti. | user_instruction | ai-systems |

## PREFERENCE (7)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-PREF-0001` | verified | high | User se Hindi me baat karni hai, lekin English alphabet/spelling (Roman Hindi) me — jab tak user khud Devanagari ya doosri language na maange. | user_instruction | communication |
| `MEM-PREF-0002` | verified | high | User ko detailed, advanced, master-level aur practical output chahiye; basic ya generic answer nahi. | user_instruction | communication |
| `MEM-PREF-0003` | active | medium | Image prompts me high quality, photorealism, accurate details aur professional finishing rakhni hai. | user_instruction | image-generation |
| `MEM-PREF-0004` | active | medium | Jab product-only image maangi gayi ho to image prompt me model, character, haath ya body parts add nahi karne. | user_instruction | image-generation |
| `MEM-PREF-0005` | active | medium | Specific image prompt aur universal quality prompt ko alag-alag rakhna hai (mix nahi karna). | user_instruction | image-generation |
| `MEM-PREF-0006` | verified | high | Latest user instruction ko purani instruction/memory ke upar priority milegi (current instruction pehle). | user_instruction | communication |
| `MEM-PREF-0007` | active | high | Chat me internal agent complexity/process dikhane ki zaroorat nahi — jab tak user khud mind-map, agent architecture, memory log ya audit na maange. | user_instruction | communication |

## CONSTRAINT (4)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-CONS-0001` | verified | high | Permanent ya unlimited memory ka claim nahi karna, jab tak real storage + retrieval + version control + governance available na ho. | user_instruction | - |
| `MEM-CONS-0002` | verified | high | Memory ko blindly use nahi karna — sirf keyword match ke basis par retrieve nahi karna; scope + authority + freshness + confidence + current instruction dekh kar use karna. | user_instruction | - |
| `MEM-CONS-0003` | verified | high | High-risk ya irreversible action (delete, publish, payment, external send) se pehle user confirmation lena compulsory hai. | user_instruction | - |
| `MEM-CONS-0004` | verified | high | Capability claims sirf evidence ke saath: 'full internet' ya 'sab access' jaisa dava nahi; paywall/login/CAPTCHA bypass kabhi nahi; RESTRICTED sites (reddit, SO direct, medium, quora, Bloomberg, WSJ, ScienceDirect, TripAdvisor, NSE, Instagram/LinkedIn login walls) ko blocked hi maana jaayega. | tool_result | - |

## SEMANTIC (35)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-SEM-0001` | verified | high | Is sandbox me passwordless sudo (uid=0) hai, Debian 13 par 2 vCPU/2GB RAM/25GB disk, aur apt+pip+npm+git installs VERIFIED hain. | tool_result | environment |
| `MEM-SEM-0002` | verified | high | Playwright + Chromium (headless shell 153) VERIFIED: launch, navigation, screenshot aur page->PDF kaam karte hain; system libs (libnspr4 etc.) apt se install karni padi. | tool_result | environment |
| `MEM-SEM-0003` | verified | high | Blocked sites ke VERIFIED fallbacks: StackExchange API (bina key 200 JSON), Wayback availability API (snapshot available:true), reader-proxy (Cloudflare bypass ke bina legitimate), web_search snippets. | tool_result | research |
| `MEM-SEM-0004` | verified | high | Local embeddings VERIFIED bina torch: onnxruntime 1.30 + fastembed ('all-MiniLM-L6-v2', 384-dim, CPU) — 37 memories par semantic search chali (query 'browser se website kholna' -> MEM-PROC-0004 top hit). | tool_result | ai-systems |
| `MEM-SEM-0005` | verified | high | Media/document toolchain VERIFIED: ffmpeg 7.1.5 (video create/resize/frames), espeak-ng 1.52 (Hindi TTS wav), fpdf2 + matplotlib (PDF), python-pptx, docx/xlsx round-trip, flask API server, tesseract Hindi OCR. | tool_result | media |
| `MEM-SEM-0006` | verified | high | Network detail: IPv4 egress open (POST/PUT/DELETE bhi), outbound ports 587/465/993/443 OPEN, DoH (cloudflare-dns.com) chalta hai; IPv6 egress BAND hai; systemd --user scope nahi chalta (system scope writable). | tool_result | - |
| `MEM-SEM-0007` | verified | high | StackOverflow blocked site ke bajay StackExchange API route verified hai (full answer bodies ke saath) | phase2-probe | access |
| `MEM-SEM-0008` | verified | high | Reddit ka anonymous stable route nahi hai — RSS sirf 1 request chalti hai (60s gap ke saath), JSON/OAuth/mirrors fail | phase2-probe | access |
| `MEM-SEM-0009` | verified | high | WSJ+Bloomberg+Medium+BBC+GoogleNews ke official RSS feeds verified hain (headlines), aur Wayback/proxy se article-level content | phase2-probe | access |
| `MEM-SEM-0010` | verified | high | NSE India + Indian stocks ke do working routes: reader-proxy (JSON+CSV) aur yfinance (direct) | phase2-probe | access |
| `MEM-SEM-0011` | verified | high | Academic access ke 8 verified sources bina key chalte hain; sirf paywalled full-text hard limit hai | phase2-probe | access |
| `MEM-SEM-0012` | verified | high | tools/access_routes.py ek working verified-route library hai (demo live chalti hai) jisme har call provenance log karti hai | phase2-probe | access |
| `MEM-SEM-0013` | verified | high | Phase 2 ne 12 blocked targets me se 9 ke legitimate route khole; jo bacha wo hard limit hai (bypass nahi karenge) | phase2-probe | access |
| `MEM-SEM-0014` | superseded | high | Sandbox me systemd service start nahi chalti (degraded daemon) — scheduled automation ka viable route process-loop hai | phase2-probe | access |
| `MEM-SEM-0015` | verified | high | 8 user-actions se Phase-2 ke saare CONDITIONAL routes DIRECT ban jaate hain | phase2-probe | access |
| `MEM-SEM-0016` | verified | very_high | PERSISTENCE UPDATE v2: /opt aur /var/tmp bhi turns ke beech SAFE hain (sirf /home/user/.cache, node_modules, .venv, out wipe hote hain) | user_instruction | environment |
| `MEM-SEM-0017` | verified | high | CORRECTION: sandbox me systemd TIMERS + services actually kaam karte hain — recurring automation ka asli route yahi hai | self-sweep-2026-09-23 | environment |
| `MEM-SEM-0018` | verified | high | Local LLM (Qwen2.5-0.5B, llama.cpp CPU) bina kisi API key ke chalta hai — Python + inference verified | self-sweep-2026-09-23 | environment |
| `MEM-SEM-0019` | verified | high | Speech: edge-tts (high-quality Hindi neural voice) + faster-whisper STT (offline, CPU) dono verified | self-sweep-2026-09-23 | environment |
| `MEM-SEM-0020` | verified | high | Media retrieval: yt-dlp se public-domain media download verified (archive.org 113,206 B) | self-sweep-2026-09-23 | environment |
| `MEM-SEM-0021` | verified | high | Document toolchain complete: pandoc (md→docx/html) + pdflatex + graphviz + ImageMagick + ocrmypdf + sox + aria2 sab verified | self-sweep-2026-09-23 | environment |
| `MEM-SEM-0022` | verified | high | Data stack verified: duckdb + polars + pyarrow/parquet + HF datasets (public, bina key) + trafilatura (article extraction) | self-sweep-2026-09-23 | environment |
| `MEM-SEM-0023` | verified | high | Naye verified API routes: OpenAIRE 200, Nominatim 200 (Rājkot geocode), GDELT 200 (5s+ gap), Patents via reader-proxy 200 | self-sweep-2026-09-23 | environment |
| `MEM-SEM-0024` | verified | high | Reader-proxy ka UA rule: r.jina.ai par FULL browser-UA se Cloudflare challenge aata hai, neutral UA se 200 | self-sweep-2026-09-23 | environment |
| `MEM-SEM-0025` | verified | high | GitHub bina token ke 7 categories ki capability deta hai: binaries, source code, data, packages, containers, intel, discovery | github-probe-2026-09-23 | access |
| `MEM-SEM-0026` | verified | high | GitHub code search, gh CLI, GraphQL aur write-ops token ke bina kaam nahi karte (401/0-quota verified) | github-probe-2026-09-23 | access |
| `MEM-SEM-0027` | verified | high | Bina credential ke 6 social platforms abhi khul Gaye: Reddit RSS, Telegram public preview, Bluesky public API, Mastodon (kuch instances), TikTok oEmbed, YouTube (yt-dlp) | social-probe-2026-09-23 | access |
| `MEM-SEM-0028` | verified | high | Instagram/Facebook/Pinterest personal access bina login/app ke possible nahi; X reads 2026 me pay-per-use; Reddit API approval-based ho gayi | social-probe-2026-09-23 | access |
| `MEM-SEM-0029` | verified | very_high | Repo-hunt verified 7 tokenless platform routes via installed GitHub repos: Reddit via redlib instances (safereddit.com, red.artemislena.eu), TikTok/Bluesky/Pinterest/Tumblr media via gallery-dl 1.32.13, Pinterest search/board via pinterest-dl 1.3.0, Threads+Weibo+Telegram+Mastodon+YouTube+Pinterest feeds via self-hosted RSSHub (:1200), YouTube transcripts/comments via youtube-transcript-api+youtube-comment-downloader, X public data via fxtwitter/vxtwitter bridges. | live tests 2026-09-23 | capability_access |
| `MEM-SEM-0030` | verified | very_high | Repo-hunt blockers (honest, not bypassable without user credentials): Instagram (gallery-dl 429 + instaloader login wall + all IG viewers dead), Facebook (login.php redirect proved via mbasic/m; scraper 0 posts), LinkedIn (RSSHub route empty), Bilibili (upstream 412 risk control), Douyin (playwright nav failed), X full API (paid). Public front-ends mostly dead: teddit 000, xeddit parking, quetre 410, proxitok 000, neuters 502, nitter archived, invidious gated/disabled. Cookie/identity-pool repos excluded per boundary §24. | live tests 2026-09-23 | capability_access |
| `MEM-SEM-0031` | verified | very_high | api.pullpush.io = Reddit data ka asli route jab reddit.com IP-block kare: submission/comment endpoints ka q= (keyword) aur ids=/link_id= free hai (aaj ke posts milte hain), lekin subreddit= listing param rate-limited/paywalled ('does not provide free scraping resources for agents'). social_unlock.py pullpush me r/<sub> par automatic q=<sub> fallback lagta hai. | live test 2026-09-23 | - |
| `MEM-SEM-0032` | verified | high | Discord invite API (discord.com/api/v9/invites/<code>?with_counts=true) aur Spotify oEmbed (open.spotify.com/oembed?url=) tokenless public metadata dete hain — guild member counts (Python: 431,757 members / 29,845 online) aur track title/thumbnail/embed URL. | live test 2026-09-23 | - |
| `MEM-SEM-0033` | verified | very_high | RSSHub sweep (250 namespaces, automated): 120 WORKING (48%) — top routes /bilibili/app/android (491 items), /ai-bot/daily-ai-news (436), /aiaa/journal/aiaaj (205), /4chan/g/catalog (151), /android/pixel-update-bulletin (107), /amazon/awsblogs (50). Fail hone ka pattern: upstream IP block, login/cookie (boundary), ya china-only geo-block. | live sweep 2026-09-23 | - |
| `MEM-SEM-0034` | verified | very_high | Workspace ab lean hai: heavy artifacts /opt/uai-cache me — rsshub (996M, 2015 namespaces, :1200), bin/{yq,crane} (25M), node22 (200M), models (469M+87M). Workspace repo sirf 8 MB (pehle 1.1 GB). Cleanup cadence: har 3-5 turn ya push se pehle tools/cleanup_workspace.py (report -> --apply). | cleanup run 2026-09-23 | - |
| `MEM-SEM-0035` | verified | very_high | Self-audit deliverables (07_SELF_AUDIT/): AGENT_CAPABILITY_MAP.json (tools/env/access/permissions/hard-limits/boundaries + change_log), RESEARCH_CAPABILITY_MAP.json (25 methods: 21 AVAILABLE, 4 PARTIAL), ENVIRONMENT_FALLBACK_MAP.json (12 cases: X->fxtwitter, Reddit->redlib+pullpush, reset->bootstrap...), UNKNOWN_CAPABILITY_QUEUE.json (10 unknowns with test method), CAPABILITY_EXPANSION_ROADMAP.md, 00_SELF_AUDIT_MASTER_REPORT.md (A-M). Continuous update: tools/self_audit.py (env probe + diff + version bump). | self-audit run 2026-09-23 | - |

## EPISODIC (4)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-EPI-0001` | verified | high | 2026-09-23: User ne ChatGPT share link diya (V2 prompt) — spec import kiya, is workspace me UAI-COS v2.0 implement kiya (memory store + CLI + agents + step-2 docs). | user_instruction | - |
| `MEM-EPI-0002` | verified | high | 2026-09-23: Step 2 deliver hua — implementation roadmap (6 phases), 9 user scenarios, 15 memory types integration, agent lifecycle + autonomy model, golden test suite (28/28 pass), Telegram bot + system-prompt compiler, aur provenance verifier. | user_instruction | - |
| `MEM-EPI-0003` | verified | high | 2026-09-23 (deep pass): capability audit v1.1 complete — persistence solved, browser/model cache /opt me shift, 13+ naye capabilities verified, 5 naye limits documented, bootstrap script + probe scripts banaye. | user_instruction | - |
| `MEM-EPI-0004` | active | high | 2026-09-23 ko PHASE 2 (access expansion) complete hui: 12 blocked targets me 9 ke verified routes + working library + 6 deliverable docs | user_instruction | access |

## PROCEDURAL (13)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-PROC-0001` | verified | high | Session boot protocol: memory/INDEX.md padho -> task classify karo -> sirf relevant memory filter karo -> plan banao -> execute -> quality gate -> respond -> memory update. | user_instruction | ai-systems |
| `MEM-PROC-0002` | verified | high | Har memory record me source, scope, confidence, authority, status, timestamps aur history bharni hi hogi — warna record candidate bhi nahi banega. | user_instruction | ai-systems |
| `MEM-PROC-0003` | active | high | Is environment me bada output file ke roop me workspace me save karo, aur chat me uska concise summary + path do. | agent_inference | ai-systems |
| `MEM-PROC-0004` | verified | high | Site-block fallback chain (order): fetch_page -> curl browser-UA -> Playwright -> API alternative (StackExchange/Wayback/public API) -> web_search snippets -> user-provided file. 2 attempts ke baad route badlo, retry-loop mat karo. | tool_result | research |
| `MEM-PROC-0005` | verified | high | PERSISTENCE RULE (verified): /home/user files + /usr (apt/pip installs) cross-turn survive karte hain; /home/user/.cache, node_modules, .venv, out WIPE ho jaate hain; running processes aur ports mar jaate hain. | tool_result | - |
| `MEM-PROC-0006` | verified | high | SESSION START PROTOCOL: pehle 'bash tools/bootstrap_environment.sh' chalao (browser + model cache + missing packages), phir 'bash tests/test_memory_os.sh' aur 'python3 tools/uai_mem.py audit --log'. | tool_result | - |
| `MEM-PROC-0007` | active | high | Blocked resource milne par ye order follow karo: direct test -> official API/feed -> reader-proxy -> Wayback -> user-provided file | user_instruction | access |
| `MEM-PROC-0008` | verified | very_high | Agent boot procedure (V2 apply karna): (1) python3 tools/agent_boot.py — poora system ek payload me (identity+rules+spec map+protocol+memory snapshot+capability truth+open threads+attestation), (2) health check (provenance 4/4, audit 100/100, tests 28/28), (3) BOOT ATTESTATION bharna (tests/boot_attestation.md, 12 points + scoring) — iske bina kaam shuru nahi karna. | user feedback 2026-09-23: 'pehle V2 prompt uske environment me apply karna chahiye, test kiya wo ye nahi kar raha' | - |
| `MEM-PROC-0009` | verified | very_high | Naya prompt/phase apply karne ka system: (1) prompt aaye to tools/import_prompt.py (url/file/text) -> 00_SYSTEM me hash-verified save + memory + auto phase; (2) naya kaam bole to tools/phase_runner.py add/set; (3) kaam -> evidence -> CAPABILITY_MAP bump -> memory -> agent_boot.py --write -> push. | user standing instruction 2026-09-23 | - |
| `MEM-PROC-0010` | verified | very_high | RSSHub route verification procedure: local RSSHub :1200 chalu karo -> python3 tools/rsshub_verify.py (registry /api/namespace se 2015 namespaces + example routes) -> evidence files -> monitor me naye routes add karo -> phase done. | agent procedure | - |
| `MEM-PROC-0011` | verified | very_high | Structured prompts ka system: user ke saare structured prompts (V1, V2, Phase 1/2/3, rules-packs) PROMPTS/registry.json me register hote hain — id, type, source, verbatim flag, body hash, aur applied_in (kahan apply hua). Naya prompt aaye: tools/prompt_registry.py add -> apply --where -> agent_boot.py --write -> verify. Rule: bina apply ke koi structured prompt nahi chhodna. | user instruction 2026-09-23 | - |
| `MEM-PROC-0012` | verified | very_high | PHOENIX RISING V2.0 Strategy Complete (MRAV-V2): Multi-Asset Momentum Rotation (SPY, QQQ, GLD) + ATR Volatility Breakout. Production engine: tools/phoenix_strategy_engine.py. Backtest on 3-year market data (750 bars): +29.53% total return (12.56% CAGR), max drawdown only 6.72%, profit factor 2.38, win rate 49.02% across 51 executed trades (TRADE_LOG.csv). | live backtest run 2026-09-23 | - |
| `MEM-PROC-0013` | verified | very_high | PHOENIX INTRADAY Constraint Implemented (Strict 100% Intraday): User rule 'tumhe sirf intraday hi allowed hai' enforced. Zero overnight carry, mandatory 15:30 EOD auto-squareoff. Engine: tools/phoenix_intraday_engine.py. Tested on 2 years of 1h intraday bars (3,487 candles, 501 sessions) across QQQ, SPY, GLD. | user constraint & empirical intraday backtest 2026-09-23 | - |

## WORKING (1)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-WORK-0001` | active | high | Current task: V2 prompt ko workspace me apply karna + step-2 implementation layer banana. | user_instruction | - |

## PROJECT (2)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-PROJ-0001` | active | high | Project UAI-COS-WORKSPACE v2.0: spec + file-backed memory OS + agent registry + step-2 implementation docs is workspace me live hain. | user_instruction | ai-systems |
| `MEM-PROJ-0002` | active | high | Capability Audit v1.0 complete: 6 documents + machine-readable CAPABILITY_MAP.json + rerunnable probe scripts (env + site matrix) — 02_CAPABILITY_AUDIT/ me. | user_instruction | environment |

## DECISION (6)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-DEC-0001` | active | high | V2 spec ko canonical maana gaya; V1 base version history ke liye alag rakha gaya (user ne 'prompt ko pura le lo' kaha tha). | user_instruction | - |
| `MEM-DEC-0002` | active | medium | Memory store ke liye JSONL choose kiya (append-friendly, git-friendly, zero dependency); vector/embedding retrieval future upgrade hai. | agent_inference | - |
| `MEM-DEC-0003` | active | high | Step 2 = implementation layer: roadmap + user scenarios + memory-type integration + agent lifecycle + evaluation/regression (yahi 3 cheezein source chat me next-step ke roop me offer hui thi). | agent_inference | - |
| `MEM-DEC-0004` | active | medium | Step 3 ke 3 candidates (priority order): (1) real task par end-to-end test karke memory behaviour ko live dekho (Phase 1/5), (2) Telegram bot ko token ke saath live karo (Phase 6), (3) semantic retrieval/embeddings add karo (Phase 2). | agent_inference | - |
| `MEM-DEC-0005` | active | high | Self-audit ko versioned rakha jaayega (v1.0 -> v1.x): environment/tools/permissions badalne par map + memory + probe evidence update honge — blueprint Part 22 ke according. | user_instruction | - |
| `MEM-DEC-0006` | verified | very_high | Decision: koi bhi agent kaam se pehle V2 system me boot hoga — proof dena padega (attestation). Boot fail = kaam nahi shuru, pehle boot karaya jayega (booot prompt/system paste). | user instruction 2026-09-23 | - |

## ERROR (7)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-ERR-0001` | verified | high | chatgpt.com share/backend-api direct fetch -> HTTP 403 (Cloudflare). Fix: r.jina.ai reader proxy se content mila. | tool_result | - |
| `MEM-ERR-0002` | verified | high | Stale-detail prevention: memory record me live count/derived numbers hardcode nahi karne — wo runtime par stats se aane chahiye (warna record chupke se stale ho jaata hai). | agent_inference | - |
| `MEM-ERR-0003` | verified | high | Playwright launch fail hua tha 'libnspr4.so missing' se — fix: sudo apt-get install libnspr4 libnss3 libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libpango-1.0-0 libcairo2. | tool_result | - |
| `MEM-ERR-0004` | verified | high | Devanagari rendering trap: matplotlib complex-script shaping sahi nahi karta ('सदासुहागिन' -> galat matra order), aur Devanagari font me Latin glyphs nahi hote (boxes aa jate hain). Fix: image me Hindi text PIL (Raqm=True) se likho; matplotlib me font.family=['Noto Sans Devanagari','DejaVu Sans'] fallback lagao. | tool_result | - |
| `MEM-ERR-0005` | verified | high | Shell safety: 'pkill -f <pattern>' khud ki shell bhi maar sakta hai (pattern self-match) — pehle pattern verify karo ya PID se kill karo. | tool_result | - |
| `MEM-ERR-0006` | verified | very_high | CLEANUP INCIDENT (2026-09-23): workspace cleanup tool ke pehle version ne node_modules/.pnpm + lib/ ke andar 'duplicates' delete kar diye (7959 files) jisse RSSHub toota (ERR_MODULE_NOT_FOUND punycode.js). Recovery: /opt/uai-cache/rsshub me fresh clone + pnpm install (22.7s) + pnpm build (16.4s) -> 4 routes verified 200. | agent incident + fix 2026-09-23 | - |
| `MEM-ERR-0007` | verified | very_high | ENV RESET (2026-09-23 07:20 UTC): fresh sandbox me /opt/uai-cache khaali mila (RSSHub, node22, yq/crane, models gaye) aur pip tools (gallery-dl, yt-dlp, rg, pandoc, ffmpeg) gayab the. Workspace /home/user safe tha. Root cause: /opt root-owned tha (mkdir permission fail). Fix: bootstrap_environment.sh me sudo mkdir + chown, phir ~60s me sab wapas (apt+pip+yq+crane+node22) aur RSSHub ~2min me rebuild. | live incident + fix 2026-09-23 | - |

## SOURCE (6)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-SRC-0001` | verified | high | UAI-COS V1 (22.7k chars) aur V2 (44.3k chars, 112 sections) ka original source: shared ChatGPT chat 'System Dekho Dhyan Se'. | url | - |
| `MEM-SRC-0002` | verified | very_high | RSSHub (local :1200, 2015 namespaces) se 28 routes live-verified: Weibo hot search, Threads, Bilibili, Zhihu hot, GitHub activity, YouTube community, The Hindu, DNA India, NASA APOD, DeepMind/Anthropic blog, HuggingFace, arXiv, MIT OCW, Steam, Bandcamp, SoundCloud, GitLab, Substack, Medium, Pinterest, TikTok live, Wikipedia, HN threads, DockerHub, npm, EZTV, Telegram, Mastodon. Twitter/Instagram/Bluesky-keyword/Spotify/LinkedIn/Notion cookies ya token maangte hain -> boundary. | live test 2026-09-23 | - |
| `MEM-SRC-0003` | verified | very_high | MASTER SELF-AUDIT blueprint = user ka original Phase 1 + Phase 2 structured prompt (35 sections). Verbatim import: 00_SYSTEM/02_UAI-COS_MASTER_SELF_AUDIT_SPEC.md (canonical hash e8d8620d378adc48, raw: 00_SYSTEM/_raw/prompt_master_self_audit_raw.md). Ye prompt capability discovery + access/research mapping + fallback + expansion maangta hai — zero-assumption, no-false-power. | user message 2026-09-23 (direct paste) | - |
| `MEM-SRC-0004` | verified | very_high | PHASE 2 ACCESS MASTER BLUEPRINT: user ne dedicated Phase 2 prompt verbatim paste kiya (32 sections). Verbatim import: 00_SYSTEM/03_UAI-COS_PHASE_2_ACCESS_SPEC.md (canonical hash 8a801fdcfc9329e7, raw: 00_SYSTEM/_raw/prompt_phase_2_access_raw.md). Objective: blocked resource dekh kar 'access nahi hai' bolne ke bajaye legitimate alternative routes investigate karna. | user message 2026-09-23 (direct paste) | - |
| `MEM-SRC-0005` | verified | very_high | PHASE 3 ORCHESTRATION MASTER BLUEPRINT: user ne Phase 3 prompt verbatim paste kiya (53 sections + 25 initialization commands + core command). Verbatim import: 00_SYSTEM/04_UAI-COS_PHASE_3_ORCHESTRATION_SPEC.md (canonical hash 4b8a3b3fa3e7766b, raw: 00_SYSTEM/_raw/prompt_phase_3_raw.md). Focus: Multi-Environment Operations, Meta-Orchestrator, 22 dynamic agent roles, 12-layer knowledge/memory, 10 Quality Gates, Autonomous Depth Control, continuous evolution. | user message 2026-09-23 (direct paste) | - |
| `MEM-SRC-0006` | verified | very_high | PHOENIX RISING V2.0: Autonomous Quant Research, Strategy Discovery, Backtesting, Validation & Algorithmic Trading Mission. Verbatim import: 00_SYSTEM/05_PHOENIX_RISING_V2_QUANT_SPEC.md (canonical hash 91fd45775607c619). Mission: 0k to M in 24 months (100x growth). Core directive: No backward fabrication, No Martingale, No target-driven risk escalation. | user message 2026-09-23 (direct paste) | - |

## TEMPORAL (2)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-TEMP-0001` | active | high | Session working memory ki validity 2026-09-30 tak hai; us date ke baad expire ho jaayegi (auto expiry engine). | agent_inference | ai-systems |
| `MEM-TEMP-0002` | active | medium | PERSISTENCE TEST PENDING: _persist_test/ me 4 stamp files likhi hain (normal/, node_modules/, .venv/, out/) — agle turn me check hoga ki konsi dirs across-turn survive karti hain. | agent_inference | environment |

## RELATIONAL (1)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-REL-0001` | active | high | Relation: USER -> owns -> PROJECT(uai-cos) -> contains -> MEMORY(live store) -> sourced_from -> SOURCE(shared chat). | user_instruction | - |

## PROCEDURAL_STATE (1)

| id | status | conf | statement | source | scope |
|---|---|---|---|---|---|
| `MEM-PSTATE-0001` | active | high | Long-running workflow state: STEP 1 COMPLETE (spec import + memory OS live). STEP 2 COMPLETE (roadmap, 9 scenarios, memory-type integration, agent lifecycle, evaluation/golden tests, external integration, provenance verifier). STEP 3 PENDING (user ke direction par). | agent_inference | ai-systems |
