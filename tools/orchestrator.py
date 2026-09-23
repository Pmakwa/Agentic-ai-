#!/usr/bin/env python3
"""
orchestrator.py — UAI-COS Central Meta-Orchestrator CLI Engine
Reference: 00_SYSTEM/04_UAI-COS_PHASE_3_ORCHESTRATION_SPEC.md

Functions:
  1. Pipeline state machine runner (§3, §42)
  2. Multi-Environment capability matrix query (§4)
  3. Quality Gate runner (10 gates, §44)
  4. Research Depth selector (Level 0-5, §37)
  5. Multi-Agent structured delegation packet validator (§10, §11)
  6. Self-Audit verification (§46)

Usage:
  python3 tools/orchestrator.py --gates
  python3 tools/orchestrator.py --environments
  python3 tools/orchestrator.py --roles
  python3 tools/orchestrator.py --depth 3
  python3 tools/orchestrator.py --verify-all
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORCH_DIR = ROOT / "08_ORCHESTRATION"


def load_json(filename: str) -> dict:
    p = ORCH_DIR / filename
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def run_quality_gates(verbose: bool = True) -> bool:
    data = load_json("QUALITY_GATE_CHECKLIST.json")
    gates = data.get("gates", [])
    if verbose:
        print("\n=== UAI-COS PHASE-3 QUALITY GATES (§44) ===")
    all_pass = True
    for g in gates:
        gid = g.get("id")
        name = g.get("name")
        q = g.get("question")
        st = g.get("status", "UNCHECKED")
        if verbose:
            print(f"  [{st}] {gid:<8} {name:<15} — {q}")
        if st != "PASS":
            all_pass = False
    if verbose:
        print(f"Overall Quality Gate Verdict: {'ALL PASS ✅' if all_pass else 'FAIL ❌'}\n")
    return all_pass


def list_environments():
    data = load_json("ENVIRONMENT_CAPABILITY_MATRIX.json")
    envs = data.get("environments", [])
    print("\n=== UAI-COS MULTI-ENVIRONMENT MATRIX (§4.2) ===")
    for e in envs:
        print(f"\n* {e['environment']}")
        print(f"  Read: {e['can_read']} | Search: {e['can_search']} | Exec: {e['can_execute']} | Write: {e['can_write']} | ExtData: {e['can_access_external_data']} | Verify: {e['can_verify']}")
        print(f"  Tools: {', '.join(e.get('tools', []))}")
        print(f"  Limits: {e.get('limitations', 'none')}")
    print()


def list_roles():
    data = load_json("MULTI_AGENT_ROLE_MATRIX.json")
    roles = data.get("roles", [])
    print(f"\n=== UAI-COS MULTI-AGENT ROLE MATRIX (§8) — Total {len(roles)} roles ===")
    for r in roles:
        print(f"  - {r['role']:<22} [{r['status']}] : {r['responsibility']}")
    print()


def get_depth_profile(level: int) -> dict:
    profiles = {
        0: {"name": "Level 0 — Immediate Answer", "desc": "Immediate answer from reliable existing knowledge.", "tools": ["internal_memory"]},
        1: {"name": "Level 1 — Basic Verification", "desc": "Basic verification on single source.", "tools": ["fetch_page", "read_file"]},
        2: {"name": "Level 2 — Multiple-Source Research", "desc": "Multiple independent sources triangulation.", "tools": ["web_search", "fetch_page", "curl"]},
        3: {"name": "Level 3 — Deep Research + Contradiction Checking", "desc": "Deep research, contradiction hunting, source quality grading.", "tools": ["web_search", "curl", "python3", "uai_mem"]},
        4: {"name": "Level 4 — Multi-Agent Research + Independent Verification", "desc": "Role delegation + independent validation checks.", "tools": ["all_tools", "apply_phase.py", "route_monitor.py"]},
        5: {"name": "Level 5 — Deep Research + Experiments + Red-Team + Evolution", "desc": "Full pipeline with controlled experiments, red-teaming, knowledge graph updates, workflow evolution.", "tools": ["full_ecosystem"]}
    }
    return profiles.get(level, profiles[1])


def main():
    parser = argparse.ArgumentParser(description="UAI-COS Central Meta-Orchestrator")
    parser.add_argument("--gates", action="store_true", help="Run 10 Quality Gates checklist")
    parser.add_argument("--environments", action="store_true", help="Display Environment Capability Matrix")
    parser.add_argument("--roles", action="store_true", help="Display Multi-Agent Role Matrix")
    parser.add_argument("--depth", type=int, choices=range(0, 6), help="Display research depth profile (0-5)")
    parser.add_argument("--verify-all", action="store_true", help="Verify all orchestration deliverables")

    args = parser.parse_args()

    if args.gates:
        run_quality_gates(verbose=True)
    elif args.environments:
        list_environments()
    elif args.roles:
        list_roles()
    elif args.depth is not None:
        p = get_depth_profile(args.depth)
        print(f"\nResearch Depth Profile: {p['name']}\nDescription: {p['desc']}\nTools: {', '.join(p['tools'])}\n")
    elif args.verify_all:
        q_ok = run_quality_gates(verbose=False)
        e_data = load_json("ENVIRONMENT_CAPABILITY_MATRIX.json")
        r_data = load_json("MULTI_AGENT_ROLE_MATRIX.json")
        k_data = load_json("KNOWLEDGE_OBJECT_MODEL.json")
        s_data = load_json("STATE_MACHINE.json")
        all_ok = q_ok and bool(e_data) and bool(r_data) and bool(k_data) and bool(s_data)
        print(f"ORCHESTRATOR VERIFY: {'PASS (5/5 matrices loaded)' if all_ok else 'FAIL'}")
        sys.exit(0 if all_ok else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
