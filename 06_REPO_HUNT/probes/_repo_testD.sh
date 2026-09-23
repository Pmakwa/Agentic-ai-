#!/usr/bin/env bash
R(){ desc="$1"; url="$2"; echo "=== [$desc]"; rm -rf /tmp/gdl && mkdir -p /tmp/gdl
  timeout 60 gallery-dl --range 1-2 -D /tmp/gdl "$url" >/tmp/g.out 2>/tmp/g.err; ec=$?
  echo "  exit=$ec files=$(find /tmp/gdl -type f 2>/dev/null|wc -l) bytes=$(du -sb /tmp/gdl 2>/dev/null|cut -f1)"; tail -c 300 /tmp/g.err|sed 's/^/    /'; echo; }
echo "##### BATCH D ($(date -u +%FT%TZ)) #####"
R "VK community ria (photos)"   "https://vk.com/ria"
R "INSTAGRAM retry instagram acct" "https://www.instagram.com/instagram/"
echo "=== [youtube-comment-downloader tokenless]"
timeout 90 python3 -c "
from youtube_comment_downloader import YoutubeCommentDownloader
import itertools
d=YoutubeCommentDownloader()
try:
    g=d.get_comments('TbkUKCm3CHQ')
    for i,c in zip(range(5), g):
        print('  ', c['author'][:22], '|', c['text'][:60].replace(chr(10),' '), '| votes:', c.get('votes'))
    print('  RESULT ok')
except Exception as e: print('  RESULT FAIL', type(e).__name__, str(e)[:200])"
