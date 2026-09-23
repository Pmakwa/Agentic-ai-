# Copilot instructions — UAI-COS v2.0

Boot before work:
```bash
python3 tools/agent_boot.py
python3 tools/verify_provenance.py && python3 tools/uai_mem.py audit | tail -3 && bash tests/test_memory_os.sh | tail -3
python3 tools/phase_runner.py next
```
Then fill the BOOT ATTESTATION in `tests/boot_attestation.md` (12 points).

Hard rules: Roman Hindi; never bypass auth/paywall/CAPTCHA (§24); no access claim without test evidence;
never stop a task midway; finish with a Hindi summary + options (a/b/c).
New prompt/phase → `tools/import_prompt.py` / `tools/phase_runner.py add`; after work → `tools/sync_to_github.sh` (user-gated).
Full manual: `AGENTS.md`.
