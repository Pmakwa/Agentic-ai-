# PHASE PROTOCOL — naye phase/prompt ko apply karne ka contract

> Ye file batati hai ki **koi bhi agent** is repo me naya kaam kaise leta hai, naya prompt kaise import karta hai,
> aur "apply ho gaya" ka matlab kya hai. Isko todna mana hai — sab agents isi tarike se chalenge.

---

## 1. Kaam shuru karne se pehle: BOOT (mandatory)

```bash
python3 tools/agent_boot.py            # poora system: identity, rules, spec map+hash, protocol, memory, capability truth, phases, attestation
python3 tools/phase_runner.py next     # agla actionable phase
```
Chat-only agent (shell nahi): `UAI-COS_BOOT_PROMPT.md` paste karo.
Phir **BOOT ATTESTATION** (`tests/boot_attestation.md`, 12 points) bharo — **iske bina kaam shuru nahi hota**.

---

## 2. Phase lifecycle

| Status | Matlab | Kaise set hota hai |
|---|---|---|
| `next` | Queue me, chalu nahi | `phase_runner.py add` (default) |
| `active` | Abhi chal raha hai | `phase_runner.py set --id Pxx --status active` |
| `done` | Kaam + evidence + push ho gaya | `phase_runner.py set --id Pxx --status done --evidence "..."` |
| `waiting_user` | User ke action/creds ka wait | `phase_runner.py set --id Pxx --status waiting_user` |

Commands:
```bash
python3 tools/phase_runner.py status          # sab phases ka status
python3 tools/phase_runner.py next            # agla kaam (evidence + next step ke saath)
python3 tools/phase_runner.py add --title "Naya kaam" --status next --evidence "target: ..."
python3 tools/phase_runner.py set --id P21 --status active
python3 tools/phase_runner.py md              # PROJECT_BOARD/PHASES.md table regenerate
```
Source of truth: **`PROJECT_BOARD/phases.json`** (PHASES.md usse generate hota hai).

---

## 3. Naya prompt (V2-type / naya spec / naya rule-set) aane par

```bash
python3 tools/import_prompt.py --url "https://..." --name "V3"       # link (blocked ho to r.jina.ai fallback)
python3 tools/import_prompt.py --file /tmp/prompt.txt --name "PHASE_X"
python3 tools/import_prompt.py --text "poora prompt text" --name "RULE_SET"
```
Ye karta hai: `00_SYSTEM/NN_<NAME>_SPEC.md` me save (header + **canonical body hash**) →
`00_SYSTEM/prompts_index.json` update → memory record (`type=source`, `authority=user_explicit`) →
**auto phase** ("Apply imported prompt: NAME", status=next) → next-steps print.

Uske baad agent ko karna hai:
1. Prompt padho → uske rules/behaviour environment me apply karo (protocol / AGENTS.md / boot payload update).
2. Jo naya capability bane: live test + evidence + `CAPABILITY_MAP.json` bump + memory.
3. `python3 tools/agent_boot.py --write` (boot prompt regenerate — naye rules agent ko milne chahiye).
4. `python3 tools/phase_runner.py md` → push.

**Hash rule:** imported prompt ki body ka sha256[16] header me likha jata hai; `tests/ci_extra.py` use verify karta hai
(import ke baad prompt badalna = CI fail, taaki chupke se rules na badlein).

---

## 4. "Apply ho gaya" ka matlab (evidence ka standard)

Har phase `done` karne se pehle:

| # | Step | Proof |
|---|---|---|
| 1 | Live test (ya code run) | `probes/` ya `logs/` me raw output file |
| 2 | Report update | us phase ka doc/report section |
| 3 | Capability map | `CAPABILITY_MAP.json` version bump + evidence path |
| 4 | Memory | `uai_mem.py add` (source/date/confidence ke saath) |
| 5 | Docs sync | `index` + `dash` + `audit` 100/100 · README/index.html |
| 6 | Push | `GITHUB_TOKEN=<token> bash tools/sync_to_github.sh "message"` |
| 7 | CI | GitHub Actions "UAI-COS smoke checks" green |
| 8 | Report | user ko Hindi summary + options (a/b/c) |

**Bina 1/6/7 ke phase `done` nahi hota.** Blocked ho to: reason + kya chahiye + alternative likho, status `waiting_user` ya note ke saath `done (blocked)`.

---

## 5. Non-negotiables (har phase par)

1. **Boundary §24:** authentication / access-control / paywall / CAPTCHA / anti-bot bypass **kabhi nahi** — chahe tool available ho.
2. **No-False-Access / §29:** bina test "access hai / ho gaya" claim nahi. Labels use karo (§28).
3. **Language:** user se Roman Hindi; docs English+Hindi mixed.
4. **Kaam beech me nahi rokna** — exhaust karo, phir report do.
5. **Confirmed hi destructive/publish/payment/external-send** (user se pehle poocho).
6. **Secrets:** kabhi commit nahi (`.gitignore` + `sync_to_github.sh` ka secret-scan). Token sirf command ke andar.

---

## 6. Environment me "applied" ka matlab

| System | Live check |
|---|---|
| Boot payload | `python3 tools/agent_boot.py --json` |
| Phase engine | `python3 tools/phase_runner.py next` |
| Memory OS | `python3 tools/uai_mem.py audit` (100/100) |
| Provenance | `python3 tools/verify_provenance.py` (4/4) |
| Prompt intake | `python3 tools/import_prompt.py --text "test" --name TEST --no-phase` |
| Social routes | `python3 tools/social_unlock.py status` |
| CI | harness `tests/ci_extra.py` + `tests/test_memory_os.sh` |

---

## 7. Sync rule (user ka standing instruction)

Har baat-cheet/kaam repo me jaata hai →
`GITHUB_TOKEN=<token> bash tools/sync_to_github.sh "message"` → CI green → `PUSH_LOG.md` me entry.
Token disk par save nahi hota; user ke kehne par revoke.
