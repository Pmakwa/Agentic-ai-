#!/usr/bin/env python3
"""
social_unlock.py — UAI-COS repo-based social-platform access layer.

Only wraps routes that were LIVE-VERIFIED in this environment on 2026-09-23
(see 06_REPO_HUNT/00_REPO_UNLOCK_REPORT.md). No login-wall / CAPTCHA / paywall bypass.

Subcommands (all tokenless):
  reddit      <subreddit|path> [--threads N]   via redlib instances (safereddit.com, red.artemislena.eu)
  rsshub      <route-path> [--n N]             local RSSHub (http://127.0.0.1:1200) -> JSON items
  gallery     <url> [--meta-only] [--limit N]  gallery-dl (tiktok, bsky, pinterest, tumblr)
  pin         search:<q> | url:<url> [--n N]   pinterest-dl (search / board / pin)
  transcript  <video-id|url>                   youtube-transcript-api
  comments    <video-id|url> [--n N]           youtube-comment-downloader
  x           <user|tweet-url>                 fxtwitter / vxtwitter public bridge
  bsky        <actor> [--query Q]              public.api.bsky.app (keyless)
  status                                       which routes are currently live
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, time, urllib.request, urllib.error, urllib.parse

UA = "UAI-COS-research/1.0"
RSSHUB = os.environ.get("RSSHUB_BASE", "http://127.0.0.1:1200")
REDLIB_INSTANCES = ["https://safereddit.com", "https://red.artemislena.eu"]


def _get(url: str, timeout: int = 30, accept: str = "*/*") -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as f:
            return f.status, f.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")[:400]
    except Exception as e:  # noqa: BLE001
        return 0, f"{type(e).__name__}: {e}"


def _strip(html: str) -> str:
    html = re.sub(r"<br\s*/?>", "\n", html)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


# ---------------------------------------------------------------- reddit
def cmd_reddit(a) -> int:
    path = a.target if a.target.startswith("/") else "/r/" + a.target.strip("/")
    if not path.endswith("/"):
        path += "/"
    out = {"route": "redlib", "path": path, "instances_tried": []}
    for base in REDLIB_INSTANCES:
        st, html = _get(base + path)
        if st == 200:
            titles = re.findall(r'<h2[^>]*class="post_title"[^>]*>\s*<a[^>]*>([^<]{3,200})</a>', html)
            links = re.findall(r'href="(/r/[^"]*/comments/[a-z0-9]+/[^"]{0,90})"', html)
            scores = re.findall(r'class="post_score"[^>]*title="([^"]+)"', html)
            authors = re.findall(r'class="post_author"[^>]*>([^<]{1,40})', html)
            posts = []
            for i, t in enumerate(titles):
                posts.append({
                    "title": t.strip(),
                    "permalink": base + links[i] if i < len(links) else None,
                    "score": scores[i] if i < len(scores) else None,
                    "author": authors[i] if i < len(authors) else None,
                })
            out.update({"instance": base, "posts": posts[: a.n], "count": len(posts)})
            if a.threads and posts:
                th_url = posts[0]["permalink"]
                st2, th = _get(th_url)
                body = re.search(r'<div class="post_body[^"]*"[^>]*>(.*?)</div>', th, re.S)
                comments = re.findall(r'<div class="comment_body[^"]*"[^>]*>(.*?)</div>', th, re.S)
                out["top_thread"] = {
                    "url": th_url,
                    "status": st2,
                    "body": _strip(body.group(1))[:1200] if body else None,
                    "comments": [_strip(c)[:600] for c in comments[: a.threads]],
                }
            break
        out["instances_tried"].append(f"{base} -> HTTP {st}")
    else:
        out["error"] = "no redlib instance answered; " + "; ".join(out["instances_tried"])
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if "error" not in out else 1


# ---------------------------------------------------------------- rsshub
def cmd_rsshub(a) -> int:
    path = a.route if a.route.startswith("/") else "/" + a.route
    st, body = _get(RSSHUB + path, timeout=90, accept="application/rss+xml, application/xml, text/xml")
    items = re.findall(r"<item>(.*?)</item>", body, re.S)
    parsed = []
    for it in items[: a.n]:
        t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S)
        l = re.search(r"<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>", it, re.S)
        p = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
        parsed.append({"title": _strip(t.group(1)) if t else None,
                       "link": (l.group(1).strip() if l else None),
                       "date": (p.group(1).strip() if p else None)})
    err = None
    if not parsed and st != 200:
        m = re.search(r"<message>(.*?)</message>", body, re.S)
        err = _strip(m.group(1))[:300] if m else f"HTTP {st}"
    print(json.dumps({"route": "rsshub", "path": path, "http": st, "items": parsed,
                      "count": len(parsed), "error": err}, indent=2, ensure_ascii=False))
    return 0 if parsed else 1


# ---------------------------------------------------------------- gallery-dl
def cmd_gallery(a) -> int:
    args = ["gallery-dl"]
    if a.meta_only:
        args += ["--simulate", "-j"]
    else:
        args += ["--range", f"1-{a.limit}", "-D", a.dest]
    args.append(a.url)
    p = subprocess.run(args, capture_output=True, text=True, timeout=300)
    out = {"route": "gallery-dl", "url": a.url, "exit": p.returncode}
    if a.meta_only:
        try:
            data = json.loads(p.stdout)
            entries = [e for e in data if isinstance(e, list) and len(e) > 1 and isinstance(e[1], dict)]
            keys = sorted({k for e in entries for k in e[1].keys()})
            out.update({"entries": len(entries), "sample_keys": keys[:25]})
        except Exception:  # noqa: BLE001
            out["raw_head"] = p.stdout[:400]
    else:
        got = []
        for root, _, files in os.walk(a.dest):
            for f in files:
                fp = os.path.join(root, f)
                got.append({"file": os.path.relpath(fp, a.dest), "bytes": os.path.getsize(fp)})
        out["files"] = got
        out["total_bytes"] = sum(f["bytes"] for f in got)
    out["stderr_tail"] = p.stderr[-350:] if p.stderr else ""
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if p.returncode == 0 else 1


# ---------------------------------------------------------------- pinterest-dl
def cmd_pin(a) -> int:
    dest = a.dest
    if a.target.startswith("search:"):
        args = ["pinterest-dl", "search", a.target[7:], "-n", str(a.n), "-o", dest]
    else:
        args = ["pinterest-dl", "scrape", a.target[4:] if a.target.startswith("url:") else a.target,
                "-n", str(a.n), "-o", dest]
    p = subprocess.run(args, capture_output=True, text=True, timeout=300)
    files = []
    for root, _, fs in os.walk(dest):
        for f in fs:
            fp = os.path.join(root, f)
            files.append({"file": os.path.relpath(fp, dest), "bytes": os.path.getsize(fp)})
    print(json.dumps({"route": "pinterest-dl", "target": a.target, "exit": p.returncode,
                      "files": files, "total_bytes": sum(f["bytes"] for f in files),
                      "stdout_tail": p.stdout[-200:]}, indent=2, ensure_ascii=False))
    return 0 if files else 1


# ---------------------------------------------------------------- youtube
def _vid(x: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|/shorts/)([A-Za-z0-9_-]{11})", x)
    return m.group(1) if m else x.strip()


def cmd_transcript(a) -> int:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi as Y
        t = Y().fetch(_vid(a.video))
        sn = t.snippets
        print(json.dumps({"route": "youtube-transcript-api", "video": _vid(a.video),
                          "segments": len(sn), "language": getattr(t, "language_code", None),
                          "text": " ".join(s.text for s in sn)[: a.chars]}, indent=2, ensure_ascii=False))
        return 0
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"route": "youtube-transcript-api", "error": f"{type(e).__name__}: {e}"}, indent=2))
        return 1


def cmd_comments(a) -> int:
    try:
        from youtube_comment_downloader import YoutubeCommentDownloader
        d = YoutubeCommentDownloader()
        rows = []
        for c in d.get_comments(_vid(a.video)):
            rows.append({"author": c.get("author"), "text": c.get("text", "")[:300],
                         "votes": c.get("votes"), "time": c.get("time")})
            if len(rows) >= a.n:
                break
        print(json.dumps({"route": "youtube-comment-downloader", "video": _vid(a.video),
                          "comments": rows, "count": len(rows)}, indent=2, ensure_ascii=False))
        return 0
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"route": "youtube-comment-downloader", "error": f"{type(e).__name__}: {e}"}, indent=2))
        return 1


# ---------------------------------------------------------------- bridges
def cmd_x(a) -> int:
    if "/status/" in a.target:
        user, sid = a.target.split("/status/")[0].rstrip("/").split("/")[-1], re.split(r"[^0-9]", a.target.split("/status/")[1])[0]
        url = f"https://api.fxtwitter.com/{user}/status/{sid}"
    else:
        url = f"https://api.vxtwitter.com/{a.target.lstrip('@')}"
    st, body = _get(url)
    try:
        print(json.dumps({"route": "fxtwitter/vxtwitter", "url": url, "http": st,
                          "data": json.loads(body)}, indent=2, ensure_ascii=False)[:4000])
    except Exception:  # noqa: BLE001
        print(json.dumps({"route": "fxtwitter/vxtwitter", "url": url, "http": st, "raw": body[:400]}, indent=2))
    return 0 if st == 200 else 1


def cmd_bsky(a) -> int:
    if a.query:
        url = f"https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q={urllib.parse.quote(a.query)}&limit={a.n}"
    else:
        url = f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={urllib.parse.quote(a.actor)}"
    st, body = _get(url)
    try:
        d = json.loads(body)
    except Exception:  # noqa: BLE001
        d = {"raw": body[:300]}
    print(json.dumps({"route": "bsky public api", "url": url, "http": st, "data": d}, indent=2, ensure_ascii=False)[:4000])
    return 0 if st == 200 else 1


# ---------------------------------------------------------------- status
def cmd_status(a) -> int:
    checks = {}
    # rsshub
    try:
        st, body = _get(RSSHUB + "/telegram/channel/telegram", timeout=45)
        checks["rsshub_local"] = {"http": st, "live": "<rss" in body or "<feed" in body}
    except Exception as e:  # noqa: BLE001
        checks["rsshub_local"] = {"error": str(e)}
    # gallery-dl
    try:
        v = subprocess.run(["gallery-dl", "--version"], capture_output=True, text=True, timeout=30)
        checks["gallery_dl"] = v.stdout.strip() or v.stderr.strip()
    except Exception as e:  # noqa: BLE001
        checks["gallery_dl"] = f"missing: {e}"
    for name, url in [("redlib_safereddit", "https://safereddit.com/r/programming"),
                      ("redlib_artemislena", "https://red.artemislena.eu/r/programming"),
                      ("fxtwitter", "https://api.fxtwitter.com/jack"), ("vxtwitter", "https://api.vxtwitter.com/jack"),
                      ("bsky_public", "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor=bsky.app"),
                      ("tiktok_oembed", "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@tiktok/video/7686945827008433439")]:
        st, body = _get(url, timeout=25)
        checks[name] = {"http": st, "bytes": len(body)}
        time.sleep(0.6)
    checks["pinterest_dl"] = subprocess.run(["pinterest-dl", "--version"], capture_output=True, text=True).stdout.strip() \
        if subprocess.run(["bash", "-lc", "command -v pinterest-dl"], capture_output=True).returncode == 0 else "missing"
    print(json.dumps(checks, indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="social_unlock.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("reddit"); r.add_argument("target"); r.add_argument("-n", type=int, default=10)
    r.add_argument("--threads", type=int, default=0); r.set_defaults(f=cmd_reddit)

    h = sub.add_parser("rsshub"); h.add_argument("route"); h.add_argument("-n", type=int, default=10)
    h.set_defaults(f=cmd_rsshub)

    g = sub.add_parser("gallery"); g.add_argument("url"); g.add_argument("--meta-only", action="store_true")
    g.add_argument("--limit", type=int, default=2); g.add_argument("--dest", default="/tmp/social_unlock")
    g.set_defaults(f=cmd_gallery)

    pi = sub.add_parser("pin"); pi.add_argument("target"); pi.add_argument("-n", type=int, default=3)
    pi.add_argument("--dest", default="/tmp/social_unlock_pins"); pi.set_defaults(f=cmd_pin)

    t = sub.add_parser("transcript"); t.add_argument("video"); t.add_argument("--chars", type=int, default=1200)
    t.set_defaults(f=cmd_transcript)

    c = sub.add_parser("comments"); c.add_argument("video"); c.add_argument("-n", type=int, default=5)
    c.set_defaults(f=cmd_comments)

    x = sub.add_parser("x"); x.add_argument("target"); x.set_defaults(f=cmd_x)

    b = sub.add_parser("bsky"); b.add_argument("actor"); b.add_argument("--query"); b.add_argument("-n", type=int, default=5)
    b.set_defaults(f=cmd_bsky)

    s = sub.add_parser("status"); s.set_defaults(f=cmd_status)

    a = p.parse_args()
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
