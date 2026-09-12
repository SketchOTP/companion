# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains
adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

PR #9 was continued from reviewed head
`1183795843f26de6b69f0a2a0828ee288f32e415`. Review 04 was merged normally as
`928ba4b8e52b8cadb9c8861ad066d2d8a91366a4`; the current R04 implementation
head is `7a79ddf9400a0d7cacd781d418fffdc625ec3c57`.
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

## Review 04 finding retained as history

The R03 coding-agent artwork was outside the identity boundary. Canonical R04
and R10 assign the original sprite library to the AI Architect under operator
approval. That R03 output remains only rejected negative evidence.

The former procedural GDScript and Python renderers are disconnected from the
candidate production path and cannot be selected as fallbacks.
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

## R04 implementation result

The branch now provides:

1. R03 procedural visual paths preserved only as rejected negative evidence;
2. `MON_AUTHORED_FRAME_PACK_V1` and a machine-checkable
   `ARCHITECT_FRAME_REQUEST_V1.md`;
3. byte-preserving content-addressed intake that rejects rather than repairs;
4. explicit Rust/schema/Godot types for approval, provenance, timing,
   landmarks, contacts, events, and completion;
5. required-path Rust validation that fails when the generated pack is absent;
6. exact-track Godot playback with frame zero observed before `started`;
7. missing, ineligible, hash-corrupt, timing/contact/event tamper rejection and
   corrupt-pack recovery;
8. identity-reference import smoke and obvious geometric synthetic test pack,
   neither represented as candidate art;
9. green focused Phase 02 hosted run `34656090767`, artifact `10285600941`
   with digest
   `sha256:39c56c9d43968e870005065b6bebf19700791986c017496b1ea5a03e0e14ff1f`.

The inherited Phase 01 exact-head workflow is still being observed before final
publication. R04 is not Phase 02 acceptance and does not request visual review.
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

No production embodiment, approved motion language, continuous aliveness, or
Phase 03+ capability is accepted. When exact-head validation and publication
complete, the bounded handoff status is `READY_FOR_ARCHITECT_FRAME_PACK`.
No Architect-authored production frame pack, accepted body construction,
approved motion language, production embodiment, visual aliveness, or Phase 03+
capability exists. R04 establishes useful synthetic intake/runtime evidence only.

## Current routing — R04-C01 (2026-09-11)

Architect Review 05 requires a narrow authored-frame contract correction on
`codex/p02-embodiment-001`, after normal merge of `origin/main` at
`658fa98defa84409e88c5ea6323579dd6c574057` (merge commit
`92d7ffe7f7038a5a591f2c6bf973e1e8bb54f322`). Source, ingested, and receipt
documents are separate; facing, landmark, identity, PNG, timing, event,
atomic-publication, Rust, and Godot gates are fail-closed. Only synthetic test
geometry is generated. Protected primary/secondary Graft files remain
untouched. Phase 01 remains accepted, Phase 02 remains active/unaccepted, and
the bounded result is `READY_FOR_ARCHITECT_FRAME_PACK` without visual approval.
