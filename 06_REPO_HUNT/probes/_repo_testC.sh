#!/usr/bin/env bash
R(){ desc="$1"; url="$2"; shift 2; echo "=== [$desc]"; rm -rf /tmp/gdl && mkdir -p /tmp/gdl
  timeout 70 gallery-dl --range 1-2 -D /tmp/gdl "$@" "$url" >/tmp/g.out 2>/tmp/g.err; ec=$?
  echo "  exit=$ec files=$(find /tmp/gdl -type f 2>/dev/null|wc -l) bytes=$(du -sb /tmp/gdl 2>/dev/null|cut -f1)"; tail -c 300 /tmp/g.err | sed 's/^/    /'; echo; }
echo "########## BATCH C: extra platforms via gallery-dl ($(date -u +%FT%TZ)) ##########"
R "WEIBO user (m.weibo.cn)"   "https://m.weibo.cn/u/2803301701"
R "WEIBO weibo.com"           "https://weibo.com/2803301701"
R "BILIBILI video"            "https://www.bilibili.com/video/BV1GJ411x7h7"
R "VK public page"            "https://vk.com/durov"
R "TUMBLR public blog"        "https://staff.tumblr.com"
R "MASTODON /media suffix"    "https://fosstodon.org/@kev/media"
R "THREADS profile"           "https://www.threads.net/@zuck"
echo "=== [pinterest-dl search tokenless]"
rm -rf /tmp/pd; timeout 90 pinterest-dl search "nature photography" -n 3 -o /tmp/pd >/tmp/pd.out 2>/tmp/pd.err; echo "  exit=$? files=$(find /tmp/pd -type f 2>/dev/null|wc -l) bytes=$(du -sb /tmp/pd 2>/dev/null|cut -f1)"; tail -c 300 /tmp/pd.out; tail -c 200 /tmp/pd.err; echo
echo "=== [pinterest-dl scrape board]"
rm -rf /tmp/pd2; timeout 90 pinterest-dl scrape "https://www.pinterest.com/pinterest/official-news/" -n 3 -o /tmp/pd2 >/tmp/pd2.out 2>/tmp/pd2.err; echo "  exit=$? files=$(find /tmp/pd2 -type f 2>/dev/null|wc -l) bytes=$(du -sb /tmp/pd2 2>/dev/null|cut -f1)"; tail -c 250 /tmp/pd2.out; tail -c 200 /tmp/pd2.err; echo
echo "=== [FACEBOOK raw evidence: mbasic login redirect?]"
for u in "https://mbasic.facebook.com/bbcnews" "https://m.facebook.com/bbcnews"; do echo -n "  $u -> "; curl -s -m 20 -A "Mozilla/5.0" -o /tmp/fb.html -w "http=%{http_code} bytes=%{size_download} final=%{url_effective}" -L "$u"; echo; grep -o -m1 -i -E "log ?in|login|password" /tmp/fb.html | head -1 | sed 's/^/     marker: /'; done
