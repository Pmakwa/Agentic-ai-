#!/usr/bin/env python3
"""
prompt_registry.py — UAI-COS **structured prompt registry**.

User ke *structured prompts* (V1, V2, Phase-1/2/3, rules packs, boot prompt) yahan register hote hain.
Har entry ka **body hash** hota hai, aur likha hota hai wo system me **kahan apply hui** — taaki koi bhi agent
check kar sake ki "sab prompts apply ho chuke hain" ya nahi.

Difference from import_prompt.py:
  import_prompt.py  = naya *raw/big* prompt import (url/file/text) -> 00_SYSTEM spec + memory + auto phase
  prompt_registry.py= saare structured prompts ka **index + apply-tracking + verification** (ye file)

Usage:
  python3 tools/prompt_registry.py seed                  # initial entries (V1, V2, Phase 1-3, rules, boot)
  python3 tools/prompt_registry.py list [--type phase]
  python3 tools/prompt_registry.py add --file /tmp/p.txt --title "Phase 4" --type phase --source "user message" [--applied-in "AGENTS.md §9"] [--verbatim]
  python3 tools/prompt_registry.py verify                # hashes + missing files check
  python3 tools/prompt_registry.py apply-check           # kaunse prompts kis jagah apply hue
  python3 tools/prompt_registry.py md                    # PROMPTS/REGISTRY.md regenerate
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "PROMPTS"
REG = PROMPTS / "registry.json"
TYPES = ["spec", "phase", "rules", "boot", "task", "reference"]


def sha16(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def canon_body(path: Path) -> str:
    """Spec-style files: HTML comments strip, `\\n---\\n` ke baad wala part = canonical body."""
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    parts = t.split("\n---\n", 1)
    return (parts[1].strip() + "\n") if len(parts) == 2 else (t.strip() + "\n")


def load() -> dict:
    if REG.exists():
        return json.loads(REG.read_text(encoding="utf-8"))
    return {"generated": time.strftime("%Y-%m-%d"), "note": "Structured prompt registry — har entry ka hash + apply-location.", "prompts": []}


def save(d: dict) -> None:
    PROMPTS.mkdir(exist_ok=True)
    d["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    REG.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def entry_file(eid: str, title: str, body: str, meta: dict, *, verbatim: bool, source: str, ptype: str) -> Path:
    PROMPTS.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_").upper()
    f = PROMPTS / f"{eid}_{slug}.md"
    header = (
        f"# {eid} — {title}\n\n"
        f"<!-- structured prompt entry | type: {ptype} | verbatim: {str(verbatim).lower()} | source: {source} "
        f"| body_sha256_16: {sha16(body)} | added: {time.strftime('%Y-%m-%d')} -->\n"
        f"| field | value |\n|---|---|\n"
        f"| Type | `{ptype}` |\n| Source | {source} |\n| Verbatim user text? | {'haan' if verbatim else 'nahi (reconstructed)'} |\n"
        f"| Applied in | {', '.join(meta.get('applied_in') or ['(pending)'])} |\n\n---\n\n{body.strip()}\n"
    )
    f.write_text(header, encoding="utf-8")
    return f


def add_prompt(d: dict, *, title: str, ptype: str, source: str, body: str = "", verbatim: bool = True,
               applied_in: list[str], file: str | None = None, note: str = "", eid: str | None = None) -> dict:
    eid = eid or f"SP-{len(d['prompts']) + 1:03d}"
    if file:
        f = ROOT / file
        body_txt = canon_body(f)
        h = sha16(body_txt)
    else:
        f = entry_file(eid, title, body, {"applied_in": applied_in}, verbatim=verbatim, source=source, ptype=ptype)
        h = sha16(body)
    e = {"id": eid, "title": title, "type": ptype, "source": source, "file": str(f.relative_to(ROOT)),
         "verbatim": verbatim, "body_sha256_16": h, "applied_in": applied_in, "applied": bool(applied_in),
         "added": time.strftime("%Y-%m-%d"), "note": note}
    d["prompts"] = [p for p in d["prompts"] if p["id"] != eid] + [e]
    d["prompts"].sort(key=lambda x: x["id"])
    return e


# ---------------------------------------------------------------- commands
def cmd_seed(a) -> int:
    d = load()
    seeded = [
        dict(eid="SP-001", title="V1.0 structured spec (Parts 1-15)", ptype="spec", verbatim=True,
             source="user structured prompt (share link) — r.jina.ai se import",
             file="00_SYSTEM/01_UAI-COS_V1.0_SPEC.md", applied_in=["AGENTS.md §1", "tools/agent_boot.py", "00_SYSTEM/OPERATIONAL_PROTOCOL.md"],
             note="Base spec — history + intent disambiguation. Hash verify: tools/verify_provenance.py (4/4)."),
        dict(eid="SP-002", title="V2.0 structured spec (112 sections)", ptype="spec", verbatim=True,
             source="user structured prompt (share link) — r.jina.ai se import",
             file="00_SYSTEM/00_UAI-COS_V2.0_SPEC.md",
             applied_in=["AGENTS.md §1-§4", "UAI-COS_BOOT_PROMPT.md", "tools/agent_boot.py (SPEC MAP)", "memory/", "tests/boot_attestation.md"],
             note="Canonical system spec — sha256[16]=4aa1c6a1f872a3f3. Isko edit nahi karte; naya prompt alag entry."),
        dict(eid="SP-003", title="Phase 1 — capability baseline + audit prompt", ptype="phase", verbatim=False,
             source="user structured prompt (conversation) — verbatim text repo me nahi tha",
             body=("# Phase 1 (reconstructed)\n\n"
                   "User ka pehla structured phase prompt: system ko *imandaari se* samjho — kya kya capability hai, kya nahi.\n\n"
                   "**Kya apply hua:**\n"
                   "- 29-site capability matrix + secrets scan -> `02_CAPABILITY_AUDIT/CAPABILITY_MAP.json` (v1.x)\n"
                   "- Evidence-only claiming (No-False-Access), status labels (VERIFIED/POSSIBLE/BLOCKED…)\n"
                   "- Environment reality doc -> `ENVIRONMENT.md`\n\n"
                   "**Note:** verbatim user text repo me nahi mila (share-link extraction me sirf assistant text tha). "
                   "Jab user verbatim de de -> `python3 tools/prompt_registry.py add --file <file> --title 'Phase 1 (verbatim)' --eid` se replace karo.\n"),
             applied_in=["02_CAPABILITY_AUDIT/", "ENVIRONMENT.md", "AGENTS.md §4"]),
        dict(eid="SP-004", title="Phase 2 — access expansion prompt", ptype="phase", verbatim=False,
             source="user structured prompt (conversation) — verbatim text repo me nahi tha",
             body=("# Phase 2 (reconstructed)\n\n"
                   "User ka doosra structured phase prompt: jo targets blocked the, unke **legitimate routes** dhoondo\n"
                   "(jina reader, Wayback, public APIs) — bypass nahi, sirf legal/open raste.\n\n"
                   "**Kya apply hua:**\n"
                   "- 12 blocked targets me se 9 ke routes khule -> `03_ACCESS_EXPANSION/` (6 deliverables)\n"
                   "- `tools/access_routes.py` (demo|fetch|rss|so|paper|nse|wb), route_provenance.jsonl\n"
                   "- Boundary saaf likhi: auth/paywall/CAPTCHA bypass = NAHI (spec §24)\n\n"
                   "**Note:** verbatim text repo me nahi; user de de to yahi entry update ho jayegi.\n"),
             applied_in=["03_ACCESS_EXPANSION/", "tools/access_routes.py", "CONVERSATION/01_ACTION_LEDGER.md §D"]),
        dict(eid="SP-005", title="Phase 3 — repo hunt + apply (GitHub repos ko capability me badlo)", ptype="phase", verbatim=False,
             source="user structured prompt (conversation) + continue-instruction",
             body=("# Phase 3 (reconstructed)\n\n"
                   "GitHub par jo open-source repos/tools hain unhe dhoondo, **test karo, aur jo kaam kare unhe lock karo** —\n"
                   "phir sab kuch repo me likho taaki koi bhi agent wahi system apply kare.\n\n"
                   "**Kya apply hua:**\n"
                   "- `06_REPO_HUNT/00_REPO_UNLOCK_REPORT.md` (15 repos, boundary-excluded bhi likhe)\n"
                   "- `tools/social_unlock.py` (reddit/rsshub/gallery/pin/transcript/comments/x/bsky/invite/spotify/pullpush/status)\n"
                   "- `tools/rsshub_verify.py` -> 28 curated + **120/250 namespaces live**\n"
                   "- `tools/github_unlock.py`, redlib instances, gallery-dl (TikTok/Bluesky/Pinterest), yt-dlp, transcript API\n"
                   "- Phase system: `phases.json` + `phase_runner.py` + `import_prompt.py` (naya prompt aate hi auto-apply)\n"),
             applied_in=["06_REPO_HUNT/", "05_SOCIAL_UNLOCK/", "tools/social_unlock.py", "PROJECT_BOARD/phases.json"]),
        dict(eid="SP-006", title="Standing instructions pack (user rules — always apply)", ptype="rules", verbatim=True,
             source="user ne har turn bola/confirm kiya (conversation)",
             file="CONVERSATION/04_STANDING_INSTRUCTIONS.md",
             applied_in=["AGENTS.md §5,§9", "UAI-COS_BOOT_PROMPT.md", "PHASE_PROTOCOL.md §5", "tests/ci_extra.py (boot freshness)"]),
        dict(eid="SP-007", title="Boot prompt (paste-ready, generated)", ptype="boot", verbatim=False,
             source="generated by tools/agent_boot.py --write",
             file="UAI-COS_BOOT_PROMPT.md",
             applied_in=["CLAUDE.md", "GEMINI.md", ".windsurfrules", ".cursor/rules/uai-cos.mdc", ".github/copilot-instructions.md", "START_HERE.md"]),
        dict(eid="SP-009", title="Structured-prompt apply rule (V2 / Phase-1 / Phase-2 / aage jo bhi)", ptype="rules", verbatim=True,
             source="user instruction 2026-09-23: 'jo jo structured prompt dunga (V2, Phase 1, Phase 2...) wo sab apply karna chahiye'",
             body=("# Structured prompts — apply rule\n\n"
                   "User ke **saare structured prompts** (V1, V2, Phase 1, Phase 2, Phase 3, aur aage jo bhi aayega) "
                   "repo me register honge aur **environment me apply** honge.\n\n"
                   "1. Entry banao: `python3 tools/prompt_registry.py add --file/--text --title ... --type phase|spec|rules`\n"
                   "2. Apply karo, phir likho kahan apply hua: `prompt_registry.py apply --id SP-xxx --where 'AGENTS.md §9, <script>'`\n"
                   "3. Boot payload me lao: `python3 tools/agent_boot.py --write` (taaki har naya agent ye rules padhe)\n"
                   "4. Verify: `python3 tools/prompt_registry.py verify` (hash + applied) — CI bhi ye chalata hai.\n"
                   "5. Jo prompt sirf conversation me tha (verbatim repo me nahi) — entry me `verbatim: recon` likho aur user se\n"
                   "   verbatim maang kar update karo.\n\n"
                   "**Rule: koi structured prompt bina apply + bina REGISTRY entry ke nahi chhodna.**\n"),
             applied_in=["PROMPTS/registry.json", "PROMPTS/REGISTRY.md", "AGENTS.md §13", "PHASE_PROTOCOL.md §8", "tests/ci_extra.py"]),
        dict(eid="SP-010", title="Cleanup safety lesson (node_modules dedupe incident)", ptype="rules", verbatim=False,
             source="agent incident 2026-09-23 + user instruction 'time to time cleanup karte rehna'",
             body=("# Cleanup safety (2026-09-23 ka incident)\n\n"
                   "Pehle cleanup run ne node_modules + `lib/` ke andar 'duplicates' delete kar diye (7959 files) → "
                   "RSSHub toot gaya. Recovery: fresh clone + `pnpm install` + build → `/opt/uai-cache/rsshub`.\n\n"
                   "**Isliye permanent rules:**\n"
                   "1. HEAVY dirs (`node_modules`, `.pnpm`, `dist`, `build`, `.venv`, `lib` of vendored deps) никогда "
                   "scan/delete nahi — protected.\n"
                   "2. Duplicate delete sirf `--dedupe` flag se (default `--apply` me nahi).\n"
                   "3. 500+ deletions ke liye `--force`, warna tool khud ruk jata hai.\n"
                   "4. Delete se pehle `--check`/report padho; reason `logs/cleanup_*.md` me likho.\n"
                   "5. Heavy deps workspace me hi nahi rakhte — `/opt/uai-cache/`.\n"),
             applied_in=["tools/cleanup_workspace.py (PROTECTED/HEAVY_SKIP/DELETE_CAP)", "AGENTS.md §12", "PHASE_PROTOCOL.md §7", "tests/ci_extra.py"]),
        dict(eid="SP-008", title="Workspace hygiene + recurring cleanup rule", ptype="rules", verbatim=True,
             source="user instruction 2026-09-23: 'faltu/bekar/duplicate cheezein delete karo, time to time karte rehna'",
             body=("# Workspace hygiene (recurring)\n\n"
                   "1. Naya prompt/phase aaye -> registry me entry (`prompt_registry.py add ...`) + apply + boot regenerate.\n"
                   "2. Har kaam ke baad: evidence rakho, kachra delete karo.\n"
                   "3. **Time-to-time cleanup:** `python3 tools/cleanup_workspace.py` (report) -> `--apply` (safe junk delete).\n"
                   "   Cadence: har 3-5 turn ya jab workspace > 1.2 GB, phir bhi har push se pehle ek report.\n"
                   "4. Duplicates: exact-duplicate files ko rakho ek copy me; obsolete files (superseded scripts/docs) delete karo\n"
                   "   aur REASON `logs/cleanup_*.md` me likho.\n"
                   "5. Heavy deps (node_modules, RSSHub) workspace ke andar nahi — `/opt/uai-cache/` me rakho.\n"),
             applied_in=["AGENTS.md §12", "PHASE_PROTOCOL.md §7", "PROJECT_BOARD/phases.json (recurring_checklist)", "tools/cleanup_workspace.py"]),
    ]
    for s in seeded:
        add_prompt(d, **s)
    save(d)
    print(f"[OK] seed complete — {len(d['prompts'])} structured prompts registered")
    cmd_md(a)
    return 0


def cmd_list(a) -> int:
    d = load()
    rows = [p for p in d["prompts"] if not a.type or p["type"] == a.type]
    print(f"{'ID':<7} {'TYPE':<10} {'VERB':<5} {'APPLIED':<8} TITLE")
    for p in rows:
        print(f"{p['id']:<7} {p['type']:<10} {'yes' if p['verbatim'] else 'recon':<5} "
              f"{'yes' if p.get('applied') else 'NO':<8} {p['title'][:60]}")
    print(f"\ntotal: {len(rows)}" + (f"  (filter: {a.type})" if a.type else ""))
    return 0


def cmd_add(a) -> int:
    d = load()
    body = a.text or ""
    if a.file:
        body = Path(a.file).read_text(encoding="utf-8")
    if not body:
        print("kuch bhi nahi diya (--file ya --text)"); return 2
    e = add_prompt(d, title=a.title, ptype=a.type, source=a.source, body=body, verbatim=not a.reconstructed,
                   applied_in=a.applied_in or [], file=None, note=a.note, eid=a.eid)
    save(d)
    print(f"[OK] {e['id']} add hua -> {e['file']}  hash={e['body_sha256_16']}")
    if not e["applied_in"]:
        print("     ⚠️  applied_in khaali hai — is prompt ko environment me apply karke location add karo:")
        print(f"     python3 tools/prompt_registry.py apply --id {e['id']} --where 'AGENTS.md §X'")
    cmd_md(a)
    return 0


def cmd_apply(a) -> int:
    d = load()
    hit = [p for p in d["prompts"] if p["id"] == a.id]
    if not hit:
        print("id nahi mila"); return 1
    p = hit[0]
    p["applied_in"] = sorted(set((p.get("applied_in") or []) + a.where))
    p["applied"] = True
    save(d)
    print(f"[OK] {p['id']} -> applied_in: {', '.join(p['applied_in'])}")
    cmd_md(a)
    return 0


def cmd_verify(a) -> int:
    d = load()
    bad = 0
    for p in d["prompts"]:
        f = ROOT / p["file"]
        if not f.exists():
            print(f"  [FAIL] {p['id']} file missing: {p['file']}"); bad += 1; continue
        txt = f.read_text(encoding="utf-8")
        body = canon_body(f)
        h = sha16(body)
        # spec files ke liye canonical hash bhi accept karo
        if h != p["body_sha256_16"]:
            if p["type"] == "boot":
                print(f"  [refreshed] {p['id']} generated file badla -> hash {p['body_sha256_16']} -> {h}")
                p["body_sha256_16"] = h
                continue
            print(f"  [FAIL] {p['id']} hash mismatch: file={h} registry={p['body_sha256_16']}"); bad += 1
        elif not p.get("applied"):
            print(f"  [warn] {p['id']} verified hai par applied_in khaali (apply karna baaki?)")
        else:
            print(f"  [PASS] {p['id']} {p['title'][:48]} -> {', '.join(p['applied_in'])[:60]}")
    save(d)
    print(f"\n{'SAARE PROMPTS OK' if not bad else str(bad) + ' FAIL'}")
    return 1 if bad else 0


def cmd_md(a) -> int:
    d = load()
    out = ["# PROMPTS/REGISTRY.md — structured prompts ka index (auto-generated)", "",
           "> Source of truth: `PROMPTS/registry.json` · regenerate: `python3 tools/prompt_registry.py md`",
           "> Naya structured prompt aaye (V3 / Phase 4 / naya rules-pack) -> `prompt_registry.py add ...` phir usko apply karke",
           "> `apply --id SP-xxx --where '...'` chalao. Rule: **koi structured prompt bina apply ke nahi chhodna.**", "",
           "| ID | Type | Prompt | Verbatim | Body hash | Applied in | File |", "|---|---|---|---|---|---|---|"]
    for p in d["prompts"]:
        out.append(f"| {p['id']} | `{p['type']}` | **{p['title']}** | {'✅' if p['verbatim'] else '◐ recon'} "
                   f"| `{p['body_sha256_16']}` | {', '.join(p.get('applied_in') or ['⏳ pending'])} | `{p['file']}` |")
    out += ["", f"**Total:** {len(d['prompts'])} structured prompts · updated {d.get('updated','')}", "",
            "## Naya structured prompt add karne ka tareeka", "",
            "```bash",
            "python3 tools/prompt_registry.py add --file /tmp/new_prompt.txt --title \"Phase 4 — X\" --type phase \\",
            "    --source \"user message 2026-09-24\" --verbatim",
            "python3 tools/prompt_registry.py apply --id SP-009 --where 'AGENTS.md §9, UAI-COS_BOOT_PROMPT.md'",
            "python3 tools/prompt_registry.py verify && python3 tools/agent_boot.py --write",
            "```", ""]
    PROMPTS.mkdir(exist_ok=True)
    (PROMPTS / "REGISTRY.md").write_text("\n".join(out), encoding="utf-8")
    print(f"[OK] PROMPTS/REGISTRY.md likha gaya ({len(d['prompts'])} prompts)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="prompt_registry.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seed").set_defaults(f=cmd_seed)
    l = sub.add_parser("list"); l.add_argument("--type", choices=TYPES); l.set_defaults(f=cmd_list)
    ad = sub.add_parser("add")
    ad.add_argument("--file"); ad.add_argument("--text"); ad.add_argument("--title", required=True)
    ad.add_argument("--type", choices=TYPES, required=True); ad.add_argument("--source", default="user")
    ad.add_argument("--applied-in", nargs="*", default=[]); ad.add_argument("--note", default="")
    ad.add_argument("--eid"); ad.add_argument("--verbatim", action="store_true", default=True)
    ad.add_argument("--reconstructed", action="store_true", help="verbatim nahi, recreate kiya hua")
    ad.set_defaults(f=cmd_add)
    ap = sub.add_parser("apply"); ap.add_argument("--id", required=True); ap.add_argument("--where", nargs="+", required=True)
    ap.set_defaults(f=cmd_apply)
    sub.add_parser("verify").set_defaults(f=cmd_verify)
    sub.add_parser("apply-check").set_defaults(f=cmd_verify)
    sub.add_parser("md").set_defaults(f=cmd_md)
    a = p.parse_args()
    return a.f(a)


if __name__ == "__main__":
    raise SystemExit(main())
