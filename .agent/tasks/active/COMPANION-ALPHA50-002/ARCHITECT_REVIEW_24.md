# Architect Review 24 — Alpha50 Partial Accepted; Live Causality Closeout Required

## Disposition

**CONTINUE — COMPANION-ALPHA50-001 PARTIAL ACCEPTED.**

The Alpha50 candidate is a substantial implementation advance, but it does not satisfy the integrated Alpha50 acceptance boundary. Retain the real Rust organism/memory substrate, companion-owned SQLite snapshot/backup path, bounded restart evidence, sensor degradation evidence, direct-care regression, and all accepted Phase 01/C06 work. Correct the material architecture and evidence defects below before Alpha50 acceptance.

Phase 02 remains unaccepted. PR #9 remains draft/open/unmerged. Issue #8 remains open.

Notion Review 24: https://app.notion.com/p/3dc833cb27ff8100bedfe20475bc031c

Reviewed candidate head: `1f37388bb50f9a96ea086676f80075f5e7a64b9f`.

Pre-review Architect main: `1ab2f168d70d7b48e9e213061404e5a2cdb84339`.

Alpha artifact: `10374764939`, SHA-256 `bd2476c0049e140988809519ab664ce9f918345c7ac94dcc4e9beb5031bd8df2`.

## Independent evidence findings

### Retained candidate capability

Retain as bounded implementation evidence:

- real Rust `OrganismState` and model-independent authority placement;
- explicit internal variables, drive calculations and body-neutral intent types;
- typed memory vocabulary, provenance fields, correction/supersession representation, abstaining retrieval, commitment lifecycle and skill records;
- companion-owned organism snapshots in the accepted SQLite authority store while the event log remains separate evidence;
- SQLite Backup API and clean-root restore mechanism;
- resident `companion-core` opt-in restore → step → event → snapshot execution;
- 500 repetitions of graceful process restart/identity continuity as bounded restart evidence;
- model-free qualification, explicit hosted sensor degradation, and retained direct-care smoke;
- frozen R06 pack identity and accepted C06 regression evidence.

### Material defect 1 — canonical numeric state violates Architecture v1.0

Canonical physiology, drive urgency/inhibition, and skill stability are Rust `f32` and JSON `number`. Architecture v1.0 requires canonical organism/drive values to use bounded integers, fixed-point integers with declared units/scales, or canonical decimal strings where needed. Canonical truth may not depend on platform floating-point serialization.

`organism-state-v1` is therefore candidate-only and is not an accepted canonical persistence format.

### Material defect 2 — learning-to-action causality is incomplete

`record_action_outcome()` updates counters and skill stability/stage, but `select_action()` does not consume learned outcomes or skill mastery. The qualification proves a counter changed, not that learning changed later behavior.

`correct_memory()` preserves and supersedes history but does not alter action policy. Its current test proves correction history, not correction-caused later behavior.

`record_interaction()` hard-codes `learned_preferences["default"] = "acknowledge"` irrespective of the passed preference content. This is a qualification shortcut rather than grounded preference learning.

### Material defect 3 — goals, development and consolidation are mostly structural

Goals are not actually proposed/arbitrated into behavior. Developmental stage/capability gates lack evidence-based promotion logic. Consolidation currently counts episodic records and checks a narrow dream invariant, but does not establish the required episode closure, contradiction/generalization proposal flow, preference/skill updates, curiosity generation, or unfinished-goal carry-forward.

### Material defect 4 — production remembered-interaction chain is not connected

Resident `companion-core` can restore/step/snapshot and append a body-neutral-intent event, but it does not deliver that intent through the accepted bridge to Godot or consume a Godot execution result.

The ordinary-observation path appends raw observation JSON to the event log but does not pass it through the organism/memory update path. The qualification binary calls organism methods directly instead.

Thus the required chain remains unproven:

`ordinary evidence → organism update → typed memory → action selection → Godot execution → observed result → outcome/learning update → durable snapshot → restart → memory-altered future action`.

### Material defect 5 — transition qualification remains a Python proxy

`alpha50_transition_qualification.py` owns a hard-coded `LEGAL` table and executes no production Godot resolver. It does not establish runtime role inventory, authored interruption ranges, observed connector playback, production routing, or real path recovery.

### Material defect 6 — 30-day simulation is insufficient

The 30-day test is a sequence of simple `step()` calls on a fresh deterministic organism with a user-presence pattern. It does not exercise memory accumulation, commitments, outcome feedback, development, sleep/recovery, goal resumption, or consolidation over the simulated period.

### Material defect 7 — failure campaign is graceful restart evidence only

The 500-case campaign waits for a durable snapshot, sends SIGTERM, restarts, waits for another snapshot, then sends SIGTERM. It does not exercise seeded pre/during/post-commit SIGKILL points, interrupted backup, corrupt-store handling, supervisor loss, Godot loss, care loss, or other required failure classes.

### Material defect 8 — shadow-care independence remains inherited smoke

The current Alpha result reuses direct-care smoke but does not execute the required kill-companion safety path and kill-care ordinary-companion/degraded-care path.

### Material defect 9 — workflow semantics need correction

- PR workflows checked out synthetic merge commit `0fc80fb758f95e936fbcfb211e10d3cfa3a908f3`; its tree exactly equals candidate head `1f37388...` tree, so current evidence is exact-tree, not exact-commit.
- the Alpha workflow uses `! rg ...` for the secret scan. Hosted logs show `rg` is unavailable; command-not-found is therefore inverted into success. Scanner absence must fail closed.

### Material defect 10 — capability matrix overstates existing acceptance

`embodiment_habitat`, `care_shadow_path`, `identity_consent_vault`, and `security_resilience` are marked `accepted-by-existing-authority` too broadly. Accepted foundations/stubs and bounded C06 evidence are not equivalent to accepted product capability in those domains.

## Completion disposition

The previous 9% estimate is superseded because real persistent-organism and typed-memory implementation now exists. However, the evidence does not justify the Alpha50 target of 50% because the central memory-to-action/Godot/result causality chain is not yet implemented and several qualification claims are proxies.

Current Architect estimate after partial acceptance: **31%**.

If `COMPANION-ALPHA50-002` fully passes independent review, the intended Architect range is approximately **50–55%** without falsely claiming semantic vision, STT/TTS, live notification, pilot, or release capability.

# CODEX DIRECTIVE — COMPANION-ALPHA50-002

## Objective

Convert the Alpha50-001 substrate into one real production-causality Companion Alpha.

Correct the canonical organism format, make memory/correction/outcome learning genuinely affect later action, connect the resident ordinary-evidence → organism/memory → Godot → execution-result → learning loop across process restart, move legal transition authority into the production Godot path, and qualify real failure/care-independence behavior.

Return one final handoff. Do not stop at intermediate workstreams unless an Architecture v1.0 authority conflict or unavoidable new runtime dependency blocks the central objective.

## Why this is next

Alpha50-001 created the right structural pieces but too much acceptance evidence bypasses the resident production path. Current long-term-agent evaluation also emphasizes memory utilization in action, not merely successful storage or recall. The next decisive proof is a single causal chain that survives restart and remains valid without model workers.

## Authoritative basis

- Architecture v1.0 remains adopted.
- Phase 01 remains accepted.
- R06-C06 remains accepted.
- Review 24 partially accepts the Alpha50-001 implementation substrate only.
- R01 remains organism/autonomy/development authority.
- R02 remains memory/learning/consolidation authority.
- Frozen R06 source-pack SHA-256 remains `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.
- Candidate Alpha50-001 implementation head is `1f37388bb50f9a96ea086676f80075f5e7a64b9f`.

## Execution policy

Merge current `origin/main` normally into the existing task branch. Preserve accepted source pixels, C06 behavior, negative evidence, public history, and protected operator files.

Use existing Rust/Godot/SQLite/IPC infrastructure. No new runtime dependency is expected or authorized.

Do not create a separate test-only implementation of a rule that production code is supposed to own. Qualification may drive production code, but it may not duplicate the canonical decision logic in Python.

## Workstream A — canonical organism state V2

1. Supersede candidate `organism-state-v1` for canonical use. Preserve it as rejected/partial evidence; do not silently rewrite history.
2. Define a V2 canonical organism contract using bounded integer/fixed-point fields with explicit units/scales for all canonical physiology, drive, confidence/stress, utility, skill stability, and other canonical continuous values.
3. No canonical organism, drive, goal-ranking, learned value, or skill state may require floating-point serialization.
4. Arithmetic must be deterministic, overflow-bounded, and independently testable.
5. If noncanonical presentation/model adapters use floats, convert only at the boundary and never persist them as canonical truth.
6. Determine whether any non-test V1 organism store exists. If none exists, state that and start V2 cleanly. If a potentially lived/non-test V1 store exists, stop migration of that store and return to Architect before destructive conversion.
7. Add schema/Rust round-trip, boundary, overflow, canonicalization and tamper-negative tests.

## Workstream B — real organism dynamics and goal arbitration

1. Make elapsed organism time explicit and deterministic rather than equating loop iterations with time.
2. Provide bounded dynamics for energy/rest pressure/social need/engagement/curiosity/confidence/stress including satiation/recovery effects where applicable.
3. Actions must have observable consequences on relevant internal state; the organism must not monotonically decay into a terminal idle condition by construction.
4. Implement actual goal proposal and arbitration from drives, commitments, remembered opportunities and unfinished work.
5. Action-selection evidence must expose the winning causal terms and inhibited alternatives.
6. Commitments must support create/resume/complete/expire/revoke through production state transitions.
7. User absence must remove unavailable actions but allow coherent autonomous internal activity and goal continuation.

## Workstream C — causal memory, correction, learning and development

For each required case, implement a paired control where all state is identical except the target memory/learning evidence, then prove different selected behavior for the intended reason.

Required cases:

1. **Preference:** a grounded preference record changes later action or parameters. Do not hard-code a single action regardless of preference content.
2. **Correction:** corrected evidence changes later action compared with the pre-correction state while the superseded record remains historically preserved.
3. **Commitment:** an unfinished commitment changes later action compared with an otherwise identical organism without that commitment.
4. **Outcome learning:** prior action outcome/skill value changes later action selection or action parameters compared with an organism lacking that outcome evidence.

Additional requirements:

- learned action values/skill mastery must be consumed by production action selection;
- retrieval must enforce temporal validity, supersession, scope/privacy and confidence;
- conflicting current evidence must abstain;
- development capability promotion must require defined competence/stability evidence and fail if only time passes;
- add at least one development-gate negative;
- consolidation must operate on real typed records and produce explicit proposals for at least episode closure, contradiction/generalization, preference or routine, skill update, unfinished-goal carry-forward, and curiosity/question generation where evidence supports them;
- every promoted factual proposal must reference real evidence;
- synthetic dream/rehearsal material must remain synthetic and a tamper case attempting to promote it as an external event must fail.

## Workstream D — production ordinary-evidence → remembered-action loop

Implement the real resident path. No direct qualification calls to `record_interaction()` or equivalent may substitute for this acceptance proof.

Required path:

1. an authorized synthetic ordinary observation enters through the actual accepted ordinary producer/sensor-gateway boundary;
2. `companion-core` validates and appends canonical event evidence;
3. production organism logic updates internal state and typed memory from that evidence;
4. production action selection creates a typed body-neutral intent with causation/provenance;
5. that intent crosses the accepted bridge/IPC boundary to the real Godot body;
6. Godot resolves a legal presentation route using frozen runtime authority and executes it;
7. an observed execution result returns across the typed result boundary;
8. `companion-core` interprets the result, records outcome evidence, and updates relevant skill/learning state;
9. state is durably snapshotted;
10. terminate `companion-core` and Godot;
11. restart the same individual and body;
12. later ordinary context activates the remembered evidence;
13. paired-control evidence proves the memory changes the later production action.

Bind every step with correlation/causation identifiers. Preserve the distinction between event evidence, derived memory and presentation observation.

Kill Godot during a separate case and prove canonical organism/memory truth survives unchanged.

## Workstream E — production legal transitions in Godot

1. Remove Python ownership of the legal graph. Python may verify traces but may not define the production legality table.
2. Inventory all frozen track roles from accepted pack/source authority.
3. Implement the fail-closed legal graph in the production Godot presentation resolver/director or the already-accepted typed presentation routing layer, without moving organism authority into Godot.
4. Preserve the one accepted presentation clock.
5. If AnimationTree is used, pre-authorize the complete path before `travel()` so Godot's documented no-path teleport behavior cannot bypass legality.
6. Exercise actual authored track entry/exit facing/posture composition and declared interruption ranges.
7. Run at least 10,000 deterministic cases through the **real production resolver**, in a real Godot process. The cases may be accelerated/headless; every case need not render a PNG.
8. Retain case-level traces for start state, request, legal path/rejection, observed track sequence, terminal state and pack identity.
9. Render-observe at least one case for every material connector/edge class, interruption boundary class, illegal/no-path class and recovery class.
10. Independent verification must reconstruct legality from pack authority and traces, not runtime PASS booleans.
11. Required negatives: removed edge, injected all-pairs edge, connector-facing/posture mutation, interruption-range mutation, source/pack mutation, runtime-success/observed-path contradiction, and post-rejection recovery.

## Workstream F — meaningful 30-day autonomy qualification

Run 30 simulated organism days in an isolated qualification store. Simulation must never contaminate the lived/runtime store.

The run must include:

- alternating user-present/absent periods;
- multiple competing internal-state regimes;
- created/completed/expired/resumed commitments;
- ordinary evidence and memory accumulation;
- at least two corrections;
- action outcome feedback;
- skill progression;
- at least one valid and one rejected development promotion;
- rest/satiation cycles;
- consolidation cycles;
- unfinished-goal carry-over and later resumption;
- model-worker absence periods.

Report action distribution, drive-state distribution, goal churn, commitment outcomes, repetition, memory counts by class, correction/supersession outcomes, skill/development changes, consolidation proposals/rejections and unresolved contradictions.

This remains simulation evidence, not lived history.

## Workstream G — real seeded failure campaign

Keep graceful restart evidence but add a real retained deterministic failure matrix using isolated qualification stores.

At minimum cover seeded interruption at materially distinct points:

- before event transaction;
- during/after event append before organism snapshot;
- after snapshot before acknowledgement/result publication;
- during ordinary-evidence processing;
- during body-intent/result handling;
- companion SIGKILL;
- Godot loss;
- care-core loss;
- supervisor restart where supported by the accepted harness;
- model-worker absence;
- store unavailable;
- injected corrupt store;
- interrupted backup/restore where safely testable.

Do not convert process failure into success by blindly retrying. Classify retryable startup contention separately from domain correctness.

Verify no identity reseed, no duplicated canonical application, no silent lost commitment, no false-memory promotion, no cross-authority write, and explicit degraded/frozen behavior for unrecoverable corruption.

Retain at least 500 deterministic cases across the matrix, not 500 copies of one graceful restart scenario.

## Workstream H — independent care path

Execute the real accepted direct-care transport with process failures:

1. while `companion-core` is running, deliver a synthetic safety candidate directly to care and record a care-owned receipt/incident state;
2. kill/stop `companion-core`; deliver a new synthetic safety candidate; prove care still accepts/rejects it according to care authority without companion participation;
3. restore companion;
4. kill/stop `care-core`; prove ordinary companion life can continue while care coverage is explicitly degraded and no assistance claim is made;
5. restart care and prove coverage recovery without modifying companion memory/goals;
6. no real notification or external provider delivery.

## Workstream I — target hardware and Openbox

On the actual project Linux host, not GitHub-hosted CI, probe existing webcam, microphone and the authorized logical X screen/Openbox habitat without host reconfiguration.

If devices/display are accessible:

- acquire bounded real webcam frames and microphone samples through `sensor-gateway` with timing/quality metadata and ephemeral raw-media handling;
- run the dedicated 1366×768 Openbox two-hour endurance using one Godot process and one resident foundation/companion instance;
- retain exact target-host evidence.

If a particular target resource is genuinely unavailable without prohibited reconfiguration, preserve the exact blocker. Do not fabricate hosted evidence and do not stop independent workstreams.

No semantic vision, STT or TTS claim is authorized by low-level acquisition.

## Workstream J — evidence/CI corrections

1. Make the Alpha workflow secret scan fail if the scanner itself is absent. Either install/pin the scanner or use an already-guaranteed tool. Test the scanner with a synthetic forbidden fixture and a clean fixture.
2. For acceptance runs, prove the exact implementation commit is executed, or explicitly bind a PR merge commit to an identical Git tree and label evidence exact-tree rather than exact-commit. Prefer an exact-head push/workflow-dispatch run where practical.
3. Correct the capability matrix so foundation/stub acceptance is not mislabeled as accepted product capability.
4. Correct the Notion/GitHub Alpha report append-only: retain the original claims, then mark unsupported Alpha50-001 learning/transition/failure claims as bounded or superseded.
5. Artifact evidence must contain enough raw traces to independently check critical claims; summary JSON alone is insufficient for live transition, remembered interaction and failure-injection acceptance.

## Do not change

No new character art, cutout/recolor/resample/source reselection, cloud service, biometric system, notification provider, model-owned state, model-owned memory, model-owned transition legality, model-owned care decision, uncontrolled online weight training, Phase 03+ self-acceptance, PR #9 merge, or live external notification.

Do not weaken C06 or Architecture v1.0 to make the Alpha pass.

## Required validation

- V2 fixed-point organism schema + Rust + canonical round trips and numeric boundary negatives;
- drive/action satiation and goal-arbitration causal tests;
- paired-control preference/correction/commitment/outcome behavior tests;
- development promotion positive + time-only negative;
- retrieval temporal/supersession/scope/conflict tests;
- consolidation provenance + dream false-evidence tamper negative;
- full production remembered-interaction trace through real Godot and across restart;
- Godot-loss canonical-state survival;
- 10,000+ real production Godot transition cases plus rendered edge-class evidence;
- 30-day rich simulation in isolated store;
- 500+ retained seeded multi-class failure cases;
- kill-companion / kill-care independence campaign;
- Backup API + clean-root restore after meaningful memory/learning state exists;
- model-worker-outage resident life evidence;
- target webcam/mic/Openbox evidence where accessible;
- fail-closed secret scanner self-test;
- Phase 01 + C06/R06 + retained Phase 02 + Alpha50-002 regression on one final implementation tree.

## Acceptance boundary

Alpha50-002 is successful only if the central production chain is real and causally complete. Passing isolated unit tests or Python models cannot substitute for the required production traces.

If all central criteria pass, the Architect intends to treat the project as having crossed the 50% overall-completion threshold, subject to independent artifact/code review. Openbox or physical sensor unavailability may remain a bounded host blocker if every independent core Alpha criterion passes; it cannot be relabeled as passed.

## Prohibited claims

Do not claim semantic vision, STT, TTS, biometric identity, live care efficacy, external escalation, security certification, SLA/reliability, pilot/release readiness, or full project completion.

## Stop and return to Architect if

Stop only if:

- correcting canonical organism format requires destructive migration of potentially lived/non-test state;
- the production ordinary→organism→Godot→result chain cannot be implemented without an Architecture v1.0 authority change;
- an unavoidable new runtime dependency is central to the objective;
- accepted source art must change;
- target-host evidence would require prohibited reconfiguration;
- continuing would create multiple canonical writers or route safety through companion-core.

Otherwise continue and preserve negative evidence.

## Required project updates

Update `.agent/CURRENT.md`, `.agent/INDEX.md`, the Alpha task packet/capability matrix, append-only implementation records, Notion Alpha report, PR #9 and Issue #8. Preserve Review 23, Review 24 and Alpha50-001 evidence as history.

## Required handoff

Return exactly:

`# CODEX RESULT — COMPANION-ALPHA50-002`

with sections:

- Verdict
- Authority sync
- Protected work
- Baseline / merge / branch
- Alpha50-001 evidence reconciliation
- Canonical organism V2 and numeric migration disposition
- Organism dynamics and goal arbitration
- Preference/correction/commitment/outcome paired causality
- Development-gate evidence
- Memory retrieval/supersession/consolidation evidence
- Production ordinary-evidence → remembered-action → Godot → result trace
- Restart remembered-action trace
- Production Godot transition graph and 10,000-case campaign
- 30-day isolated rich simulation
- Seeded multi-class failure campaign
- Care-core independence campaign
- Model-worker outage
- Backup/export/clean-root restore
- Target webcam/microphone evidence or blockers
- Openbox endurance evidence or blocker
- Workflow/scanner/exact-tree corrections
- Exact final-tree CI
- Artifact identities and raw-trace hashes
- Corrected capability matrix
- Files changed
- Failures / blockers
- Notion / GitHub publication
- Commits / remote equality
- Recommendation

Then stop for Architect review.
