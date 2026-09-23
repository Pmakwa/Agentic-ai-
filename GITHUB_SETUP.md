# GITHUB SETUP — 2 minute me repo ban jayega (phir main push kar dunga)

## Pehle ek zaroori farq samjho

| Cheez | Kya hai | Files push hoti hain? |
|---|---|---|
| **Repository** (`github.com/Pmakwa/Agentic-AI`) | code + docs ka ghar | ✅ **Haan** — yahi chahiye |
| **Project** (`github.com/users/Pmakwa/projects/1`) | kanban board (cards/tasks) | ❌ **Nahi** — board me sirf issues/notes hote hain |

Aapne jo link diya wo **Project board** ka hai — usme main repo push nahi kar sakta (technically impossible).
Iske liye **repository** chahiye. Saath me, checkout kiya:

- `github.com/users/Pmakwa/projects/1` → **HTTP 404** (bina login, private board dikhta nahi — theek hai)
- `api.github.com/repos/Pmakwa/Agentic-` → **HTTP 404** (matlab: repo public nahi hai — ya private hai, ya naam adhoora hai)
- Aapke account ke public repos abhi: `Pm`, `biisal-filter-bot`, `Movieshub`, `Movieshubbot`

---

## Step 1 — Repo banao (30 seconds)

1. https://github.com/new kholo
2. **Repository name:** `Agentic-AI` (ya jo aap chaaho — **README/add-ons kuch bhi add mat karo**, khaali repo rakho)
3. Visibility: **Private** recommended (kyunki isme aapki poori conversation hai) — baad me public bhi kar sakte ho
4. **Create repository** dabao

## Step 2 — Token banao (60 seconds)

1. https://github.com/settings/personal-access-tokens/new kholo
   *(ya: Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token)*
2. **Token name:** `uai-cos-push`
3. **Expiration:** 1 day (safest) ya 7 days
4. **Repository access:** Only select repositories → `Agentic-AI`
5. **Permissions → Repository permissions → Contents: Read and write** (bas yahi)
6. **Generate token** → token copy karo (`github_pat_...`)

## Step 3 — Mujhe bhejo (1 message)

```
Repo:  https://github.com/Pmakwa/Agentic-AI.git
Token: github_pat_xxxxxxxxxxxxxxxx
```

Main ye chalaunga (script already ready hai `tools/push_to_github.sh`):
```bash
GITHUB_REPO="https://github.com/Pmakwa/Agentic-AI.git" \
GITHUB_TOKEN="github_pat_..." bash tools/push_to_github.sh
```
→ 150 files, 3 commits, 2.5 MB — **30 seconds me push ho jayega**.
Phir main aapko bata dunga: GitHub par **Actions** tab me "UAI-COS smoke checks" green aaya ya nahi.
**Push ke baad token revoke kar dena** (main token kisi file me save nahi karta, remote se bhi hata deta hoon).

---

## Agar aap khud push karna chaho (mujhe token dene ki zaroorat nahi)

Workspace me ready files:
```
/home/user/uai-cos.bundle        (git bundle — poori history)
/home/user/uai-cos-repo.zip      (plain zip — Windows ke liye best)
/home/user/uai-cos-repo.tar.gz   (Linux/Mac)
```
Apne computer par:
```bash
git clone /path/to/uai-cos.bundle uai-cos && cd uai-cos
git remote set-url origin https://github.com/Pmakwa/Agentic-AI.git
git branch -M main && git push -u origin main --tags
```
Ya sirf web upload: repo page → **Add file → Upload files** → zip extract karke saari files drag-drop → Commit.

---

## Agar aap chahte ho ki Project board bhi use ho

Board ke liye maine **ready cards** bana diye hain: `PROJECT_BOARD/CARDS.md`
(board → "Add item" → draft note me title/body paste kar do, ya unhe issues bana ke board me add kar lo).
Board me code nahi jaata — board **kaam track karne** ke liye hai, repo **kaam rakhne** ke liye.

---

## Ye sab kyun — ek line me

Repo = almari (samaan rakhta hai) · Project = notice board (kaam track karta hai) · Token = chabi (jiske bina main
aapki almari me kuch nahi rakh sakta — verified: is sandbox me koi GitHub credential nahi hai).
