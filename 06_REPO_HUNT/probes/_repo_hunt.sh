#!/usr/bin/env bash
q() {
  echo "--- QUERY: $1"
  curl -s -m 25 -H "Accept: application/vnd.github+json" -A "UAI-COS-research/1.0" \
    "https://api.github.com/search/repositories?q=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1")&sort=stars&order=desc&per_page=4" \
  | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    for r in d.get('items',[]):
        print(f\"  {r['full_name']:<44} star={r['stargazers_count']:>7}  {(r['description'] or '')[:60]}\")
except Exception as e: print('  err', e)"
  sleep 7
}
q "reddit downloader archive api"
q "instagram downloader scraper"
q "twitter x scraper downloader"
q "tiktok downloader api"
q "pinterest downloader scraper"
q "facebook scraper public page"
q "rss bridge generator"
q "youtube transcript api"
q "redlib libreddit nitter alternative"
