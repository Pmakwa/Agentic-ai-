# GITHUB UNLOCK — poori khangal (2026-09-23)

> Sawaal: *"GitHub se kya capabilities unlock kar sakte ho, konse access unlock kar sakte ho?"*
> Method: 24 live probes (evidence: `probes/phase_gh_probe*.txt`), sab kuch **actually test kiya** — jo fail hua wo bhi likha hai.
> Toolkit: `tools/github_unlock.py` (12 commands, sab verified)

---

## 1. Ek line ka jawab

**Bina kisi token ke GitHub 7 tarah ki capability deta hai:** software (binaries), source code, data, packages, containers, research/intel, aur trending/discovery.
**Sirf 5 cheezein token maangti hain:** code search API, gh CLI, GraphQL, Actions logs, aur write operations (push/gist/PR).

---

## 2. GITHUB ACCESS MATRIX (verified)

| Capability | Bina token | Evidence |
|---|---|---|
| **API: repo metadata** | ✅ | `cli/cli` → ★46,377, MIT, Go (live) |
| **API: repo search** | ✅ 10/min | "whisper cpp" → 2,325 results |
| **API: issues search** | ✅ | yt-dlp cookies → 3,111 issues |
| **API: security advisories** | ✅ | GHSA-wx4m… critical (Home Assistant XSS) |
| **API: gists (public read)** | ✅ | public gist list aayi |
| **API: releases + assets** | ✅ | yq v4.53.6 assets live |
| **raw.githubusercontent** | ✅ (no quota) | yt-dlp version.py 200; COVID CSV **5.5 MB** |
| **codeload zip** | ✅ | Hello-World zip 200 |
| **git clone --depth 1** | ✅ **2 sec** | cli/cli 41 MB clone |
| **wiki clone** | ✅ | git/git wiki `Home.textile` |
| **Release binary download + execute** | ✅ | **yq v4.53.6** download → chmod → `--version` → JSON parse (`.b` → 42) |
| **pip install git+https** | ✅ | blessings GitHub se install hua |
| **GH Archive (public event data)** | ✅ | 18.2 MB gz, **5,000 events parsed** (PushEvent 4,010) |
| **Public container images (bina Docker)** | ✅ | **crane** se alpine:latest export → 8.7 MB tar, **515 files**, alpine-release 3.24.2 |
| **ghcr.io manifest** | ✅ | uv:latest manifest 200 (2,196 B) |
| **Trending** | ✅ (substitute) | search API `created:>date&sort=stars` |
| **API: code search** | ❌ **401** | "Requires authentication" — **token zaroori** |
| **gh CLI** | ❌ | auth ke bina refuse |
| **GraphQL** | ❌ 0/0 | token ke bina nahi |
| **Actions logs/artifacts** | ❌ | token zaroori |
| **Push / gist create / PR** | ❌ | token + (user confirmation) |

---

## 3. GITHUB SE JO NAYI CAPABILITIES UNLOCK HUI (7 categories)

### 3a. Software source — "GitHub = duniya ka software store"
Release assets se **static binaries** seedha mil jaate hain, chahiye sirf download + chmod.
Verified: `yq` (JSON/YAML processor, 5.7 MB) aur `crane` (container tool, 16.5 MB) — dono persist hote hain; **2026-09-23 se `/opt/uai-cache/bin/` me** (workspace clean rakhne ke liye).
Matlab: koi bhi tool jiska GitHub release hai (ffmpeg static, bat, fzf, delta, hugo, duckdb CLI…) bina package manager install ho sakta hai.

### 3b. Source code — research + reuse ke liye
`git clone --depth 1` **2 second** me chala (cli/cli, 41 MB). Iske alawa:
- **codeload zip** (bina git)
- **raw file fetch** (single file, no API quota) — audits, configs, data
- **wiki clone** — project documentation bhi mil jaati hai
Isse "kisi bhi open-source project ka code padho, chalао, reuse karo" — fully verified.

### 3c. Data — GitHub ek data source bhi hai
- **GH Archive**: har ghante ka **public GitHub event data** (18 MB/hour) — konsa repo trending hai, kis language me activity, 5000 events sample parse ho gaya.
- **Dataset repos**: raw CSV (COVID countries 5.5 MB) direct mila.
- **Awesome lists / curated repos** = meta-resources (naye tools/datasets dhunde ke liye).

### 3d. Packages — PyPI ke bina install
`pip install git+https://github.com/...` verified — jab koi package PyPI par latest na ho, ya fork/patched version chahiye.

### 3e. Containers — **Docker ke bina** public images 🔥
`crane` (khud GitHub release se aaya) se:
- `crane export alpine:latest` → 8.7 MB tar, **515 files** extract hue (`etc/alpine-release` = 3.24.2)
- ghcr.io manifests bhi 200
Iska matlab: kisi bhi public container image ke andar ki files nikaal kar use kar sakte hain — Docker daemon ki zaroorat nahi.

### 3f. Research / intel
- **Issues search API** — kisi bhi project ke real-world problems/solutions (e.g., yt-dlp ke cookie issues 3,111)
- **Security advisories API** — CVE/GHSA database bina key
- **Release notes / changelogs** — API se structured

### 3g. Discovery
Trending page (HTML ab React-rendered hai, parse nahi hua) → **substitute verified**: `search/repositories?q=created:>date&sort=stars` — aaj ke top naye repos (laya ★17k, ZCode ★6.4k).

---

## 4. LIMITS (honest — kitna kharch, kitni deewar)

| Limit | Value | Kaise jeetein |
|---|---|---|
| Core API (unauth) | **60 req/hour** | 43 bachi thi test ke baad; token se 5,000/hr |
| Search API (unauth) | 10 req/min | batches me chalाओ |
| Code search | **0 (401)** | token chahiye |
| GraphQL | 0 | token chahiye |
| gh CLI | auth-less refuse | token ya `GH_TOKEN` env |
| grep.app | 429 | alternate code search work nahi kiya |
| searchcode.com API | 404 | endpoint badal gaya |
| Clones | no strict limit | depth-1 rakhо (41 MB vs full history) |

## 5. TOKEN SE KYA-KYA KHULEGA (user action — 3 minute ka kaam)

**Ek fine-grained PAT banao** (github.com → Settings → Developer settings → Fine-grained tokens):
- **Public repos: read-only** (koi scope nahi chahiye) → code search + 5,000 req/hr + GraphQL
- Optional: `gist` (gists banana), `workflow` (Actions), `repo` (agar apne private repos chahiye)

| Token ke saath ye unlock hote hain | Value |
|---|---|
| **Code search API** | kisi bhi public repo me code dhundhna (abhi 401) |
| **Rate 5,000/hr** | 83× zyada research capacity |
| **gh CLI** | `gh search code`, `gh run list`, `gh api` — poora workflow |
| **Actions logs/artifacts** | CI results, build artifacts |
| **GraphQL** | efficient bulk queries |
| Gist create / repo create | write (user confirmation ke saath hi — rule MEM-CONS-0003) |

Token `.env` me `GH_TOKEN=...` daalna hai; `gh auth login --with-token` bhi chalega. **Ye credential user ke paas rahega — main use nahi maangunga, sirf env me hone par use karunga.**

---

## 6. PRACTICAL RECIPES (jo abhi chal rahe hain)

```bash
python3 tools/github_unlock.py rate                      # kitni quota bachi
python3 tools/github_unlock.py repo yt-dlp/yt-dlp        # repo info
python3 tools/github_unlock.py search "rag framework"    # repo discovery
python3 tools/github_unlock.py issues "repo:x is:issue crash"   # problem research
python3 tools/github_unlock.py advisories                # security intel
python3 tools/github_unlock.py release owner/repo        # latest + assets
python3 tools/github_unlock.py getbin mikefarah/yq linux_amd64   # binary install
python3 tools/github_unlock.py clone cli/cli             # depth-1 clone
python3 tools/github_unlock.py trending                  # naye top repos
python3 tools/github_unlock.py archive 2026-09-22-12     # GH event data
python3 tools/github_unlock.py container alpine:latest   # image export (no Docker)
```

`tools/bin/` me already ready: **yq** (JSON/YAML), **crane** (containers). PATH me jodo: `export PATH="$HOME/uai-cos/tools/bin:$PATH"`

## 7. JO NAHI MILA / FAIL HUA (bina lipa-poti)

| Koshish | Result |
|---|---|
| GitHub code search (bina token) | ❌ 401 — token ke bina possible nahi |
| Trending HTML parse | ❌ React payload me hai; substitute use kiya |
| grep.app | ❌ 429 (blocked) |
| searchcode.com | ❌ 404 (API path dead) |
| GitHub Actions trigger | ❌ token ke bina entry nahi |
| LFS large files | ⚠️ test nahi kiya (bandwidth limits ho sakti hain) |

## 8. Evidence files
`probes/phase_gh_probe.txt` (15 checks) · `probes/phase_gh_probe2.txt` (9 checks) · `tools/github_unlock.py` · `/tmp` artifacts: `_gha.json.gz` (GH Archive 18 MB), `_alpine.tar` (container export), `_yq.tgz`, `_crane.tgz`
