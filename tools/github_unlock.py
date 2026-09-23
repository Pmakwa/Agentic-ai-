#!/usr/bin/env python3
"""
github_unlock.py — UAI-COS GITHUB UNLOCK TOOLKIT (2026-09-23, verified)

GitHub se jo kuch bina token ke unlock hota hai, uska working wrapper.
Sab commands actually test kiye gaye hain (evidence: 04_GITHUB_UNLOCK/probes/).

Verified token-less capabilities:
  • API   : repo metadata, repo search (10/min), issues search, advisories, gists, releases+assets
  • RAW   : raw.githubusercontent.com (koi API quota nahi) — code/data files
  • ZIP   : codeload.github.com (bina git clone)
  • GIT   : clone --depth 1 (2 sec test), wiki clone
  • BIN   : release se static binary download + execute (yq v4.53.6 verified)
  • PKG   : pip install git+https://github.com/... (verified)
  • DATA  : GH Archive public events (18 MB/hour gz, 5000 events parsed)
  • CONT  : public container images (crane se, Docker ke bina — alpine 8.7 MB export verified)
  • TREND : trending substitute via search API (created:>date&sort=stars)

Token ke bina KAAM NAHI karta (401 verified):
  • Code search API  • gh CLI (auth required)  • GraphQL  • Actions logs/artifacts  • write ops (push/gist/PR)

Usage:
    python3 tools/github_unlock.py rate
    python3 tools/github_unlock.py repo yt-dlp/yt-dlp
    python3 tools/github_unlock.py search "whisper cpp" --sort stars
    python3 tools/github_unlock.py issues "repo:yt-dlp/yt-dlp cookies"
    python3 tools/github_unlock.py advisories
    python3 tools/github_unlock.py release yt-dlp/yt-dlp            # latest release + assets
    python3 tools/github_unlock.py getbin mikefarah/yq linux_amd64  # asset download + extract
    python3 tools/github_unlock.py raw https://raw.githubusercontent.com/.../file
    python3 tools/github_unlock.py clone cli/cli                    # depth-1 clone
    python3 tools/github_unlock.py trending                          # naye top-star repos
    python3 tools/github_unlock.py archive 2026-09-22-12             # GH Archive hourly events
    python3 tools/github_unlock.py container alpine:latest           # crane se image export
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
API = "https://api.github.com"
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")


def _curl(url: str, out: str | None = None, timeout: int = 30, extra: list[str] | None = None) -> tuple[int, bytes]:
    cmd = ["curl", "-sL", "-m", str(timeout), "-A", UA, "-H", "Accept: application/vnd.github+json",
           "-w", "\n__CODE__%{http_code}"]
    if out:
        cmd += ["-o", out]
    cmd += (extra or []) + [url]
    p = subprocess.run(cmd, capture_output=True)
    body = p.stdout
    code = 0
    marker = b"\n__CODE__"
    i = body.rfind(marker)
    if i >= 0:
        code = int(body[i + len(marker):].strip() or 0)
        body = body[:i]
    return code, body


def _api(path: str) -> dict:
    code, body = _curl(f"{API}{path}")
    if code != 200:
        raise SystemExit(f"[gh] HTTP {code} for {path}: {body[:200].decode(errors='replace')}")
    return json.loads(body)


def cmd_rate(_a):
    d = _api("/rate_limit")["resources"]
    print("GitHub API quota (bina token):")
    for k in ("core", "search", "code_search", "graphql"):
        v = d.get(k, {})
        print(f"  {k:12} {v.get('remaining', 0):>5}/{v.get('limit', 0):<5}")
    print("\nNote: code_search limit 0/0 = token ke bina kaam nahi karta (401 verified).")
    return 0


def cmd_repo(a):
    d = _api(f"/repos/{a.slug}")
    lic = (d.get("license") or {}).get("spdx_id")
    print(f"{d['full_name']}  ★{d['stargazers_count']:,}  forks={d['forks_count']:,}  "
          f"lang={d['language']}  license={lic}\n  {(d.get('description') or '')[:110]}")
    return 0


def cmd_search(a):
    d = _api(f"/search/repositories?q={a.query.replace(' ', '+')}&sort={a.sort}&order=desc&per_page={a.n}")
    print(f"total: {d['total_count']:,}")
    for r in d["items"]:
        print(f"  {r['full_name']:<42} ★{r['stargazers_count']:>8,}  {(r.get('description') or '')[:52]}")
    return 0


def cmd_issues(a):
    d = _api(f"/search/issues?q={a.query.replace(' ', '+')}&per_page={a.n}")
    print(f"total: {d['total_count']:,}")
    for i in d["items"]:
        print(f"  [{i['state']:>6}] {i['title'][:78]}")
    return 0


def cmd_advisories(a):
    d = _api(f"/advisories?per_page={a.n}")
    for x in d:
        print(f"  {x['ghsa_id']}  {x['severity']:>8}  {x['summary'][:64]}")
    return 0


def cmd_release(a):
    d = _api(f"/repos/{a.slug}/releases/latest")
    print(f"{a.slug} — {d['tag_name']}  ({d.get('published_at', '')[:10]})")
    for x in d.get("assets", []):
        print(f"  {x['name']:<44} {x['size']/1e6:>7.2f} MB  dl={x['download_count']:,}")
    return 0


def cmd_getbin(a):
    d = _api(f"/repos/{a.slug}/releases/latest")
    match = [x for x in d["assets"] if a.match in x["name"] and not x["name"].endswith(".sha256")]
    if not match:
        raise SystemExit(f"koi asset '{a.match}' nahi mila")
    asset = match[0]
    dest = os.path.join(os.path.expanduser("~"), f"/tmp/{asset['name']}")
    os.makedirs(BIN, exist_ok=True)
    t0 = time.time()
    code, _ = _curl(asset["browser_download_url"], out=dest, timeout=180)
    size = os.path.getsize(dest) if os.path.exists(dest) else 0
    print(f"downloaded {asset['name']} -> {dest} ({size/1e6:.1f} MB, {time.time()-t0:.1f}s)")
    if dest.endswith((".tar.gz", ".tgz")):
        outdir = os.path.join(BIN, a.slug.split("/")[-1])
        os.makedirs(outdir, exist_ok=True)
        subprocess.run(["tar", "-xzf", dest, "-C", outdir], check=False)
        for root, _, files in os.walk(outdir):
            for f in files:
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                print(f"  extracted: {p}")
        print(f"  -> tools/bin/{a.slug.split('/')[-1]}/ me ready (PATH me bas jodo)")
    else:
        os.chmod(dest, 0o755)
        print("  executable ready:", dest)
    return 0


def cmd_raw(a):
    code, body = _curl(a.url)
    print(f"HTTP {code}, {len(body)} B")
    sys.stdout.write(body[:1200].decode("utf-8", "replace"))
    return 0


def cmd_clone(a):
    dest = f"/tmp/gh_{a.slug.replace('/', '_')}"
    t0 = time.time()
    r = subprocess.run(["git", "clone", "-q", "--depth", "1", f"https://github.com/{a.slug}", dest])
    if r.returncode == 0:
        size = subprocess.run(["du", "-sh", dest], capture_output=True).stdout.decode().split()[0]
        print(f"cloned {a.slug} -> {dest} ({size}, {time.time()-t0:.1f}s)")
    return r.returncode


def cmd_trending(a):
    since = time.strftime("%Y-%m-%d", time.localtime(time.time() - a.days * 86400))
    d = _api(f"/search/repositories?q=created:>{since}&sort=stars&order=desc&per_page={a.n}")
    print(f"top naye repos (created > {since}):")
    for r in d["items"]:
        print(f"  {r['full_name']:<42} ★{r['stargazers_count']:>8,}  {(r.get('description') or '')[:50]}")
    return 0


def cmd_archive(a):
    url = f"https://data.gharchive.org/{a.hour}.json.gz"
    dest = f"/tmp/gharchive_{a.hour}.json.gz"
    code, _ = _curl(url, out=dest, timeout=240)
    size = os.path.getsize(dest) if os.path.exists(dest) else 0
    print(f"GH Archive {a.hour}: HTTP {code}, {size/1e6:.1f} MB -> {dest}")
    if size > 0:
        import gzip
        n, types = 0, {}
        with gzip.open(dest, "rt", errors="replace") as f:
            for line in f:
                try:
                    e = json.loads(line)
                except Exception:
                    continue
                n += 1
                types[e.get("type")] = types.get(e.get("type"), 0) + 1
                if n >= 2000:
                    break
        print(f"  events sample: {n} | types: {sorted(types.items(), key=lambda x: -x[1])[:3]}")
    return 0


def cmd_container(a):
    crane = os.path.join(BIN, "crane")
    if not os.path.exists(crane):
        raise SystemExit("crane missing — pehle: python3 tools/github_unlock.py getbin google/go-containerregistry Linux_x86_64")
    dest = f"/tmp/img_{a.image.replace(':', '_').replace('/', '_')}.tar"
    r = subprocess.run([crane, "export", a.image, dest])
    if r.returncode == 0:
        n = subprocess.run(["tar", "-tf", dest], capture_output=True).stdout.count(b"\n")
        print(f"container export: {a.image} -> {dest} ({os.path.getsize(dest)/1e6:.1f} MB, {n} files)")
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="GitHub unlock toolkit (bina token)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("rate").set_defaults(fn=cmd_rate)

    p = sub.add_parser("repo"); p.add_argument("slug"); p.set_defaults(fn=cmd_repo)
    p = sub.add_parser("search"); p.add_argument("query"); p.add_argument("--sort", default="stars"); p.add_argument("-n", type=int, default=5); p.set_defaults(fn=cmd_search)
    p = sub.add_parser("issues"); p.add_argument("query"); p.add_argument("-n", type=int, default=5); p.set_defaults(fn=cmd_issues)
    p = sub.add_parser("advisories"); p.add_argument("-n", type=int, default=5); p.set_defaults(fn=cmd_advisories)
    p = sub.add_parser("release"); p.add_argument("slug"); p.set_defaults(fn=cmd_release)
    p = sub.add_parser("getbin"); p.add_argument("slug"); p.add_argument("match"); p.set_defaults(fn=cmd_getbin)
    p = sub.add_parser("raw"); p.add_argument("url"); p.set_defaults(fn=cmd_raw)
    p = sub.add_parser("clone"); p.add_argument("slug"); p.set_defaults(fn=cmd_clone)
    p = sub.add_parser("trending"); p.add_argument("--days", type=int, default=7); p.add_argument("-n", type=int, default=5); p.set_defaults(fn=cmd_trending)
    p = sub.add_parser("archive"); p.add_argument("hour", help="YYYY-MM-DD-HH"); p.set_defaults(fn=cmd_archive)
    p = sub.add_parser("container"); p.add_argument("image"); p.set_defaults(fn=cmd_container)

    a = ap.parse_args()
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
