#!/usr/bin/env bash
# UAI-COS repo -> GitHub push helper.
# Token ko file me save NAHI karta; sirf is command ke liye use karta hai, phir remote se hata deta hai.
#
# Use:
#   GITHUB_REPO="https://github.com/<user>/<repo>.git" GITHUB_TOKEN="github_pat_xxx" bash tools/push_to_github.sh
#   (ya: bash tools/push_to_github.sh https://github.com/user/repo.git github_pat_xxx)
set -euo pipefail
REPO="${1:-${GITHUB_REPO:-}}"; TOKEN="${2:-${GITHUB_TOKEN:-}}"
BRANCH="${BRANCH:-main}"
[ -n "$REPO" ]  || { echo "ERROR: repo URL nahi diya. (GITHUB_REPO=... )"; exit 1; }
[ -n "$TOKEN" ] || { echo "ERROR: token nahi diya. (GITHUB_TOKEN=...)"; exit 1; }
case "$TOKEN" in
  ghp_*|github_pat_*|ghs_*) ;; *) echo "WARN: token GitHub format jaisa nahi lagta — phir bhi try kar raha hoon.";;
esac
cd "$(dirname "$0")/.."                       # repo root
git rev-parse --git-dir >/dev/null 2>&1 || { echo "ERROR: ye git repo nahi hai."; exit 1; }

AUTH_URL="$(printf '%s' "$REPO" | sed -E "s#https://#https://x-access-token:${TOKEN}@#")"
cleanup(){ git remote remove uai-push 2>/dev/null || true; }
trap cleanup EXIT

git remote remove uai-push 2>/dev/null || true
git remote add uai-push "$AUTH_URL"
echo "-> branch: $BRANCH | commits: $(git rev-list --count HEAD) | files: $(git ls-files | wc -l)"
git branch -M "$BRANCH"
git push uai-push "$BRANCH" --tags --force-with-lease
echo "✅ PUSH OK -> $REPO ($BRANCH)"

# friendly post-push info (token ke bina)
SAFE_URL="$(printf '%s' "$REPO" | sed -E 's#//[^@]*@#//#')"
echo "   repo: $SAFE_URL"
echo "   agla step: GitHub par Actions tab check karo -> 'UAI-COS smoke checks' green hona chahiye."
echo "   security: push ke baad is token ko revoke kar dena (Settings -> Developer settings -> Tokens)."
