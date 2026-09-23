#!/usr/bin/env bash
# bootstrap_environment.sh — UAI-COS environment ko zero se khada karta hai (koi bhi agent, koi bhi fresh sandbox).
# Naya finding (2026-09-23): sandbox RESET ke baad /opt aur pip tools gayab ho sakte hain —
# isliye ye script repo me hai: `bash tools/bootstrap_environment.sh` chalao aur sab wapas aa jata hai.
set -uo pipefail
LOG=/tmp/uai_bootstrap.log
say() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }

say "== UAI-COS bootstrap shuru =="

# 0) /opt writable banao (root-owned hota hai; sudo passwordless verified)
if [ -d /opt ]; then
  sudo mkdir -p /opt/uai-cache/bin /opt/uai-cache/node22 2>/dev/null
  sudo chown -R "$(id -u):$(id -g)" /opt/uai-cache 2>/dev/null && say "/opt/uai-cache writable OK"
fi

# 1) OS packages
if command -v apt-get >/dev/null; then
  say "apt: ripgrep fd-find pandoc ffmpeg jq sqlite3 tesseract-ocr poppler-utils imagemagick"
  sudo apt-get update -qq >>"$LOG" 2>&1
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ripgrep fd-find pandoc ffmpeg jq sqlite3 \
      tesseract-ocr poppler-utils imagemagick >>"$LOG" 2>&1 && say "apt OK" || say "apt partial (log dekho)"
fi

# 2) Python tools (system pip; sandbox me --break-system-packages chahiye)
say "pip: core research/social/ai tools"
python3 -m pip install --quiet --break-system-packages --disable-pip-version-check \
  gallery-dl yt-dlp yfinance feedparser trafilatura pypdf duckdb polars requests beautifulsoup4 lxml \
  youtube-transcript-api edge-tts python-docx openpyxl python-pptx >>"$LOG" 2>&1 && say "pip OK" || say "pip partial"

# 3) yq + crane (GitHub releases, tokenless) -> /opt/uai-cache/bin
if [ ! -x /opt/uai-cache/bin/yq ] && command -v curl >/dev/null; then
  say "yq + crane download"
  curl -sL -o /tmp/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 && install -m 755 /tmp/yq /opt/uai-cache/bin/yq && say "yq OK"
  curl -sL -o /tmp/crane.tgz https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Linux_x86_64.tar.gz \
    && tar -xzf /tmp/crane.tgz -C /opt/uai-cache/bin crane 2>/dev/null && say "crane OK"
fi

# 4) Node 22 (RSSHub ke liye) -> /opt/uai-cache/node22
if [ ! -x /opt/uai-cache/node22/bin/node ]; then
  say "node22 download"
  curl -sL -o /tmp/node22.tar.xz https://nodejs.org/dist/v22.14.0/node-v22.14.0-linux-x64.tar.xz \
    && mkdir -p /opt/uai-cache/node22 && tar -xJf /tmp/node22.tar.xz -C /opt/uai-cache/node22 --strip-components=1 \
    && say "node22 OK: $(/opt/uai-cache/node22/bin/node -v)"
fi

# 5) RSSHub (self-host, 2015 namespaces) -> /opt/uai-cache/rsshub  [~5 min, optional]
if [ "${UAI_SKIP_RSSHUB:-0}" != "1" ] && [ ! -f /opt/uai-cache/rsshub/dist/index.mjs ]; then
  say "RSSHub clone + install + build (sabar karo)"
  rm -rf /opt/uai-cache/rsshub
  git clone --depth 1 -q https://github.com/DIYgod/RSSHub /opt/uai-cache/rsshub >>"$LOG" 2>&1
  ( cd /opt/uai-cache/rsshub && PATH=/opt/uai-cache/node22/bin:$PATH pnpm install --config.confirmModulesPurge=false >>"$LOG" 2>&1 \
    && PATH=/opt/uai-cache/node22/bin:$PATH pnpm build >>"$LOG" 2>&1 ) && say "RSSHub build OK" || say "RSSHub build FAIL (log dekho)"
fi

# 6) Persistence stamp + health
date -u +"%Y-%m-%dT%H:%M:%SZ" > /opt/uai-cache/PERSIST_STAMP.txt
say "PERSIST_STAMP likha"
say "== health =="
python3 tools/uai_mem.py audit 2>/dev/null | tail -2 | tee -a "$LOG"
python3 tools/verify_provenance.py 2>/dev/null | tail -1 | tee -a "$LOG"
say "== bootstrap khatam (log: $LOG) =="
