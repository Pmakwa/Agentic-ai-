# PROJECT BOARD CARDS — ready to paste (GitHub Project ya Issues me)

> Kaise use karein: GitHub Project board kholo → **Add item** → "Create draft" me Title + Body paste karo.
> (Ya: repo ke Issues me ek-ek karke naye issue banao, phir board me "Add items" se add karo.)
> Ye cards `AGENTS.md` §5 ke open threads + current state se banaye gaye hain.

---

## P0 — Foundation (ho chuka, sirf verify karna hai)

**1. Boot-check pass karo (provenance 4/4, audit 100/100, tests 28/28)**
Body:
```bash
python3 tools/verify_provenance.py        # 4/4 PASS
python3 tools/uai_mem.py audit | tail -3  # 100/100
bash tests/test_memory_os.sh | tail -3    # 28 passed / 0 failed
python3 tools/social_unlock.py status     # routes live?
```
Fail ho to `RUNBOOK.md` §1 (bootstrap) chalao.

**2. Repo GitHub par push karo (150 files, 3 commits, 2.5 MB)**
Body: `GITHUB_SETUP.md` follow karo. Push ke baad Actions tab me "UAI-COS smoke checks" green hona chahiye.

---

## P1 — Abhi ke open kaam

**3. RSSHub ke baaki namespaces verify karo (2015 me se)**
Body: `/vimeo/user`, `/spotify/*`, `/hackernews/*`, `/zhihu/*`, regional news routes test karo.
Sab kuch `tools/social_unlock.py rsshub <route>` se check hota hai. Jo chale, `06_REPO_HUNT/00_REPO_UNLOCK_REPORT.md` me add karo.
Server restart: `RUNBOOK.md` §3(e).

**4. Verified routes ko monitor me daalo (30-min health cycle)**
Body: `tools/route_monitor.py` me naye routes add karo (redlib instances, RSSHub /threads, /weibo, pinterest-dl).
`systemctl status uai-cos-monitor.timer` — oneshot ka `inactive (dead)` = SUCCESS (failure nahi).

**5. Dead/live instance health tracker banao (redlib + bridges)**
Body: `redlib_instances` ki list (GitHub: redlib-org/redlib-instances) 6 ghante me ek baar check karo;
jo 429/502 de rahe hain unhe `redlib_working.txt` se hata ke next best instance me fallback karo.
Script me auto-fallback already hai — bas list update karni hai.

---

## P2 — Naye routes (test karke add karne wale)

**6. Discord public invite info (bina token)**
Body: `https://discord.com/api/v9/invites/<code>?with_counts=true` — public endpoint hai, test karo. Kaam kare to `social_unlock.py` me `discord` subcommand add karo.

**7. Spotify public endpoints (bina token)**
Body: `open.spotify.com/oembed?url=<track/album>` test karo; RSSHub `/spotify/*` bhi dekho.

**8. Pullpush / Reddit archive retry (rate-limit ke saath)**
Body: `api.pullpush.io` ko 30–60 s gap par hit karo; agar chale to redlib ke saath **second Reddit route** ban jayega (archives ke liye). Evidence `probes/` me save karo.

**9. Instagram ke legit raste dobara check karo (sirf official)**
Body: Instagram Graph API (business account) — user se creds maango. Bina creds koi legit route nahi (429/login wall) — ye conclusion `CAPABILITY_MAP.json` me already hai, isliye **bypass try mat karo** (§24).

---

## P3 — System hygiene

**10. Naya capability add karte waqt "definition of done" follow karo**
Body: install → live test → evidence `probes/` me → report update → `CAPABILITY_MAP.json` version bump →
`uai_mem.py add` → `index` + `dash` + `audit` (100/100) → `README.md` + `index.html` sync → user ko Hindi summary + options.

**11. Memory hygiene (har kaam ke baad)**
Body: `python3 tools/uai_mem.py stats` — count badhta rahe; stale records ko `supersede` karo (`expire` nahi).

**12. Keyed APIs ka wait-list (jab user keys de)**
Body: Reddit OAuth (`praw` installed) · YouTube Data API · Telegram BotFather (2 min) · Discord bot · Meta app (business) · Pinterest app.
Jab key mile: `.env` file banao (`.gitignore` me already hai — commit mat karo), phir live test karo.

---

## Board ke labels (suggestion)

`P0-foundation` · `P1-active` · `P2-new-routes` · `P3-hygiene` · `verified` · `blocked` · `needs-creds` · `evidence`
