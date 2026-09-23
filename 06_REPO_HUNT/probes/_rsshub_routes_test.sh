#!/usr/bin/env bash
B="http://127.0.0.1:1200"
echo "##### RSSHub local routes test ($(date -u +%FT%TZ)) #####"
t(){ name="$1"; path="$2"; printf "%-34s " "$name"
  curl -s -m 50 -o /tmp/rss.xml -w "http=%{http_code} bytes=%{size_download}" "$B$path"
  items=$(grep -c "<item>" /tmp/rss.xml 2>/dev/null || echo 0)
  kind=$(grep -o -m1 -E "<rss|<feed|<!DOCTYPE html" /tmp/rss.xml | head -1)
  err=$(grep -o -m1 -E '<title>[^<]{0,80}' /tmp/rss.xml | head -1 | sed 's/<title>//')
  echo " items=$items kind=${kind:-none}"
  [ "$items" = "0" ] && echo "        -> $err"
}
t "telegram/channel/telegram"   "/telegram/channel/telegram"
t "twitter/user/jack"           "/twitter/user/jack"
t "twitter/trends/US"           "/twitter/trends/23424977"
t "instagram/user/instagram"    "/instagram/user/instagram"
t "tiktok/user/@tiktok"         "/tiktok/user/tiktok"
t "tumblr/posts/staff"          "/tumblr/posts/staff.tumblr.com"
t "threads/user/zuck"           "/threads/zuck"
t "linkedin/company/microsoft"  "/linkedin/company/microsoft/posts"
t "mastodon/acct fosstodon"     "/mastodon/acct/kev@fosstodon.org/statuses"
t "weibo/user/2803301701"       "/weibo/user/2803301701"
t "youtube/user/Fireship"       "/youtube/user/Fireship"
t "bilibili/user/video 2267573" "/bilibili/user/video/2267573"
t "pinterest/user/pinterest"    "/pinterest/user/pinterest"
t "douyin/user"                 "/douyin/user/MS4wLjABAAAA"
t "github/trending/python"      "/github/trending/daily/python"
t "zhihu/hot (control)"         "/zhihu/hot"
