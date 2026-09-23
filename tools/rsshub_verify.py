#!/usr/bin/env python3
"""
rsshub_verify.py — RSSHub ke routes ko automatically verify karta hai (tokenless, live).

Kaam: local RSSHub (:1200) ke /api/namespace se route registry uthata hai,
diye gaye namespaces ke example URLs test karta hai, aur evidence file likhta hai.

Usage:
  python3 tools/rsshub_verify.py --list vimeo,spotify,zhihu      # kuch namespaces
  python3 tools/rsshub_verify.py --all --workers 6 --limit 400    # bada sweep (dheere chalega)
  python3 tools/rsshub_verify.py --list github,youtube --out 06_REPO_HUNT/probes/x.txt
  python3 tools/rsshub_verify.py --working-only                   # sirf kaam karne wale (monitor ke liye)
"""
from __future__ import annotations
import argparse, concurrent.futures as cf, json, re, sys, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:1200"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
DEFAULT_LIST = (
    "vimeo,spotify,zhihu,github,bsky,hackernews,telegram,mastodon,bilibili,weibo,douyin,tiktok,"
    "youtube,twitter,instagram,threads,pinterest,linkedin,reddit,medium,substack,producthunt,"
    "huggingface,openai,anthropic,deepmind,npm,dockerhub,steam,soundcloud,bandcamp,twitch,gitlab,"
    "wikipedia,notion,imdb,nasa,arxiv,thehindu,dnaindia,espn,mit,ted,daily,producthunt,eztv,quora"
)


def get(url: str, timeout: int = 35, max_bytes: int = 400_000) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml, */*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(max_bytes).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(4000).decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return 0, f"EXC {type(e).__name__}: {e}"


def registry(base: str) -> dict:
    code, body = get(f"{base}/api/namespace", 90, max_bytes=12_000_000)
    if code != 200:
        sys.exit(f"registry fetch fail ({code}) — RSSHub chal raha hai? `cd /opt/uai-cache/rsshub && PORT=1200 node dist/index.mjs`")
    return json.loads(body)


def items(xml: str) -> int:
    return len(re.findall(r"<item[\s>]", xml))


def titles(xml: str, n: int = 2) -> list[str]:
    return [re.sub("<[^>]+>", "", t).strip()[:70] for t in re.findall(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", xml, re.S)[1 : n + 1]]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", default=DEFAULT_LIST, help="comma separated namespaces (ya 'ALL')")
    ap.add_argument("--all", action="store_true", help="saare 2015 namespaces ka pehla route test karo")
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=35)
    ap.add_argument("--out", default="06_REPO_HUNT/probes/rsshub_routes_test2.txt")
    ap.add_argument("--json-out", default="logs/rsshub_routes_verified.json")
    ap.add_argument("--working-only", action="store_true", help="sirf 200 + items>0 wale print karo")
    ap.add_argument("--limit", type=int, default=0, help="--all ke saath max namespaces")
    a = ap.parse_args()

    reg = registry(a.base)
    names = sorted(reg) if a.all else [n.strip() for n in a.list.split(",") if n.strip()]
    if a.limit:
        names = names[: a.limit]

    targets: list[tuple[str, str]] = []
    for ns in names:
        routes = reg.get(ns, {}).get("routes", {})
        for path, meta in routes.items():
            ex = (meta.get("example") or "").strip()
            if ex:
                targets.append((ns, ex))
                break  # ek namespace = ek example (kaafi hai)
    print(f"namespaces: {len(names)} -> {len(targets)} routes test ho rahe hain (workers={a.workers})\n")

    results = []
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(get, f"{a.base}{path}", a.timeout): (ns, path) for ns, path in targets}
        for f in cf.as_completed(futs):
            ns, path = futs[f]
            code, body = f.result()
            n = items(body)
            ok = code == 200 and n > 0
            results.append({"namespace": ns, "route": path, "code": code, "items": n,
                            "ok": ok, "bytes": len(body), "titles": titles(body) if ok else [],
                            "note": "" if ok else (body[:180].replace("\n", " ") if code != 200 else "0 items")})
            if not a.working_only or ok:
                mark = "OK " if ok else "XX "
                print(f"{mark}{code:>3} items={n:<3} {path[:78]}")
    dt = time.time() - t0

    working = [r for r in results if r["ok"]]
    lines = [
        f"# RSSHub route verification — {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"# instance: {a.base} · namespaces tested: {len(targets)} · time: {dt:.0f}s · workers: {a.workers}",
        f"# RESULT: {len(working)} WORKING / {len(results)} tested ({100*len(working)//max(1,len(results))}%)",
        "# legend: OK = 200 + items>0 · XX = fail (code shown)",
        "",
    ]
    for r in sorted(results, key=lambda x: (not x["ok"], x["namespace"])):
        mark = "OK " if r["ok"] else "XX "
        t = (" | " + " · ".join(r["titles"])[:120]) if r["titles"] else (" | " + r["note"][:90])
        lines.append(f"{mark} {r['code']:>3} items={r['items']:<3} {r['route'][:70]:<72}{t}")
    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    jout = ROOT / a.json_out
    jout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps({"tested_at": time.strftime("%Y-%m-%d %H:%M:%S"), "base": a.base,
                                "working": working, "total": len(results)}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{len(working)}/{len(results)} WORKING ({100*len(working)//max(1,len(results))}%) · {dt:.0f}s")
    print(f"evidence -> {a.out}\njson     -> {a.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
