# CAPABILITY EXPANSION ROADMAP — kya unlock karne se kitna milega

> Spec §27(M) + §22/§32. Ye roadmap **user action** vs **agent action** me banta hai (Roman Hindi).
> Har item me: kya chahiye → kya unlock hoga → effort → priority. Jo already ho chuka wo ✅ marked hai.

---

## 1. USER ACTIONS (aap kuch dein → capability jump)

| # | Kya chahiye | Unlock | Effort | Priority |
|---|---|---|---|---|
| 1 | **Reddit OAuth app** (script type, 1 min) → client id+secret | Reddit 100 QPM authorized API — redlib/pullpush par depend nahi | 1 min | ⭐⭐⭐ |
| 2 | **YouTube Data API key** (Google Cloud, free tier) | Search/trending/channel stats at scale (abhi yt-dlp/transcript tak) | 3 min | ⭐⭐⭐ |
| 3 | **Telegram bot token** (BotFather) | Notifications, reports delivery, remote commands (bot code repo me ready hai) | 2 min | ⭐⭐⭐ |
| 4 | **GitHub PAT scope check** (repo+messages permissions) | Actions control, issue/PR automation, private repos | 2 min | ⭐⭐ |
| 5 | **Platform connectors** (Google Drive / Notion / MCP) — agar platform de | Cloud files par seedha kaam (abhi user ko file bhejni padti hai) | platform dep | ⭐⭐ |
| 6 | **X (Twitter) API access ya Apify-type credit** | X full search/timeline (abhi fxtwitter bridge tak) | paid | ⭐ |
| 7 | **News/paywall account jo aap already paas rakhte hon** (aapka subscription) | Aapke apne credential se aapke liye reading — **bypass nahi, aapka access** | 2 min | ⭐⭐ |
| 8 | **Apna VPS / always-on box** (5$ tier chalta hai) | 24/7 monitoring, RSSHub local, bade jobs (sandbox turn ke baad die hote hain) | setup | ⭐⭐ |
| 9 | **Apni daily kaam ki list / priority** | Agent aapke real workflows par kaam kare, generic nahi | - | ⭐⭐⭐ |

## 2. AGENT ACTIONS (main khud kar sakta hoon / kar chuka hoon ✅)

| # | Action | Status | Kya mila |
|---|---|---|---|
| 1 | Repo-based research stack (RSSHub, redlib, pullpush, gallery-dl, yt-dlp, APIs) | ✅ | 120+ RSSHub namespaces, social subset, academic/news/finance |
| 2 | Boot + apply system (agent_boot, apply_phase, prompt_registry) | ✅ | koi bhi agent same setup khada kar sakta hai |
| 3 | Bootstrap script (fresh sandbox recovery) | ✅ (aaj verify) | 60s me toolchain + RSSHub rebuild |
| 4 | CI checks (provenance, memory audit, hygiene, phases, prompts) | ✅ | har push par quality gate |
| 5 | Monitoring (30-min route health + hygiene) | ✅ | drift detection |
| 6 | P21 — repo sweep (30+ starred tools test) | 🟡 next | aur verified tools (social/media/utility) |
| 7 | RSSHub full sweep (1765 baaki namespaces) | 🟡 queue | regional/vertical feeds |
| 8 | Local AI (Qwen 0.5B) + embeddings | ✅ (models reset ke baad re-download lagega) | offline summarize/semantic memory |
| 9 | Rate-limit profiles per API | 🟡 queue | bade research batches safely |

## 3. Capability Map versioning (spec §22)

| Version | Kab | Kya badla | Evidence |
|---|---|---|---|
| v1.0 | 2026-09-23 | Pehla self-audit: sandbox reset finding + recovery + 4 maps + report | `07_SELF_AUDIT/`, `logs/phase_apply_*.json` |
| v1.1 (next) | jab `/opt` persistence dobara check ho | persistence policy final | `probes/self_audit_env.txt` next run |
| v1.2 | P21 ke baad | naye verified tools add | repo sweep evidence |

**Update rule (koi bhi agent):** naya tool/permission/environment change aaye → `tools/self_audit.py` chalao →
`07_SELF_AUDIT/` maps refresh → version bump → memory record → push.
