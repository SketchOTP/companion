# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

## Latest Architect disposition

Architect Review 18 partially accepts R06-C05. Retain the frozen R05 production selection, controller-owned `MonRoot` authority, true left/right profile selection, immutable source identity, nominal Godot translated playback, and exact-head hosted regression. C05 is not accepted as a complete locomotion primitive because intent replay/cancellation is not implemented end to end, runtime 24 Hz scheduling is simulated by `process_frame`, animation phase/rate is not coupled to commanded velocity, quarter-speed is only trace metadata, and the mid-loop interruption case can resume cruise.

Current authority:

- Architect Review 18: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_18.md`
- Notion Review 18: https://app.notion.com/p/3db833cb27ff81748624fa3ed8132b8d
- Current Codex directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06`
- Reviewed C05 implementation head: `24b4919a48eeef49fbcbb9305b9f2ad66639b3bd`
- Reviewed C05 publication head: `3f8846c761ecc46e7cf2f5e3d94a2bbd5c6416e1`
- Frozen visual task head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- PR #9: draft/open/unmerged
- Issue #8: open
- Branch: `codex/p02-embodiment-001`

## Frozen visual authority

- Review ZIP SHA-256: `45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b`
- Manifest SHA-256: `d8a0277272f0ccd6f948a24153b7f954aff138111ab840f22e09204aa359e595`
- Review HTML SHA-256: `7bd9e0cd5c64b89259dc2780825457a16144cebe02d259fd73a644591aa38cd2`
- R06 source-pack SHA-256: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`

No new character artwork is authorized.

## Retained R06 engineering boundary

Retain:

- 58 immutable native 1254x1254 RGB runtime masters;
- 24 tracks / 283 frame slots;
- source-role separation and byte-preserving intake;
- schema/Rust typed consumption;
- atomic publication/failure cleanup;
- real-art Godot loading and source timing;
- missing/corrupt/ineligible failure and recovery;
- export/restore;
- strict `RenderingServer.frame_post_draw` render commitment;
- transformed-source black-field compositor sampling;
- C03/C04 raster support/contact investigations as negative evidence;
- controller-owned actor translation rather than raster-derived root motion;
- true left/right profile track mapping;
- bounded slow/nominal/fast displacement arithmetic and nominal left/right Godot translation;
- implementation SHA `24b4919a...` hosted success for R06 + Phase 01 + inherited Phase 02.

## C05 findings retained as limitations

C05 does not yet prove a production-worthy locomotion command path:

- `mon_locomotion_controller.gd` stores no monotonic intent sequence and does not reject replayed IDs;
- `cancellation_id` is not enforced;
- Godot tests submit non-UUID intent strings despite the schema/Rust UUID contract;
- the Python negative matrix hard-codes stale replay, missing track, and corrupt/ineligible results instead of exercising all through the C05 protected path;
- gait frame timing is identical at 48/96/144 px/s, so commanded velocity does not actually control presentation rate/phase;
- `quarter_speed_trace` is a copied trace label, not rendered quarter-speed playback;
- the interruption case injects one stop tick and can continue later cruise phases;
- `tick_once()` is called once per render `process_frame`, so an explicit fixed 24 Hz simulation clock independent of render cadence is not demonstrated.

## Active objective

Codex executes `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06` only:

1. fetch and normally merge current main into the existing Phase 02 branch;
2. preserve all approved pixels and C02-C05 evidence;
3. keep controller-owned `MonRoot` authority unchanged;
4. create a separately versioned locomotion-intent wire profile with UUID `intent_id` plus explicit monotonic `intent_sequence` freshness semantics;
5. reject duplicate/equal/lower replayed intents and implement active-intent cancellation semantics;
6. drive the controller from schema-valid serialized intents rather than ad-hoc invalid IDs;
7. schedule canonical movement on an explicit fixed 24 Hz clock independent of render cadence and prove render-FPS variation does not alter semantic tick count;
8. couple loop animation phase/playback rate to commanded velocity under a declared calibration while preserving commanded world displacement;
9. make mid-loop stop/cancel terminate cruise and enter the stop presentation without later cruise resumption;
10. publish actual rendered normal and quarter-speed translated playback;
11. exercise all C06 negatives through the protected implementation path rather than static result booleans;
12. retain render/compositor/Rust/intake/failure/export regressions and pass R06 + Phase 01 + inherited Phase 02 on one implementation SHA;
13. return to Architect before transition or Openbox qualification.

## Remaining Phase 02 gates

Not yet accepted:

- replay-safe fixed-step velocity-synchronized controller locomotion under C06;
- real legal-transition campaign;
- dedicated 1366x768 Openbox two-hour endurance;
- Phase 02 completion;
- organism, autobiographical memory, perception, speech, learning, dreaming, caregiving efficacy, production reliability, or Phase 03+ capability.

## Protected work

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` modifications remain protected. Do not inspect them for evidence, commit, reset, stash, overwrite, copy, or reformat them.
