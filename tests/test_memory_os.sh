#!/usr/bin/env bash
# test_memory_os.sh — UAI-COS v2.0 regression suite (Section #55 golden tests, #56 regression prevention)
#
# Ye suite memory OS ke governance rules ko TOD kar dekhti hai — happy path nahi, *rules* test hote hain.
# Har test isolated store par chalta hai (UAI_STORE env var), isliye live memory ko chhoota nahi.
#
# Run: bash tests/test_memory_os.sh
set -uo pipefail
cd "$(dirname "$0")/.."

PASS=0; FAIL=0
SB=$(mktemp -d)
export UAI_STORE="$SB/memory.jsonl"
export UAI_ARCHIVE="$SB/archive.jsonl"
export UAI_INDEX="$SB/INDEX.md"
export UAI_DASH="$SB/DASHBOARD.html"
export UAI_AUDIT_LOG="$SB/AUDIT_LOG.md"
MEM="python3 tools/uai_mem.py"

ok()   { PASS=$((PASS+1)); printf "  \033[32mPASS\033[0m  %s\n" "$1"; }
bad()  { FAIL=$((FAIL+1)); printf "  \033[31mFAIL\033[0m  %s\n" "$1"; }
head_() { printf "\n\033[1m%s\033[0m\n" "$1"; }

expect_exit() { # expect_exit <expected_code> <label> <cmd...>
  local exp="$1"; local label="$2"; shift 2
  out=$("$@" 2>&1); code=$?
  if [[ "$code" == "$exp" ]]; then ok "$label (exit=$code)"; else bad "$label (expected exit=$exp, got=$code)"; printf "        %s\n" "$(echo "$out" | tail -2)"; fi
}

# ---------------------------------------------------------------- G-01 schema governance
head_ "G-01  Governance validation (Section #13, #0.7)"
expect_exit 2 "high-confidence 'semantic' fact bina source -> BLOCKED" \
  $MEM add --type semantic --confidence high --status verified --authority agent_inference \
        --source agent_inference --statement "Duniya flat hai"
expect_exit 0 "high-confidence fact verified source ke saath -> ALLOWED" \
  $MEM add --type semantic --confidence high --status verified --authority verified_source \
        --source url --url "https://example.com/fact" --statement "Python 3.13 me free-threading option hai" --tag global
expect_exit 2 "invalid confidence band -> BLOCKED" \
  $MEM add --type preference --confidence "definitely_true" --source user_instruction --statement "test"

# ---------------------------------------------------------------- G-02 duplicate
head_ "G-02  Duplicate detection (Section #19 dedupe)"
$MEM add --type preference --status active --confidence high --authority user_explicit \
     --source user_instruction --statement "Client billing GST format me chahiye" >/dev/null
expect_exit 3 "same statement dobara -> DUPLICATE (skip)" \
  $MEM add --type preference --status active --confidence high --authority user_explicit \
        --source user_instruction --statement "client billing gst format me chahiye"

# ---------------------------------------------------------------- G-03 conflict engine
head_ "G-03  Conflict engine (Section #21)"
$MEM add --type preference --status active --confidence high --authority user_explicit \
     --source user_instruction --statement "Answer hamesha English me do" --conflict-key language.answer >/dev/null
$MEM add --type preference --status active --confidence high --authority user_explicit \
     --source user_instruction --statement "Answer hamesha Hindi me do" --conflict-key language.answer >/dev/null
conf=$(python3 - <<'PY'
import json,os
rows=[json.loads(l) for l in open(os.environ["UAI_STORE"],encoding='utf-8')]
print(sum(1 for r in rows if r["status"]=="conflicted"))
PY
)
[[ "$conf" == "2" ]] && ok "conflict par dono records 'conflicted' hue (count=$conf)" || bad "conflict par conflicted count galat ($conf, expected 2)"

# ---------------------------------------------------------------- G-04 supersede chain
head_ "G-04  Supersede chain, no data loss (Section #39, #87)"
old=$($MEM list --type semantic --status verified --confidence high 2>/dev/null | awk '/MEM-SEM/{print $1}' | head -1)
$MEM add --type semantic --status verified --confidence high --authority user_explicit \
     --source user_instruction --statement "Python 3.14 me free-threading default ho sakta hai" >/dev/null
new=$($MEM list --type semantic 2>/dev/null | awk '/MEM-SEM/{print $1}' | tail -1)
$MEM supersede "$old" "$new" --note "naya version" >/dev/null
chk=$(OLD="$old" NEW="$new" python3 - <<'PY'
import json,os
rows={json.loads(l)["id"]:json.loads(l) for l in open(os.environ["UAI_STORE"],encoding='utf-8')}
old,new=os.environ["OLD"],os.environ["NEW"]
ok = rows[old]["status"]=="superseded" and rows[old]["superseded_by"]==new and rows[new]["supersedes"]==old and len(rows[old]["history"])>=2
print("yes" if ok else "no")
PY
)
[[ "$chk" == "yes" ]] && ok "purani record superseded + bidirectional link + history intact ($old -> $new)" || bad "supersede chain toot gayi"

# ---------------------------------------------------------------- G-05 expiry engine
head_ "G-05  Expiry engine (Section #20)"
$MEM add --type temporal --status active --confidence high --authority user_explicit \
     --source user_instruction --statement "Ye info sirf kal tak valid hai" --expires "2020-01-01" >/dev/null
$MEM expire >/dev/null
expired=$(python3 - <<'PY'
import json,os
rows=[json.loads(l) for l in open(os.environ["UAI_STORE"],encoding='utf-8')]
print(sum(1 for r in rows if r["status"]=="expired"))
PY
)
[[ "$expired" -ge 1 ]] && ok "past expiry wali record auto-expire hui (count=$expired)" || bad "expiry engine kaam nahi kiya"

# ---------------------------------------------------------------- G-06T8 health audit detections
head_ "G-06  Health audit detection powers (Section #79, #80)"
$MEM add --type working --status active --confidence high --authority user_implied \
     --source agent_inference --statement "Purani working memory (stale)" --force >/dev/null 2>&1
python3 - <<'PY' >/dev/null
import json,os,datetime
p=os.environ["UAI_STORE"]
rows=[json.loads(l) for l in open(p,encoding='utf-8')]
for r in rows:
    if r["type"]=="working":
        r["created_at"]=(datetime.date.today()-datetime.timedelta(days=30)).isoformat()+"T10:00:00"
open(p,'w',encoding='utf-8').write("\n".join(json.dumps(r,ensure_ascii=False) for r in rows)+"\n")
PY
$MEM add --type preference --status active --confidence high --authority user_explicit \
     --source user_instruction --statement "Scope ke bina preference (flag hona chahiye)" >/dev/null
$MEM add --type preference --status verified --confidence low --authority agent_inference \
     --source agent_inference --statement "Verified par low confidence (flag hona chahiye)" >/dev/null
$MEM add --type constraint --status active --confidence high --authority user_explicit \
     --source user_instruction --statement "Private data shared tag ke saath (privacy leak risk)" --sensitivity private --tag shared >/dev/null
$MEM add --type preference --status verified --confidence high --authority user_explicit \
     --source user_instruction --statement "Global scope declare kiya hua preference (flag NAHI honi chahiye)" --tag global >/dev/null

audit_out=$($MEM audit --working-ttl 7 || true)
for k in stale_working_memory unscoped_preference verified_but_low_conf privacy_leak_risk; do
  if grep -q "\[$k\]" <<<"$audit_out"; then ok "audit ne '$k' detect kiya"; else bad "audit ne '$k' miss kiya"; fi
done
if python3 -c "
import sys
sys.exit(0 if 'global scope declare' not in open('$UAI_STORE',encoding='utf-8').read() else 0)"; then :; fi
if grep -q "global scope declare" <<<"$audit_out"; then bad "global-tag wali preference ko galti se flag kiya"; else ok "global-tag wali preference flag nahi hui (correct scope handling)"; fi

# ---------------------------------------------------------------- G-07T9 retrieval + artifacts
head_ "G-07  Retrieval & artifacts (Section #17, #73, #77)"
$MEM search "billing" >/dev/null && ok "search command chalti hai" || bad "search fail"
$MEM index >/dev/null && [[ -f "$UAI_INDEX" ]] && ok "INDEX.md generate hui" || bad "index generate nahi hui"
$MEM dash  >/dev/null && [[ -f "$UAI_DASH"  ]] && grep -q "Memory Dashboard" "$UAI_DASH" && ok "DASHBOARD.html generate hui aur valid hai" || bad "dashboard generate nahi hui"
[[ -f "$UAI_AUDIT_LOG" ]] && ok "AUDIT_LOG.md trail likha gaya" || bad "audit log missing"

# ---------------------------------------------------------------- G-08 command surface
head_ "G-08  Command surface integrity"
for sub in add list search show update supersede expire audit stats index dash export; do
  python3 tools/uai_mem.py "$sub" --help >/dev/null 2>&1 && ok "subcommand '$sub' available" || bad "subcommand '$sub' missing"
done

# ---------------------------------------------------------------- result
echo
echo "==============================================="
printf "  TOTAL: %d passed, %d failed\n" "$PASS" "$FAIL"
echo "==============================================="
rm -rf "$SB"
[[ "$FAIL" == 0 ]] && exit 0 || exit 1
