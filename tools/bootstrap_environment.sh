#!/usr/bin/env bash
# PERSISTENCE-AWARE (v2, 2026-09-23): /opt aur /var/tmp turns ke beech persist karte hain.
# Browser/cache/model pehle se ho to download skip — sirf verify.
# bootstrap_environment.sh — UAI-COS session bootstrap (Capability Map v1.1 ke findings par)
#
# VERIFIED (2026-09-23):
#   survives : /home/user files, /usr me apt+pip installs, memory store
#   wipes    : /home/user/.cache, node_modules, .venv, out; running processes/ports
#   fix      : heavy caches /opt me (sudo + chown) => browser + embedding model
#
# Usage: bash tools/bootstrap_environment.sh
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright
export FASTEMBED_CACHE_PATH=/opt/uai-cache/fastembed
export HF_HOME=/opt/uai-cache/hf
say() { printf "\n== %s\n" "$*"; }

say "0) persistent dirs (/opt)"
if [ ! -d /opt/ms-playwright ]; then
  sudo -n mkdir -p /opt/ms-playwright /opt/uai-cache/{fastembed,hf} 2>/dev/null \
    && sudo -n chown -R "$(id -u):$(id -g)" /opt/ms-playwright /opt/uai-cache 2>/dev/null \
    && echo "created /opt dirs" || echo "WARN: /opt banana fail (sudo?)"
else echo "/opt dirs maujood"; fi

say "1) apt packages"
MISS=""; for c in sqlite3 tesseract ffmpeg espeak-ng jq; do command -v "$c" >/dev/null || MISS="$MISS $c"; done
[ -n "$MISS" ] && sudo -n apt-get install -y -qq --no-install-recommends $MISS >/dev/null 2>&1 && echo "apt: installed$MISS" || echo "apt: $( [ -n "$MISS" ] && echo "install issue" || echo 'sab present')"

say "2) fonts (Devanagari + emoji — Debian 13 me 'fonts-noto-core' hai, 'fonts-noto-devanagari' NAHI)"
fc-list 2>/dev/null | grep -qi devanagari || sudo -n apt-get install -y -qq --no-install-recommends fonts-noto-core fonts-noto-color-emoji >/dev/null 2>&1
echo "fonts: $(fc-list 2>/dev/null | wc -l) total, $(fc-list 2>/dev/null | grep -ic devanagari) devanagari"

say "3) browser libs + chromium (persistent /opt path)"
ldconfig -p 2>/dev/null | grep -q libnspr4 || sudo -n apt-get install -y -qq libnspr4 libnss3 libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libpango-1.0-0 libcairo2 >/dev/null 2>&1
[ -d /opt/ms-playwright/chromium_headless_shell-* ] 2>/dev/null || python3 -m playwright install chromium >/dev/null 2>&1
ls -d /opt/ms-playwright/chromium* >/dev/null 2>&1 && echo "chromium: /opt me OK" || echo "chromium: MISSING"

say "4) python packages"
python3 - <<'PY'
import importlib.util, subprocess, sys
want = ["playwright","fastembed","onnxruntime","flask","fpdf2","python-pptx","python-docx","openpyxl","pypdf","html5lib","pandas","matplotlib"]
alias = {"fpdf2":"fpdf","python-pptx":"pptx","python-docx":"docx"}
miss = [w for w in want if not importlib.util.find_spec(alias.get(w, w))]
if miss:
    print("installing:", miss); subprocess.run([sys.executable,"-m","pip","install","-q",*miss])
else: print("pip: sab present")
PY

say "5) verify (browser + embeddings + memory)"
PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('https://example.com',timeout=30000)
    print('  browser OK ->', pg.title()); b.close()" 2>/dev/null || echo "  browser: FAIL"
FASTEMBED_CACHE_PATH=/opt/uai-cache/fastembed python3 -c "
from fastembed import TextEmbedding
m=TextEmbedding('sentence-transformers/all-MiniLM-L6-v2'); print('  embeddings OK | dim', len(list(m.embed(['x']))[0]))" 2>/dev/null || echo "  embeddings: FAIL"
python3 tools/uai_mem.py audit | tail -2
bash tests/test_memory_os.sh | tail -3
echo; echo "bootstrap complete."
