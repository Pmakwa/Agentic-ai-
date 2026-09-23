#!/usr/bin/env python3
"""
cleanup_workspace.py — UAI-COS workspace hygiene tool (faltu/bekar/duplicate cheezein hatao).

User rule (standing): "jo bhi kaam ki nahi / bekaar / duplicate hai wo delete karo, aur ye time to time karte rehna."

Kya dhoondhta hai:
  1. JUNK      : __pycache__, *.pyc, *.pyo, *.tmp, *.bak, *~, *.orig, .DS_Store, Thumbs.db, 0-byte files
  2. DUPLICATES: exact same content (sha256) — ek rakho, baaki delete (sirf untracked; tracked = report)
  3. OBSOLETE  : `tools/_regen_*.py` jaise one-shot helpers, purane superseded logs (config list)
  4. HEAVY     : 5MB+ files / bade dirs (node_modules, caches) — workspace ke bahar /opt me hone chahiye
  5. SIZE      : workspace ka total size + by-directory top list

Modes:
  python3 tools/cleanup_workspace.py                # report (kuch delete nahi)
  python3 tools/cleanup_workspace.py --apply        # SAFE delete: junk + 0-byte + untracked duplicates
  python3 tools/cleanup_workspace.py --apply --include-tracked   # tracked duplicates/junk bhi (phir commit karo)
  python3 tools/cleanup_workspace.py --check        # CI/monitor ke liye: junk mile to exit 1

Safety:
  - `.git/`, `tools/bin/`, `assets/`, `00_SYSTEM/_raw/`, `memory/store/` kabhi delete nahi.
  - HEAVY dirs (node_modules, .pnpm, dist, build, .venv, ...) kabhi scan/delete nahi — ye environment artifacts hain,
    inko `/opt/uai-cache/` me rakha jata hai (workspace ke andar nahi).
  - Duplicate delete sirf `--dedupe` flag ke saath (default `--apply` me nahi).
  - Safety cap: 500 se zyada delete karne ke liye `--force` chahiye.

LESSON (2026-09-23 — isi tool ke pehle version se seekha): pehla version node_modules ke andar bhi "duplicates"
delete kar gaya tha (7959 files) jisse RSSHub toot gaya (lib/ + node_modules me identical license/stub files).
Isliye ab HEAVY dirs hard-protected hain aur dedupe alag opt-in flag hai. Koi bhi agent ye protection hataaye bina
cleanup nahi chalayega.
Har run ka record: `logs/cleanup_YYYY-MM-DD.md` (+ .json).
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "logs"
PROTECTED = {".git", "tools/bin", "assets", "00_SYSTEM/_raw", "memory/store", "tools/rsshub", "tools/douyin_api"}
HEAVY_SKIP = {"node_modules", ".pnpm", "dist", "build", "out", "target", "coverage", ".venv", "venv",
              "site-packages", ".next", ".nuxt", ".svelte-kit", ".cache", ".local", ".turbo",
              ".parcel-cache", "__pypackages__", ".pnpm-store"}
JUNK_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints"}
DELETE_CAP = 500
JUNK_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}
JUNK_SUFFIX = (".pyc", ".pyo", ".tmp", ".bak", "~", ".orig", ".rej", ".swp")
HEAVY_MB = 5


def is_protected(rel: str) -> bool:
    return any(rel == p or rel.startswith(p + "/") for p in PROTECTED)


def tracked(root: Path) -> set[str]:
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True).stdout
        return {l.strip() for l in out.splitlines() if l.strip()}
    except FileNotFoundError:
        return set()


def scan(root: Path) -> dict:
    tr = tracked(root)
    junk, empty, dupes, heavy, bigdirs = [], [], [], [], []
    by_hash: dict[str, list[str]] = defaultdict(list)
    total = 0
    for dp, dn, fn in os.walk(root):
        rel_dp = os.path.relpath(dp, root)
        rel_dp = "" if rel_dp == "." else rel_dp
        if is_protected(rel_dp):
            dn[:] = []
            continue
        keep = []
        for d in list(dn):
            r = f"{rel_dp}/{d}".strip("/")
            if d in {".git"} or d in HEAVY_SKIP or is_protected(r):
                continue
            if d in JUNK_DIRS:
                junk.append((r, "cache-dir", _dirsize(os.path.join(dp, d))))
                dn.remove(d); continue
            keep.append(d)
        dn[:] = keep
        for f in fn:
            p = Path(dp) / f
            rel = str(p.relative_to(root))
            if is_protected(rel):
                continue
            try:
                sz = p.stat().st_size
            except OSError:
                continue
            total += sz
            if f.endswith(JUNK_SUFFIX) or f in JUNK_FILES:
                junk.append((rel, "junk-file", sz)); continue
            if sz == 0:
                empty.append((rel, "empty", 0)); continue
            if sz >= HEAVY_MB * 1024 * 1024:
                heavy.append((rel, "heavy", sz))
            if 0 < sz <= 3_000_000:
                try:
                    h = hashlib.sha256(p.read_bytes()).hexdigest()
                except OSError:
                    continue
                by_hash[h].append(rel)
    for h, files in by_hash.items():
        if len(files) > 1:
            sz = (root / files[0]).stat().st_size
            keep = min(files, key=lambda x: (x.count("/"), len(x)))
            for f in files:
                if f != keep:
                    dupes.append((f, f"duplicate-of {keep}", sz))
    for d in ("tools/rsshub", "tools/douyin_api", "tools/bin", ".git"):
        dd = root / d
        if dd.exists():
            bigdirs.append((d, _dirsize(dd)))
    bigdirs.sort(key=lambda x: -x[1])
    return {"total_bytes": total, "junk": junk, "empty": empty, "dupes": dupes, "heavy": heavy,
            "bigdirs": bigdirs, "tracked_count": len(tr), "untracked_files": [x[0] for x in junk + empty + dupes if x[0] not in tr]}


def _dirsize(p) -> int:
    t = 0
    for dp, _dn, fn in os.walk(p):
        for f in fn:
            try:
                t += os.path.getsize(os.path.join(dp, f))
            except OSError:
                pass
    return t


def human(n: int) -> str:
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.1f} {u}" if u != "B" else f"{n} B"
        n /= 1024
    return f"{n:.1f} GB"


def main() -> int:
    ap = argparse.ArgumentParser(prog="cleanup_workspace.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="SAFE junk delete (__pycache__/tmp/0-byte). Duplicates NAHI.")
    ap.add_argument("--dedupe", action="store_true", help="--apply ke saath: untracked exact-duplicates bhi delete karo")
    ap.add_argument("--force", action="store_true", help=f"{DELETE_CAP}+ items delete karne ke liye")
    ap.add_argument("--include-tracked", action="store_true", help="git-tracked files bhi delete karo (commit karna mat bhoolo)")
    ap.add_argument("--check", action="store_true", help="junk mile to exit 1 (monitor/CI ke liye)")
    ap.add_argument("--json", action="store_true", help="sirf JSON output")
    a = ap.parse_args()

    s = scan(ROOT)
    tr = tracked(ROOT)
    deleted, skipped, freed = [], [], 0

    targets = s["junk"] + s["empty"] + (s["dupes"] if a.dedupe else [])
    if a.apply and len(targets) > DELETE_CAP and not a.force:
        print(f"⚠️  {len(targets)} items delete hone the (> {DELETE_CAP} cap). Safety ke liye ruk gaya —"
              f" chahiye to --force do, ya report dekh lo.")
        a.apply = False
    if a.apply:
        for rel, why, sz in targets:
            p = ROOT / rel
            if rel in tr and not a.include_tracked:
                skipped.append((rel, "git-tracked (report only)")); continue
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
                deleted.append((rel, why, sz)); freed += sz
            except OSError as e:
                skipped.append((rel, f"error: {e}"))
        # khaali dirs
        for dp, dn, fn in os.walk(ROOT, topdown=False):
            r = os.path.relpath(dp, ROOT)
            if r == "." or is_protected(r) or f"{r}" in PROTECTED:
                continue
            try:
                if not os.listdir(dp):
                    os.rmdir(dp); deleted.append((r + "/", "empty-dir", 0))
            except OSError:
                pass

    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    rep = {
        "ts": ts, "workspace": str(ROOT), "total_before": s["total_bytes"], "freed": freed,
        "apply": a.apply, "junk": [x for x in s["junk"]], "empty": s["empty"], "duplicates": s["dupes"],
        "heavy": s["heavy"], "bigdirs": s["bigdirs"], "deleted": deleted, "skipped": skipped,
    }
    LOGS.mkdir(exist_ok=True)
    (LOGS / f"cleanup_{time.strftime('%Y-%m-%d')}.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False) + "\n")
    lines = [f"# Workspace cleanup report — {ts}", "",
             f"- Workspace: `{ROOT}` · total (excluding protected/heavy dirs): **{human(s['total_bytes'])}**",
             f"- Junk items: **{len(s['junk'])}** · 0-byte files: **{len(s['empty'])}** · duplicate files: **{len(s['dupes'])}**",
             f"- Mode: {'APPLY' if a.apply else 'report-only'} · deleted: **{len(deleted)}** · freed: **{human(freed)}**", ""]
    if s["bigdirs"]:
        lines += ["## Bade directories (workspace me nahi hone chahiye)", "",
                  "| dir | size | note |", "|---|---|---|"]
        for d, sz in s["bigdirs"]:
            note = "gitignored / env artifact — /opt/uai-cache me rakho" if "rsshub" in d or "node_modules" in d else ""
            lines.append(f"| `{d}` | {human(sz)} | {note} |")
        lines.append("")
    for title, key in [("Junk", "junk"), ("0-byte files", "empty"), ("Duplicates (ek rakho, baaki delete)", "dupes")]:
        if s[key]:
            lines += [f"## {title}", ""]
            for rel, why, sz in s[key][:60]:
                lines.append(f"- `{rel}` — {why} ({human(sz)})" + (" · *deleted*" if any(d[0] == rel for d in deleted) else ""))
            if len(s[key]) > 60:
                lines.append(f"- … +{len(s[key]) - 60} more")
            lines.append("")
    if s["heavy"]:
        lines += ["## 5MB+ files", ""] + [f"- `{r}` — {human(z)}" for r, _, z in s["heavy"][:20]] + [""]
    if deleted:
        lines += ["## Delete kiye gaye", ""] + [f"- `{r}` ({why})" for r, why, _ in deleted[:80]] + [""]
    if skipped:
        lines += ["## Skip (tracked/manual decide)", ""] + [f"- `{r}` — {why}" for r, why in skipped[:40]] + [""]
    (LOGS / f"cleanup_{time.strftime('%Y-%m-%d')}.md").write_text("\n".join(lines) + "\n")

    if a.json:
        print(json.dumps({"total_before": s["total_bytes"], "junk": len(s["junk"]), "empty": len(s["empty"]),
                          "dupes": len(s["dupes"]), "deleted": len(deleted), "freed": freed,
                          "bigdirs": s["bigdirs"]}, ensure_ascii=False))
    else:
        print(f"UAI-COS CLEANUP — {ts}")
        print(f"  workspace total   : {human(s['total_bytes'])}")
        print(f"  junk              : {len(s['junk'])}  ·  0-byte: {len(s['empty'])}  ·  duplicates: {len(s['dupes'])}")
        print(f"  mode              : {'APPLY' if a.apply else 'report-only'}{' + dedupe' if a.dedupe else ''}")
        if deleted:
            print(f"  deleted           : {len(deleted)} items · {human(freed)} freed")
        if skipped:
            print(f"  skipped (tracked) : {len(skipped)} (--include-tracked se delete honge)")
        for d, sz in s["bigdirs"][:4]:
            print(f"  big dir           : {d} = {human(sz)}")
        print(f"  report            : logs/cleanup_{time.strftime('%Y-%m-%d')}.md")
        if not a.apply and (s["junk"] or s["empty"] or s["dupes"]):
            print("  -> delete karne ke liye: python3 tools/cleanup_workspace.py --apply")
    if a.check and (s["junk"] or s["empty"] or s["dupes"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
