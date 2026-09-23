import re, json, urllib.request, sys, time
UA="UAI-COS-research/1.0"
def get(url, timeout=30):
    r=urllib.request.Request(url, headers={"User-Agent":UA})
    with urllib.request.urlopen(r, timeout=timeout) as f: return f.status, f.read().decode('utf-8','ignore')
print("##### BATCH H: redlib deep verify (%s) #####" % time.strftime("%FT%TZ", time.gmtime()))
for base in ["https://safereddit.com","https://red.artemislena.eu"]:
    print("=== [%s] /r/programming" % base)
    try:
        st, html = get(base+"/r/programming")
        titles = re.findall(r'<a[^>]*class="post_title"[^>]*>([^<]{5,120})</a>', html)
        if not titles:
            titles = re.findall(r'<h2[^>]*class="post_title"[^>]*>\s*<a[^>]*>([^<]{5,120})</a>', html)
        permalinks = re.findall(r'href="(/r/programming/comments/[a-z0-9]+/[^"]{0,80})"', html)
        scores = re.findall(r'class="post_score"[^>]*title="([^"]+)"', html)
        print("  http=%s bytes=%d titles=%d posts=%d scores=%s" % (st, len(html), len(titles), len(permalinks), scores[:4]))
        for t in titles[:5]: print("   -", t.strip()[:95])
        if permalinks:
            pl = base + permalinks[0]
            print("  --- thread:", pl[:100])
            st2, th = get(pl)
            title = re.search(r'<h1[^>]*class="post_title"[^>]*>\s*(?:<a[^>]*>)?([^<]{5,140})', th)
            body  = re.search(r'<div class="post_body[^"]*"[^>]*>(.*?)</div>', th, re.S)
            comments = re.findall(r'<div class="comment_body[^"]*"[^>]*>(.*?)</div>', th, re.S)
            text = re.sub(r'<[^>]+>','', body.group(1)).strip()[:150] if body else '(selftext empty/link post)'
            print("  http=%s bytes=%d | title: %s" % (st2, len(th), (title.group(1).strip()[:90] if title else '?')))
            print("  post_body:", text.replace('\n',' ')[:140])
            print("  comments_found=%d" % len(comments))
            for c in comments[:2]:
                print("    c:", re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',c)).strip()[:110])
    except Exception as e:
        print("  FAIL", type(e).__name__, str(e)[:180])
    time.sleep(3)
