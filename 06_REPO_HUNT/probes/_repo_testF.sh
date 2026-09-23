#!/usr/bin/env bash
UA="UAI-COS-research/1.0"
J(){ desc="$1"; url="$2"; py="$3"; echo "=== [$desc]"; curl -s -m 25 -A "$UA" "$url" -o /tmp/j.json -w "  http=%{http_code} bytes=%{size_download}\n"; python3 -c "$py" 2>&1 | head -6 | sed 's/^/  /'; echo; }
echo "##### BATCH F: Invidious API deep test ($(date -u +%FT%TZ)) #####"
J "search"          "https://yewtu.be/api/v1/search?q=fireship%20ai&type=video" "import json;d=json.load(open('/tmp/j.json'));print('results=',len(d));[print(' ',x['title'][:60],'|',x['videoId'],'|views',x.get('viewCount')) for x in d[:3]]"
J "video details"   "https://yewtu.be/api/v1/videos/TbkUKCm3CHQ" "import json;d=json.load(open('/tmp/j.json'));print('title=',d['title'][:70]);print('views=',d.get('viewCount'),'| likes=',d.get('likeCount'),'| subs=',d.get('subCountText'));print('desc:',(d.get('description') or '')[:100].replace(chr(10),' '))"
J "comments"        "https://yewtu.be/api/v1/comments/TbkUKCm3CHQ" "import json;d=json.load(open('/tmp/j.json'));print('comments=',d.get('commentCount'));[print(' ',c['author'][:20],'|',c['content'][:60].replace(chr(10),' ')) for c in d.get('comments',[])[:3]]"
J "channel about"   "https://yewtu.be/api/v1/channels/UCsBjURrPoezykLs9EqgamOA" "import json;d=json.load(open('/tmp/j.json'));print('author=',d.get('author'),'| subs=',d.get('subCount'),'| videos=',d.get('videoCount'));[print(' latest:',v['title'][:55]) for v in (d.get('latestVideos') or [])[:3]]"
J "trending IN"     "https://yewtu.be/api/v1/trending?region=IN" "import json;d=json.load(open('/tmp/j.json'));print('trending=',len(d));[print(' ',x['title'][:55]) for x in d[:3]]"
J "playlist"        "https://yewtu.be/api/v1/playlists/PL0Ml5XWQqpWwES4j9XEmCnEQpp8LGDsHo" "import json;d=json.load(open('/tmp/j.json'));print('title=',d.get('title'),'| videos=',len(d.get('videos') or []))"
