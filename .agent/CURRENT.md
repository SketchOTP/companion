# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

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

## Decisive blocker

The machine validator does not match `ARCHITECT_FRAME_REQUEST_V1.md`. The published request uses family `neutral_construction` at `front`, `right`, and `front_left`, while the validator expects three different neutral family names and uses `left` for the profile. It also indexes tracks by family, so three correct neutral-construction tracks collapse to one.

Supplying production art against this contract would immediately fail or require false metadata. One final executable-profile correction is required before Architect frame authoring.

## Active objective

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

No Architect-authored production frame pack, accepted body construction, approved motion language, production embodiment, visual aliveness, or Phase 03+ capability exists. C01 remains bounded synthetic engineering evidence only.
