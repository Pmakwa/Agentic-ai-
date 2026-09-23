#!/usr/bin/env bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
probe() {
  local name="$1" url="$2"; shift 2
  local out="/tmp/_p2b_body"; local code
  code=$(curl -s -o "$out" -m 14 -w "%{http_code}" -L -A "$UA" "$@" "$url" 2>/dev/null || echo 000)
  local bytes; bytes=$(wc -c <"$out" 2>/dev/null || echo 0)
  local snip; snip=$(head -c 110 "$out" 2>/dev/null | tr '\n' ' ' | tr -s ' ')
  printf "%-36s %-4s %-8s %s\n" "$name" "$code" "$bytes" "$snip"
}
echo "== READER-PROXY ROUTE (r.jina.ai) — blocked sites =="
probe "r.jina reddit"        "https://r.jina.ai/https://www.reddit.com/r/programming/"
probe "r.jina stackoverflow" "https://r.jina.ai/https://stackoverflow.com/questions/11227809/"
probe "r.jina medium"        "https://r.jina.ai/https://medium.com/"
probe "r.jina bloomberg"     "https://r.jina.ai/https://www.bloomberg.com/"
probe "r.jina wsj"           "https://r.jina.ai/https://www.wsj.com/"
probe "r.jina sciencedirect" "https://r.jina.ai/https://www.sciencedirect.com/"
probe "r.jina nseindia"      "https://r.jina.ai/https://www.nseindia.com/"
probe "r.jina x.com"         "https://r.jina.ai/https://x.com/OpenAI"
echo
echo "== RSS / FEED ROUTES =="
probe "bbc-rss"         "https://feeds.bbci.co.uk/news/rss.xml"
probe "google-news-rss" "https://news.google.com/rss/search?q=finance&hl=en-IN&gl=IN&ceid=IN:en"
probe "wsj-rss"         "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"
probe "bloomberg-rss"   "https://feeds.bloomberg.com/markets/news.rss"
probe "medium-rss-tag"  "https://medium.com/feed/tag/programming"
probe "scribe-rip"      "https://scribe.rip/@medium"
probe "hn-rss"          "https://hnrss.org/frontpage"
probe "reddit-rss"      "https://www.reddit.com/r/programming/.rss"
probe "github-blog-rss" "https://github.blog/feed/"
echo
echo "== FINANCE / DATA ALTERNATIVES =="
probe "yahoo-chart-api" "https://query1.finance.yahoo.com/v8/finance/chart/RELIANCE.NS?range=1d&interval=1d"
probe "nse-bhavcopy"    "https://archives.nseindia.com/products/content/sec_bhavdata_full.csv"
probe "nse-api-alt"     "https://www.nseindia.com/api/marketStatus"
probe "worldbank"       "https://api.worldbank.org/v2/country/IN/indicator/NY.GDP.MKTP.CD?format=json&per_page=1"
probe "osm-overpass"    "https://overpass-api.de/api/interpreter?data=[out:json];node[name=India%20Gate];out%201;"
probe "wikidata-sparql" "https://query.wikidata.org/sparql?query=SELECT%20?item%20WHERE%20{?item%20wdt:P31%20wd:Q5}%20LIMIT%201&format=json"
probe "openlibrary"     "https://openlibrary.org/search.json?q=transformer&limit=1"
probe "coingecko"       "https://api.coingecko.com/api/v3/ping"
probe "exchangerate"    "https://open.er-api.com/v6/latest/USD"
