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
