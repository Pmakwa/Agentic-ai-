# CLAUDE.md — UAI-COS v2.0

**Ye repo ek self-contained AI operating system hai. Kaam shuru karne se pehle BOOT karo.**

## STEP 0 — HARD BOOT (skip mat karo)
```bash
python3 tools/agent_boot.py                 # poora system ek payload me (rules + spec map + memory + capability truth + phases)
python3 tools/verify_provenance.py          # expect 4/4 PASS
python3 tools/uai_mem.py audit | tail -3    # expect 100/100
bash tests/test_memory_os.sh | tail -3      # expect 28/28
python3 tools/phase_runner.py next          # agla kaam
```
Phir `BOOT ATTESTATION` bharo (`tests/boot_attestation.md`, 12 points) — uske baad hi kaam shuru.

## Rules (short)
- **Hindi (Roman script)** me baat karo, English spelling me.
- **Auth / paywall / CAPTCHA / anti-bot bypass nahi** (spec §24).
- Bina test/evidence koi "access hai / ho gaya" claim nahi (No-False-Access).
- **Kaam beech me nahi rokna**; end me Hindi summary + options (a/b/c).
- Naya prompt/phase aaye → `python3 tools/import_prompt.py` ya `python3 tools/phase_runner.py add`.
- Kaam ke baad: `GITHUB_TOKEN=<token> bash tools/sync_to_github.sh "message"` (sirf jab user bole/token de).

## Read order
`AGENTS.md` (full manual) → `00_SYSTEM/OPERATIONAL_PROTOCOL.md` → `memory/INDEX.md` → `PROJECT_BOARD/PHASES.md` → `CONVERSATION/00_A_TO_Z_LOG.md`
