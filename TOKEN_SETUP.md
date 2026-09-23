# TOKEN SETUP — GitHub token banane ke exact steps (2 minute)

Aapka repo confirm ho gaya: **`Pmakwa/Agentic-ai-`** ✅ (public, khaali, default branch `main`, bana 2026-09-23)

> ⚠️ **Ek baat pehle:** ye repo abhi **public** hai. Push hone ke baad isme aapki **poori conversation,
> reports, memory** sab public me dikhega. Agar ye nahi chahte to push se pehle private kar lo:
> Repo → **Settings** → **General** → neeche **Danger Zone** → **Change repository visibility** → *Make private* → naam type karke confirm.
> (Warna public chhod do — koi dikkat nahi, bas pata hona chahiye.)

---

## Tareeka 1 — Fine-grained token (recommended, sirf ek repo ka access)

### Step-by-step

1. Ye link kholo: **https://github.com/settings/personal-access-tokens/new**
   *(Agar page na khule: GitHub → apni photo (top-right) → **Settings** → left sidebar me neeche **Developer settings** → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**)*

2. **Token name:** `uai-cos-push`

3. **Expiration:** `1 day` chuno *(sabse safe — push ke baad khud expire ho jayega)*

4. **Repository access:** ✅ **Only select repositories** → dropdown me **`Agentic-ai-`** select karo
   *(❌ "All repositories" mat chuno — zaroorat nahi)*

5. **Permissions** (neeche expand karo) → **Repository permissions** → list me **`Contents`** dhoondo →
   dropdown me **`Read and write`** karo
   *(bas yahi ek permission — baaki kuch mat chhedo)*

6. Neeche **Generate token** button dabao

7. Top par token dikhega: `github_pat_...` → **copy** karo (page band karne ke baad dobara nahi dikhega)

### Mujhe ye 2 line bhejo
```
Repo:  https://github.com/Pmakwa/Agentic-ai-.git
Token: github_pat_xxxxxxxxxxxxxxxx
```
Main turant push kar dunga (`tools/push_to_github.sh` ready hai) aur result bata dunga.

---

## Tareeka 2 — Classic token (agar upar wala UI confusing lage)

1. **https://github.com/settings/tokens/new** kholo
   *(Settings → Developer settings → Personal access tokens → **Tokens (classic)** → Generate new token (classic))*
2. **Note:** `uai-cos-push` · **Expiration:** 1 day
3. **Scopes:** sirf ✅ **`repo`** wala box tick karo *(baaki kuch nahi)*
4. **Generate token** → `ghp_...` copy karo → mujhe bhejo (wahi 2 line format)

---

## Push ke baad (safety)

1. Main push karke bata dunga — GitHub par **Actions** tab me "UAI-COS smoke checks" green hoga (provenance 4/4, audit 100/100, tests 28/28).
2. **Token revoke kar do:** https://github.com/settings/tokens → token ke saamne **Delete/Revoke**
   *(1-day expiry wala khud bhi expire ho jayega)*
3. Main token ko **kisi file me save nahi karta** aur push ke baad remote se bhi hata deta hoon.

---

## Agar token bilkul nahi banana chahte

Bina token bhi ho jayega — do tareeke:

**A) Zip upload (sabse aasan):** workspace me file ready hai → `uai-cos-repo.zip` (2.6 MB)
download karo → extract karo → repo page par **Add file → Upload files** → saari files drag-drop → **Commit changes**.
*(Dhyan: `.github/` aur `.gitignore` jaise hidden files web upload me skip ho jaate hain — wo baad me add karna padega.)*

**B) Git se push (apne computer se):** workspace se `uai-cos.bundle` (2.5 MB) download karo, phir:
```bash
git clone uai-cos.bundle uai-cos && cd uai-cos
git remote set-url origin https://github.com/Pmakwa/Agentic-ai-.git
git branch -M main && git push -u origin main --tags
```
(yahan push aapke computer ke GitHub login se hoga — koi token banane ki zaroorat nahi)

---

## Chhota FAQ

**Q: Token kya hota hai?** Ek temporary password jaisa — sirf us kaam ke liye jo aap allow karo (yahan: `Contents: Read and write` = files likhna).
**Q: Kya main token aapko chat me de sakta hoon?** Haan, par **1-day expiry** wala banao aur push ke baad **revoke** kar dena — best practice.
**Q: Fine-grained me repo list me `Agentic-ai-` nahi dikh raha?** Page refresh karo; ya "All repositories" chuno (par tab token zyada powerful ho jata hai, isliye 1-day expiry rakho).
**Q: Push ke baad kya main repo private kar sakta hoon?** Haan, kabhi bhi — Settings → General → Change visibility.
