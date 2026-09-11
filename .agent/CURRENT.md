# Current Project State

## Current stage

Planning Phase 02 remains the governing delivery roadmap.

Roadmap Phase 00 is complete. Architecture v1.0 remains adopted. Roadmap Phase
01 is accepted at the bounded engineering-foundation boundary and merged in
`fc31717bba8c4833736d1792d7a5fe1c6cca4900`.

Roadmap Phase 02 — Mon Body, Habitat, and Sprite Pipeline remains active but is
**not accepted**. PR #9 at
`9a65b8db032c97e13fce5d6a305989d32f2cc879` is continued under Architect
Review 01 and its source-recheck correction.

## Architect Review 01 disposition

The dedicated 1366x768 Openbox target was unavailable, so final target-host
playback is legitimately blocked. It is not the only blocker.

Independent review found:

- no dedicated Phase 02 workflow and a failing inherited Phase 01 workflow;
- the exact approved native identity source was not durably available to Codex;
- each current clip uses eight directional views as temporal frames;
- the 256-image count is a directional pose catalog, not a temporal animation
  library;
- Godot frame duration is interpreted incorrectly;
- generated construction geometry is not derived from the exact approved native
  reference package;
- visible body placement moves while fixed root/contact metadata is declared;
- declared atlas gutters and extrusion are not physically implemented;
- bulk generated PNGs, duplicate runtime copies, atlases, and ZIP output are
  committed to ordinary Git contrary to the adopted artifact policy; and
- operator review assets were referenced through local paths instead of being
  attached or published accessibly.

A source recheck withdrew the initial statement that the reviewed generator uses
Python runtime `hash()`. No `hash()` call was found in that file. This does not
change the verdict or the requirement for explicit, stable authoring inputs and
byte-identical clean-process rebuilding.

The 32-family, 256-animation-frame, eight-direction animation, atlas-gutter,
10,000-transition, runtime-performance, Phase 02 CI, and operator-review-ready
claims are superseded as Phase 02 evidence.

## Active objective

Complete one substantial correction in the existing Phase 02 branch and PR:

1. obtain and hash-verify the exact native approved identity and turnaround;
2. rebuild the construction model from those sources;
3. separate direction selection from temporal frame progression;
4. produce an identity-faithful temporal core-motion approval pack;
5. correct Godot FPS, relative-duration, transition, event, interruption,
   continuation, and BodyA/BodyB semantics;
6. validate rendered root/contact/anatomy/alpha properties;
7. implement real trim, extrusion, gutter, and source-placement reconstruction;
8. remove bulk generated binaries from the final ordinary-Git tree;
9. add dedicated Phase 02 CI and versioned workflow artifacts;
10. publish operator-accessible visual and motion review materials.

Bulk completion of the remaining 32-family library waits for operator approval
of identity, diagonal construction, and the temporal core-motion language.

## Active directive and review

- Directive: `COMPANION-P02-EMBODIMENT-001`
- Status: `ARCHITECT REVIEW 01 — REFERENCE AND TEMPORAL-ANIMATION CORRECTION`
- Reviewed task head: `9a65b8db032c97e13fce5d6a305989d32f2cc879`
- Repository review:
  `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_01.md`
- Source-recheck correction:
  `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_01_CORRECTION.md`
- Notion review:
  https://app.notion.com/p/3d8833cb27ff81778c22d2c73cf0dc9f
- Notion directive:
  https://app.notion.com/p/3d8833cb27ff810e858acd029ac0ea05
- Notion report:
  https://app.notion.com/p/3d8833cb27ff817d9d01d754ec852c10
- GitHub Issue #8:
  https://github.com/SketchOTP/companion/issues/8
- Pull request #9:
  https://github.com/SketchOTP/companion/pull/9
- Required branch: `codex/p02-embodiment-001`
- Required publication: continue existing draft/open/unmerged PR #9
- Acceptance authority: ChatGPT AI Architect plus explicit operator visual
  approval
- Phase 03 and later: `CLOSED`

## Retained implementation

Retain exact Godot 4.7.2, the accepted Phase 01 foundation, the animation schema
and manifest direction, layered `MonAvatar` structure, bridge/habitat direction,
deterministic ZIP metadata correction, and useful QA/review/build scaffolding.
Retain all negative and rejected asset evidence.

## Fixed embodiment authority

- Approved original purple mon and hard anatomy/style invariants.
- `MON_FRAME_V1`: 1024x1024 RGBA/sRGB, transparent, root `(512,896)`, baseline
  `896`, safety region `x=64..960`, `y=32..960`, zero root drift, 24 Hz timing
  grid, no source crop, no encoded translation.
- Direction is a selection axis. Each direction requires its own temporal track.
- Runtime embodiment remains raster sprite-frame based.
- Godot owns only animation execution state.
- No canonical organism, memory, perception, speech, identity, contact, or care
  authority may enter Godot.

## Asset storage boundary

The final Phase 02 tree keeps approved references, authored source, clip specs,
manifests, validators, Godot resources, hashes, and selected review derivatives.
The full generated frame corpus, atlases, and packs must be produced as
versioned workflow artifacts and local export bundles. Do not configure Git LFS
or rewrite branch history. A later accepted Phase 02 merge is expected to use a
squash merge so rejected intermediate binary blobs do not enter `main` history.

## Target-host boundary

The final two-hour Openbox playback remains blocked until the actual dedicated
target is available. Codex may run headless and current-session development
checks without changing host configuration. It may not reconfigure displays,
compositors, services, audio, power, or the existing Godot 4.6 installation.

## Protected operator work

The primary SSHFS worktree contains operator-owned uncommitted root
`.gitignore` and `AGENTS.md` changes. Do not read their modified contents into
evidence, commit, discard, reset, overwrite, stash, copy, reformat, or
reinterpret them. Continue only in the clean local ext4/NVMe secondary
worktree.

## Product boundary

No organism, needs, drives, goals, personality, autonomy, autobiographical
memory, learning, development, dreaming, camera/microphone, STT/TTS, model,
biometric, contact, notification, spoken-help, live care, security
certification, product reliability, medical/emergency capability, or Phase 03+
completion is established or authorized.

## Next review point

Codex executes Architect Review 01 and the source-recheck correction in the
existing Phase 02 branch and PR. It returns either the complete accessible
reference/construction/core-motion approval package with green dedicated CI, or
one precise reference-transfer blocker before further bulk generation.
Architect and operator review follow.
