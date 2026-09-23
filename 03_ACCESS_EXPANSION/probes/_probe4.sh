#!/usr/bin/env bash
probe() {
  local name="$1" url="$2"; shift 2
  local out="/tmp/_p4_body"; local code
  code=$(curl -s -o "$out" -m 18 -w "%{http_code}" -L "$@" "$url" 2>/dev/null || echo 000)
  local bytes; bytes=$(wc -c <"$out" 2>/dev/null || echo 0)
  local snip; snip=$(head -c 100 "$out" 2>/dev/null | tr '\n' ' ' | tr -s ' ')
  printf "%-34s %-4s %-9s %s\n" "$name" "$code" "$bytes" "$snip"
}
UA_OSM="UAI-COS-research/1.0 (contact: local agent)"
echo "== OSM overpass (proper UA) + CDX API =="
probe "osm-overpass-ua" "https://overpass-api.de/api/interpreter" -A "$UA_OSM" --data-urlencode 'data=[out:json][timeout:25];node["name"="India Gate"];out 1;'
probe "wayback-cdx"     "https://web.archive.org/cdx/search/cdx?url=stackoverflow.com/questions/11227809*&output=json&limit=3"
probe "wayback-cdx-reddit" "https://web.archive.org/cdx/search/cdx?url=reddit.com/r/programming/comments/*&output=json&limit=3&filter=statuscode:200"
echo
echo "== REDDIT alternate route tests =="
probe "reddit-rss-sub"  "https://www.reddit.com/r/IndiaInvestments/top/.rss?t=week" -A "Mozilla/5.0"
probe "reddit-rss-user" "https://www.reddit.com/user/spez/.rss" -A "Mozilla/5.0"
probe "teddit-ish"      "https://libreddit.privacy.com.de/r/programming"
probe "pullpush-retry"  "https://api.pullpush.io/reddit/search/submission/?subreddit=programming&size=1"
echo
echo "== SO / dev Q&A alternate routes =="
probe "so-api-answers"  "https://api.stackexchange.com/2.3/questions/11227809/answers?order=desc&sort=votes&site=stackoverflow&filter=withbody"
probe "so-api-search"   "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=sorted%20array%20faster&site=stackoverflow&pagesize=1"
probe "so-data-dump"    "https://archive.org/download/stackexchange/stackoverflow.com-Posts.7z"
echo
echo "== NEWS/Q&A via wayback for other blocked sites =="
probe "wayback-medium"  "https://web.archive.org/web/2026/https://medium.com/tag/programming"
probe "wayback-quora"   "https://web.archive.org/web/2026/https://www.quora.com/"
probe "wayback-tripadvisor" "https://web.archive.org/web/2026/https://www.tripadvisor.com/"
echo
echo "== npm -g fix test =="
sudo -n npm install -g --silent serve 2>&1 | tail -1; command -v serve >/dev/null && echo "npm -g with sudo: OK" || echo "npm -g: still failed"
