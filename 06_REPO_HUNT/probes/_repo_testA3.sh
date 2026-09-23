#!/usr/bin/env bash
R(){ desc="$1"; url="$2"; shift 2; echo "=== [$desc]"; rm -rf /tmp/gdl && mkdir -p /tmp/gdl
  timeout 90 gallery-dl --range 1-2 -D /tmp/gdl "$@" "$url" >/tmp/g.out 2>/tmp/g.err; ec=$?
  echo "  exit=$ec files=$(find /tmp/gdl -type f 2>/dev/null | wc -l) bytes=$(du -sb /tmp/gdl 2>/dev/null | cut -f1)"
  echo "  --log--"; tail -c 400 /tmp/g.err | sed 's/^/    /'; echo; }
echo "########## BATCH A3 real-download ($(date -u +%FT%TZ)) ##########"
R "X (twitter) user jack"       "https://x.com/jack"
R "X single tweet /jack/status/20" "https://x.com/jack/status/20"
R "Instagram user instagram"    "https://www.instagram.com/instagram/"
R "TikTok user tiktok"          "https://www.tiktok.com/@tiktok"
R "Facebook page NASA"          "https://www.facebook.com/NASA"
R "Bluesky profile bsky.app media" "https://bsky.app/profile/bsky.app/media"
echo "=== [Bluesky single post via public API + gallery-dl]"
rkey=$(curl -s -m 20 -A "UAI-COS-research/1.0" "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=bsky.app&limit=1" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['feed'][0]['post']['uri'].split('/')[-1])" 2>/dev/null)
echo "  rkey=$rkey"; [ -n "$rkey" ] && R "Bluesky post $rkey" "https://bsky.app/profile/bsky.app/post/$rkey"
echo "=== [Pinterest: does the 105KB payload contain real image URLs?]"
timeout 60 gallery-dl --range 1-1 --simulate -j "https://www.pinterest.com/pin/424605071136961057/" 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
pins=[x for x in d if x[0]==2]
if pins:
    m=pins[0][1]
    print('  RESULT pin keys:', len(m.keys()))
    for k in ('id','grid_title','pinner','images','videos','link','description'):
        v=m.get(k)
        if k=='images' and v: 
            img=v.get('orig') or list(v.values())[0]; print('   images.orig.url:', str(img)[:120])
        elif k=='pinner' and v: print('   pinner:', str(v.get('username') or v.get('full_name'))[:60])
        else: print(f'   {k}:', str(v)[:110])
else: print('  RESULT no pin metadata')"
echo "=== [facebook-scraper retry pages=3]"
timeout 90 python3 -c "
import facebook_scraper as fs
try:
    n=0
    for p in fs.get_posts('bbcnews', pages=3):
        print('  post:', repr((p.get('text') or '')[:70]), '| time:', p.get('time'), '| imgs:', len(p.get('images') or [])); n+=1
        if n>=4: break
    print('  RESULT ok posts=',n)
except Exception as e: print('  RESULT FAIL', type(e).__name__, str(e)[:200])"
