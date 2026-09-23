# SP-005 — Phase 3 — repo hunt + apply (GitHub repos ko capability me badlo)

<!-- structured prompt entry | type: phase | verbatim: false | source: user structured prompt (conversation) + continue-instruction | body_sha256_16: 1fb384c1d6e99c2e | added: 2026-09-23 -->
| field | value |
|---|---|
| Type | `phase` |
| Source | user structured prompt (conversation) + continue-instruction |
| Verbatim user text? | nahi (reconstructed) |
| Applied in | 06_REPO_HUNT/, 05_SOCIAL_UNLOCK/, tools/social_unlock.py, PROJECT_BOARD/phases.json |

---

# Phase 3 (reconstructed)

GitHub par jo open-source repos/tools hain unhe dhoondo, **test karo, aur jo kaam kare unhe lock karo** —
phir sab kuch repo me likho taaki koi bhi agent wahi system apply kare.

**Kya apply hua:**
- `06_REPO_HUNT/00_REPO_UNLOCK_REPORT.md` (15 repos, boundary-excluded bhi likhe)
- `tools/social_unlock.py` (reddit/rsshub/gallery/pin/transcript/comments/x/bsky/invite/spotify/pullpush/status)
- `tools/rsshub_verify.py` -> 28 curated + **120/250 namespaces live**
- `tools/github_unlock.py`, redlib instances, gallery-dl (TikTok/Bluesky/Pinterest), yt-dlp, transcript API
- Phase system: `phases.json` + `phase_runner.py` + `import_prompt.py` (naya prompt aate hi auto-apply)
