#!/usr/bin/env bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
probe() {
  local name="$1" url="$2"; shift 2
  local out="/tmp/_p3_body"; local code
  code=$(curl -s -o "$out" -m 15 -w "%{http_code}" -L -A "$UA" "$@" "$url" 2>/dev/null || echo 000)
  local bytes; bytes=$(wc -c <"$out" 2>/dev/null || echo 0)
  local snip; snip=$(head -c 110 "$out" 2>/dev/null | tr '\n' ' ' | tr -s ' ')
  printf "%-38s %-4s %-8s %s\n" "$name" "$code" "$bytes" "$snip"
}
echo "== OSM / WIKIDATA retry (corrected) =="
probe "osm-overpass-v2" "https://overpass-api.de/api/interpreter" --data-urlencode "data=[out:json][timeout:20];node[\"name\"=\"India Gate\"];out 1;"
probe "wikidata-entity" "https://www.wikidata.org/wiki/Special:EntityData/Q42.json"
probe "wikipedia-rest"  "https://en.wikipedia.org/api/rest_v1/page/summary/Transformer_(deep_learning_architecture)"
echo
echo "== JINA PROXY on DATA endpoints (NSE fix test) =="
probe "jina nse-bhavcopy" "https://r.jina.ai/https://archives.nseindia.com/products/content/sec_bhavdata_full.csv"
probe "jina reddit-thread" "https://r.jina.ai/https://www.reddit.com/r/programming/comments/1fq7k9q/"
probe "jina medium-article" "https://r.jina.ai/https://medium.com/tag/programming"
probe "jina scidir-article" "https://r.jina.ai/https://www.sciencedirect.com/science/article/pii/S0167739X23000804"
echo
echo "== WAYBACK on blocked pages =="
probe "wayback reddit-thread" "https://web.archive.org/web/2026/https://www.reddit.com/r/programming/comments/1fq7k9q/"
probe "wayback so-answer" "https://web.archive.org/web/2026/https://stackoverflow.com/questions/11227809/"
probe "wayback wsj-article" "https://web.archive.org/web/2026/https://www.wsj.com/"
echo
echo "== ALT MIRRORS / ARCHIVES =="
probe "timetravel"      "http://timetravel.mementoweb.org/timemap/link/https://www.reddit.com/"
probe "openalex-cited-by" "https://api.openalex.org/works?filter=cites:W2741809807&per-page=1"
probe "europepmc-fulltext" "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=OPEN_ACCESS:Y%20AND%20transformer&format=json&pageSize=1"
probe "crossref-doi"    "https://api.crossref.org/works/10.1038/nature12373"
probe "arxiv-pdf-direct" "https://arxiv.org/pdf/1706.03762v7"
