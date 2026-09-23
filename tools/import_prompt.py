#!/usr/bin/env python3
"""
import_prompt.py — naya prompt (V2-type / naya phase / nayi spec) ko UAI-COS me import karne ka system.

Kya karta hai (ek command me):
  1. Prompt ko source se laata hai: --url (blocked page ho to r.jina.ai fallback), --file, ya --text
  2. `00_SYSTEM/NN_<NAME>_SPEC.md` me save karta hai (header + canonical body hash)
  3. `00_SYSTEM/prompts_index.json` update karta hai (source, date, hash, chars)
  4. Memory me record add karta hai (type=source, authority=user_explicit)
  5. `PROJECT_BOARD/phases.json` me auto phase add karta hai: "Apply <name> prompt"
  6. Batata hai aage kya karna hai (apply -> evidence -> push)

Usage:
  python3 tools/import_prompt.py --url "https://chatgpt.com/share/..." --name "V3"
  python3 tools/import_prompt.py --file /tmp/prompt.txt --name "PHASE_X"
  python3 tools/import_prompt.py --text "prompt ka poora text" --name "RULE_SET"
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, re, subprocess, sys, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYS = ROOT / "00_SYSTEM"
IDX = SYS / "prompts_index.json"
UA = "UAI-COS-research/1.0"


def fetch(url: str) -> tuple[str, str]:
    """(text, method). Direct try -> 403/HTML chhota -> r.jina.ai reader fallback (neutral UA)."""
    def _get(u: str) -> tuple[int, str]:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as f:
                return f.status, f.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "ignore")[:500]
        except Exception as e:  # noqa: BLE001
            return 0, f"{type(e).__name__}: {e}"

    st, body = _get(url)
    if st == 200 and len(body) > 800 and "Just a moment" not in body:
        return body, f"direct ({len(body)} chars)"
    st2, body2 = _get("https://r.jina.ai/" + url)
    if st2 == 200 and len(body2) > 800:
        return body2, f"r.jina.ai reader (direct HTTP {st}, {len(body2)} chars)"
    raise SystemExit(f"FETCH FAIL — direct HTTP {st}, reader HTTP {st2}. Page manually copy karke --text/--file use karo.")


def canon_hash(text: str) -> str:
    t = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    parts = t.split("\n---\n", 1)
    body = (parts[1].strip() + "\n") if len(parts) == 2 else (t.strip() + "\n")
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def next_number() -> str:
    nums = []
    for p in SYS.glob("[0-9][0-9]_*_SPEC.md"):
        m = re.match(r"(\d\d)_", p.name)
        if m:
            nums.append(int(m.group(1)))
    return f"{max(nums)+1 if nums else 0:02d}"


def main() -> int:
    ap = argparse.ArgumentParser(description="UAI-COS prompt importer")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--url"); src.add_argument("--file"); src.add_argument("--text")
    ap.add_argument("--name", required=True, help="prompt ka naam (e.g., V3, PHASE_X, RULE_SET)")
    ap.add_argument("--note", default="")
    ap.add_argument("--no-phase", action="store_true", help="phase entry auto-add mat karo")
    a = ap.parse_args()

    if a.url:
        text, method = fetch(a.url); source = a.url
    elif a.file:
        text = Path(a.file).read_text(encoding="utf-8", errors="ignore"); method = f"file: {a.file}"; source = str(a.file)
    else:
        text = a.text; method = "inline text"; source = "user message"
    text = text.strip()
    if len(text) < 50:
        print("ERROR: prompt bahut chhota lag raha hai — check karo."); return 1

    num = next_number()
    slug = re.sub(r"[^A-Za-z0-9]+", "_", a.name).strip("_").upper()
    out = SYS / f"{num}_{slug}_SPEC.md"
    h = canon_hash(text)
    header = (f"<!-- source: {source}\n"
              f"     imported: {datetime.datetime.utcnow().isoformat(timespec='seconds')}Z\n"
              f"     method: {method}\n"
              f"     canonical_body_sha256_16: {h}\n"
              f"     NOTE: ye file import ke waqt ki snapshot hai — canonical source user ke paas hai.\n-->\n\n")
    out.write_text(header + text + "\n", encoding="utf-8")

    idx = json.loads(IDX.read_text(encoding="utf-8")) if IDX.exists() else {"prompts": []}
    idx["prompts"].append({"name": a.name, "file": str(out.relative_to(ROOT)), "source": source,
                           "method": method, "chars": len(text), "body_sha256_16": h,
                           "imported": datetime.date.today().isoformat(), "note": a.note})
    IDX.write_text(json.dumps(idx, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # memory record
    subprocess.run([sys.executable, str(ROOT / "tools" / "uai_mem.py"), "add",
                    "--type", "source", "--statement", f"Prompt import: {a.name} ({len(text)} chars, sha256[16]={h})",
                    "--detail", f"source: {source} | method: {method} | file: {out.relative_to(ROOT)}. "
                                f"Naya prompt aane par use import karke phases me apply karna hai.",
                    "--source", source, "--ref", str(out.relative_to(ROOT)),
                    "--confidence", "very_high", "--status", "verified", "--authority", "user_explicit",
                    "--tag", "prompt-import", "--tag", a.name.lower()],
                   check=False, capture_output=True)

    # phase entry
    if not a.no_phase:
        subprocess.run([sys.executable, str(ROOT / "tools" / "phase_runner.py"), "add",
                        "--title", f"Apply imported prompt: {a.name}", "--status", "next",
                        "--evidence", str(out.relative_to(ROOT)),
                        "--next-step", "prompt padho -> rules/behaviour environment me apply karo -> evidence -> push"],
                       check=False, capture_output=True)

    print(f"""[OK] prompt import ho gaya
  file        : {out.relative_to(ROOT)}
  chars       : {len(text):,}
  body hash   : {h}
  method      : {method}
  memory      : record add (source)
  phase       : {'skip' if a.no_phase else 'auto-added (status=next)'}

Aage kya:
  1. Prompt padho aur uske rules environment me apply karo (agent_boot.py update / AGENTS.md / protocol)
  2. Jo bhi naya capability/rule bane -> evidence + CAPABILITY_MAP bump + memory
  3. python3 tools/agent_boot.py --write   (boot prompt regenerate, taaki naye rules agent ko milen)
  4. python3 tools/phase_runner.py md && GITHUB_TOKEN=<token> bash tools/sync_to_github.sh "import: {a.name}"
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
