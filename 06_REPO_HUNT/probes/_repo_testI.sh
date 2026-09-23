#!/usr/bin/env bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
echo "##### BATCH I: Instagram embed / ddinstagram routes ($(date -u +%FT%TZ)) #####"
echo "--- extract public post shortcodes from instagram.com homepage HTML:"
curl -s -m 30 -A "$UA" -o /tmp/ighome.html -w "  http=%{http_code} bytes=%{size_download}\n" "https://www.instagram.com/instagram/"
sc=$(grep -o '/p/[A-Za-z0-9_-]\{8,14\}/' /tmp/ighome.html | sort -u | head -3)
echo "  shortcodes: $(echo $sc | tr '\n' ' ')"
for c in $(echo "$sc" | head -1); do
  code=$(basename $(dirname "$c"))
  for u in "https://www.instagram.com/p/$code/embed/captioned/" "https://www.ddinstagram.com/p/$code/" "https://api.ddinstagram.com/p/$code/"; do
    printf "  %-58s " "$u"; curl -s -m 25 -A "$UA" -L -o /tmp/ige.html -w "http=%{http_code} bytes=%{size_download}\n" "$u"
    grep -o -m1 -iE "embed|login|not found|error" /tmp/ige.html | head -1 | sed 's/^/     marker=/'
  done
done
echo "--- Instagram oEmbed (no token):"
printf "  %-58s " "https://api.instagram.com/oembed/?url=..."; curl -s -m 20 -A "$UA" -o /tmp/igo.json -w "http=%{http_code} bytes=%{size_download}\n" "https://api.instagram.com/oembed/?url=https://www.instagram.com/p/$code/"; head -c 200 /tmp/igo.json; echo
