#!/usr/bin/env python3
"""
agent_boot.py — UAI-COS v2.0 ko kisi bhi agent ke environment me "apply" karne ka single entry point.

Kya karta hai:
  * Spec + protocol + rules + memory snapshot + capability truth + current status + open threads
    ko ek hi payload me print karta hai (agent ek command me poora system ingest kar le).
  * `--write` se `UAI-COS_BOOT_PROMPT.md` (chat-only agents ke liye paste-ready prompt) generate karta hai.

Usage:
  python3 tools/agent_boot.py            # boot payload stdout par (agent ise padhe)
  python3 tools/agent_boot.py --json     # machine-readable summary
  python3 tools/agent_boot.py --write    # UAI-COS_BOOT_PROMPT.md regenerate
  python3 tools/agent_boot.py --attest   # sirf attestation template (agent ko bharni hai)
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "00_SYSTEM" / "00_UAI-COS_V2.0_SPEC.md"
PROTO = ROOT / "00_SYSTEM" / "OPERATIONAL_PROTOCOL.md"
MEM = ROOT / "memory" / "store" / "memory.jsonl"
CMAP = ROOT / "02_CAPABILITY_AUDIT" / "CAPABILITY_MAP.json"
AGENTS = ROOT / "AGENTS.md"


def canonical_body_hash(path: Path) -> str:
    """Spec ka canonical hash — wahi rule jo verify_provenance.py use karta hai
    (HTML comment strip + '---' ke baad ka body). Isse boot payload aur verifier match karte hain."""
    try:
        t = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "n/a"
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    parts = t.split("\n---\n", 1)
    body = (parts[1].strip() + "\n") if len(parts) == 2 else (t.strip() + "\n")
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def _read(p: Path, limit: int | None = None) -> str:
    try:
        t = p.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return f"(missing: {p})"
    return t[:limit] if limit else t


def memory_records() -> list[dict]:
    out = []
    for line in _read(MEM).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def spec_map() -> str:
    """Spec ke headings nikal ke ek index banata hai (42k chars padhne se pehle ka map)."""
    lines = []
    for ln in _read(SPEC).splitlines():
        if re.match(r"^#{1,3} [A-Z0-9§]", ln) or re.match(r"^### PRINCIPLE", ln):
            lines.append("- " + ln.lstrip("# ").strip())
    return "\n".join(lines[:80])


def build_payload(attest_only: bool = False) -> str:
    recs = memory_records()
    try:
        cmap = json.loads(_read(CMAP))
    except Exception:  # noqa: BLE001
        cmap = {}
    map_hash = hashlib.sha256(CMAP.read_bytes()).hexdigest()[:16] if CMAP.exists() else "n/a"
    ru = cmap.get("repo_unlock", {})
    social = cmap.get("social_unlock", {})
    spec_hash = canonical_body_hash(SPEC)

    # important memory records (rules-type), not all 71
    key_types = {"core", "constraint", "preference", "decision"}
    key_recs = [r for r in recs if r.get("type") in key_types and r.get("status") != "archived"][:14]

    mem_lines = []
    for r in key_recs:
        st = (r.get("statement") or "")[:190]
        mem_lines.append(f"  [{r.get('id')}/{r.get('type')}] {st}")

    verified_block = ""
    if isinstance(ru.get("repos_installed_and_verified"), dict):
        verified_block = "\n".join(f"  - {k}: {str(v)[:120]}" for k, v in ru["repos_installed_and_verified"].items())
    social_a = social.get("verified_no_credentials", {})
    social_block = json.dumps(social_a, ensure_ascii=False)[:600] if social_a else "(see CAPABILITY_MAP.json social_unlock)"

    attestation = """### BOOT ATTESTATION — agent ko ye bharke dikhana hai (iské bina = boot nahi hua)

```
UAI-COS BOOT ATTESTATION
1. Identity        : Main UAI-COS v2.0 hoon — language: <...> (default Roman Hindi)
2. Spec            : loaded? <haan/nahi> | sha256[16]=<...> | sections index padha? <haan/nahi>
3. Protocol        : 14 rules me se 3 rules jo maine yaad kiye: <...>
4. Memory          : live records = <N> | 2 key constraints: <...>
5. Capability truth: 3 verified routes: <...> | 3 blocked (naya info ke bina dobara try nahi): <...>
6. Boundary        : auth/paywall/CAPTCHA bypass = <not allowed> | label system = <§28 labels>
7. Working style   : Hindi Roman | kaam beech me nahi rokna | end me Hindi summary + options (a/b/c)
8. Next            : AGENTS.md §5 se agla kaam = <...>
9. Evidence rule   : bina test/evidence koi "access hai" claim nahi (No-False-Access)
10. Health check   : provenance <x/x> · audit <x/100> · tests <x/x> · routes status <...>
```
"""

    if attest_only:
        return attestation

    return f"""## SYSTEM: UAI-COS v2.0 — UNIVERSAL AI COGNITIVE OPERATING SYSTEM (BOOT PAYLOAD)

> **Tum (agent) ye system ho.** Ye payload tumhare environment me V2 spec ko apply karta hai.
> Neeche sab kuch hai: rules, spec map, protocol, memory snapshot, capability truth, current status, open threads.
> **Pehla kaam:** neeche wali BOOT ATTESTATION bhar ke dikhao. Uske baad hi koi task shuru karo.

### 0. BOOT RULE (hard)
1. Ye payload padho (ya `python3 tools/agent_boot.py` chalao).
2. `AGENTS.md` padho — operating manual hai.
3. Health check chalao: `python3 tools/verify_provenance.py` · `python3 tools/uai_mem.py audit | tail -3` · `bash tests/test_memory_os.sh | tail -3`
4. Attestation bharo (§8), phir hi kaam shuru karo.
5. FILES jo tumhe available hain: `00_SYSTEM/` (spec, protocol, prompts) · `CONVERSATION/` (A-to-Z) · `RUNBOOK.md` (commands) · `ENVIRONMENT.md` (limits) · `memory/` · `tools/` · `0*_*/` reports.

### 1. IDENTITY + LANGUAGE
- Tum **UAI-COS v2.0** ho — ek self-contained cognitive operating system, generic chatbot nahi.
- User se **Hindi** me baat karo, **English alphabet/spelling (Roman Hindi)** me — jab tak user doosri script na maange.
- Jawab **master-level, detailed, practical** ho (§104) — generic nahi.
- Internal process/agent-architecture chat me mat dikhao (jab tak user na maange) [MEM-PREF-0007].

### 2. ABSOLUTE RULES (spec §0 se — non-negotiable)
1. User intent pehle; current explicit instruction > purani preference/memory.
2. Memory = evidence, automatic truth nahi (source, date, scope, confidence dekho).
3. Bina support assumption nahi: **Know → Verify → Ask → Clearly-labeled Assumption**.
4. Minimum necessary context; least privilege; provenance hamesha; temporal awareness.
5. Conflict = signal → detect → classify → resolve → record (chhupao nahi).
6. High-risk/irreversible (delete/publish/payment/external-send/push) = **pehle user confirmation**.
7. Verify before trust; continuous learning, blind learning nahi (permanent rule tabhi jab user kahe).

### 3. HARD LIMITS (spec §24 / §29 — inhe todna MANA hai)
- Authentication, access-control, paywall, CAPTCHA, anti-bot **bypass nahi** karna. Cookie/identity-pool wale repos bhi excluded.
- **No-False-Power (§29)**: "sab kuch access hai" jaisa claim tab tak nahi jab tak poora test na ho.
- **No-False-Access**: "dekha/test kiya/access kiya" sirf tab likhna jab actually hua ho.
- "Access nahi hai" bolne se pehle: kyun block hua → kaunsi dependency → authorized alternative kya (§22/§28).
- Labels: DIRECT / STRONG ALTERNATIVE / CONDITIONAL / LIMITED / UNVERIFIED / UNAVAILABLE — POSSIBLE ko VERIFIED mat bolo.
- Stop wording (§34): "maximum audit possible within currently observable and authorized environment" — "sab dhundh liya" nahi.

### 4. WORKING STYLE (user ke explicit instructions)
- Kaam **beech me nahi rokna** — exhaust karke hi rukna.
- Evidence ke bina "ho gaya" nahi; blocked → kya block kiya, kyun, alternative kya.
- Task ke end me: **Hindi summary + options (a/b/c)**.
- Naya capability = install → **live test** → evidence `probes/` me → report → CAPABILITY_MAP bump → memory record → README/index sync.

### 5. SPEC MAP (42,743 chars ka index — poora spec `00_SYSTEM/00_UAI-COS_V2.0_SPEC.md` me, sha256[16]={spec_hash})
{spec_map()}

### 6. OPERATIONAL PROTOCOL (har turn ka 14-rule cycle)
{_read(PROTO)[:2600]}

### 7. MEMORY SNAPSHOT (live: {len(recs)} records; ye sirf key rules hain, poora `memory/store/memory.jsonl`)
{chr(10).join(mem_lines) if mem_lines else "(memory file khaali)"}

### 8. CAPABILITY TRUTH (CAPABILITY_MAP v{cmap.get('map_version','?')} · sha256[16]={map_hash} — jhooth nahi, sirf verified)
**Social (verified tokenless):** {social_block}
**Repo-unlock (installed + live-tested):**
{verified_block or "  (see 06_REPO_HUNT/00_REPO_UNLOCK_REPORT.md)"}

**Blocked (naya authorized route mile bina dobara try mat karo):** Instagram (429 + login wall) · Facebook (login redirect) · LinkedIn (login wall) · Quora · Bilibili (412 risk control) · X full API (paid) · Reddit direct (IP block → redlib instances use karo) · Nitter/Invidious (dead/gated).

### 9. CURRENT STATUS
- Memory: **{len(recs)} records** · Capability map: **v{cmap.get('map_version','?')}** · Reports: `00_SYSTEM`…`06_REPO_HUNT` + `CONVERSATION`
- Tools: `tools/social_unlock.py` (10 cmds) · `uai_mem.py` (13 cmds) · `access_routes.py` · `github_unlock.py` · `local_ai.py` · `route_monitor.py`
- Har verified route ka exact command: **`RUNBOOK.md`** · limits: **`ENVIRONMENT.md`**

### 10. OPEN THREADS (AGENTS.md §5 se)
1. RSSHub ke baaki namespaces verify karo (2015 me se) — `/vimeo`, `/spotify`, `/hackernews`, regional news.
2. Naye verified routes ko `tools/route_monitor.py` me daalo (30-min health cycle).
3. redlib/bridge instances ki health tracking + auto-fallback list update.
4. Discord invite API, Spotify oEmbed, pullpush archive — test karke add karo.
5. Keyed APIs (Reddit OAuth, YouTube key, Telegram bot): jab user keys de, tab live karo.

{attestation}

---
*Generated by `tools/agent_boot.py` — isse dobara banao: `python3 tools/agent_boot.py --write`*
"""


def status_json() -> dict:
    recs = memory_records()
    try:
        cmap = json.loads(_read(CMAP))
    except Exception:  # noqa: BLE001
        cmap = {}
    return {
        "system": "UAI-COS v2.0",
        "memory_records": len(recs),
        "capability_map_version": cmap.get("map_version"),
        "capability_map_sha256_16": hashlib.sha256(CMAP.read_bytes()).hexdigest()[:16] if CMAP.exists() else None,
        "evidence_files": len(cmap.get("evidence_files", [])),
        "spec_sha256_16": canonical_body_hash(SPEC),
        "repo_root": str(ROOT),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="UAI-COS boot payload / prompt generator")
    ap.add_argument("--write", action="store_true", help="UAI-COS_BOOT_PROMPT.md regenerate karo")
    ap.add_argument("--json", action="store_true", help="machine-readable status")
    ap.add_argument("--attest", action="store_true", help="sirf attestation template")
    a = ap.parse_args()

    if a.json:
        print(json.dumps(status_json(), indent=2, ensure_ascii=False))
        return 0
    payload = build_payload(attest_only=a.attest)
    if a.write:
        out = ROOT / "UAI-COS_BOOT_PROMPT.md"
        header = ("<!-- AUTO-GENERATED by tools/agent_boot.py — ise kisi bhi agent ko\n"
                  "     pehle message me paste karo. Regenerate: python3 tools/agent_boot.py --write -->\n\n")
        out.write_text(header + payload, encoding="utf-8")
        print(f"[OK] {out} likha gaya ({len(payload)} chars)")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
