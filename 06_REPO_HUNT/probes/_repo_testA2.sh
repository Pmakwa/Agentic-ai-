#!/usr/bin/env bash
# deep tests: real metadata extraction, bounded output, no outer pipe
D(){ desc="$1"; shift; echo "=== [$desc]"; timeout 60 "$@" >/tmp/t.out 2>/tmp/t.err; ec=$?;
  echo "  exit=$ec stdout_bytes=$(wc -c </tmp/t.out) stderr_bytes=$(wc -c </tmp/t.err)";
  echo "  --stdout--"; head -c 500 /tmp/t.out; echo; echo "  --stderr(tail)--"; tail -c 400 /tmp/t.err; echo; echo; }
G(){ D "$1" gallery-dl --range 1-2 --simulate -j "$2"; }
echo "########## BATCH A2 deep ($(date -u +%FT%TZ)) ##########"
G "gallery-dl REDDIT listing"  "https://www.reddit.com/r/programming/"
G "gallery-dl X jack"          "https://x.com/jack"
G "gallery-dl INSTAGRAM"       "https://www.instagram.com/instagram/"
G "gallery-dl TIKTOK"          "https://www.tiktok.com/@tiktok"
G "gallery-dl BLUESKY"         "https://bsky.app/profile/bsky.app"
G "gallery-dl FACEBOOK NASA"   "https://www.facebook.com/NASA"
G "gallery-dl PINTEREST pin"   "https://www.pinterest.com/pin/424605071136961057/"
D "facebook-scraper bbcnews page" python3 -c "
import facebook_scraper as fs
try:
    posts=fs.get_posts('bbcnews', pages=1, options={'allow_extra_requests':False})
    n=0
    for p in posts:
        print('post:', (p.get('text') or '')[:70].replace(chr(10),' '), '| time:', p.get('time')); n+=1
        if n>=3: break
    print('RESULT ok posts=',n)
except Exception as e: print('RESULT FAIL', type(e).__name__, str(e)[:250])"
D "instaloader profile instagram" bash -c "instaloader --no-pictures --no-videos --count 2 --dirname-pattern '/tmp/il' profile instagram 2>&1 | tail -5"
D "youtube-transcript-api" bash -c "vid=\$(yt-dlp --flat-playlist --print id 'https://www.youtube.com/@Fireship/videos' 2>/dev/null | head -1); echo \"video_id=\$vid\"; python3 -c \"
from youtube_transcript_api import YouTubeTranscriptApi as A
import sys
v='\$vid'
try:
    t=A().fetch(v); print('RESULT ok segments=', len(t.snippets)); print(' sample:', t.snippets[0].text[:90])
except Exception as e: print('RESULT FAIL', type(e).__name__, str(e)[:250])\""
