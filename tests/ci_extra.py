#!/usr/bin/env python3
"""
ci_extra.py — CI ke extra checks (GitHub Actions me chalta hai).

Checks:
  1. phases.json valid (unique ids, valid status, required fields)
  2. PROJECT_BOARD/PHASES.md ka auto-table phases.json se match karta hai (drift check)
  3. UAI-COS_BOOT_PROMPT.md current hai (regenerate kar ke compare)
  4. 00_SYSTEM/prompts_index.json ke saare imported prompts ka body hash match karta hai
  5. boot payload generate hota hai aur usme zaroori sections hain
"""
from __future__ import annotations
import hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
fails: list[str] = []


def ok(msg: str) -> None:
    print(f"  [PASS] {msg}")


def bad(msg: str) -> None:
    fails.append(msg)
    print(f"  [FAIL] {msg}")


# 1. phases.json
try:
    d = json.loads((ROOT / "PROJECT_BOARD" / "phases.json").read_text(encoding="utf-8"))
    ids = [p["id"] for p in d["phases"]]
    assert len(ids) == len(set(ids)), "duplicate phase ids"
    for p in d["phases"]:
        assert p["status"] in {"next", "active", "done", "waiting_user"}, f"bad status {p['status']}"
        assert p.get("title"), f"{p['id']} has no title"
    ok(f"phases.json valid ({len(ids)} phases)")
except Exception as e:  # noqa: BLE001
    bad(f"phases.json invalid: {e}")

# 2. PHASES.md drift
try:
    md = (ROOT / "PROJECT_BOARD" / "PHASES.md").read_text(encoding="utf-8")
    missing = [p["id"] for p in d["phases"] if f"| {p['id']} |" not in md]
    if missing:
        bad(f"PHASES.md me ye phases missing: {missing} — `python3 tools/phase_runner.py md` chalao")
    else:
        ok("PHASES.md table phases.json se sync hai")
except Exception as e:  # noqa: BLE001
    bad(f"PHASES.md check failed: {e}")

# 3. boot prompt freshness (file vs freshly generated payload — local aur CI dono me kaam karta hai)
try:
    live = subprocess.run([sys.executable, str(ROOT / "tools" / "agent_boot.py")],
                          capture_output=True, text=True).stdout.strip()
    f = ROOT / "UAI-COS_BOOT_PROMPT.md"
    disk = re.sub(r"^<!--.*?-->\s*", "", f.read_text(encoding="utf-8"), flags=re.S).strip() if f.exists() else ""
    if disk != live:
        bad("UAI-COS_BOOT_PROMPT.md stale hai — `python3 tools/agent_boot.py --write` chalao aur commit karo")
    else:
        ok(f"UAI-COS_BOOT_PROMPT.md current hai ({len(disk):,} chars)")
except Exception as e:  # noqa: BLE001
    bad(f"boot prompt check failed: {e}")

# 4. prompts_index hashes
try:
    idx = json.loads((ROOT / "00_SYSTEM" / "prompts_index.json").read_text(encoding="utf-8"))
    for p in idx.get("prompts", []):
        f = ROOT / p["file"]
        if not f.exists():
            bad(f"prompt file missing: {p['file']}"); continue
        t = f.read_text(encoding="utf-8")
        t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        parts = t.split("\n---\n", 1)
        body = (parts[1].strip() + "\n") if len(parts) == 2 else (t.strip() + "\n")
        h = hashlib.sha256(body.encode()).hexdigest()[:16]
        if h != p.get("body_sha256_16"):
            bad(f"prompt hash mismatch: {p['name']} (file={h} index={p.get('body_sha256_16')})")
        else:
            ok(f"prompt hash OK: {p['name']} ({h})")
except FileNotFoundError:
    ok("prompts_index.json abhi nahi hai (koi naya prompt import nahi hua) — skip")
except Exception as e:  # noqa: BLE001
    bad(f"prompts_index check failed: {e}")

# 5. boot payload sections
try:
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "agent_boot.py")],
                         capture_output=True, text=True).stdout
    need = ["BOOT ATTESTATION", "ABSOLUTE RULES", "CAPABILITY TRUTH", "OPEN THREADS", "SPEC MAP"]
    miss = [n for n in need if n not in out]
    if miss:
        bad(f"boot payload me sections missing: {miss}")
    else:
        ok(f"boot payload OK ({len(out):,} chars)")
except Exception as e:  # noqa: BLE001
    bad(f"boot payload check failed: {e}")

print()
if fails:
    print(f"CI EXTRA: {len(fails)} FAIL")
    sys.exit(1)
print("CI EXTRA: saare checks PASS")
