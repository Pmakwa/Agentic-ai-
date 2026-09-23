#!/usr/bin/env bash
# seed_initial_memory.sh — UAI-COS v2.0 ko boot karne ke liye initial memory bootstrap.
# Ye script CLI ke zariye hi records daalti hai (taaki governance validation bhi test ho).
# Idempotent nahi hai: dobara chalane par duplicate detector record skip kar dega.
set -u
cd "$(dirname "$0")/.."
MEM="python3 tools/uai_mem.py"
D="2026-09-23"

echo "== CORE =="
$MEM add --type core --status active --confidence high --authority user_explicit \
  --source user_instruction --ref "chat:$D" --domain ai-systems --tag goal --tag governance \
  --statement "User ka long-term goal: ek governed, memory-aware, multi-agent AI operating system chalana (UAI-COS), jisme memory verify hoti hai aur blind use nahi hoti." \
  --detail "V1 part 1-15 + V2 spec (112 sections) isi goal ka product hai. Isliye har bade task me: memory-first, verify-before-trust, audit-before-release." \
  --note "seeded from imported V1/V2 spec"

echo "== PREFERENCES =="
$MEM add --type preference --status verified --confidence high --authority user_explicit \
  --source user_instruction --ref "V1 PART 14" --verified "$D" --domain communication --tag language \
  --statement "User se Hindi me baat karni hai, lekin English alphabet/spelling (Roman Hindi) me — jab tak user khud Devanagari ya doosri language na maange." \
  --applies-when "har conversation turn" \
  --note "Part 14 current preference layer"

$MEM add --type preference --status verified --confidence high --authority user_explicit \
  --source user_instruction --ref "V1 PART 14" --verified "$D" --domain communication --tag style --tag depth \
  --statement "User ko detailed, advanced, master-level aur practical output chahiye; basic ya generic answer nahi." \
  --applies-when "har deliverable" --note "Part 14: professional/master-level output preference"

$MEM add --type preference --status active --confidence medium --authority user_explicit \
  --source user_instruction --ref "V1 PART 14" --domain image-generation --tag image --tag quality \
  --statement "Image prompts me high quality, photorealism, accurate details aur professional finishing rakhni hai." \
  --applies-when "jab user image ya image-prompt maange" \
  --note "medium confidence: purane task context se aayi hai, per-task confirm karna behtar hai"

$MEM add --type preference --status active --confidence medium --authority user_explicit \
  --source user_instruction --ref "V1 PART 14" --domain image-generation --tag image --tag constraint \
  --statement "Jab product-only image maangi gayi ho to image prompt me model, character, haath ya body parts add nahi karne." \
  --applies-when "product-only image / catalogue shot" \
  --does-not-apply-when "user ne lifestyle shot ya model ke saath shot maanga ho" \
  --conflict-key "image.product_only.no_human"

$MEM add --type preference --status active --confidence medium --authority user_explicit \
  --source user_instruction --ref "V1 PART 14" --domain image-generation --tag prompt-architecture \
  --statement "Specific image prompt aur universal quality prompt ko alag-alag rakhna hai (mix nahi karna)." \
  --applies-when "image prompt building"

$MEM add --type preference --status verified --confidence high --authority user_explicit \
  --source user_instruction --ref "V1 PART 14 + user msg $D" --verified "$D" --domain communication --tag priority \
  --statement "Latest user instruction ko purani instruction/memory ke upar priority milegi (current instruction pehle)." \
  --applies-when "jab purani preference aur nayi instruction aapas me takrayen"

$MEM add --type preference --status active --confidence high --authority user_explicit \
  --source user_instruction --ref "V1 PART 15 rule 12" --domain communication --tag verbosity \
  --statement "Chat me internal agent complexity/process dikhane ki zaroorat nahi — jab tak user khud mind-map, agent architecture, memory log ya audit na maange." \
  --applies-when "normal answer" --does-not-apply-when "user ne audit/log/architecture maanga ho"

echo "== CONSTRAINTS =="
$MEM add --type constraint --status verified --confidence high --authority user_explicit \
  --source user_instruction --ref "V1 reality rule" --verified "$D" --tag memory --tag honesty \
  --statement "Permanent ya unlimited memory ka claim nahi karna, jab tak real storage + retrieval + version control + governance available na ho." \
  --detail "Is workspace me memory actually disk par persist hoti hai (memory/store/memory.jsonl) — lekin phir bhi 'unlimited/permanent' jaisa jhootha claim nahi karna."

$MEM add --type constraint --status verified --confidence high --authority user_explicit \
  --source user_instruction --ref "V1 PART 4 / V2 #17-21" --verified "$D" --tag memory \
  --statement "Memory ko blindly use nahi karna — sirf keyword match ke basis par retrieve nahi karna; scope + authority + freshness + confidence + current instruction dekh kar use karna."

$MEM add --type constraint --status verified --confidence high --authority user_explicit \
  --source user_instruction --ref "V2 #10, #49" --verified "$D" --tag safety --tag approval \
  --statement "High-risk ya irreversible action (delete, publish, payment, external send) se pehle user confirmation lena compulsory hai."

echo "== PROCEDURAL =="
$MEM add --type procedural --status verified --confidence high --authority user_explicit \
  --source user_instruction --ref "V2 #107 master system loop" --verified "$D" --domain ai-systems --tag workflow --tag boot \
  --statement "Session boot protocol: memory/INDEX.md padho -> task classify karo -> sirf relevant memory filter karo -> plan banao -> execute -> quality gate -> respond -> memory update." \
  --detail "UNDERSTAND -> CLASSIFY -> RETRIEVE -> FILTER -> PLAN -> ASSIGN -> VERIFY -> EXECUTE -> AUDIT -> CORRECT -> APPROVE -> RESPOND -> LEARN"

$MEM add --type procedural --status verified --confidence high --authority user_explicit \
  --source user_instruction --ref "V2 #13 memory record schema" --verified "$D" --domain ai-systems --tag memory \
  --statement "Har memory record me source, scope, confidence, authority, status, timestamps aur history bharni hi hogi — warna record candidate bhi nahi banega."

$MEM add --type procedural --status active --confidence high --authority derived \
  --source agent_inference --ref "workspace capability" --domain ai-systems --tag workspace \
  --statement "Is environment me bada output file ke roop me workspace me save karo, aur chat me uska concise summary + path do." \
  --detail "Workspace files turn ke baad bhi persist karti hain, isliye deliverable files = durable memory."

echo "== EPISODIC / SOURCE / ERROR =="
$MEM add --type episodic --status verified --confidence high --authority user_explicit \
  --source user_instruction --ref "chat $D" --verified "$D" --tag milestone \
  --statement "$D: User ne ChatGPT share link diya (V2 prompt) — spec import kiya, is workspace me UAI-COS v2.0 implement kiya (memory store + CLI + agents + step-2 docs)." \
  --detail "Link: https://chatgpt.com/share/6ab02379-e58c-83ee-b573-63caedeca943"

$MEM add --type source --status verified --confidence high --authority verified_source \
  --source url --url "https://chatgpt.com/share/6ab02379-e58c-83ee-b573-63caedeca943" --ref "share id 6ab02379" \
  --verified "$D" --tag provenance \
  --statement "UAI-COS V1 (22.7k chars) aur V2 (44.3k chars, 112 sections) ka original source: shared ChatGPT chat 'System Dekho Dhyan Se'." \
  --detail "Files: 00_SYSTEM/00_UAI-COS_V2.0_SPEC.md, 00_SYSTEM/01_UAI-COS_V1.0_SPEC.md, 00_SYSTEM/IMPORT_LOG.md"

$MEM add --type error --status verified --confidence high --authority verified_source \
  --source tool_result --ref "curl $D" --verified "$D" --tag scraping --tag cloudflare \
  --statement "chatgpt.com share/backend-api direct fetch -> HTTP 403 (Cloudflare). Fix: r.jina.ai reader proxy se content mila." \
  --detail "Prevention: shared ChatGPT conversations ke liye pehle reader proxy try karo; direct curl par 403 ko failure na maan kar fallback maango."

echo "== PROJECT / DECISION =="
$MEM add --type project --status active --confidence high --authority user_explicit \
  --source user_instruction --ref "user msg $D" --domain ai-systems --project uai-cos --tag active \
  --statement "Project UAI-COS-WORKSPACE v2.0: spec + file-backed memory OS + agent registry + step-2 implementation docs is workspace me live hain." \
  --detail "Root: /home/user/uai-cos — dekho README.md, memory/INDEX.md, DASHBOARD.html"

$MEM add --type decision --status active --confidence high --authority user_explicit \
  --source user_instruction --ref "user msg $D, step 1" --tag architecture \
  --statement "V2 spec ko canonical maana gaya; V1 base version history ke liye alag rakha gaya (user ne 'prompt ko pura le lo' kaha tha)." \
  --note "Section 39 version control: V1 = superseded-by-design, delete nahi kiya"

$MEM add --type decision --status active --confidence medium --authority derived \
  --source agent_inference --ref "engineering choice $D" --tag storage \
  --statement "Memory store ke liye JSONL choose kiya (append-friendly, git-friendly, zero dependency); vector/embedding retrieval future upgrade hai." \
  --detail "Rejected: SQLite (dependency + merge conflicts), pure markdown (query/validation mushkil)."

$MEM add --type decision --status active --confidence high --authority derived \
  --source agent_inference --ref "step 2 plan $D" --tag roadmap \
  --statement "Step 2 = implementation layer: roadmap + user scenarios + memory-type integration + agent lifecycle + evaluation/regression (yahi 3 cheezein source chat me next-step ke roop me offer hui thi)."

echo "== WORKING =="
$MEM add --type working --status active --confidence high --authority user_explicit \
  --source user_instruction --ref "current turn" --expires "2026-09-30" --tag current-task \
  --statement "Current task: V2 prompt ko workspace me apply karna + step-2 implementation layer banana." \
  --detail "Is turn ke baad ye working memory expire ho sakti hai; project memory me promote karna hai agar user continue kare."

echo
$MEM stats
