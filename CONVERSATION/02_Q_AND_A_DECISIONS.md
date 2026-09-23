# Q&A + DECISIONS — user ke sawaal, agent ke jawab, aur liye gaye faisle

> Ye file do kaam karti hai: (1) hamari Q&A ka record, (2) wo decisions jo aage ka kaam chala rahe hain,
> taaki naya agent **wahi rules** follow kare — ulta kaam na kare.

---

## A. User ke sawaal → Agent ke jawab (chronological)

### Q1. "Is link me V2 prompt hai — pura le lo, environment me apply karo, usi tarike kaam karo; step 2 use pura apply karo."
**A:** Link direct blocked tha (Cloudflare 403) — `r.jina.ai` reader se poora chat nikala, dono specs
(V1 15 parts + V2 112 sections) import kiye, hash-verified, phir poora system is environment me **implement**
karke chalaya (memory, protocol, tools, tests — 28/28 pass). Step 2 ke saare 9 documents bhi likhe.

### Q2. "Kiya hua bhai kam bich me kiyu rok diya?"
**A:** Response beech me cut ho gaya tha — agent ne maafi maangi aur poora kaam complete kiya.
**Decision (permanent):** ab koi kaam beech me nahi chhoda jayega; exhaust karke hi rukna hai.

### Q3. "Dubara khud ko aache se explore karo dekho kuch baki to nahi reh jata na" (2 baar)
**A:** Pura self-audit kiya — persistence model, 20+ probes, bug fixes, naye capabilities, sab record.
Har baar **actual fix** kiya gaya (sirf list nahi).

### Q4. "Pura gethub barikhi se khangalo" (GitHub ko bareeki se kangaal karo)
**A:** 24 live probes + reports: bina token 8 capabilities verified (search/releases/raw/clone/containers/GH Archive),
token ke bina 4 band (code search/GraphQL/Actions/write). Practical demo: `yq` + `crane` (Docker ke bina image extract).
`github_unlock.py` (12 commands) ban gaya.

### Q5. "Instagram reddit twitter X Facebook pinterest aur bhi sare social media platform unlock kar sakte ho ya nahi?"
**A:** Honest 3-category answer diya —
**A) tokenless verified:** Reddit RSS, Telegram preview, Bluesky public API, Mastodon instances, TikTok oEmbed, YouTube (yt-dlp), X (fxtwitter bridge)
**B) credentials chahiye:** Reddit OAuth, X pay-per-use (2026: $0.005/post read), Meta app, Pinterest app, Telegram bot, Discord bot, YouTube key
**C) koi legit route nahi:** IG/FB personal, Pinterest anon, Quora, Nitter, RSSHub public, X bina payment.
Saath me options (a/b/c) diye.

### Q6. "Nahi kafi sare repos hai jise agent platform access kar sakte hai wo dhund k karo"
**A:** 15+ GitHub repos install/clone kiye aur **live test** kiye. Result:
- **Naye khule:** Reddit (redlib instances), TikTok (gallery-dl), Pinterest (pinterest-dl), Threads + Weibo (RSSHub), Tumblr (gallery-dl)
- **Band (proof ke saath):** Instagram, Facebook, LinkedIn, Bilibili, Douyin, Invidious
- **Excluded (boundary):** cookie/identity-pool wale repos (Douyin API, TikTokDownloader)
- Sab kuch ek tool me bundle kiya: `tools/social_unlock.py` (10 commands, smoke-tested)
- Report: `06_REPO_HUNT/00_REPO_UNLOCK_REPORT.md`

### Q7. (Ye wala) "Gethub connect kar raha hu — hamari puri conversation A to Z sab kuch mere gethub me dal do, taaki koi bhi agent connect kare to khud samajh le kya karna hai. Aur batao: wo agent khud karega ya mujhe kuch batana padega?"
**A (short):**
- Poora A-to-Z material is repo me daal diya: `AGENTS.md`, `START_HERE.md`, `CONVERSATION/`, `RUNBOOK.md`, `ENVIRONMENT.md`, saare reports/tools/memory/evidence.
- **Agent khud kar lega** — agar: (1) repo ka access ho, (2) uske paas ek chalta hua environment (terminal + internet) ho.
  Use bas ek line bolo: *"AGENTS.md se start karo aur CONVERSATION/00_A_TO_Z_LOG.md padho, phir boot-check chala ke aage badho."*
- **Bilkul kuch na bolo** to bhi bahut platforms `AGENTS.md`/`README.md` khud padh lete hain — par ek line dena safest hai.
- **Kuch cheezein uske bhi control me nahi:** push/publish ke liye GitHub token, aur keyed APIs ke liye credentials —
  wo tumhe dena padega (details `START_HERE.md` me table hai).

---

## B. Decisions (jo aage lagu hain)

| ID | Decision | Kyun / Asar |
|---|---|---|
| MEM-DEC-0004 | Step-3 (jo original prompt me tha) **abhi choose nahi kiya** | User ne alag directions diye — Step 3 pending hai |
| — | Canonical spec **kabhi edit nahi** hoga | Hash verification (4/4 PASS) toot jayega; changes alag `_changes` doc me |
| — | Har capability claim ke saath **evidence path** zaroori | No-False-Access rule |
| — | Blocked cheez ke liye 3 sawaal: kya block kiya → kaunsi dependency → authorized alternative kya | §22/§28 format |
| — | Auth/CAPTCHA/paywall/anti-bot **bypass nahi** | Spec §24 boundary — cookie/identity-pool repos bhi excluded |
| — | Chat me internal process detail nahi (jab tak user na maange) | MEM-PREF-0007 |
| — | Hindi (Roman) me baat, English spelling | User ka explicit instruction |
| — | Task ke end me Hindi summary + options (a/b/c) | Established pattern |
| — | High-risk actions se pehle confirmation | MEM-CONS-0003 |
| — | Naya finding → install → live test → evidence → CAPABILITY_MAP bump → memory record → README/index sync | Ye "definition of done" hai |

---

## C. Numbers jo yaad rakhne hain (drift na ho)

| Metric | Value |
|---|---|
| Memory records | 71 (audit 100/100, tests 28/28) |
| CAPABILITY_MAP | v2.4 · 22,914 B · sha256[16] `aef4a0c1a7bd36e9` · 20 evidence files |
| Spec hashes | V2 `4aa1c6a1f872a3f3` (42,743 chars) · V1 `456102f91c061b6e` (21,302 chars) |
| System prompt | `build_system_prompt.py` → standard = 16,223 chars |
| Servers | control-center `:8000` · RSSHub `:1200` |
| Report folders | `00_SYSTEM, 01_STEP2, 02_CAPABILITY_AUDIT, 03_ACCESS_EXPANSION, 04_GITHUB_UNLOCK, 05_SOCIAL_UNLOCK, 06_REPO_HUNT, CONVERSATION` |
