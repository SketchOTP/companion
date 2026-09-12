# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

PR #9 at reviewed head `1d7ea24295b505c6beb0f612a6b248a6f8d5edfb` is continued under:

- Directive: `COMPANION-P02-EMBODIMENT-001-R04-C03`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_07.md`
- Notion review: https://app.notion.com/p/3d9833cb27ff81109a7add09837f7b2b
- Issue #8: open
- PR #9: draft, open, unmerged

## Review 07 disposition

C02 semantics are retained as bounded local/hosted evidence:

- complete positive 8-track / 31-frame bounded synthetic pack;
- request-profile alignment and exact event/endpoint semantics;
- PNG V1 and sRGB validation;
- reuse semantics;
- fsync-backed staged publication and atomic rename;
- actual generated-pack Rust validation;
- local Godot render-boundary result;
- local validator/tamper negatives;
- Phase 01 hosted run `34667692938` success;
- direct Phase 02 Godot gate success in hosted run `34667692926`.

`READY_FOR_ARCHITECT_FRAME_PACK` remains unaccepted because the same Phase 02 hosted run failed only in sanitized evidence validation with `unexpected Godot ERROR output`.


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

The direct hosted Godot step and `run_r04_evidence.py` execute Godot separately with different diagnostic-capture semantics. The direct gate scans stdout-only files; the evidence runner captures stdout and stderr and found an `ERROR:`. The exact error line was not retained, and the failing workflow skipped artifact upload.

The current evidence therefore cannot classify the line as wrapper noise or as a runtime defect. One narrow diagnostic-parity investigation is required.

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

Codex executes only R04-C03:

1. preserve C02 contract/intake semantics;
2. create one canonical Godot evidence runner used by direct CI and evidence generation;
3. separately capture Godot stdout, stderr, `--log-file`, Xvfb/xauth diagnostics, exit code, environment/render summary, and log hashes;
4. retain exact Godot `ERROR:` lines;
5. run identical cold and warm qualification invocations in one hosted workspace;
6. diagnose the exact line before changing runtime code;
7. publish diagnostics even when semantic validation fails;
8. keep unknown Godot errors fail-closed;
9. keep Phase 01 and Phase 02 CI green;
10. rerun the green hosted result once before claiming readiness.

No production character pixels or operator visual-review request are authorized in C03.

## External evidence basis

- Godot supports `--log-file` for explicit output/error logging.
- `xvfb-run -e` captures Xvfb/xauth diagnostics separately from the client process.
- Unknown Godot `ERROR:` diagnostics remain failures until exact source evidence exists.

## Protected work

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` modifications remain protected. Continue only in the clean local ext4/NVMe secondary worktree.

## Capability boundary

No production embodiment, approved motion language, continuous aliveness, or
Phase 03+ capability is accepted. No Architect-authored production frame pack,
accepted body construction, approved motion language, production embodiment,
visual aliveness, or Phase 03+ capability exists. R04 establishes useful
synthetic intake/runtime evidence only.

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

## R04-C02 execution result — 2026-09-12

The tuple-keyed request and complete synthetic `phase02_bounded_motion_proof_v1`
pack are implemented (8 tracks, 31 frames). Python schema/semantic intake,
byte-preservation, local export/restore, exact PNG checks, atomic staging, and
the expanded 19-case negative matrix pass. Rust 1.98.1 and exact Godot 4.7.2
are unavailable in this worktree; their required gates are `NOT RUN`/`BLOCKED`.
The final readiness status is therefore not claimed; Phase 02 remains active and
unaccepted.

## R04-C02 exact-tool rerun — 2026-09-12

The private existing Rust 1.98.1 toolchain and a transient official Godot
4.7.2 artifact were available without system modification. The complete
`phase02_bounded_motion_proof_v1` result bundle was regenerated: 8 tracks,
31 frames, exact Rust typed round-trip, missing-pack-path rejection, exact
Godot 4.7.2 frame-post-draw observation, event/timing/recovery checks, and
the 19-case intake negative matrix all pass locally. The independent result
validator and five tamper-negative mutations pass. Hosted exact-head CI and
publication remain required; no production art or Phase 02 acceptance is
claimed.
No Architect-authored production frame pack, accepted body construction, approved motion language, production embodiment, visual aliveness, or Phase 03+ capability exists. C02 establishes substantial bounded synthetic engineering evidence but not final frame-pack readiness.

## R04-C03 diagnostic-parity investigation — 2026-09-12

Review 07 was merged normally as `8523692` from `origin/main` at
`11e1139de780b44e37c6fa94f07e0ab8090ce7c1`. The canonical runner
`experiments/p02-embodiment/scripts/run_godot_qualification.py` now owns Godot
import/semantic capture for local, workflow, and evidence paths. It retains
separate stdout, stderr, `--log-file` engine output, and Xvfb wrapper logs,
hashes each channel, retains exact error/warning lines, records import/cold/warm
cache digests, and fails closed on application `ERROR:` diagnostics. Synthetic
classifier tests cover stdout/stderr/engine failures, wrapper-only warnings,
ordinary warnings, clean output, and the former stdout-only regression.

The prior hosted exact error was not retained by the superseded run, so no
runtime fix was made speculatively. Local canonical import/cold/warm runs and
the existing C02 semantic validator pass with zero Godot error lines. Hosted
qualification and its always-published diagnostic artifact remain required;
Phase 02 is active/unaccepted and `READY_FOR_ARCHITECT_FRAME_PACK` is not yet
claimed.

## R04-C03 completion — 2026-09-12

The first hosted run retained the exact ALSA diagnostic before any change:
`ERROR: Condition "status < 0" is true. Returning: ERR_CANT_OPEN` at
`drivers/alsa/audio_driver_alsa.cpp:97`, duplicated in stdout and the Godot
engine log, with empty stderr and separate Xvfb xkbcomp warnings. It was a
host audio-backend initialization issue. The canonical runner now passes
Godot's documented `--audio-driver Dummy` explicitly; no genuine Godot error
is whitelisted or hidden.

At task head `e022d18c59a836272e1470ae4905e10641abfea2`, Phase 02 hosted run
`34670472778` and its stability rerun both pass import/cold/warm, semantic
validation, and always-upload diagnostics; Phase 01 rerun `34670472829` also
passes. Published artifacts are `10290328716`
(`sha256:4d8685f808a3b0dcc74ecbb1e837fb7726fe689663dbe7a5ba3a1afc8319a651`)
and `10290383849`
(`sha256:5970ba4a5745f0a11e5368c7ae585ec2bece1fa48bc888be086237e0d2cc2dbf`).
Bounded handoff is `READY_FOR_ARCHITECT_FRAME_PACK`; Phase 02 remains
active/unaccepted and no production art or later-phase capability is claimed.
