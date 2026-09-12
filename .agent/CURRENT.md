# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.


PR #9 was continued from reviewed head
`1183795843f26de6b69f0a2a0828ee288f32e415`. Review 04 was merged normally as
`928ba4b8e52b8cadb9c8861ad066d2d8a91366a4`; the current R04 implementation
head is `7a79ddf9400a0d7cacd781d418fffdc625ec3c57`.
PR #9 at reviewed head `925073601b039bc66e83de272b5378997cd8ec70` is continued under:


- Directive: `COMPANION-P02-EMBODIMENT-001-R04-C02`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_06.md`
- Notion review: https://app.notion.com/p/3d9833cb27ff81089f25cd955f5efb23
- Issue #8: open
- PR #9: draft, open, unmerged

## Review 06 disposition

Retain:

- exact approved visual references and hashes;
- source/ingested/receipt contract split;
- per-frame facing and landmark-state model;
- bounded synthetic byte-preserving intake;
- approval-state enforcement;
- required-path Rust validation;
- 24 Hz timing direction;
- synthetic missing/corrupt/restored-track behavior;
- green Phase 01 and Phase 02 hosted workflows.

Do not accept:

- `READY_FOR_ARCHITECT_FRAME_PACK`;
- the current `phase02_bounded_motion_proof_v1` executable profile as matching the Architect request;
- positive proof that a complete bounded pack can pass;
- exact required event/endpoint enforcement;
- exact source-reuse semantics;
- exact sRGB/PNG-profile validation;
- crash-durable intake publication;
- headless fallback as render-commit evidence;
- exact runtime event/timing evidence;
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

## Decisive blocker

The machine validator does not match `ARCHITECT_FRAME_REQUEST_V1.md`. The published request uses family `neutral_construction` at `front`, `right`, and `front_left`, while the validator expects three different neutral family names and uses `left` for the profile. It also indexes tracks by family, so three correct neutral-construction tracks collapse to one.


Supplying production art against this contract would immediately fail or require false metadata. One final executable-profile correction is required before Architect frame authoring.

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

Codex executes only R04-C02:


1. make the human and executable bounded request identical;
2. build one complete positive synthetic `phase02_bounded_motion_proof_v1` pack;
3. enforce exact endpoints, event names/order, postures, completion, counts, and no ambiguous extra tracks;
4. bind `reuse_of` to the actual same-track source occurrence;
5. require exact PNG V1 structure with one valid `sRGB` chunk and no fake ICC substitute;
6. add fsync-backed durable atomic publication and injected mid-intake failure evidence;
7. emit render-commit only after actual `RenderingServer.frame_post_draw` observation;
8. record monotonic runtime timestamps and assert the entire expected sequence/timing;
9. keep Phase 01 and Phase 02 CI green;
10. return `READY_FOR_ARCHITECT_FRAME_PACK` only when the complete bounded synthetic pack passes source→intake→Rust→Godot.

No production character pixels or operator visual-review request are authorized in C02.

## Online evidence basis

- Linux `rename(2)` provides an atomic same-filesystem namespace switch; cross-filesystem rename fails with `EXDEV`. Durable publication still requires the appropriate fsync discipline around files/directories.
- W3C PNG defines color type 6 as RGBA with both 8- and 16-bit allowed sample depths; Phase 02 must independently enforce bit depth 8 and its explicit sRGB source policy.

## Protected work

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` modifications remain protected. Continue only in the clean local ext4/NVMe secondary worktree.

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

## R04-C01 publication reconciliation — 2026-09-12

Implementation `04570503c957e34e2ddcf2f1ab1cb1151a352b59` and evidence bundle
`5d29b51e48073077abbdffad453226ce7e8cfddc` are pushed to
`codex/p02-embodiment-001`. The committed validator passes independently and
the protected primary/secondary Graft files remain untouched. PR #9 is
draft/open/unmerged and Issue #8 is open. Phase 02 remains active/unaccepted.

No Architect-authored production frame pack, accepted body construction, approved motion language, production embodiment, visual aliveness, or Phase 03+ capability exists. C01 remains bounded synthetic engineering evidence only.
