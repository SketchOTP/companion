# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains
adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

PR #9 at reviewed head `ee2e47595271777bfbb253a6639c6ebac7198a1b`
is continued under:

- Directive: `COMPANION-P02-EMBODIMENT-001-R04-C01`
- Repository review:
  `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_05.md`
- Notion review:
  https://app.notion.com/p/3d8833cb27ff81588285f477678ad3d3
- Issue #8: open
- PR #9: draft, open, unmerged

## Review 05 disposition

R04 is partially accepted at a bounded synthetic engineering boundary.

Retain:

- exact approved reference hashes;
- byte-preserving synthetic source intake;
- content-addressed copies and export/restore evidence;
- manifest approval-state enforcement;
- non-skipping generated-pack Rust validation;
- 24 Hz relative-duration configuration;
- synthetic missing/corrupt/restored-track behavior;
- green Phase 01 and focused Phase 02 workflows.

Do not accept:

- `READY_FOR_ARCHITECT_FRAME_PACK`;
- the combined source/runtime pack contract as final;
- orientation-track representability;
- occluded-landmark representability;
- complete R10 landmark coverage;
- atomic production intake;
- complete PNG source-profile validation;
- full runtime pack/track/reference integrity;
- physical or target first-frame presentation;
- exact measured event/tick behavior;
- Phase 02 acceptance.

## Main blocker

The current Architect-input contract cannot truthfully represent the requested
front-to-front-left orientation tracks because facing exists only at track level
and filenames must match that one facing. It also requires concrete coordinates
for landmarks that can be occluded in profile or turned poses.

Supplying art now would force false metadata and an immediate breaking schema
migration. The contract must be corrected before identity-critical frames are
authored.

## Adopted source/runtime authority split

The Architecture Decision Ledger now requires:

1. `MON_AUTHORED_FRAME_SOURCE_PACK_V1` — immutable Architect input;
2. `MON_INGESTED_FRAME_PACK_V1` — validated derived runtime/build document;
3. `MON_FRAME_INTAKE_RECEIPT_V1` — input/output digests, byte equality,
   validation result, and atomic publication state.

Source manifests do not contain runtime-derived paths or content addresses.
Godot consumes only a validated ingested pack.

## Active objective

Codex must execute only R04-C01:

1. split source, ingested, and receipt schemas;
2. add track entry/exit facing and per-frame facing/posture/action phase;
3. represent visible, occluded, and not-applicable landmarks without invented
   coordinates;
4. include the complete canonical R10 landmark set and typed optional anchors;
5. enforce the bounded frame-request families, counts, endpoints, and events;
6. enforce unique identities and explicit source-asset reuse/hold semantics;
7. validate PNG IHDR bit depth/color type, actual sRGB, nonempty alpha,
   transparency, and safety region;
8. stage and atomically publish intake into a fresh destination;
9. bind pack, track, reference, relationship, and path integrity in Godot;
10. observe the render boundary before a render-commit acknowledgment;
11. prove exact event tick/frame consistency and the expanded tamper matrix;
12. keep Phase 01 and Phase 02 CI green;
13. return `READY_FOR_ARCHITECT_FRAME_PACK` only after the correction passes.

Codex must not create production character pixels or request operator visual
approval.

## Authority records

- Live ledger after Review 05: 56 ADRs — 34 adopted, 20 interim, 2 rejected.
- Research evidence: 58 records.
- New adopted ruling: Architect source packs and ingested runtime packs are
  separate immutable contracts.
- New official evidence: W3C PNG profile semantics and Godot render-observation
  semantics.

## Protected work

The primary SSHFS worktree contains operator-owned modified `.gitignore` and
`AGENTS.md`. Do not inspect their modified contents for evidence or alter them.
Continue only in the local ext4/NVMe secondary worktree.

## Capability boundary

No Architect-authored production frame pack, accepted body construction,
approved motion language, production embodiment, visual aliveness, or Phase 03+
capability exists. R04 establishes useful synthetic intake/runtime evidence only.
