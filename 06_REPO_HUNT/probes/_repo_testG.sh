#!/usr/bin/env bash
UA="UAI-COS-research/1.0"
echo "##### BATCH G: reddit frontends + X/IG bridges + jina-reddit ($(date -u +%FT%TZ)) #####"
echo "--- redlib public instances list:"
curl -s -m 25 -A "$UA" https://raw.githubusercontent.com/redlib-org/redlib-instances/main/instances.json -o /tmp/ri.json -w "  http=%{http_code} bytes=%{size_download}\n"
python3 - <<'PY'
import json
try:
    d=json.load(open('/tmp/ri.json')); inst=d.get('instances',[])
    print('  instances:',len(inst))
    for i in inst[:6]: print('   ', i.get('url'), '| tor:', i.get('tor'))
except Exception as e: print('  parse fail', e, open('/tmp/ri.json').read()[:150])
PY
echo "--- live-test first 4 redlib instances:"
python3 -c "
import json
d=json.load(open('/tmp/ri.json'));print('\n'.join(i['url'].rstrip('/') for i in d.get('instances',[])[:4]))" > /tmp/inst.txt 2>/dev/null
while read -r base; do
  printf "  %-42s " "$base"
  curl -s -m 25 -A "$UA" -L -o /tmp/rl.html -w "http=%{http_code} bytes=%{size_download}" "$base/r/programming"
  grep -o -m1 -iE "programming|blocked|error|429|too many" /tmp/rl.html | head -1 | sed 's/^/  hit=/'
  echo
done < /tmp/inst.txt
echo "--- X bridges:"
for u in "https://api.vxtwitter.com/jack" "https://api.fxtwitter.com/jack/status/20"; do printf "  %-45s " "$u"; curl -s -m 20 -A "$UA" -o /tmp/x.json -w "http=%{http_code} bytes=%{size_download}\n" "$u"; python3 -c "
import json;d=json.load(open('/tmp/x.json'));print('     keys:', list(d.keys())[:6])" 2>/dev/null | head -2; done
echo "--- Instagram viewers:"
for u in "https://imginn.com/instagram/" "https://www.picuki.com/profile/instagram" "https://instanavigation.com/user-profile/instagram"; do printf "  %-45s " "$u"; curl -s -m 20 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -L -o /tmp/ig.html -w "http=%{http_code} bytes=%{size_download}\n" "$u"; done
echo "--- r.jina.ai on reddit JSON:"
printf "  jina reddit .json  "; curl -s -m 30 -A "UAI-COS-research/1.0" -o /tmp/jr.txt -w "http=%{http_code} bytes=%{size_download}\n" "https://r.jina.ai/https://www.reddit.com/r/programming/top.json?limit=3"; head -c 220 /tmp/jr.txt; echo
