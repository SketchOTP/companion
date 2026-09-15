# Architect Review 25 — Alpha50-002 Partial Accepted; Live Integrated Alpha Still Required

## Disposition

**CONTINUE — `COMPANION-ALPHA50-002` PARTIAL ACCEPTED.**

The fixed-point V2 organism correction and resident V2 plumbing are retained as bounded implementation evidence. The integrated Alpha50 milestone is **not accepted**. Roadmap Phase 02 remains unaccepted. PR #9 stays draft/open/unmerged and Issue #8 remains open.

Next directive: `COMPANION-ALPHA50-003-LIVE-001`.

Notion authority: https://app.notion.com/p/3dc833cb27ff8128a1f8cb920146a791

## Authority sync

- Architect `main` at review start: `b42ec6d242fe0f0927d13bcd18b4b26d3adba215`.
- Candidate executable head: `70b2a5ca51a7c8adb688a97e42243f88c36cc5fc`.
- Candidate publication head: `3d05123f9d1c04a9605f12fc6e42ed4c585ca88b`.
- PR #9: draft/open/unmerged at publication head.
- Issue #8: open.
- Alpha50, Phase 01, focused R06, and retained Phase 02 exact-head **push** workflows are green on `70b2a5c...`.
- Alpha artifact `10387094480` is bound to `70b2a5c...`; independently downloaded ZIP SHA-256 matches `d032bc5e436a470c40f43e337e6eaa49fc83e7e60d71c7babde18d6286f95395`.
- `70b2a5c...` → `3d05123...` is one documentation-only commit changing `.agent/CURRENT.md`, `.agent/INDEX.md`, `.agent/OUTCOMES.md`, and the Alpha50-002 implementation record.
- Frozen R06 pack identity remains `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.

## Retain from Alpha50-002

Retain as bounded candidate implementation:

- `organism_v2` milli-integer representation for canonical physiology, drive urgency/inhibition, confidence/stress and skill stability;
- deterministic V2 action scoring which actually consumes learned outcome and preference state;
- bounded V2 action-result effects on confidence/stress and skill state;
- resident `companion-core` V2 restore → optional preference-memory update → action selection → body-neutral-intent event → V2 snapshot path;
- V2 schema/fixture and schema-validation regression;
- corrected fail-closed scanner self-test using an available Python implementation;
- exact executable-head push-CI separation from later documentation publication;
- graceful V2 restart/identity-continuity evidence;
- all previously accepted Phase 01 and C06 evidence.

These advances supersede Review 24's floating-point canonical-state defect. They do **not** establish the complete Alpha50 acceptance boundary.

## Material defects / incomplete acceptance evidence

### 1. Alpha qualification is still predominantly V1

The published artifact is labeled `COMPANION_ALPHA50_ORGANISM_MEMORY_V2`, but `alpha50_qualification` still performs its 30-day simulation, backup/restore, 500 serialization restarts, memory-class declaration, preference/correction/commitment checks and most causal flags using `OrganismState` V1. V2 receives a narrow fixed-point learned-outcome check.

Therefore the broad artifact label is not evidence that organism/memory Alpha qualification has moved to V2.

### 2. V2 canonical schema is not yet fully fail-closed

`organism-state-v2.schema.json` constrains internal fixed-point fields, drives and skills, but `goals`, `commitments`, and `memories` remain generic arrays and `last_intent` remains a generic object. The complete canonical state contract is therefore under-specified.

The resident V2 path also reuses `BodyNeutralIntent.intent_sequence: u64`; the accepted common signed-64 Rust/Godot wire ceiling must be explicitly carried into the organism-generated intent contract before live Godot integration.

### 3. V1-store discovery used the wrong search boundary

The result states that no **repository-located** lived/non-test V1 store was found. Architecture v1.0 intentionally places canonical stores outside the repository under XDG local-host paths. Before any V1→V2 activation/migration decision, actual configured/default XDG authority roots must be inspected read-only. Do not destructively migrate any potentially lived state.

### 4. Ordinary observation remains a runtime-file side channel

Alpha life mode reads `ordinary-observation.json` directly from the runtime directory. This proves resident method integration but not the architecture-required authorized ordinary producer/sensor-gateway → companion evidence boundary with freshness, provenance, replay and causation semantics.

The existing sensor-gateway sequenced-packet path remains care-directed safety transport. The Alpha must add or reuse a separately authenticated ordinary evidence boundary without routing safety through companion.

### 5. Required learning causality is not closed in V2 production

V2 learned outcomes and preferences now affect scoring in unit-level implementation, which is retained. However:

- correction-caused changed behavior is still only demonstrated by V1 history preservation, not V2 paired behavior;
- unfinished-commitment evidence is still primarily V1 and not a paired V2 production trace;
- preference/outcome causal checks have not been run through the resident ordinary-input → body execution → result → restart path;
- goals do not yet perform production proposal/arbitration;
- developmental promotion and evidence-bound consolidation remain incomplete.

### 6. The production remembered-interaction loop remains open

There is no accepted evidence chain:

`authorized ordinary evidence → companion V2 memory/state → body-neutral intent → real Godot → observed result → companion V2 outcome learning → durable snapshot → restart → remembered evidence changes later production action`.

The Godot bridge still provides foundation handshake/state behavior rather than this full typed intent/result exchange.

### 7. Transition qualification remains Python-owned proxy evidence

The 10,000-case artifact is unchanged from Alpha50-001 (`transitions.json` SHA-256 `c246e3ed...`). It is produced by the hard-coded Python resolver and executes no production Godot transition director. It does not close Phase 02 legal routing.

### 8. Long-horizon and failure evidence remain below the directive

The artifact's 30-day and most organism evidence remain V1 shallow stepping.

The 500-case failure artifact is still orderly process startup → ready/snapshot → SIGTERM → restart, with identity continuity. It is useful graceful-restart evidence but not a seeded multi-class pre/during/post-commit failure campaign.

### 9. Care process-loss independence remains inherited smoke

`care.json` is the retained direct-care smoke artifact. It does not execute the required kill-companion candidate delivery and kill-care ordinary-life/degraded-coverage sequence.

### 10. Capability matrix still overstates embodiment authority

The updated matrix correctly narrows vault, security and care boundaries, but `embodiment_habitat` remains `accepted-by-existing-authority`. Phase 02 is not accepted. Only the bounded accepted C06 runtime/controller/render/timing evidence may carry accepted status.

### 11. Physical target blockers remain legitimate blockers, not failures of independent software work

Hosted CI observed no webcam/audio devices, and dedicated Openbox target endurance remains unavailable without prohibited reconfiguration. Preserve those as explicit host blockers. They do not justify stopping independently executable live-service, Godot-headless, failure, memory or care-independence work.

## Capability boundary after Review 25

Accepted authority remains:

- Architecture v1.0;
- Roadmap Phase 01;
- bounded C06 frozen-art/controller/render/timing closeout.

Newly retained bounded Alpha implementation includes:

- fixed-point V2 organism numerical state direction;
- V2 preference/outcome-aware action-scoring implementation;
- resident V2 restore/step/snapshot and local preference-memory plumbing;
- V2 graceful restart continuity;
- corrected Alpha scanner and exact-head workflow evidence.

Not accepted yet:

- full organism autonomy;
- V2 autobiographical memory lifecycle as a complete production subsystem;
- learning/development capability;
- resident remembered-action vertical slice;
- Phase 02 legal transitions/endurance;
- sensor perception/speech;
- care efficacy/process-loss qualification;
- release/security/reliability claims.

## Completion estimate

Review 25 sets evidence-grounded overall completion to **35%**.

This supersedes Review 24's 31%. The increase reflects the canonical fixed-point V2 correction and real resident V2 integration. It remains below 50% because the central continuous-individual causality, production Godot routing, real multi-class failure behavior and care process-loss independence are still unproven.

If `COMPANION-ALPHA50-003-LIVE-001` fully closes the central software boundary and passes independent review, the intended Architect assessment range is approximately **50–55%**, even if genuinely unavailable physical webcam/microphone/Openbox resources remain explicit host blockers.

## Next action

Execute only `COMPANION-ALPHA50-003-LIVE-001` from current `main`. Its primary objective is to replace the remaining V1/proxy/file-side-channel evidence with one production V2 remembered-action loop and production-path transition/failure/care evidence.
