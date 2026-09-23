#!/usr/bin/env bash
# run_environment_probe.sh — UAI-COS capability audit: environment inventory refresh
# Blueprint Part 14 (self-exploration loop) + Part 22 (continuous update).
# Read-only except: koi bhi install NAHI karta. Sirf detect karta hai.
# Usage: bash run_environment_probe.sh | tee probe_results_$(date +%F).txt
set -uo pipefail
echo "=========== ENVIRONMENT PROBE — $(date -Iseconds) ==========="
echo
echo "--- identity / os ---"
id; uname -srmo; (source /etc/os-release 2>/dev/null && echo "$PRETTY_NAME")
echo
echo "--- compute ---"
echo "vCPU: $(nproc)"; free -m | awk 'NR<=2{print}'; df -h /home/user /tmp | tail -n +2
echo
echo "--- runtimes ---"
for c in python3 pip3 node npm deno bun go rustc java gcc g++ make; do
  printf "%-9s " "$c"; command -v "$c" >/dev/null 2>&1 && ("$c" --version 2>&1 | head -1) || echo "NOT FOUND"
done
echo
echo "--- cli tools ---"
for c in git curl wget jq sqlite3 pandoc ffmpeg convert magick tesseract libreoffice soffice zip unzip ssh scp rsync pdftotext qpdf playwright gh docker systemctl crontab; do
  printf "%-13s " "$c"; command -v "$c" >/dev/null 2>&1 && echo "OK" || echo "NOT FOUND"
done
echo
echo "--- sudo ---"
sudo -n id 2>&1 | head -1
echo
echo "--- python libs (import check) ---"
python3 - <<'PY'
mods = ["requests","httpx","aiohttp","bs4","lxml","pandas","numpy","matplotlib","scipy","openpyxl",
        "docx","PIL","cv2","sklearn","yaml","jsonschema","rich","tqdm","sqlite3","pypdf","playwright",
        "pytesseract","torch","cryptography","duckdb"]
ok, bad = [], []
for m in mods:
    try: __import__(m); ok.append(m)
    except Exception: bad.append(m)
print("present:", ", ".join(ok) or "—")
print("missing:", ", ".join(bad) or "—")
PY
echo
echo "--- network egress (spot check) ---"
for u in https://example.com https://pypi.org https://api.github.com/zen https://en.wikipedia.org; do
  printf "%-34s " "$u"; curl -s -o /dev/null -m 8 -w "HTTP:%{http_code}\n" "$u" || echo "FAIL"
done
echo
echo "--- secrets present? (names only) ---"
for v in OPENAI_API_KEY ANTHROPIC_API_KEY GEMINI_API_KEY TELEGRAM_BOT_TOKEN GITHUB_TOKEN AWS_ACCESS_KEY_ID; do
  [ -n "${!v:-}" ] && echo "  PRESENT $v" || echo "  absent  $v"
done
echo
echo "--- running processes (background services) ---"
ps -eo pid,comm --sort=pid | tail -n +2 | awk '$2 ~ /python|http|node/ {print}' | head -10
echo
echo "=========== PROBE COMPLETE ==========="
