#!/usr/bin/env bash
T(){ desc="$1"; shift; echo "=== [$desc]"; timeout 50 "$@" 2>&1 | head -c 600; echo; echo "   exit=$?"; echo; }
echo "########## BATCH A: installed-repo live tests ($(date -u +%FT%TZ)) ##########"
T "gallery-dl REDDIT subreddit"      gallery-dl -j "https://www.reddit.com/r/programming/" | head -c 600
T "gallery-dl X/Twitter user"        gallery-dl -j "https://x.com/jack"
T "gallery-dl INSTAGRAM profile"     gallery-dl -j "https://www.instagram.com/instagram/"
T "gallery-dl TIKTOK user"           gallery-dl -j "https://www.tiktok.com/@tiktok"
T "gallery-dl BLUESKY profile"       gallery-dl -j "https://bsky.app/profile/bsky.app"
T "gallery-dl MASTODON profile"      gallery-dl -j "https://fosstodon.org/@kev"
T "gallery-dl PINTEREST board"       gallery-dl -j "https://www.pinterest.com/pinterest/official-news/"
T "gallery-dl FACEBOOK page"         gallery-dl -j "https://www.facebook.com/NASA"
T "facebook-scraper public page bbcnews" python3 -c "
import facebook_scraper as fs
try:
  posts=fs.get_posts('bbcnews', pages=1, options={'allow_extra_requests':False})
  n=0
  for p in posts:
    print(' post:', (p.get('text') or '')[:80].replace(chr(10),' '), '| time:', p.get('time')); n+=1
    if n>=3: break
  print('OK posts=',n)
except Exception as e: print('FAIL', type(e).__name__, str(e)[:200])"
T "instaloader public profile (expect login wall?)" bash -c "instaloader --no-pictures --no-videos --count 2 --dirname-pattern /tmp/il profile instagram 2>&1 | tail -6"
