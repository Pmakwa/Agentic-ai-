#!/usr/bin/env python3
"""
uai_mem.py — UAI-COS v2.0 Memory Operating System (file-backed implementation)

Ye tool UAI-COS V2.0 spec ke Memory Record Schema (Section 13), Memory Status Model
(Section 14), Confidence Engine (Section 15), Provenance (Section 16), Decay/Expiry
(Section 20), Conflict Engine (Section 21) aur Memory Health Audit (Section 80) ka
concrete, chalne wala implementation hai.

Storage : memory/store/memory.jsonl   (append-friendly, line-per-record, git-friendly)
Index   : memory/INDEX.md             (generated - kabhi manually edit na karo)
Dashboard: DASHBOARD.html             (generated, offline single-file)

Usage examples:
  python3 tools/uai_mem.py add --type preference --statement "User Roman Hindi me baat chahta hai" \
      --source user_instruction --authority user_explicit --confidence high --tags language
  python3 tools/uai_mem.py list --type preference --status active
  python3 tools/uai_mem.py search "image prompt"
  python3 tools/uai_mem.py audit
  python3 tools/uai_mem.py index && python3 tools/uai_mem.py dash
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# UAI_STORE / UAI_ARCHIVE env vars se test isolation possible hai (tests/test_memory_os.sh dekho).
STORE = os.environ.get("UAI_STORE", os.path.join(ROOT, "memory", "store", "memory.jsonl"))
ARCHIVE = os.environ.get("UAI_ARCHIVE", os.path.join(ROOT, "memory", "store", "archive.jsonl"))
INDEX = os.environ.get("UAI_INDEX", os.path.join(ROOT, "memory", "INDEX.md"))
DASHBOARD = os.environ.get("UAI_DASH", os.path.join(ROOT, "DASHBOARD.html"))
AUDIT_LOG = os.environ.get("UAI_AUDIT_LOG", os.path.join(ROOT, "logs", "AUDIT_LOG.md"))

# ---------------------------------------------------------------- enums / schema
# Spec V2 #12 — 15 advanced memory types (V1 ke 12 + temporal, relational, procedural_state)
TYPES = [
    "core", "preference", "constraint", "semantic", "episodic", "procedural",
    "working", "project", "decision", "error", "source", "shared",
    "temporal", "relational", "procedural_state",
]
# Spec V2 #14 — status model (primary flow + alternative states)
STATUSES = ["candidate", "unverified", "verified", "active", "uncertain",
            "conflicted", "expired", "superseded", "archived", "deleted", "quarantined"]
# Spec V2 #15 — confidence engine bands (false precision avoid karna hai)
CONFIDENCE = ["very_high", "high", "medium", "low", "very_low"]
AUTHORITY = ["user_explicit", "user_correction", "user_implied", "verified_source",
             "derived", "agent_inference"]
SENSITIVITY = ["normal", "private", "secret"]

PREFIX = {
    "core": "CORE", "preference": "PREF", "constraint": "CONS", "semantic": "SEM",
    "episodic": "EPI", "procedural": "PROC", "working": "WORK", "project": "PROJ",
    "shared": "SHAR", "source": "SRC", "decision": "DEC", "error": "ERR",
    "temporal": "TEMP", "relational": "REL", "procedural_state": "PSTATE",
}

REQUIRED = ["id", "type", "statement", "source", "scope", "confidence",
            "status", "authority", "created_at", "history"]


def today() -> str:
    return dt.date.today().isoformat()


def now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()


def sha(text: str) -> str:
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()[:12]


# ---------------------------------------------------------------- store io
def load(path: str = STORE) -> list[dict]:
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[WARN] store line {ln} corrupt: {e}", file=sys.stderr)
    return out


def save(records: list[dict], path: str = STORE) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def next_id(records: list[dict], mtype: str) -> str:
    pre = PREFIX[mtype]
    nums = [int(r["id"].split("-")[-1]) for r in records
            if r["id"].startswith(f"MEM-{pre}-") and r["id"].split("-")[-1].isdigit()]
    return f"MEM-{pre}-{(max(nums) + 1) if nums else 1:04d}"


def log_audit(action: str, detail: str) -> None:
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    line = f"| {now()} | {action} | {detail} |"
    header = "| timestamp | action | detail |\n|---|---|---|\n"
    if not os.path.exists(AUDIT_LOG):
        open(AUDIT_LOG, "w", encoding="utf-8").write(
            "# AUDIT LOG — UAI-COS v2.0\n\n"
            "Section 61 (Decision Audit Trail) aur Section 51 (Observability) ka backing log.\n\n" + header)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------- validation
def validate(rec: dict) -> list[str]:
    issues = []
    for k in REQUIRED:
        if k not in rec or rec[k] in ("", None, []):
            issues.append(f"missing field: {k}")
    if rec.get("type") not in TYPES:
        issues.append(f"invalid type: {rec.get('type')}")
    if rec.get("status") not in STATUSES:
        issues.append(f"invalid status: {rec.get('status')}")
    if rec.get("confidence") not in CONFIDENCE:
        issues.append(f"invalid confidence: {rec.get('confidence')}")
    if rec.get("authority") not in AUTHORITY:
        issues.append(f"invalid authority: {rec.get('authority')}")
    if rec.get("sensitivity", "normal") not in SENSITIVITY:
        issues.append(f"invalid sensitivity: {rec.get('sensitivity')}")
    src = rec.get("source") or {}
    if not src.get("kind"):
        issues.append("source.kind missing (Section 7 — Provenance Always)")
    # Governance rule: high-confidence fact ko provenance chahiye
    if rec.get("confidence") == "high" and rec.get("type") in ("semantic", "source"):
        if src.get("kind") in (None, "", "agent_inference", "unknown"):
            issues.append("high-confidence fact without verifiable source")
    return issues


# ---------------------------------------------------------------- commands
def cmd_add(a) -> int:
    records = load()
    src_kind = a.source
    rec = {
        "id": a.id or next_id(records, a.type),
        "type": a.type,
        "statement": a.statement.strip(),
        "detail": (a.detail or "").strip(),
        "source": {"kind": src_kind, "ref": a.ref or "", "url": a.url or "",
                   "observed_at": a.observed or today()},
        "scope": {"domains": a.domain or [], "projects": a.project or [],
                  "agents": a.agent or []},
        "applies_when": a.applies_when or "",
        "does_not_apply_when": a.does_not_apply_when or "",
        "confidence": a.confidence,
        "status": a.status,
        "authority": a.authority,
        "sensitivity": a.sensitivity,
        "tags": a.tag or [],
        "created_at": now(),
        "last_verified": a.verified or (today() if a.status == "verified" else ""),
        "expires_at": a.expires or "",
        "supersedes": a.supersedes or "",
        "superseded_by": "",
        "fingerprint": sha(a.statement),
        "history": [{"ts": now(), "action": "created", "note": a.note or ""}],
    }
    issues = validate(rec)
    if issues and not a.force:
        print("[BLOCKED] Record governance rules fail hua:")
        for i in issues:
            print("  -", i)
        print("  (schema ke liye --force use karo, lekin audit me issue rahega)")
        return 2

    # duplicate / conflict detection (Section 21 + Memory Deduplication)
    for other in records:
        if other["status"] in ("deleted", "archived") :
            continue
        if other.get("fingerprint") == rec["fingerprint"]:
            print(f"[DUPLICATE] {other['id']} me same statement pehle se hai. Skip.")
            return 3
        if a.conflict_key and other.get("conflict_key") == a.conflict_key \
           and other["statement"] != rec["statement"] \
           and other["status"] in ("active", "verified", "candidate"):
            rec["status"] = "conflicted"
            other["status"] = "conflicted"
            other.setdefault("history", []).append(
                {"ts": now(), "action": "conflict_detected", "note": f"conflict with {rec['id']} (key={a.conflict_key})"})
            print(f"[CONFLICT] {other['id']} <-> {rec['id']} same key '{a.conflict_key}' par alag statement. "
                  f"Dono ko 'conflicted' mark kiya — Section 21 conflict engine please.")

    rec["conflict_key"] = a.conflict_key or ""
    rec["supersedes_by_note"] = None
    rec.pop("supersedes_by_note")
    records.append(rec)
    save(records)
    log_audit("memory.add", f"{rec['id']} ({rec['type']}/{rec['status']}) '{rec['statement'][:70]}'")
    print(f"[OK] {rec['id']} added ({rec['type']}, status={rec['status']}, confidence={rec['confidence']})")
    return 0


def _fmt_row(r: dict, wide: bool = False) -> str:
    base = f"{r['id']:<13} {r['type']:<11} {r['status']:<11} {r['confidence']:<7} {r['statement']}"
    if wide:
        base += f"\n    src={r['source'].get('kind')}:{r['source'].get('ref','') or '-'}  tags={','.join(r.get('tags') or []) or '-'}"
        if r.get("detail"):
            base += f"\n    detail: {r['detail']}"
    return base[:4000]


def cmd_list(a) -> int:
    rows = load()
    if a.type:
        rows = [r for r in rows if r["type"] in a.type]
    if a.status:
        rows = [r for r in rows if r["status"] in a.status]
    if a.confidence:
        rows = [r for r in rows if r["confidence"] in a.confidence]
    if a.tag:
        rows = [r for r in rows if set(a.tag) & set(r.get("tags") or [])]
    if a.project:
        rows = [r for r in rows if set(a.project) & set((r.get("scope") or {}).get("projects") or [])]
    if not a.all:
        rows = [r for r in rows if r["status"] not in ("deleted",)]
    rows.sort(key=lambda r: (r["type"], r["id"]))
    print(f"# {len(rows)} record(s)\n")
    for r in rows:
        print(_fmt_row(r, wide=a.wide))
    return 0


def cmd_search(a) -> int:
    q = a.query.lower()
    rows = [r for r in load() if q in json.dumps(r, ensure_ascii=False).lower()]
    print(f"# {len(rows)} hit(s) for '{a.query}'\n")
    for r in rows:
        print(_fmt_row(r, wide=a.wide))
    return 0


def cmd_show(a) -> int:
    for r in load():
        if r["id"].lower() == a.id.lower():
            print(json.dumps(r, ensure_ascii=False, indent=2))
            return 0
    print(f"[MISS] {a.id} nahi mila")
    return 1


def cmd_update(a) -> int:
    rows = load()
    hit = None
    for r in rows:
        if r["id"].lower() == a.id.lower():
            hit = r
            break
    if not hit:
        print(f"[MISS] {a.id} nahi mila")
        return 1
    before = {k: hit.get(k) for k in ("status", "confidence", "statement", "expires_at")}
    for field in ("status", "confidence", "statement", "detail", "authority",
                  "sensitivity", "expires", "scope_note"):
        val = getattr(a, field.replace("expires", "expires"), None)
        if val is None:
            continue
        key = "expires_at" if field == "expires" else field
        if key == "scope_note":
            continue
        hit[key] = val
    if a.tag is not None:
        hit["tags"] = a.tag
    hit.setdefault("history", []).append(
        {"ts": now(), "action": "updated", "note": a.note or f"before={before}"})
    save(rows)
    log_audit("memory.update", f"{hit['id']} {a.note or ''}")
    print(f"[OK] {hit['id']} updated. history += 1")
    return 0


def cmd_supersede(a) -> int:
    rows = {r["id"]: r for r in load()}
    old, new = rows.get(a.old), rows.get(a.new)
    if not old or not new:
        print("[MISS] old ya new id nahi mila")
        return 1
    old["status"] = "superseded"
    old["superseded_by"] = new["id"]
    new["supersedes"] = old["id"]
    ts = now()
    old.setdefault("history", []).append({"ts": ts, "action": "superseded", "note": f"by {new['id']} — {a.note or ''}"})
    new.setdefault("history", []).append({"ts": ts, "action": "supersedes", "note": f"{old['id']} — {a.note or ''}"})
    save(list(rows.values()))
    log_audit("memory.supersede", f"{old['id']} -> {new['id']} ({a.note or ''})")
    print(f"[OK] {old['id']} superseded by {new['id']}")
    return 0


def cmd_expire(a) -> int:
    rows = load()
    n = 0
    for r in rows:
        if r.get("expires_at") and r["expires_at"] <= a.date and r["status"] in ("active", "verified", "candidate"):
            r["status"] = "expired"
            r.setdefault("history", []).append({"ts": now(), "action": "expired", "note": f"expires_at={r['expires_at']}"})
            n += 1
    save(rows)
    log_audit("memory.expire", f"{n} record(s) expired as of {a.date}")
    print(f"[OK] {n} record(s) expired")
    return 0


def cmd_archive(a) -> int:
    rows = load()
    keep, moved = [], []
    for r in rows:
        if r["id"].lower() == a.id.lower() or (a.status and r["status"] == a.status and r["type"] in a.type):
            r["status"] = "archived"
            r.setdefault("history", []).append({"ts": now(), "action": "archived", "note": a.note or ""})
            moved.append(r)
        else:
            keep.append(r)
    save(keep)
    if moved:
        old = load(ARCHIVE)
        save(old + moved, ARCHIVE)
    else:
        save(keep)
    print(f"[OK] {len(moved)} record(s) archived")
    return 0


def cmd_audit(a) -> int:
    """Memory Health Audit — Section 80 + Quality Metrics (Section 53)."""
    rows = load()
    live = [r for r in rows if r["status"] != "deleted"]
    issues = defaultdict(list)

    for r in live:
        for i in validate(r):
            issues["schema"].append(f"{r['id']}: {i}")
        if r.get("expires_at") and r["expires_at"] <= today() and r["status"] in ("active", "verified"):
            issues["expired_but_active"].append(r["id"])
        if r["confidence"] == "low" and r["status"] == "verified":
            issues["verified_but_low_conf"].append(r["id"])
        if r["authority"] == "agent_inference" and r["status"] in ("active", "verified") and r["type"] in ("semantic", "core"):
            issues["inference_promoted_to_fact"].append(r["id"])
        if r["type"] in ("working",) and r["status"] == "active":
            age = (dt.date.today() - dt.date.fromisoformat(r["created_at"][:10])).days
            if age > a.working_ttl:
                issues["stale_working_memory"].append(f"{r['id']} ({age}d)")
        # Section 6/17: preference/constraint/core ka scope ya applies_when hona chahiye.
        # "global" tag ek explicit, documented scope declaration maana jaata hai.
        if r["type"] in ("preference", "constraint", "core") \
           and not (r.get("scope") or {}).get("domains") \
           and not r.get("applies_when") and "global" not in (r.get("tags") or []):
            issues["unscoped_preference"].append(r["id"])
        if r["sensitivity"] in ("private", "secret") and "shared" in (r.get("tags") or []):
            issues["privacy_leak_risk"].append(r["id"])

    # conflicts
    bykey = defaultdict(list)
    for r in live:
        if r.get("conflict_key") and r["status"] in ("active", "verified", "conflicted", "candidate"):
            bykey[r["conflict_key"]].append(r)
    for k, group in bykey.items():
        if len(group) > 1:
            issues["open_conflict"].append(f"{k}: {', '.join(x['id'] for x in group)}")

    # dangling / duplicated
    ids = {r["id"] for r in rows}
    for r in live:
        if r.get("superseded_by") and r["superseded_by"] not in ids:
            issues["dangling_supersede"].append(r["id"])
    seen = defaultdict(list)
    for r in live:
        if r["status"] != "archived":
            seen[r["fingerprint"]].append(r["id"])
    for fp, group in seen.items():
        if len(group) > 1:
            issues["duplicate"].append(", ".join(group))

    # freshness
    stale = []
    for r in live:
        if r["type"] in ("semantic", "source") and r.get("last_verified"):
            age = (dt.date.today() - dt.date.fromisoformat(r["last_verified"])).days
            if age > a.fact_freshness_days:
                stale.append(f"{r['id']} ({age}d)")
    if stale:
        issues["stale_facts"] = stale

    print(f"# MEMORY HEALTH AUDIT — {today()}  ({len(live)} live records)\n")
    if not issues:
        print("PASS — koi issue nahi mila.")
    for k in sorted(issues):
        print(f"[{k}] {len(issues[k])}")
        for i in issues[k][:20]:
            print("   -", i)
    score = max(0, 100 - 5 * sum(len(v) for v in issues.values())if issues else 100)
    print(f"\nHEALTH SCORE: {score}/100")
    if a.log:
        log_audit("memory.audit", f"score={score} issues={ {k: len(v) for k, v in issues.items()} }")
    return 0 if score >= a.fail_under else 1


def cmd_stats(a) -> int:
    rows = load()
    print(f"total records      : {len(rows)}")
    print("by type            :", dict(Counter(r["type"] for r in rows)))
    print("by status          :", dict(Counter(r["status"] for r in rows)))
    print("by confidence      :", dict(Counter(r["confidence"] for r in rows)))
    print("by authority       :", dict(Counter(r["authority"] for r in rows)))
    print("by sensitivity     :", dict(Counter(r.get("sensitivity", "normal") for r in rows)))
    return 0


def cmd_index(a) -> int:
    rows = load()
    live = [r for r in rows if r["status"] not in ("deleted", "archived")]
    live.sort(key=lambda r: (TYPES.index(r["type"]), r["id"]))
    out = [f"# MEMORY INDEX — UAI-COS v2.0", "",
           f"> Generated: {now()}  |  live records: **{len(live)}**  |  total (incl. archived/deleted): {len(rows)}",
           "> Ye file auto-generated hai — edit na karo. Source of truth: `memory/store/memory.jsonl`",
           "> Retrieval rule (Section 17): keyword match kaafi nahi — scope + authority + freshness + confidence + current instruction dekh kar use karo.", ""]
    grouped = defaultdict(list)
    for r in live:
        grouped[r["type"]].append(r)
    for t in TYPES:
        if t not in grouped:
            continue
        out.append(f"## {t.upper()} ({len(grouped[t])})")
        out.append("")
        out.append("| id | status | conf | statement | source | scope |")
        out.append("|---|---|---|---|---|---|")
        for r in grouped[t]:
            sc = ", ".join((r.get("scope") or {}).get("domains") or []) or "-"
            out.append(f"| `{r['id']}` | {r['status']} | {r['confidence']} | {r['statement']} | "
                       f"{r['source'].get('kind')} | {sc} |")
        out.append("")
    open(INDEX, "w", encoding="utf-8").write("\n".join(out))
    log_audit("memory.index", f"{len(live)} live records indexed")
    print(f"[OK] INDEX.md regenerated ({len(live)} live records)")
    return 0


def cmd_dash(a) -> int:
    rows = load()
    live = [r for r in rows if r["status"] not in ("deleted",)]
    stats = {
        "total": len(rows),
        "live": sum(1 for r in rows if r["status"] not in ("deleted", "archived")),
        "conflicted": sum(1 for r in rows if r["status"] == "conflicted"),
        "expired": sum(1 for r in rows if r["status"] == "expired"),
        "active": sum(1 for r in rows if r["status"] == "active"),
        "verified": sum(1 for r in rows if r["status"] == "verified"),
    }
    by_type = Counter(r["type"] for r in live)
    by_status = Counter(r["status"] for r in live)
    e = html.escape
    cards = "".join(
        f'<div class="card"><div class="k">{e(k)}</div><div class="v">{v}</div></div>'
        for k, v in [("Live memories", stats["live"]), ("Active", stats["active"]),
                     ("Verified", stats["verified"]), ("Conflicted", stats["conflicted"]),
                     ("Expired", stats["expired"]), ("Total (all time)", stats["total"])])
    typebars = "".join(
        f'<div class="bar"><span class="lbl">{e(t)}</span>'
        f'<span class="track"><i style="width:{min(100, n * 8)}%"></i></span>'
        f'<span class="n">{n}</span></div>'
        for t, n in sorted(by_type.items(), key=lambda x: -x[1]))
    statbars = "".join(
        f'<div class="bar"><span class="lbl">{e(s)}</span>'
        f'<span class="track s-{e(s)}"><i style="width:{min(100, n * 10)}%"></i></span>'
        f'<span class="n">{n}</span></div>'
        for s, n in sorted(by_status.items(), key=lambda x: -x[1]))
    trs = ""
    for r in sorted(live, key=lambda r: (r["type"], r["id"])):
        trs += ("<tr>"
                f'<td class="mono">{e(r["id"])}</td><td>{e(r["type"])}</td>'
                f'<td><span class="pill p-{e(r["status"])}">{e(r["status"])}</span></td>'
                f'<td>{e(r["confidence"])}</td>'
                f'<td>{e(r["statement"])}<div class="det">{e(r.get("detail", "")[:220])}</div></td>'
                f'<td class="mono small">{e(r["source"].get("kind", ""))}</td>'
                f'<td class="mono small">{e(r.get("created_at", "")[:10])}</td>'
                "</tr>")
    doc = f"""<!doctype html>
<html lang="hi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UAI-COS v2.0 — Memory Dashboard</title>
<style>
 :root{{--bg:#0b1020;--panel:#131a2f;--line:#243050;--fg:#e8ecf7;--mut:#93a0c0;--acc:#6ea8fe;--ok:#39d98a;--warn:#ffc857;--bad:#ff6b81}}
 *{{box-sizing:border-box}}
 body{{margin:0;background:linear-gradient(180deg,#0b1020,#0a0f1c 60%);color:var(--fg);
   font:15px/1.5 "Segoe UI",system-ui,-apple-system,"Noto Sans",Arial,sans-serif;padding:28px}}
 h1{{font-size:24px;margin:0 0 4px}} .sub{{color:var(--mut);margin-bottom:22px;font-size:13px}}
 .cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:22px}}
 .card{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px}}
 .card .k{{color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:.06em}}
 .card .v{{font-size:26px;font-weight:700;margin-top:4px}}
 .grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:22px}}
 @media(max-width:820px){{.grid{{grid-template-columns:1fr}}}}
 .panel{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}}
 .panel h2{{font-size:14px;margin:0 0 12px;color:var(--mut);text-transform:uppercase;letter-spacing:.08em}}
 .bar{{display:flex;align-items:center;gap:10px;margin:7px 0;font-size:13px}}
 .bar .lbl{{width:110px;color:var(--mut)}} .bar .n{{width:26px;text-align:right;color:var(--mut)}}
 .track{{flex:1;height:9px;background:#0e152a;border:1px solid var(--line);border-radius:99px;overflow:hidden}}
 .track i{{display:block;height:100%;background:linear-gradient(90deg,#3b82f6,#6ea8fe)}}
 table{{width:100%;border-collapse:collapse;font-size:13.5px}}
 th,td{{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
 th{{color:var(--mut);font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;position:sticky;top:0;background:#101731}}
 .mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}} .small{{font-size:12px;color:var(--mut)}}
 .det{{color:var(--mut);font-size:12.5px;margin-top:3px;white-space:pre-wrap}}
 .pill{{padding:2px 9px;border-radius:99px;font-size:11.5px;border:1px solid var(--line);background:#0e152a}}
 .p-active{{color:#cbd7f5}} .p-active,.p-verified{{border-color:#27506b}}
 .p-verified{{color:var(--ok)}} .p-candidate{{color:var(--warn)}} .p-conflicted{{color:var(--bad)}}
 .p-superseded{{color:#8b93ad}} .p-expired{{color:#ff9f6b}}
 .wrap{{overflow:auto;max-height:68vh;border:1px solid var(--line);border-radius:14px}}
 footer{{color:var(--mut);font-size:12px;margin-top:18px}}
 code{{background:#0e152a;border:1px solid var(--line);padding:1px 6px;border-radius:6px;font-size:12px}}
</style></head><body>
<h1>UAI-COS v2.0 — Memory Dashboard</h1>
<div class="sub">Universal AI Cognitive Operating System · generated {e(now())} · store: <code>memory/store/memory.jsonl</code> · index: <code>memory/INDEX.md</code></div>
<div class="cards">{cards}</div>
<div class="grid">
  <div class="panel"><h2>Memories by type</h2>{typebars or '<div class="sub">koi record nahi</div>'}</div>
  <div class="panel"><h2>Memories by status</h2>{statbars or '<div class="sub">koi record nahi</div>'}</div>
</div>
<div class="panel" style="padding:0">
  <div class="wrap"><table>
   <thead><tr><th>ID</th><th>Type</th><th>Status</th><th>Conf</th><th>Statement</th><th>Source</th><th>Created</th></tr></thead>
   <tbody>{trs or '<tr><td colspan="7" class="small">koi record nahi</td></tr>'}</tbody>
  </table></div>
</div>
<footer>Retrieval rule: keyword match kaafi nahi — scope + authority + freshness + confidence + current instruction dekh kar memory use karo (spec Section 17–21).</footer>
</body></html>"""
    open(DASHBOARD, "w", encoding="utf-8").write(doc)
    log_audit("memory.dash", f"dashboard generated ({len(live)} rows)")
    print(f"[OK] DASHBOARD.html regenerated ({len(live)} rows)")
    return 0


def cmd_export(a) -> int:
    print(json.dumps(load(), ensure_ascii=False, indent=2))
    return 0


# ---------------------------------------------------------------- cli
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="uai_mem", description="UAI-COS v2.0 memory operating system (file-backed).")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="naya memory record")
    a.add_argument("--id"), a.add_argument("--type", required=True, choices=TYPES)
    a.add_argument("--statement", required=True); a.add_argument("--detail", default="")
    a.add_argument("--source", default="user_instruction")
    a.add_argument("--ref", default=""); a.add_argument("--url", default=""); a.add_argument("--observed", default="")
    a.add_argument("--domain", action="append"); a.add_argument("--project", action="append"); a.add_argument("--agent", action="append")
    a.add_argument("--applies-when", dest="applies_when", default="")
    a.add_argument("--does-not-apply-when", dest="does_not_apply_when", default="")
    a.add_argument("--confidence", default="medium", choices=CONFIDENCE)
    a.add_argument("--status", default="candidate", choices=STATUSES)
    a.add_argument("--authority", default="user_implied", choices=AUTHORITY)
    a.add_argument("--sensitivity", default="normal", choices=SENSITIVITY)
    a.add_argument("--tag", action="append"); a.add_argument("--verified", default="")
    a.add_argument("--expires", default=""); a.add_argument("--supersedes", default="")
    a.add_argument("--conflict-key", dest="conflict_key", default="")
    a.add_argument("--note", default=""); a.add_argument("--force", action="store_true")
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("list", help="records filter kar ke dikhao")
    l.add_argument("--type", action="append", choices=TYPES); l.add_argument("--status", action="append", choices=STATUSES)
    l.add_argument("--confidence", action="append", choices=CONFIDENCE); l.add_argument("--tag", action="append")
    l.add_argument("--project", action="append"); l.add_argument("--wide", action="store_true"); l.add_argument("--all", action="store_true")
    l.set_defaults(func=cmd_list)

    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--wide", action="store_true"); s.set_defaults(func=cmd_search)
    sh = sub.add_parser("show"); sh.add_argument("id"); sh.set_defaults(func=cmd_show)
    u = sub.add_parser("update"); u.add_argument("id")
    u.add_argument("--status", choices=STATUSES); u.add_argument("--confidence", choices=CONFIDENCE)
    u.add_argument("--statement"); u.add_argument("--detail"); u.add_argument("--authority", choices=AUTHORITY)
    u.add_argument("--sensitivity", choices=SENSITIVITY); u.add_argument("--expires"); u.add_argument("--tag", action="append")
    u.add_argument("--note", default=""); u.set_defaults(func=cmd_update)
    sp = sub.add_parser("supersede"); sp.add_argument("old"); sp.add_argument("new"); sp.add_argument("--note", default=""); sp.set_defaults(func=cmd_supersede)
    ex = sub.add_parser("expire"); ex.add_argument("--date", default=today()); ex.set_defaults(func=cmd_expire)
    ar = sub.add_parser("archive"); ar.add_argument("id", nargs="?"); ar.add_argument("--status"); ar.add_argument("--type", action="append", choices=TYPES, default=[])
    ar.add_argument("--note", default=""); ar.set_defaults(func=cmd_archive)
    au = sub.add_parser("audit"); au.add_argument("--log", action="store_true"); au.add_argument("--fail-under", dest="fail_under", type=int, default=70)
    au.add_argument("--working-ttl", dest="working_ttl", type=int, default=7); au.add_argument("--fact-freshness-days", dest="fact_freshness_days", type=int, default=180)
    au.set_defaults(func=cmd_audit)
    sub.add_parser("stats").set_defaults(func=cmd_stats)
    sub.add_parser("index").set_defaults(func=cmd_index)
    sub.add_parser("dash").set_defaults(func=cmd_dash)
    sub.add_parser("export").set_defaults(func=cmd_export)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
