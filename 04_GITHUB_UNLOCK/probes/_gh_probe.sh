#!/usr/bin/env bash
# GitHub capability probe — 2026-09-23
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
G() { curl -s -m 25 -A "$UA" -H "Accept: application/vnd.github+json" "$@"; }

echo "=== [1] RATE LIMIT (bina token) ==="
G "https://api.github.com/rate_limit" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for k,v in d.get('resources',{}).items():
    if k in ('core','search','code_search','graphql'): print(f'  {k:12} limit={v[\"limit\"]:>5} remaining={v[\"remaining\"]:>5}')
"

echo "=== [2] REPO METADATA ==="
G "https://api.github.com/repos/yt-dlp/yt-dlp" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'  {d.get(\"full_name\")} | stars={d.get(\"stargazers_count\"):,} | lang={d.get(\"language\")} | license={ (d.get(\"license\") or {}).get(\"spdx_id\") }')
"

echo "=== [3] REPO SEARCH (unauth) ==="
G "https://api.github.com/search/repositories?q=whisper+cpp&sort=stars&per_page=3" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  total:', d.get('total_count'))
for r in d.get('items',[])[:3]: print(f'  - {r[\"full_name\"]:<38} ★{r[\"stargazers_count\"]:>7,}  {r[\"description\"][:50] if r[\"description\"] else \"\"}')
"

echo "=== [4] CODE SEARCH (unauth — expect 401 needs auth) ==="
code=$(curl -s -o /tmp/_cs.json -w "%{http_code}" -m 25 -A "$UA" -H "Accept: application/vnd.github+json" "https://api.github.com/search/code?q=def+main+language:python&per_page=1")
echo "  HTTP $code"; head -c 200 /tmp/_cs.json; echo

echo "=== [5] ISSUES SEARCH (unauth) ==="
G "https://api.github.com/search/issues?q=repo:yt-dlp/yt-dlp+is:issue+cookies&per_page=2" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  total:', d.get('total_count'))
for i in d.get('items',[])[:2]: print(f'  - [{i[\"state\"]}] {i[\"title\"][:60]}')
"

echo "=== [6] RELEASES / LATEST ASSET ==="
G "https://api.github.com/repos/mikefarah/yq/releases/latest" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('  tag:', d.get('tag_name'), '| assets:')
for a in d.get('assets',[])[:6]:
    print(f'    {a[\"name\"]:<34} {a[\"size\"]/1e6:>6.1f} MB  dl={a[\"download_count\"]:,}')
"

echo "=== [7] RAW FILE (no API limit) ==="
curl -s -o /tmp/_raw.py -w "  raw.githubusercontent: HTTP %{http_code}, %{size_download} B\n" -m 25 -A "$UA" "https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/yt_dlp/version.py"
head -3 /tmp/_raw.py

echo "=== [8] CODELOAD ZIP (bina git) ==="
curl -sL -o /tmp/_zip.zip -w "  codeload zip: HTTP %{http_code}, %{size_download} B\n" -m 60 -A "$UA" "https://codeload.github.com/octocat/Hello-World/zip/refs/heads/master"

echo "=== [9] GIT CLONE --depth 1 (time it) ==="
t0=$(date +%s); git clone -q --depth 1 https://github.com/cli/cli /tmp/_clone_test 2>&1 | tail -1; t1=$(date +%s)
echo "  cli/cli cloned in $((t1-t0))s, size: $(du -sh /tmp/_clone_test 2>/dev/null | cut -f1)"

echo "=== [10] GITHUB CLI (gh) unauth ==="
gh api rate_limit 2>&1 | head -c 150; echo
gh repo view cli/cli --json name,stargazerCount 2>&1 | head -c 150; echo

echo "=== [11] TRENDING (HTML, no API) ==="
curl -s -m 25 -A "$UA" "https://github.com/trending?since=daily" -o /tmp/_trend.html -w "  trending page: HTTP %{http_code}, %{size_download} B\n"
grep -oE '<h2 class="h3 lh-condensed">[^<]*' /tmp/_trend.html | head -4 | sed 's/<[^>]*>//g' | sed 's/^/  /'

echo "=== [12] GH ARCHIVE (public event data) ==="
curl -sI -m 25 -A "$UA" "https://data.gharchive.org/2026-09-22-12.json.gz" | head -4 | sed 's/^/  /'

echo "=== [13] GREEK.APP / grep.app CODE SEARCH alternative ==="
curl -s -m 25 -A "$UA" "https://grep.app/api/search?q=def%20main&filter[lang][0]=Python" -o /tmp/_grep.json -w "  grep.app: HTTP %{http_code}, %{size_download} B\n"
head -c 200 /tmp/_grep.json; echo

echo "=== [14] PUBLIC GIST (read) ==="
curl -s -m 25 -A "$UA" "https://api.github.com/gists/public?per_page=1" | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin); g=d[0]; print('  gist:', g['id'][:12], '| files:', list(g['files'])[:2])
except Exception as e: print('  gist failed:', e)
"

echo "=== [15] RATE LIMIT AFTER (kitna kharch hua) ==="
G "https://api.github.com/rate_limit" | python3 -c "
import json,sys; d=json.load(sys.stdin)['resources']; print('  core remaining:', d['core']['remaining'], '| search remaining:', d['search']['remaining'])"
