#!/usr/bin/env bash
B="http://127.0.0.1:1200"
t(){ name="$1"; path="$2"; printf "%-32s " "$name"
  curl -s -m 90 -o /tmp/r2.xml -w "http=%{http_code} bytes=%{size_download}" "$B$path"
  items=$(grep -c "<item>" /tmp/r2.xml 2>/dev/null | head -1)
  echo " items=${items:-0}"
  if [ "${items:-0}" = "0" ]; then python3 -c "
import re,sys
t=open('/tmp/r2.xml',errors='ignore').read()
m=re.search(r'<message>(.*?)</message>',t,re.S) or re.search(r'<title>(.*?)</title>',t,re.S)
print('       ->', re.sub(r'<[^>]+>','',m.group(1))[:150] if m else t[:120].replace(chr(10),' '))"; fi; }
echo "##### RSSHub retest after PLAYWRIGHT_BROWSERS_PATH fix ($(date -u +%FT%TZ)) #####"
t "bilibili/user/video"     "/bilibili/user/video/2267573"
t "douyin/user"             "/douyin/user/MS4wLjABAAAA"
t "linkedin/company posts"  "/linkedin/company/microsoft/posts"
t "weibo/user retry"        "/weibo/user/2803301701"
t "weibo/hot-search"        "/weibo/search/hot"
t "tumblr/posts"            "/tumblr/posts/staff.tumblr.com"
t "threads/search"          "/threads/search/ai"
t "mastodon/tag"            "/mastodon/tag/fosstodon.org/linux"
t "pinterest/user"          "/pinterest/user/pinterest"
t "tiktok/live"             "/tiktok/live/tiktok"
t "youtube/playlist"        "/youtube/playlist/PL0Ml5XWQqpWwES4j9XEmCnEQpp8LGDsHo"
t "telegram/blog"           "/telegram/blog"
