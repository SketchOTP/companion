# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains
adopted. Roadmap Phase 01 remains accepted.

PR #9 at reviewed head `1183795843f26de6b69f0a2a0828ee288f32e415`
is continued under:

- Directive: `COMPANION-P02-EMBODIMENT-001-R04`
- Repository review:
  `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_04.md`
- Notion review:
  https://app.notion.com/p/3d8833cb27ff81b0ae0bd8815885e2f6
- Issue #8: open
- PR #9: draft, open, unmerged
- Phase 03 and later: closed

## Review 04 disposition

Retain:

- exact approved native references and hashes;
- final-tree removal of prior generated bulk outputs;
- useful 24 Hz and temporal-track direction;
- artifact publication and focused workflow infrastructure;
- green inherited Phase 01 workflow.

Do not accept:

- the R03 rendered character;
- `MON_BODY_SOURCE_V2` as a production visual source;
- the Godot-rig source-of-truth claim;
- the duplicate Python raster source;
- identity fidelity, motion-language quality, facing-transition quality, or
  operator-review readiness;
- the current contract/runtime/CI claim as complete.

## Main blocker

The coding agent is still inventing identity-critical artwork. Canonical R04 and
R10 assign the original sprite library to the AI Architect under operator
approval. The R03 output is visibly a different construction: polygon torso,
segmented limbs, bead-like digits/toes, angular eyes, and triangular crown
spikes rather than the approved smooth rounded mon.

The source is also split between a procedural GDScript drawing and a separate
procedural Python renderer. The TSCN contains Bone2D names but no Skeleton2D-bound
visual geometry. There is no single identity-faithful visual source of truth.

## Adopted visual-authorship boundary

- AI Architect creates or edits production source art and temporal key poses.
- Operator approves identity, construction, and motion language.
- Codex owns lossless intake, typed contracts, deterministic derivatives,
  packaging, runtime integration, CI, and evidence.
- Codex may create only obviously synthetic non-product fixtures.
- Godot executes approved sprite tracks; it does not own identity truth.

The decision is recorded in the Architecture Decision Ledger and Architect
Review 04.

## Active objective

Codex must complete only R04:

1. merge current `origin/main` normally;
2. supersede R03 procedural character art and duplicate renderers while
   preserving negative evidence;
3. create `MON_AUTHORED_FRAME_PACK_V1` and
   `ARCHITECT_FRAME_REQUEST_V1.md`;
4. implement byte-preserving frame intake with no automatic art mutation;
5. strongly type landmarks, contacts, events, timing, facing, approval state,
   and provenance across schema/Rust/Godot;
6. make generated-pack Rust validation non-skipping;
7. emit `started` only after the exact requested first frame is visible;
8. prove missing/corrupt/tamper failure and recovery;
9. keep Phase 01 and Phase 02 CI green;
10. return `READY_FOR_ARCHITECT_FRAME_PACK`.

Codex must not create new production character artwork or request operator visual
approval in this directive.

## Protected work

The primary SSHFS worktree contains operator-owned modified `.gitignore` and
`AGENTS.md`. Do not inspect their modified contents for evidence or alter them.
Continue only in the local ext4/NVMe secondary worktree.

## Capability boundary

No production embodiment, approved motion language, continuous aliveness, or
Phase 03+ capability is accepted. The branch contains useful source-transfer,
contract, and CI scaffolding plus retained negative evidence.
