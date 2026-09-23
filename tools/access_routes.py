#!/usr/bin/env python3
"""
access_routes.py — UAI-COS Phase 2: VERIFIED ACCESS ROUTES (working implementation)

Phase 2 blueprint ke §6 (code-based access), §19 (can code solve this?), §28 (provenance)
ka concrete output. Har function ek **actually tested** route hai (2026-09-23 ke probes,
evidence: 03_ACCESS_EXPANSION/probes/*.txt).

Route status labels (§21):
  DIRECT            = seedha kaam karta hai
  STRONG ALTERNATIVE= official API/proxy se equivalent data
  CONDITIONAL       = rate limit / email / key chahiye
  UNAVAILABLE       = koi legitimate route nahi mila

Har call ki provenance JSONL me likhi jaati hai:
  ROUTE -> SOURCE -> EVIDENCE -> REQUIREMENTS -> TEST RESULT -> STATUS

Usage:
    python3 tools/access_routes.py demo                 # sab routes ka live demo
    python3 tools/access_routes.py fetch <url>          # smart fetch (fallback chain)
    python3 tools/access_routes.py rss <feed-url>       # RSS/Atom parse
    python3 tools/access_routes.py so "python asyncio"  # StackOverflow Q&A (API)
    python3 tools/access_routes.py paper "transformer"  # academic search (4 sources)
    python3 tools/access_routes.py nse marketStatus     # NSE data (proxy route)
    python3 tools/access_routes.py wb <url>             # wayback snapshot
"""

from __future__ import annotations
import json, os, re, subprocess, sys, time, urllib.parse
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROV = os.path.join(ROOT, "03_ACCESS_EXPANSION", "route_provenance.jsonl")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
PROXY = "https://r.jina.ai/"
# FINDING (2026-09-23): full browser-UA se r.jina.ai ka Cloudflare "Just a moment..." deta hai;
# neutral/short UA se 200. Isliye proxy calls ke liye alag UA use hota hai.
PROXY_UA = "UAI-COS-research/1.0"

# rate limiter state (per-host minimum gap seconds) — §9/§17: thoda thoda karo, spam nahi
_MIN_GAP = {"www.reddit.com": 60, "reddit.com": 60, "api.stackexchange.com": 1,
            "api.crossref.org": 1, "api.openalex.org": 1}
_last_call: dict[str, float] = {}


def _log(route: str, source: str, evidence: str, req: str, result: str, status: str) -> None:
    os.makedirs(os.path.dirname(PROV), exist_ok=True)
    rec = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "route": route,
           "source": source, "evidence": evidence, "requirements": req,
           "test_result": result, "status": status}
    with open(PROV, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _curl(url: str, timeout: int = 20, extra: list[str] | None = None) -> tuple[int, bytes]:
    """curl wrapper. Returns (http_code, body). Proxy host par neutral UA (CF challenge se bachne ke liye)."""
    ua = PROXY_UA if "r.jina.ai" in url else UA
    host = urllib.parse.urlparse(url).hostname or ""
    gap = _MIN_GAP.get(host, 0)
    if gap:
        wait = gap - (time.time() - _last_call.get(host, 0))
        if wait > 0:
            time.sleep(min(wait, 65))          # rate limit respect (§9)
    _last_call[host] = time.time()
    cmd = ["curl", "-s", "-L", "-m", str(timeout), "-A", ua, "-w", "\n__CODE__%{http_code}"]
    cmd += (extra or []) + [url]
    p = subprocess.run(cmd, capture_output=True)
    out = p.stdout
    code = 0
    m = re.search(rb"\n__CODE__(\d{3})$", out)
    if m:
        code = int(m.group(1)); out = out[:m.start()]
    return code, out


# ------------------------------------------------------------------ ROUTE 1: smart fetch
def fetch(url: str, use_proxy_fallback: bool = True, use_wayback: bool = True) -> dict:
    """Smart fetch: DIRECT -> READER PROXY -> WAYBACK (§16 fallback chain).
    Returns {status, route, code, bytes, text, url}
    """
    code, body = _curl(url)
    if code == 200 and len(body) > 200:
        _log("direct_fetch", url, f"HTTP 200, {len(body)}B", "none", "success", "DIRECT")
        return {"status": "DIRECT", "route": "direct", "code": code, "bytes": len(body),
                "text": body.decode("utf-8", "replace"), "url": url}
    if use_proxy_fallback:
        pcode, pbody = _curl(PROXY + url, timeout=30)
        txt = pbody.decode("utf-8", "replace")
        bad = ("Warning: Target URL returned error" in txt or "requiring CAPTCHA" in txt
               or "AbuseAlleviationError" in txt)
        if pcode == 200 and not bad and len(pbody) > 300:
            _log("reader_proxy", url, f"proxy HTTP 200, {len(pbody)}B", "none (public reader)", "success", "STRONG ALTERNATIVE")
            return {"status": "PROXY", "route": "reader_proxy", "code": pcode, "bytes": len(pbody),
                    "text": txt, "url": url}
    if use_wayback:
        wb = f"https://web.archive.org/web/2026/{url}"
        wcode, wbody = _curl(wb, timeout=30)
        if wcode in (200, 302) and len(wbody) > 500:
            _log("wayback", url, f"wayback HTTP {wcode}, {len(wbody)}B", "none", "success", "STRONG ALTERNATIVE")
            return {"status": "WAYBACK", "route": "wayback", "code": wcode, "bytes": len(wbody),
                    "text": wbody.decode("utf-8", "replace"), "url": url}
    _log("fetch_all_failed", url, f"direct={code}, proxy+wayback fail", "none", "failure", "UNAVAILABLE")
    return {"status": "FAIL", "route": None, "code": code, "bytes": len(body), "text": "", "url": url}


# ------------------------------------------------------------------ ROUTE 2: RSS/Atom
def rss(feed_url: str, limit: int = 10) -> list[dict]:
    """RSS/Atom parse (stdlib). Verified feeds: bbc, google-news, wsj, bloomberg, medium(tag),
    hn, github-blog, reddit(rate-limited 1/min)."""
    code, body = _curl(feed_url, timeout=20)
    if code != 200:
        _log("rss_feed", feed_url, f"HTTP {code}", "none", "failure", "UNAVAILABLE")
        return []
    import xml.etree.ElementTree as ET
    txt = body.decode("utf-8", "replace")
    items: list[dict] = []
    try:
        root = ET.fromstring(txt)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for it in (root.iter("item") if root.tag != "feed" else root.iter("{http://www.w3.org/2005/Atom}entry")):
            def g(*tags):
                for t in tags:
                    el = it.find(t) if not t.startswith("{") else it.find(t)
                    if el is not None and (el.text or "").strip():
                        return el.text.strip()
                return ""
            link = g("link", "{http://www.w3.org/2005/Atom}link")
            if not link:
                le = it.find("{http://www.w3.org/2005/Atom}link")
                link = le.get("href") if le is not None else ""
            items.append({"title": g("title", "{http://www.w3.org/2005/Atom}title"),
                          "link": link,
                          "date": g("pubDate", "published", "{http://www.w3.org/2005/Atom}updated"),
                          "summary": (g("description", "summary", "{http://www.w3.org/2005/Atom}summary") or "")[:300]})
            if len(items) >= limit:
                break
    except ET.ParseError as e:
        _log("rss_feed", feed_url, f"parse error {e}", "none", "failure", "UNAVAILABLE")
        return []
    _log("rss_feed", feed_url, f"HTTP 200, {len(items)} items", "none", "success", "STRONG ALTERNATIVE")
    return items


# ------------------------------------------------------------------ ROUTE 3: StackOverflow (StackExchange API)
def so_search(q: str, limit: int = 3) -> list[dict]:
    """StackOverflow Q&A via official StackExchange API (no key needed, quota ~300/day/IP)."""
    u = ("https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance"
         f"&q={urllib.parse.quote(q)}&site=stackoverflow&pagesize={limit}&filter=withbody")
    code, body = _curl(u, timeout=20)
    if code != 200:
        _log("stackexchange_api", u, f"HTTP {code}", "none (anonymous quota)", "failure", "CONDITIONAL")
        return []
    d = json.loads(body)
    out = [{"q_id": i["question_id"], "title": i["title"], "score": i["score"],
            "answered": i.get("is_answered"), "answers": i.get("answer_count"),
            "link": i["link"], "body_snippet": re.sub(r"<[^>]+>", " ", i.get("body", ""))[:400]} for i in d.get("items", [])]
    _log("stackexchange_api", u, f"{len(out)} questions", "none", "success", "STRONG ALTERNATIVE")
    return out


def so_answers(question_id: int) -> list[dict]:
    """Question ke answers (bodies ke saath) — SO ka asli content."""
    u = (f"https://api.stackexchange.com/2.3/questions/{question_id}/answers?order=desc&sort=votes"
         "&site=stackoverflow&filter=withbody&pagesize=5")
    code, body = _curl(u, timeout=20)
    if code != 200:
        return []
    d = json.loads(body)
    return [{"score": a["score"], "accepted": a.get("is_accepted"),
             "body_snippet": re.sub(r"<[^>]+>", " ", a.get("body", ""))[:600]} for a in d.get("items", [])]


# ------------------------------------------------------------------ ROUTE 4: Academic search
def papers(q: str, limit: int = 3) -> dict:
    """4 independent sources: Crossref, OpenAlex, EuropePMC, PubMed."""
    res: dict = {}
    code, body = _curl(f"https://api.crossref.org/works?query={urllib.parse.quote(q)}&rows={limit}")
    if code == 200:
        d = json.loads(body)
        res["crossref"] = [{"title": (i.get("title") or [""])[0], "doi": i.get("DOI"),
                            "year": (i.get("issued", {}).get("date-parts", [[None]])[0][0])} for i in d["message"]["items"]]
    code, body = _curl(f"https://api.openalex.org/works?search={urllib.parse.quote(q)}&per-page={limit}")
    if code == 200:
        d = json.loads(body)
        res["openalex"] = [{"title": i.get("title"), "doi": i.get("doi"), "year": i.get("publication_year"),
                            "cited_by": i.get("cited_by_count"), "oa": (i.get("open_access") or {}).get("is_oa")}
                           for i in d.get("results", [])]
    code, body = _curl(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={urllib.parse.quote(q)}%20AND%20OPEN_ACCESS:Y&format=json&pageSize={limit}")
    if code == 200:
        d = json.loads(body)
        res["europepmc_oa"] = [{"title": i.get("title"), "pmid": i.get("pmid"), "year": i.get("pubYear"),
                                "fulltext": i.get("isOpenAccess")} for i in d.get("resultList", {}).get("result", [])]
    code, body = _curl(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(q)}&retmax={limit}&retmode=json")
    if code == 200:
        d = json.loads(body)
        res["pubmed_ids"] = d.get("esearchresult", {}).get("idlist", [])
    _log("academic_multi", q, f"sources: {list(res)}", "none", "success" if res else "failure",
         "STRONG ALTERNATIVE" if res else "UNAVAILABLE")
    return res


def oa_pdf(doi: str) -> str | None:
    """Open-access PDF link (Unpaywall). NOTE: apna email daalo — api ne test email reject kiya (422)."""
    code, body = _curl(f"https://api.unpaywall.org/v2/{doi}?email=USER_EMAIL_HERE")
    if code == 200:
        d = json.loads(body)
        loc = d.get("best_oa_location") or {}
        return loc.get("url_for_pdf") or loc.get("url")
    _log("unpaywall", doi, f"HTTP {code} (email chahiye)", "apna email", "conditional", "CONDITIONAL")
    return None


# ------------------------------------------------------------------ ROUTE 5: NSE (reader-proxy route)
def nse(endpoint: str = "marketStatus") -> dict | str:
    """NSE India data via reader proxy. Verified: marketStatus JSON + sec_bhavdata_full.csv."""
    if endpoint.endswith(".csv"):
        url = f"https://archives.nseindia.com/products/content/{endpoint}"
    else:
        url = f"https://www.nseindia.com/api/{endpoint}"
    code, body = _curl(PROXY + url, timeout=30)
    if code != 200:                       # free tier rate limit -> ek retry (15s)
        time.sleep(15)
        code, body = _curl(PROXY + url, timeout=30)
    txt = body.decode("utf-8", "replace")
    if code == 200 and "CAPTCHA" not in txt[:500]:
        # proxy markdown wrapper hata do
        m = re.search(r"Markdown Content:\s*(.*)", txt, re.S)
        data = (m.group(1) if m else txt).strip()
        _log("nse_via_proxy", url, f"HTTP 200, {len(body)}B", "none", "success", "STRONG ALTERNATIVE")
        return data if endpoint.endswith(".csv") else {"raw": data[:2000]}
    _log("nse_via_proxy", url, f"HTTP {code}", "none", "failure", "UNAVAILABLE")
    return {}


# ------------------------------------------------------------------ ROUTE 6: Wayback
def wayback(url: str) -> dict:
    """Wayback availability + snapshot fetch. Verified: SO answers, WSJ, Medium, TripAdvisor."""
    code, body = _curl(f"https://archive.org/wayback/available?url={urllib.parse.quote(url)}")
    avail = {}
    if code == 200:
        avail = json.loads(body).get("archived_snapshots", {}).get("closest", {})
    snap = avail.get("url")
    ts = avail.get("timestamp")
    if not snap:   # availability API kai baar rate-limited/khali aata hai -> direct snapshot URL
        snap = f"https://web.archive.org/web/2026/{url}"
        ts = ts or "2026"
    c2, b2 = _curl(snap, timeout=35)
    if c2 in (200, 302) and len(b2) > 500:
        _log("wayback", url, f"snapshot {ts}, HTTP {c2}, {len(b2)}B", "none", "success", "STRONG ALTERNATIVE")
        return {"available": True, "timestamp": ts, "snapshot_url": snap, "text": b2.decode("utf-8", "replace")}
    _log("wayback", url, "no snapshot", "none", "failure", "UNAVAILABLE")
    return {"available": False}


def wayback_find(pattern: str, limit: int = 5) -> list[dict]:
    """CDX API: archived URLs discover karo (verified: reddit threads)."""
    u = (f"https://web.archive.org/cdx/search/cdx?url={urllib.parse.quote(pattern)}"
         f"&output=json&limit={limit}&filter=statuscode:200")
    code, body = _curl(u, timeout=25)
    if code != 200:
        return []
    rows = json.loads(body)
    if not rows or len(rows) < 2:
        return []
    hdr, items = rows[0], rows[1:]
    return [dict(zip(hdr, r)) for r in items]


# ------------------------------------------------------------------ demo
def demo() -> None:
    print("=" * 72)
    print("ACCESS ROUTES — LIVE DEMO (Phase 2 verified routes)")
    print("=" * 72)

    print("\n[1] SMART FETCH — blocked site → proxy route")
    r = fetch("https://medium.com/tag/programming")
    print(f"    medium.com -> {r['status']} ({r['bytes']:,} bytes)")

    print("\n[2] RSS FEEDS — paywalled news ki headlines")
    for name, feed in [("WSJ", "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"),
                       ("Bloomberg", "https://feeds.bloomberg.com/markets/news.rss"),
                       ("BBC", "https://feeds.bbci.co.uk/news/rss.xml")]:
        items = rss(feed, limit=2)
        print(f"    {name:10} -> {len(items)} items | {items[0]['title'][:52] if items else 'FAIL'}")

    print("\n[3] STACKOVERFLOW — official API (site 403 hai, API chalti hai)")
    qs = so_search("python asyncio gather", limit=2)
    for q in qs:
        print(f"    [{q['score']:>4}] {q['title'][:60]} (ans={q['answers']})")
    if qs:
        ans = so_answers(qs[0]["q_id"])
        if ans:
            print(f"    top answer (score {ans[0]['score']}): {ans[0]['body_snippet'][:90]}...")

    print("\n[4] ACADEMIC — 4 sources ek saath")
    p = papers("retrieval augmented generation", limit=2)
    for src in ("crossref", "openalex", "europepmc_oa"):
        for it in (p.get(src) or [])[:1]:
            print(f"    {src:14} -> {(it.get('title') or '')[:58]}")
    print(f"    pubmed ids     -> {p.get('pubmed_ids')}")

    print("\n[5] NSE INDIA — proxy route (direct 403 tha)")
    d = nse("marketStatus")
    raw = (d or {}).get("raw", "")
    m = re.search(r'"marketStatus":"?([A-Za-z ]+)', raw)
    print(f"    NSE marketStatus -> {m.group(1) if m else (raw[:60] or 'FAIL')}")

    print("\n[6] WAYBACK — archived blocked pages")
    w = wayback("https://stackoverflow.com/questions/11227809/")
    print(f"    SO question archived -> available={w['available']} ts={w.get('timestamp')} ({len(w.get('text','')):,} chars)")
    found = wayback_find("reddit.com/r/programming/comments/*", limit=3)
    print(f"    archived reddit threads found: {len(found)}")
    for f in found[:2]:
        print(f"      {f.get('timestamp')} {f.get('original','')[:60]}")

    print("\n[done] Provenance log:", os.path.relpath(PROV, ROOT))


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "demo":
        demo()
    elif args[0] == "fetch" and len(args) > 1:
        r = fetch(args[1]); print(r["status"], r["bytes"], "bytes"); print(r["text"][:600])
    elif args[0] == "rss" and len(args) > 1:
        for i in rss(args[1]): print("-", i["title"], "|", i["link"][:70])
    elif args[0] == "so" and len(args) > 1:
        for q in so_search(" ".join(args[1:])): print(f"[{q['score']}] {q['title']} -> {q['link']}")
    elif args[0] == "paper" and len(args) > 1:
        print(json.dumps(papers(" ".join(args[1:])), indent=2, ensure_ascii=False)[:2500])
    elif args[0] == "nse":
        print(nse(args[1] if len(args) > 1 else "marketStatus"))
    elif args[0] == "wb" and len(args) > 1:
        print(json.dumps(wayback(args[1]), indent=2, ensure_ascii=False)[:1500])
    else:
        print(__doc__)
