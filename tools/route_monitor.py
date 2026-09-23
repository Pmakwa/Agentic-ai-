#!/usr/bin/env python3
"""
route_monitor.py — UAI-COS background route-health monitor (systemd timer ke through chalta hai)

Phase-2 discovery: sandbox me systemd TIMERS actually kaam karte hain (2026-09-23 verified:
15s interval par 3/3 fires, direct systemctl start Result=success). Isliye ab recurring
automation ka real route hai — process-loop ki zaroorat nahi.

Ye script har run par verified routes ka health check karta hai aur JSONL log likhta hai:
    logs/route_health.jsonl   -> har check ka record (machine-readable history)
    logs/route_health.txt     -> latest summary (human-readable)

Rate-limit discipline: 11 halke checks, 30 min ka gap (systemd timer se) — koi target spam nahi.
'local_rsshub'/'rsshub_thehindu' sirf tab OK honge jab RSSHub :1200 par chal raha ho (RUNBOOK §3).
"""
from __future__ import annotations
import json, os, subprocess, sys, time
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS = os.path.join(ROOT, "logs")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

CHECKS = [
    ("crossref_api",      "https://api.crossref.org/works?rows=1",                          "JSON"),
    ("stackexchange_api", "https://api.stackexchange.com/2.3/questions?site=stackoverflow&pagesize=1", "JSON"),
    ("wikipedia_api",     "https://en.wikipedia.org/api/rest_v1/page/summary/India",        "JSON"),
    ("wsj_rss",           "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",                  "XML"),
    ("wayback_cdx",       "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&limit=1", "JSON"),
    ("reader_proxy",      "https://r.jina.ai/https://example.com",                          "TEXT"),
    # ---- P15 (2026-09-23): naye live-verified routes (06_REPO_HUNT/probes/rsshub_routes_test2.txt)
    ("local_rsshub",      "http://127.0.0.1:1200/hackernews/best",                          "XML"),
    ("rsshub_thehindu",   "http://127.0.0.1:1200/thehindu/topic/rains",                     "XML"),
    ("discord_invite",    "https://discord.com/api/v9/invites/python?with_counts=true",     "JSON"),
    ("spotify_oembed",    "https://open.spotify.com/oembed?url=https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT", "JSON"),
    ("pullpush_reddit",   "https://api.pullpush.io/reddit/search/submission/?q=rss&size=1",  "JSON"),
]


def _one(url: str) -> tuple[int, int, str]:
    # IMPORTANT (2026-09-23 finding): reader-proxy (r.jina.ai) apne Cloudflare par FULL browser-UA ko
    # challenge karta hai ("Just a moment...") — neutral UA se 200 aata hai. Isliye proxy par alag UA.
    ua = "UAI-COS-monitor/1.0" if "r.jina.ai" in url else UA
    p = subprocess.run(["curl", "-s", "-L", "-m", "20", "-A", ua, "-o", "/tmp/_rm.out",
                        "-w", "%{http_code}", url], capture_output=True)
    code = int((p.stdout or b"0").decode() or 0)
    size = os.path.getsize("/tmp/_rm.out") if os.path.exists("/tmp/_rm.out") else 0
    snippet = ""
    if code != 200:
        try:
            snippet = open("/tmp/_rm.out", encoding="utf-8", errors="replace").read(200).replace("\n", " ")
        except OSError:
            pass
    return code, size, snippet


def check(name: str, url: str, expect: str) -> dict:
    """1 retry with backoff — transient rate-limits (e.g. reader-proxy burst limit) ko handle karta hai."""
    t0 = time.time()
    code, size, snippet = _one(url)
    if code != 200:
        time.sleep(8)
        code, size, snippet = _one(url)
    ok = code == 200 and size > 50
    rec = {"check": name, "http": code, "bytes": size, "ok": ok,
           "ms": int((time.time() - t0) * 1000)}
    if not ok and snippet:
        rec["error_snippet"] = snippet
    return rec


def hygiene() -> dict:
    """Workspace hygiene record — cleanup tool ka summary (delete nahi karta, sirf report)."""
    try:
        out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cleanup_workspace.py"), "--json"],
                             capture_output=True, text=True, timeout=180).stdout.strip()
        d = json.loads(out.splitlines()[-1])
        ok = (d["junk"] == 0 and d["empty"] == 0 and d["dupes"] == 0)
        return {"check": "workspace_hygiene", "http": 200, "bytes": d["total_before"], "ok": ok,
                "ms": 0, "detail": {k: d[k] for k in ("junk", "empty", "dupes", "bigdirs")}}
    except Exception as e:  # noqa: BLE001
        return {"check": "workspace_hygiene", "http": 0, "bytes": 0, "ok": False, "ms": 0, "error": str(e)}


def main() -> int:
    os.makedirs(LOGS, exist_ok=True)
    results = [check(*c) for c in CHECKS] + [hygiene()]
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    failed = [r["check"] for r in results if not r["ok"]]
    rec = {"ts": ts, "total": len(results), "passed": len(results) - len(failed),
           "failed": failed, "results": results}

    with open(os.path.join(LOGS, "route_health.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    lines = [f"UAI-COS ROUTE HEALTH — {ts}",
             f"passed {rec['passed']}/{rec['total']}" + (f"  | FAILED: {', '.join(failed)}" if failed else "  | sab routes theek"),
             ""]
    for r in results:
        extra = ""
        if r["check"] == "workspace_hygiene" and isinstance(r.get("detail"), dict):
            d = r["detail"]
            extra = f"  junk={d['junk']} empty={d['empty']} dupes={d['dupes']}"
        lines.append(f"  {'OK ' if r['ok'] else 'FAIL'}  {r['check']:18} HTTP {r['http']:<4} {r['bytes']:>8,} B  {r['ms']:>5} ms{extra}")
    out = "\n".join(lines) + "\n"
    with open(os.path.join(LOGS, "route_health.txt"), "w", encoding="utf-8") as f:
        f.write(out)
    print(out)
    return 0  # route failure = DATA, service failure nahi (systemd "failed" na dikhaye)


if __name__ == "__main__":
    sys.exit(main())
