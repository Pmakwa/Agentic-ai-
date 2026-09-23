#!/usr/bin/env bash
UA="UAI-COS-research/1.0"
P(){ desc="$1"; url="$2"; marker="$3"; printf "=== [%s]\n  " "$desc"; curl -s -m 25 -A "$UA" -L -o /tmp/p.html -w "http=%{http_code} bytes=%{size_download} final=%{url_effective}\n" "$url"; 
  if [ -n "$marker" ]; then grep -o -m2 -i -E "$marker" /tmp/p.html | head -2 | sed 's/^/     hit: /'; fi; }
echo "##### BATCH E: third-party front-end instances ($(date -u +%FT%TZ)) #####"
P "TeddiT (reddit frontend)"        "https://teddit.net/r/privacy"                "privacy|blocked|error"
P "Xeddit (reddit frontend)"        "https://www.xeddit.com/r/privacy"            "privacy|error"
P "Quetre (quora frontend)"         "https://quetre.iket.me/search?q=python"      "question|answer|error"
P "ProxiTok (tiktok frontend)"      "https://proxitok.pabloferreiro.es/@tiktok"   "video|tiktok|error"
P "Nitter (twitter frontend)"       "https://nitter.net/troyhunt"                 "tweet|error|not found"
P "Neuters (reuters frontend)"      "https://neuters.de/"                         "reuters|article|error"
P "Invidious yewtu.be API"          "https://yewtu.be/api/v1/stats"               "version|software"
P "Invidious inv.nadeko.net API"    "https://inv.nadeko.net/api/v1/stats"         "version|software"
P "Piped API kavin.rocks"           "https://pipedapi.kavin.rocks/streams/TbkUKCm3CHQ" "title|error"
P "LibreMDB (imdb frontend)"        "https://libremdb.iket.me/title/tt0111161"    "shawshank|error"
P "Biblio (medium frontend)"        "https://biblio.iket.me/"                     "medium|error"
