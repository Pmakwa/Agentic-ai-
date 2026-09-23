# GEMINI.md — UAI-COS v2.0

Is repo me kaam karne se pehle **boot** karo:
- `python3 tools/agent_boot.py` — poora system (rules, spec map 42k chars ka index, memory 73 records, capability truth, phases)
- Health check: `python3 tools/verify_provenance.py` (4/4) · `python3 tools/uai_mem.py audit` (100/100) · `bash tests/test_memory_os.sh` (28/28)
- `python3 tools/phase_runner.py next` — agla kaam
- Attestation: `tests/boot_attestation.md` (12 points) — boot proof

**Rules:** Roman Hindi · §24 boundary (auth/paywall/CAPTCHA bypass nahi) · No-False-Access ·
kaam beech me nahi · end me summary + options (a/b/c) · naya phase/prompt → `tools/import_prompt.py` / `phase_runner.py add`.

Full manual: `AGENTS.md`.
