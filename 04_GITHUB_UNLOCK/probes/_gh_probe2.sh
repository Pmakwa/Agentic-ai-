#!/usr/bin/env bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"

echo "=== [16] RELEASE ASSET DOWNLOAD + EXECUTE (yq linux binary) ==="
url=$(curl -s -m 25 -A "$UA" "https://api.github.com/repos/mikefarah/yq/releases/latest" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for a in d['assets']:
    if 'linux_amd64' in a['name'] and a['name'].endswith('.tar.gz'): print(a['browser_download_url']); break")
echo "  asset: $url"
curl -sL -m 120 -A "$UA" -o /tmp/_yq.tgz -w "  download: HTTP %{http_code}, %{size_download} B\n" "$url"
mkdir -p /tmp/_yqbin && tar -xzf /tmp/_yq.tgz -C /tmp/_yqbin yq 2>/dev/null && chmod +x /tmp/_yqbin/yq && echo "  EXEC TEST: $(/tmp/_yqbin/yq --version)"

echo "=== [17] PIP INSTALL FROM GIT (GitHub se seedha package) ==="
timeout 180 pip install -q "git+https://github.com/erikrose/blessings" 2>&1 | tail -1
python3 -c "import blessings; print('  blessings installed from GitHub:', blessings.__file__.split('/')[-3:])" 2>&1 | head -2

echo "=== [18] GH ARCHIVE (public event data) — download + verify ==="
curl -s -m 120 -A "$UA" -o /tmp/_gha.json.gz "https://data.gharchive.org/2026-09-22-12.json.gz" -w "  downloaded: %{size_download} B\n"
python3 -c "
import gzip, json
n=0; types={}
with gzip.open('/tmp/_gha.json.gz','rt',errors='replace') as f:
    for line in f:
        try: e=json.loads(line)
        except: continue
        n+=1; types[e.get('type')]=types.get(e.get('type'),0)+1
        if n>=5000: break
print(f'  events parsed (pehle 5000): {n} | top types:', sorted(types.items(), key=lambda x:-x[1])[:4])
"

echo "=== [19] CODE SEARCH ALTERNATIVES (bina token) ==="
curl -s -m 25 -A "$UA" -o /tmp/_grep2.json -w "  grep.app: HTTP %{http_code}, %{size_download} B\n" "https://grep.app/api/search?q=async+def+main"
head -c 150 /tmp/_grep2.json; echo
curl -s -m 25 -A "$UA" -o /tmp/_sc.json -w "  searchcode.com: HTTP %{http_code}, %{size_download} B\n" "https://searchcode.com/api/codesearch_I/?q=urllib+parse&per_page=2"
head -c 150 /tmp/_sc.json; echo

echo "=== [20] GITHUB ADVISORIES (public security DB) ==="
curl -s -m 25 -A "$UA" -H "Accept: application/vnd.github+json" "https://api.github.com/advisories?per_page=3" | python3 -c "
import json,sys
for a in json.load(sys.stdin)[:3]:
    print(f\"  {a['ghsa_id']} | {a['severity']:>8} | {a['summary'][:55]}\")
"

echo "=== [21] TRENDING (python parse) ==="
python3 -c "
import re
h=open('/tmp/_trend.html',encoding='utf-8',errors='replace').read()
repos=re.findall(r'<a href=\"/([^\"/]+/[^\"/]+)\" data-view-component=\"true\" class=\"Link\">', h)
seen=[];
for r in repos:
    if r not in seen and r.count('/')==1: seen.append(r)
print('  top trending:', seen[:6])
" 2>/dev/null || echo "  (parse failed - HTML structure changed)"

echo "=== [22] GHCR (container registry) — bina docker access ==="
tok=$(curl -s -m 20 "https://ghcr.io/token?scope=repository:astral-sh/uv:pull" | python3 -c "import json,sys; print(json.load(sys.stdin).get('token','')[:20]+'...')" 2>/dev/null)
echo "  token: ${tok:-FAIL}"
curl -s -m 25 -H "Authorization: Bearer $(curl -s "https://ghcr.io/token?scope=repository:astral-sh/uv:pull" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("token",""))')" -H "Accept: application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json" -o /tmp/_ghcr.json -w "  manifest: HTTP %{http_code}, %{size_download} B\n" "https://ghcr.io/v2/astral-sh/uv/manifests/latest"
head -c 200 /tmp/_ghcr.json; echo

echo "=== [23] WIKI CLONE ==="
timeout 60 git clone -q --depth 1 https://github.com/git/git.wiki.git /tmp/_wiki 2>&1 | tail -1
ls /tmp/_wiki 2>/dev/null | head -3 | sed 's/^/  wiki file: /'

echo "=== [24] RAW DATA FILE (dataset repo se CSV) ==="
curl -s -m 25 -A "$UA" -o /tmp/_csv.csv -w "  raw csv: HTTP %{http_code}, %{size_download} B\n" "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
head -2 /tmp/_csv.csv | sed 's/^/  /'
