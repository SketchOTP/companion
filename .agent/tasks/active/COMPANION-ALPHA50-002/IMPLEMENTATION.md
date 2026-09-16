# COMPANION-ALPHA50-002 implementation record

This candidate preserves Alpha50-001 history and adds a fixed-point V2
organism path without destructively migrating any existing store. V1 remains
available only for historical fixtures.

Implemented in this pass:

- `organism_v2` with bounded integer milli-units, deterministic arithmetic,
  typed drives, action scoring, preference consumption, outcome consumption,
  memory provenance, and V2 snapshot/restore helpers.
- Resident `companion-core` Alpha life mode now restores V2 state, consumes an
  ordinary observation into typed preference memory before selecting its
  body-neutral intent, records the memory event, and snapshots the V2 state.
- V2 schema and fixture are included in semantic schema and contract closeout
  gates.
- Alpha workflow now runs the schema gate and a fail-closed `rg` scanner
  self-test with synthetic detection and clean-fixture checks.

Evidence ceiling remains `E3_TARGET_TESTED` for new behavior. A complete
resident Godot result/learning loop, production Godot transition campaign,
multi-class failure campaign, process-loss care independence, sensor hardware,
and Openbox endurance remain bounded or unavailable and are not claimed.

Follow-up correction: the retained restart campaign now waits for the
production `companion-core.ready` marker before sending shutdown signals,
including classified retry attempts, eliminating the startup signal race
observed in hosted case 118.  The Alpha workflow uses a guaranteed Python
regex scanner with synthetic fail/pass self-tests because hosted runners do
not provide `rg`; scanner absence remains fail-closed at the executable step.

Exact implementation head `d83e5c396427ba8a193db2febdb359d7294a57e5` passed
hosted Alpha50 (`34946179230`, `34946183524`), Phase 01 (`34946179362`,
`34946183516`), focused R06 (`34946179214`, `34946183515`), and inherited
Phase 02 (`34946179206`, `34946183562`) push/PR runs. The published Alpha
artifact is `10387258357` with ZIP SHA-256
`2d81281a09e1d8edd40667bce5e800d2ba7b06a7a893984479ea0efd15937f08`.

The final executable qualification head is `70b2a5ca51a7c8adb688a97e42243f88c36cc5fc`;
its Alpha50, Phase 01, focused R06, and inherited Phase 02 hosted push/PR
runs all passed. Artifact `10387094480` has ZIP SHA-256
`d032bc5e436a470c40f43e337e6eaa49fc83e7e60d71c7babde18d6286f95395`.
