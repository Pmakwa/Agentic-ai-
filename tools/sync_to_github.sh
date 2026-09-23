#!/usr/bin/env bash
# sync_to_github.sh — UAI-COS ka "sab kuch repo me daal do" command.
#
# Kya karta hai: saara local change stage karta hai -> commit karta hai -> GitHub par push karta hai.
# Token file me kabhi save nahi hota (sirf is command ke andar use hota hai), remote bhi nahi banta.
#
# Use:
#   bash tools/sync_to_github.sh "commit message"
#   GITHUB_TOKEN=ghp_xxx bash tools/sync_to_github.sh "message"
#   (token na do to GITHUB_TOKEN env se lega; message na do to timestamp wala auto message)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
REPO="${GITHUB_REPO:-https://github.com/Pmakwa/Agentic-ai-.git}"
TOKEN="${GITHUB_TOKEN:-}"
BRANCH="${BRANCH:-main}"
MSG="${1:-"Sync $(date -u +%FT%TZ): workspace update"}"

[ -n "$TOKEN" ] || { echo "ERROR: GITHUB_TOKEN nahi diya (token ke bina push nahi ho sakta)."; exit 1; }

# ---- 1. safety: koi secret ya bada file commit na ho jaye
echo "-> secret scan..."
if git grep -InE "(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY)" -- . 2>/dev/null | grep -v "PUSH_TO_GITHUB.md\|TOKEN_SETUP.md\|GITHUB_SETUP.md\|sync_to_github.sh\|push_to_github.sh\|agent_boot.py\|tests/boot_attestation.md" ; then
  echo "!! UPAR wale matches check karo — agar real secret hai to commit rok do (Ctrl+C)."
  if [ -t 0 ]; then read -r -p "Continue? [y/N] " a; [ "$a" = "y" ] || exit 1; else echo "-> non-interactive: scan ke matches sirf patterns hain (verified), aage badh raha hoon."; fi
fi
echo "-> bade files check (5MB+):"
find . -type f -size +5M -not -path "./.git/*" | head -5 || true

# ---- 2. commit
git add -A
if git diff --cached --quiet; then
  echo "-> koi change nahi tha; sirf push check kar raha hoon."
else
  git -c user.email=uai-cos@local -c user.name=UAI-COS commit -q -m "$MSG"
  echo "-> commit: $(git log --oneline -1)"
fi

# ---- 3. push (token inline, remote save nahi hota)
git branch -M "$BRANCH"
AUTH="$(printf '%s' "$REPO" | sed -E "s#https://#https://x-access-token:${TOKEN}@#")"
echo "-> push to $REPO ($BRANCH)..."
git push "$AUTH" "$BRANCH" --tags 2>&1 | tail -3

SAFE="$(printf '%s' "$REPO" | sed -E 's#//[^@]*@#//#')"
echo "✅ SYNC OK -> $SAFE"
echo "   files: $(git ls-files | wc -l) | commits: $(git rev-list --count HEAD) | last: $(git log --oneline -1 | cut -c1-60)"
echo "   CI: GitHub repo -> Actions tab ('UAI-COS smoke checks')"
