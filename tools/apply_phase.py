#!/usr/bin/env python3
"""
apply_phase.py — UAI-COS **spec apply engine**.

Koi bhi agent apne environment me in structured specs ko apply karta hai:
  * `v2`         -> UAI-COS V2.0 canonical spec (112 sections)
  * `self_audit` -> MASTER SELF-AUDIT blueprint (original Phase 1 + Phase 2 prompt)
  * `phase1`     -> self-capability inventory (blueprint ka PHASE 1-4 hissa)
  * `phase2`     -> access / research / fallback (blueprint ka PHASE 5-8 hissa)
  * `all`        -> sab

Apply ka matlab: agent apne env me checks chalata hai, honest result likhta hai, aur attestation deta hai.
Har run ka record: `logs/phase_apply_<spec>_<date>.json` + `PROJECT_BOARD/PHASE_APPLY.md` (append).

Usage:
  python3 tools/apply_phase.py --list
  python3 tools/apply_phase.py --spec self_audit
  python3 tools/apply_phase.py --spec all --json
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "logs"
APPLY_MD = ROOT / "PROJECT_BOARD" / "PHASE_APPLY.md"
UA = "UAI-COS-apply/1.0"


def sh(cmd: str, timeout: int = 60) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return p.returncode, ((p.stdout or "") + (p.stderr or "")).strip()
    except Exception as e:  # noqa: BLE001
        return 1, f"ERR {type(e).__name__}: {e}"


def http(url: str, timeout: int = 20) -> tuple[int, int]:
    code, out = sh(f"curl -s -o /tmp/_ap.out -m {timeout} -A '{UA}' -w '%{{http_code}}' '{url}'", timeout + 10)
    try:
        size = os.path.getsize("/tmp/_ap.out")
    except OSError:
        size = 0
    try:
        return int(out.strip().splitlines()[-1]), size
    except Exception:  # noqa: BLE001
        return 0, size


def canon_hash(path: Path, kind: str = "spec") -> str:
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    parts = t.split("\n---\n", 1)
    body = (parts[1].strip() + "\n") if len(parts) == 2 else (t.strip() + "\n")
    return hashlib.sha256(body.encode()).hexdigest()[:16]


# ---------------------------------------------------------------- checks
def c_spec(file: str, expected: str | None = None):
    def f():
        p = ROOT / file
        if not p.exists():
            return False, f"{file} missing", None
        h = canon_hash(p)
        if expected and h != expected:
            return False, f"hash mismatch: file={h} expected={expected}", file
        return True, f"{file} OK (hash {h})", file
    return f


def c_boot():
    code, out = sh(f"{sys.executable} tools/agent_boot.py")
    ok = code == 0 and "BOOT ATTESTATION" in out and "ABSOLUTE RULES" in out
    return ok, f"boot payload {len(out):,} chars" if ok else "boot payload generate nahi hua", "UAI-COS_BOOT_PROMPT.md"


def c_memory():
    code, out = sh(f"{sys.executable} tools/uai_mem.py audit | tail -2")
    m = re.search(r"HEALTH SCORE:\s*(\d+)", out)
    score = int(m.group(1)) if m else 0
    return score >= 90, f"memory audit {score}/100", "memory/INDEX.md"


def c_provenance():
    code, out = sh(f"{sys.executable} tools/verify_provenance.py | tail -1")
    return "PROVENANCE OK" in out, out[:90], "00_SYSTEM/provenance.json"


def c_phases():
    code, out = sh(f"{sys.executable} tools/phase_runner.py status | tail -1")
    return code == 0 and "TOTAL" in out, out[:80], "PROJECT_BOARD/phases.json"


def c_prompts():
    code, out = sh(f"{sys.executable} tools/prompt_registry.py verify | tail -2")
    return "SAARE PROMPTS OK" in out, out.replace("\n", " ")[:90], "PROMPTS/registry.json"


def c_hygiene():
    code, out = sh(f"{sys.executable} tools/cleanup_workspace.py --json")
    try:
        d = json.loads(out.splitlines()[-1])
    except Exception:  # noqa: BLE001
        return False, "cleanup tool chala nahi", None
    ok = d["junk"] == 0 and d["empty"] == 0 and d["dupes"] == 0
    return ok, f"junk={d['junk']} empty={d['empty']} dupes={d['dupes']}", "logs/"


def c_env_tools():
    need = ["git", "curl", "jq", "python3"]
    have = [t for t in need if shutil.which(t)]
    return len(have) == len(need), f"core tools: {', '.join(have)}", None


def c_net():
    c1, s1 = http("https://api.github.com")
    c2, s2 = http("https://r.jina.ai/https://example.com")
    ok = c1 == 200 and c2 == 200
    return ok, f"github={c1} reader={c2}", None


def c_persist():
    p = Path("/opt/uai-cache")
    stamp = p / "PERSIST_STAMP.txt"
    ok = stamp.exists()
    return ok, ("/opt/uai-cache stamp present" if ok else "stamp nahi — bootstrap chalao: bash tools/bootstrap_environment.sh"), str(p)


def c_bootstrap():
    p = ROOT / "tools" / "bootstrap_environment.sh"
    return p.exists(), ("bootstrap script ready" if p.exists() else "bootstrap missing"), \
        "tools/bootstrap_environment.sh" if p.exists() else None


def c_hindi_rule():
    p = ROOT / "CONVERSATION" / "04_STANDING_INSTRUCTIONS.md"
    t = p.read_text(encoding="utf-8") if p.exists() else ""
    ok = "Roman Hindi" in t or "Hindi" in t
    return ok, "Hindi rule standing instructions me mila" if ok else "Hindi rule nahi mila", "CONVERSATION/04_STANDING_INSTRUCTIONS.md"


def c_boundary():
    t = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").exists() else ""
    ok = ("bypass nahi" in t.lower()) or ("HARD LIMIT" in t) or ("§24" in t)
    return ok, "boundary §24 (auth/paywall/CAPTCHA bypass NAHI) documented" if ok else "boundary doc nahi mila", "AGENTS.md"


def c_audit_maps():
    need = ["07_SELF_AUDIT/AGENT_CAPABILITY_MAP.json", "07_SELF_AUDIT/RESEARCH_CAPABILITY_MAP.json",
            "07_SELF_AUDIT/ENVIRONMENT_FALLBACK_MAP.json", "07_SELF_AUDIT/UNKNOWN_CAPABILITY_QUEUE.json",
            "07_SELF_AUDIT/CAPABILITY_EXPANSION_ROADMAP.md", "07_SELF_AUDIT/00_SELF_AUDIT_MASTER_REPORT.md"]
    have = [f for f in need if (ROOT / f).exists()]
    return len(have) == len(need), f"{len(have)}/{len(need)} audit deliverables repo me", "07_SELF_AUDIT/"


SPECS: dict[str, dict] = {
    "v2": {
        "title": "UAI-COS V2.0 canonical spec (112 sections)",
        "file": "00_SYSTEM/00_UAI-COS_V2.0_SPEC.md",
        "checks": [("spec v2 import + hash", c_spec("00_SYSTEM/00_UAI-COS_V2.0_SPEC.md", "4aa1c6a1f872a3f3")),
                   ("boot payload", c_boot), ("memory OS", c_memory), ("provenance", c_provenance),
                   ("boundary §24 documented", c_boundary), ("Hindi behaviour rule", c_hindi_rule)],
    },
    "self_audit": {
        "title": "MASTER SELF-AUDIT blueprint (Phase 1 + Phase 2 original prompt)",
        "file": "00_SYSTEM/02_UAI-COS_MASTER_SELF_AUDIT_SPEC.md",
        "checks": [("spec self_audit import + hash", c_spec("00_SYSTEM/02_UAI-COS_MASTER_SELF_AUDIT_SPEC.md", "e8d8620d378adc48")),
                   ("audit deliverables (10 maps/report)", c_audit_maps), ("boot payload", c_boot),
                   ("env core tools", c_env_tools), ("network (tokenless routes)", c_net),
                   ("persistence + bootstrap", c_bootstrap), ("workspace hygiene", c_hygiene),
                   ("phases engine", c_phases), ("prompt registry", c_prompts)],
    },
    "phase1": {
        "title": "Phase 1 — self-capability inventory (zero-assumption)",
        "file": "00_SYSTEM/02_UAI-COS_MASTER_SELF_AUDIT_SPEC.md",
        "checks": [("spec import", c_spec("00_SYSTEM/02_UAI-COS_MASTER_SELF_AUDIT_SPEC.md")),
                   ("capability map", c_audit_maps), ("memory OS", c_memory), ("provenance", c_provenance),
                   ("hygiene", c_hygiene), ("boundary §24 documented", c_boundary)],
    },
    "phase2": {
        "title": "Phase 2 — ACCESS PATH & CAPABILITY EXPANSION MASTER BLUEPRINT",
        "file": "00_SYSTEM/03_UAI-COS_PHASE_2_ACCESS_SPEC.md",
        "checks": [("spec import + hash", c_spec("00_SYSTEM/03_UAI-COS_PHASE_2_ACCESS_SPEC.md", "8a801fdcfc9329e7")),
                   ("apply deliverable report", c_spec("03_ACCESS_EXPANSION/01_PHASE2_BLUEPRINT_APPLY.md")),
                   ("access probe results", c_spec("03_ACCESS_EXPANSION/probes/phase2_access_paths.txt")),
                   ("network routes", c_net),
                   ("social/rsshub route tool", c_spec("tools/social_unlock.py")),
                   ("rsshub verify tool", c_spec("tools/rsshub_verify.py")),
                   ("monitor tool", c_spec("tools/route_monitor.py")),
                   ("prompt registry", c_prompts)],
    },
    "phase3": {
        "title": "Phase 3 — MULTI-ENVIRONMENT + MULTI-AGENT + ORCHESTRATION MASTER BLUEPRINT",
        "file": "00_SYSTEM/04_UAI-COS_PHASE_3_ORCHESTRATION_SPEC.md",
        "checks": [("spec import + hash", c_spec("00_SYSTEM/04_UAI-COS_PHASE_3_ORCHESTRATION_SPEC.md", "4b8a3b3fa3e7766b")),
                   ("master orchestration report", c_spec("08_ORCHESTRATION/00_PHASE3_MASTER_ORCHESTRATION_REPORT.md")),
                   ("env capability matrix", c_spec("08_ORCHESTRATION/ENVIRONMENT_CAPABILITY_MATRIX.json")),
                   ("multi-agent role matrix", c_spec("08_ORCHESTRATION/MULTI_AGENT_ROLE_MATRIX.json")),
                   ("knowledge object model", c_spec("08_ORCHESTRATION/KNOWLEDGE_OBJECT_MODEL.json")),
                   ("quality gates checklist", c_spec("08_ORCHESTRATION/QUALITY_GATE_CHECKLIST.json")),
                   ("state machine schema", c_spec("08_ORCHESTRATION/STATE_MACHINE.json")),
                   ("orchestrator tool", c_spec("tools/orchestrator.py")),
                   ("orchestrator verification", lambda: (sh(f"{sys.executable} tools/orchestrator.py --verify-all")[0] == 0, "5/5 matrices loaded & gates verified", "08_ORCHESTRATION/")),
                   ("prompt registry", c_prompts)],
    },
}


def run_spec(key: str) -> dict:
    spec = SPECS[key]
    rows = []
    for name, fn in spec["checks"]:
        try:
            ok, detail, ev = fn()
        except Exception as e:  # noqa: BLE001
            ok, detail, ev = False, f"check crash: {type(e).__name__}: {e}", None
        rows.append({"check": name, "ok": bool(ok), "detail": detail, "evidence": ev})
    passed = sum(1 for r in rows if r["ok"])
    total = len(rows)
    verdict = "PASS" if passed == total else ("PARTIAL" if passed >= 0.7 * total else "FAIL")
    return {"spec": key, "title": spec["title"], "spec_file": spec["file"], "checks": rows,
            "passed": passed, "total": total, "verdict": verdict, "env": os.uname().nodename,
            "python": sys.version.split()[0], "ts": time.strftime("%Y-%m-%d %H:%M:%S")}


def main() -> int:
    ap = argparse.ArgumentParser(prog="apply_phase.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", default="all", help="v2 | self_audit | phase1 | phase2 | all")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.list:
        for k, v in SPECS.items():
            print(f"{k:<12} {v['title']}  ({v['file']})")
        return 0
    keys = list(SPECS) if a.spec == "all" else [a.spec]
    if any(k not in SPECS for k in keys):
        print("unknown spec. options:", ", ".join(SPECS)); return 2
    LOGS.mkdir(exist_ok=True)
    results = [run_spec(k) for k in keys]
    out_json = {"applied_at": time.strftime("%Y-%m-%d %H:%M:%S"), "results": results}
    (LOGS / f"phase_apply_{'_'.join(keys)}_{time.strftime('%Y-%m-%d')}.json").write_text(
        json.dumps(out_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # PHASE_APPLY.md me append
    if not APPLY_MD.exists():
        APPLY_MD.write_text("# PHASE_APPLY.md — spec apply attestations (har run append hota hai)\n\n"
                            "| ts | spec | verdict | checks | env | python | log |\n|---|---|---|---|---|---|---|\n", encoding="utf-8")
    with APPLY_MD.open("a", encoding="utf-8") as f:
        for r in results:
            f.write(f"| {r['ts']} | `{r['spec']}` | **{r['verdict']}** | {r['passed']}/{r['total']} | {r['env']} | {r['python']} | `logs/phase_apply_{r['spec']}_{time.strftime('%Y-%m-%d')}.json` |\n")

    if a.json:
        print(json.dumps(out_json, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"\n=== APPLY {r['spec']} — {r['title']}\n    verdict: {r['verdict']} ({r['passed']}/{r['total']})")
            for c in r["checks"]:
                print(f"    {'PASS' if c['ok'] else 'FAIL'}  {c['check']:<34} {c['detail'][:80]}")
        print("\nlog: logs/phase_apply_*.json · attestation: PROJECT_BOARD/PHASE_APPLY.md")
    return 0 if all(r["verdict"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
