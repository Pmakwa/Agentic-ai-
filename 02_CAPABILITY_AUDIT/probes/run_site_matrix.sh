#!/usr/bin/env bash
# run_site_matrix.sh — UAI-COS capability audit: web access matrix refresh
# Blueprint Part 6 (web discovery) + Part 22 (continuous update).
# Read-only: sirf HTTP GET, browser-UA, 8s timeout, no auth bypass, no aggressive crawling.
# Usage: bash run_site_matrix.sh > site_matrix.csv
set -uo pipefail
OUT="${1:-/dev/stdout}"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
SITES=(
  "https://example.com|control"
  "https://github.com|code-host"
  "https://api.github.com/zen|api-open"
  "https://raw.githubusercontent.com/torvalds/linux/master/README|raw-content"
  "https://pypi.org/simple/|package-index"
  "https://registry.npmjs.org/express|package-index"
  "https://en.wikipedia.org/wiki/Hindi|encyclopedia"
  "https://arxiv.org/pdf/1706.03762|academic-pdf"
  "https://data.gov|gov-data"
  "https://finance.yahoo.com|finance"
  "https://www.google.com|search-engine"
  "https://duckduckgo.com/html/?q=test|search-engine"
  "https://x.com|social"
  "https://www.instagram.com|social"
  "https://www.linkedin.com|social"
  "https://www.reddit.com|forum"
  "https://stackoverflow.com|qa-dev"
  "https://medium.com|publishing"
  "https://www.quora.com|qa-general"
  "https://www.bloomberg.com|news-paid"
  "https://www.wsj.com|news-paid"
  "https://www.sciencedirect.com|academic-paid"
  "https://www.tripadvisor.com|travel"
  "https://www.nseindia.com|finance-local"
  "https://www.amazon.in|ecommerce"
  "https://www.jstor.org|academic"
  "https://api.stackexchange.com/2.3/search?order=desc&sort=relevance&intitle=python&site=stackoverflow|api-dev-qa"
  "https://archive.org/wayback/available?url=reddit.com|api-archive"
  "https://api.semanticscholar.org/graph/v1/paper/search?query=transformer&limit=1|api-academic"
)
{
echo "site,category,http_code,bytes,fetch_time,HARDLINE"
for row in "${SITES[@]}"; do
  url="${row%%|*}"; cat="${row##*|}"
  body=$(mktemp)
  code=$(curl -s -o "$body" -m 8 -w "%{http_code}" -L -A "$UA" "$url" 2>/dev/null || echo "000")
  bytes=$(wc -c <"$body" 2>/dev/null || echo 0)
  rm -f "$body"
  case "$code" in
    200) verdict="READABLE" ;;
    401|402|403) verdict="BLOCKED(paywall/bot-wall)" ;;
    000) verdict="NO-CONNECT" ;;
    *) verdict="CHECK" ;;
  esac
  echo "$url,$cat,$code,$bytes,$(date -Iseconds),$verdict"
done
} > "$OUT"
echo "# site matrix complete -> $OUT" >&2
