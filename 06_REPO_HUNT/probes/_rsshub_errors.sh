#!/usr/bin/env bash
B="http://127.0.0.1:1200"
echo "##### RSSHub 503 error reasons + working-route content ($(date -u +%FT%TZ)) #####"
for p in /twitter/user/jack /instagram/user/instagram /tumblr/posts/staff.tumblr.com /linkedin/company/microsoft/posts /weibo/user/2803301701 /bilibili/user/video/2267573 /github/trending/daily/python /douyin/user/MS4wLjABAAAA; do
  echo "=== $p"
  curl -s -m 40 "$B$p" | python3 -c "
import sys,re
t=sys.stdin.read()
m=re.search(r'<message>(.*?)</message>', t, re.S) or re.search(r'<title>(.*?)</title>', t, re.S)
print('   ', re.sub(r'\s+',' ', (m.group(1) if m else t))[:260])"
done
echo
echo "=== WORKING ROUTES: first items"
for p in /telegram/channel/telegram /tiktok/user/tiktok /threads/zuck /mastodon/acct/kev@fosstodon.org/statuses /youtube/user/Fireship /pinterest/user/pinterest; do
  echo "--- $p"
  curl -s -m 45 "$B$p" | python3 -c "
import sys,re
t=sys.stdin.read()
items=re.findall(r'<item>(.*?)</item>', t, re.S)
print('    items:', len(items))
for it in items[:3]:
    ti=re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', it, re.S)
    ln=re.search(r'<link>(.*?)</link>', it, re.S)
    print('     -', (ti.group(1).strip()[:80] if ti else '?').replace('\n',' '), '|', (ln.group(1)[:70] if ln else ''))"
done
