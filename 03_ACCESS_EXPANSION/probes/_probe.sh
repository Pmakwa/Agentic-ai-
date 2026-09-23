#!/usr/bin/env bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
probe() { # name url [extra curl args]
  local name="$1" url="$2"; shift 2
  local out="/tmp/_p2_body"; local code
  code=$(curl -s -o "$out" -m 12 -w "%{http_code}" -L -A "$UA" "$@" "$url" 2>/dev/null || echo 000)
  local bytes; bytes=$(wc -c <"$out" 2>/dev/null || echo 0)
  local snip; snip=$(head -c 120 "$out" 2>/dev/null | tr '\n' ' ' | tr -s ' ')
  printf "%-34s %-4s %-8s %s\n" "$name" "$code" "$bytes" "$snip"
}
echo "== ACADEMIC / RESEARCH API ROUTES =="
probe "crossref"        "https://api.crossref.org/works?query=transformer&rows=1"
probe "openalex"        "https://api.openalex.org/works?search=transformer&per-page=1"
probe "unpaywall"       "https://api.unpaywall.org/v2/10.1038/nature12373?email=test@example.com"
probe "pubmed-eutils"   "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=transformer&retmax=1&retmode=json"
probe "arxiv-api"       "https://export.arxiv.org/api/query?search_query=all:transformer&max_results=1"
probe "semanticscholar" "https://api.semanticscholar.org/graph/v1/paper/search?query=transformer&limit=1"
probe "doaj"            "https://doaj.org/api/search/articles/transformer?pageSize=1"
probe "openaire"        "https://api.openaire.eu/search/publications?title=transformer&size=1"
probe "ia-scholar"      "https://scholar.archive.org/search?q=transformer"
probe "googlebooks"     "https://www.googleapis.com/books/v1/volumes?q=transformer"
probe "hathi"           "https://babel.hathitrust.org/cgi/ls?q1=transformer;a=srchls;anyall1=all;lmt=ft"
probe "core-api"        "https://api.core.ac.uk/v3/search/works?q=transformer"
probe "europepmc"       "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=transformer&format=json&pageSize=1"
probe "biorxiv"         "https://api.biorxiv.org/details/biorxiv/10.1101/2020.01.01.000000"
echo
echo "== COMMUNITY / Q&A / DEV ROUTES =="
probe "hn-algolia"      "https://hn.algolia.com/api/v1/search?query=transformer&hitsPerPage=1"
probe "stackexchange"   "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&pagesize=1"
probe "stackexch-tags"  "https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&pagesize=3"
probe "github-ratelimit" "https://api.github.com/rate_limit"
probe "gh-trending-alt" "https://api.github.com/search/repositories?q=stars:>50000&per_page=1"
probe "reddit-pullpush" "https://api.pullpush.io/reddit/search/submission/?subreddit=programming&size=2"
probe "reddit-old"      "https://old.reddit.com/r/programming/.json?limit=2"
probe "reddit-newjson"  "https://www.reddit.com/r/programming/new.json?limit=2"
probe "nitter-unofficial" "https://nitter.net/OpenAI"
probe "lobsters"        "https://lobste.rs/hottest.json"
probe "devto"           "https://dev.to/api/articles?per_page=1"
probe "discourse-demo"  "https://meta.discourse.org/latest.json"
