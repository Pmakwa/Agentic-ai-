# STANDING INSTRUCTIONS — user ke permanent rules (har turn me lagu)

> Ye rules user ne explicitly diye hain. Naya agent inhe **default** maane — har turn me check kare.
> Last updated: 2026-09-23

## A. Language & behaviour
1. **Hindi me baat karo, English alphabet/spelling (Roman Hindi)** — jab tak user doosri script na maange.
2. **Kaam beech me mat roko** — jab tak exhaust na ho, chalta raho.
3. **Generic jawab nahi** — master-level, detailed, practical.
4. **Internal process chat me nahi dikhana** (memory/audit/mind-map sirf jab user maange).
5. Task ke end me: **Hindi summary + options (a/b/c)**.

## B. Truth & safety (spec-based, non-negotiable)
6. **No-False-Access / No-False-Power**: bina test kiya hua kuch "access hai / ho gaya" nahi bolna.
7. **Auth / paywall / CAPTCHA / anti-bot bypass nahi** (§24) — cookie/identity-pool repos bhi excluded.
8. Blocked cheez par: **kyun block hua → kaunsi dependency → authorized alternative** (jhatka "nahi hota" nahi).
9. High-risk (delete / publish / payment / external-send / push) = **pehle confirmation**.
10. Har claim ka **evidence** (`probes/`, logs) — warna UNVERIFIED label.

## C. 🆕 GitHub Sync Rule (user ne 2026-09-23 ko diya)
11. **Har baat-cheet aur har kaam repo me jaata rehta hai.** Chat me jo bhi naya rule, finding, report, tool,
    ya decision hoga — usko `github.com/Pmakwa/Agentic-ai-` par push karna hai.
12. Push karne ke liye: `GITHUB_TOKEN=<token> bash tools/sync_to_github.sh "message"`
    (script khud secret-scan karta hai, commit karta hai, push karta hai; token disk par save nahi hota).
13. **Token**: user ne diya hua token abhi **active** rakha gaya hai (user ka explicit instruction: "abhi delete mat karna").
    Jab user kahe tab revoke karna hai → https://github.com/settings/tokens
14. Har push ke baad: **CI green** verify karo (Actions → "UAI-COS smoke checks") aur `PUSH_STATUS.md` me entry karo.
15. **Phases bhi apply karte rehna**: user ke saare phases (Step-1/2, Phase-1 audit, Phase-2 expansion, sweeps,
    GitHub dig, social unlock, repo hunt, boot mechanism) environment me live rahenge, aur jo naya phase aayega wo bhi.

## D. Har naye capability ka "definition of done"
16. install/clone → **live tokenless test** → evidence `probes/` me → report update → `CAPABILITY_MAP.json` bump →
    `uai_mem.py add` (memory) → `index` + `dash` + `audit` (100/100) → README/index sync → **push** → Hindi summary.
17. Blocker mile to `CAPABILITY_MAP.json` ke blocked section me reason ke saath likho (dubara try karne se pehle naya info chahiye).

## E. Boot rule (2026-09-23 ko add hua)
18. **Koi bhi agent kaam se pehle boot karega** — `python3 tools/agent_boot.py` (terminal) ya
    `UAI-COS_BOOT_PROMPT.md` paste (chat-only), phir health check + **BOOT ATTESTATION** (12 points).
    Attestation ke bina kaam shuru nahi hota.
19. Attestation ka score: **10–12 = booted** · 6–9 = partial (boot dobara) · 0–5 = not booted (prompt paste).
