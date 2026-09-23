# PUSH TO GITHUB — 3 tareeke (jo aapke liye sabse aasan ho wahi chuno)

**Sach pehle (No-False-Access):** is sandbox me **koi GitHub credential nahi hai** — `gh auth status` → "not logged in",
na token env var, na SSH key. Isliye main **yahan se push nahi kar sakta** jab tak aap token na dein.
Baki sab kuch ready hai: repo git-initialized, commit ho chuka, aur bundle ban chuka hai.

---

## Option A — Aap token do, main yahin se push kar dun (sabse aasan)

1. GitHub → **Settings → Developer settings → Personal access tokens → Fine-grained tokens**
2. Repo select karo (ya "All repositories"), permission: **Contents = Read and write**
3. Token copy karo (`github_pat_...`)

Mujhe chat me do (repo ka URL + token), jaise:
```
Repo: https://github.com/<username>/<repo>.git
Token: github_pat_xxx...
```
Main ye chalaunga:
```bash
cd /home/user/uai-cos
git remote add origin "https://<username>:<token>@github.com/<username>/<repo>.git"
git branch -M main && git push -u origin main --tags
```
> ⚠️ Security: token chat me aata hai — push ke baad usko **revoke** kar dena (ya short-expiry token banana, jaise 1 din).
> Main token ko kisi file me save nahi karunga (command ke baad remote se bhi hata dunga).

---

## Option B — Aap apne computer se push karo (token mujhe dene ki zaroorat nahi)

Repo ka bundle/zips aapke workspace me hi hain:
```
/home/user/uai-cos.bundle        # git bundle — poori history
/home/user/uai-cos-repo.tar.gz   # plain archive (git ke bina bhi kaam karega)
```
Apne computer par:
```bash
# 1) bundle se clone
git clone /path/to/uai-cos.bundle uai-cos && cd uai-cos

# 2) apna GitHub repo banao (browser me), phir:
git remote set-url origin https://github.com/<username>/<repo>.git
git branch -M main
git push -u origin main --tags
```
(yahan push aapke computer ke credentials se hoga — GitHub CLI ya password manager)

---

## Option C — Sirf files upload karo (git ki zaroorat nahi)

GitHub repo page → **Add file → Upload files** → `uai-cos-repo.tar.gz` extract karke
saari files/folders upload kar do (GitHub web upload 100 MB per file tak leta hai — hamara repo ~4 MB hai).
**Dhyan:** `.github/workflows/smoke.yml` aur hidden files web upload me skip ho jaati hain — unhe baad me add karna.

---

## Push ke baad kya check karo

1. Repo page par `AGENTS.md` aur `START_HERE.md` dikhne chahiye (root me).
2. GitHub par **Actions** tab → "UAI-COS smoke checks" workflow chalega → green hona chahiye
   (provenance 4/4, audit 100/100, tests 28/28, capability map evidence OK).
3. Kisi bhi agent ko repo connect karke bolo:
   > "AGENTS.md se start karo, CONVERSATION/00_A_TO_Z_LOG.md padho, boot-check chalao, phir aage kaam continue karo."

---

## Kya-kya repo me nahi gaya (jaan-bujh ke)

| Cheez | Kyun |
|---|---|
| `tools/rsshub/` (994 MB node_modules) | Build recipe `RUNBOOK.md` §3 me hai — clone+install se dobara ban jata hai |
| `tools/bin/yq`, `crane` (25 MB) | `bash tools/fetch_binaries.sh` se wapas aa jate hain |
| `tools/douyin_api/` (external clone) | Boundary me excluded repo hai — sirf report me mention hai |
| Koi bhi credential/token | Repo me koi secret nahi (scan kiya gaya) |

**Repo ka size:** ~4 MB (git object ke saath chhota) — GitHub par seconds me push ho jayega.
