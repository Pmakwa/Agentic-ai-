#!/usr/bin/env bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
CC() { curl -s -m 25 -A "$UA" -o /tmp/_sp.out -w "%{http_code}|%{size_download}" "$@"; }

echo "=== [1] BLUESKY (AT Protocol) — public API, koi key nahi ==="
r=$(CC "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=india&limit=3")
echo "  HTTP ${r%%|*}, ${r##*|} B"; head -c 220 /tmp/_sp.out; echo

echo "=== [2] MASTODON (fediverse) — public timeline ==="
r=$(CC "https://mastodon.social/api/v1/timelines/public?limit=3")
echo "  HTTP ${r%%|*}, ${r##*|} B"; head -c 200 /tmp/_sp.out; echo

echo "=== [3] TELEGRAM — public channel web preview (t.me/s/) ==="
r=$(CC "https://t.me/s/telegram")
echo "  HTTP ${r%%|*}, ${r##*|} B"; grep -o 'tgme_widget_message_text[^<]*' /tmp/_sp.out | head -1 | cut -c1-100

echo "=== [4] YOUTUBE — official channel RSS feed ==="
r=$(CC "https://www.youtube.com/@Fireship")
cid=$(grep -o '"channelId":"UC[A-Za-z0-9_-]*"' /tmp/_sp.out | head -1 | cut -d'"' -f4)
echo "  channelId mila: ${cid:-NAHI}"
if [ -n "$cid" ]; then r2=$(CC "https://www.youtube.com/feeds/videos.xml?channel_id=$cid"); echo "  RSS: HTTP ${r2%%|*}, ${r2##*|} B"; grep -o "<title>[^<]*" /tmp/_sp.out | head -3 | sed 's/<title>/  - /'; fi

echo "=== [5] REDDIT — RSS (60s window ke andar ek fetch) ==="
r=$(CC "https://www.reddit.com/r/programming/.rss")
echo "  HTTP ${r%%|*}, ${r##*|} B"; grep -o "<title>[^<]*" /tmp/_sp.out | head -2 | sed 's/<title>/  - /'

echo "=== [6] X / TWITTER — koi public route? ==="
r=$(CC "https://api.fxtwitter.com/"); echo "  fxtwitter api: HTTP ${r%%|*}, ${r##*|} B"
for n in nitter.net nitter.poast.org lightbrd.com; do
  code=$(curl -s -o /dev/null -m 12 -w "%{http_code}" "https://$n/")
  echo "  $n: HTTP $code"
done

echo "=== [7] INSTAGRAM ==="
r=$(CC "https://www.instagram.com/"); echo "  homepage: HTTP ${r%%|*}, ${r##*|} B"
r=$(CC "https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram"); echo "  web_profile_info (bina auth): HTTP ${r%%|*}, ${r##*|} B"

echo "=== [8] FACEBOOK ==="
r=$(CC "https://www.facebook.com/"); echo "  homepage: HTTP ${r%%|*}, ${r##*|} B"
r=$(CC "https://graph.facebook.com/v19.0/facebook/posts"); echo "  Graph API (bina token): HTTP ${r%%|*}, ${r##*|} B"; head -c 150 /tmp/_sp.out; echo

echo "=== [9] PINTEREST ==="
r=$(CC "https://www.pinterest.com/"); echo "  homepage: HTTP ${r%%|*}, ${r##*|} B"
r=$(CC "https://www.pinterest.com/resource/UserResource/get/?data=%7B%22options%22%3A%7B%22username%22%3A%22pinterest%22%7D%7D"); echo "  UserResource (bina auth): HTTP ${r%%|*}, ${r##*|} B"

echo "=== [10] TIKTOK — public oEmbed ==="
r=$(CC "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@tiktok/video/7106594312292453675"); echo "  oembed: HTTP ${r%%|*}, ${r##*|} B"; head -c 150 /tmp/_sp.out; echo

echo "=== [11] RSSHUB public instance (GitHub-backed bridge) ==="
for route in "github/trending/daily" "youtube/user/@Fireship"; do
  r=$(CC "https://rsshub.app/$route"); echo "  /$route: HTTP ${r%%|*}, ${r##*|} B"
done
