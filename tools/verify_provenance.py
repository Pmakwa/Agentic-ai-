#!/usr/bin/env python3
"""verify_provenance.py — Section #16/#71: canonical spec files aur raw extraction ka hash
provenance.json ke saath match karta hai ya nahi. Har badi change ke baad chalao.

Usage: python3 tools/verify_provenance.py
"""
import hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, "00_SYSTEM", "provenance.json"), encoding="utf-8"))

def body(path):
    t = open(os.path.join(ROOT, path), encoding="utf-8").read()
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    parts = t.split("\n---\n", 1)
    return (parts[1].strip() + "\n") if len(parts) == 2 else (t.strip() + "\n")

def h(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]

fail = 0
for tag, meta in P["canonical"].items():
    got = h(body(meta["file"]))
    ok = got == meta["body_sha256_16"]
    fail += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] canonical {tag.upper():<3} {meta['file']}  hash={got}  chars={len(body(meta['file'])):,}")
for tag, meta in P["raw_extraction"].items():
    got = h(open(os.path.join(ROOT, meta["file"]), encoding="utf-8").read())
    ok = got == meta["sha256_16"]
    fail += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] raw       {tag.upper():<3} {meta['file']}  hash={got}")
print()
if fail:
    print("PROVENANCE FAIL — koi file badal gayi. Naya hash provenance.json me likho aur IMPORT_LOG update karo (Section #39).")
else:
    print("PROVENANCE OK — imported spec + raw extraction untouched hain, source traceable hai.")
sys.exit(1 if fail else 0)
