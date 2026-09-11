# Architect Review 01 — COMPANION-P02-EMBODIMENT-001

## Verdict

`CONTINUE — PHASE 02 NOT ACCEPTED; REFERENCE AND TEMPORAL-ANIMATION CORRECTION REQUIRED`

- Reviewed PR: `#9`
- Reviewed branch: `codex/p02-embodiment-001`
- Reviewed head: `9a65b8db032c97e13fce5d6a305989d32f2cc879`
- Required PR state: `OPEN / DRAFT / UNMERGED`
- GitHub Issue: `#8 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACCEPTED`
- Roadmap Phase 02: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 03 and later: `CLOSED`
- Product capability: `NOT ESTABLISHED`
- Canonical Notion review: https://app.notion.com/p/3d8833cb27ff81778c22d2c73cf0dc9f

## Objective

Correct the Phase 02 asset and animation model before more bulk production.
The submitted branch contains useful pipeline, manifest, Godot-scene, QA, and
reproducibility work, but its 256 counted body images are primarily one pose per
clip family and direction. Directional views are then played as temporal
animation frames. That does not establish a sprite-animation library or visual
aliveness.

This continuation is substantial but bounded:

1. obtain durable access to the exact approved references;
2. rebuild the construction and authoring basis from those references;
3. implement real temporal animation tracks;
4. correct Godot timing, selection, transition, and event semantics;
5. move bulk generated binaries out of ordinary Git;
6. add dedicated Phase 02 CI and versioned workflow artifacts; and
7. publish an operator-accessible construction and core-motion approval package.

Do not expand to the remaining full 32-family library until the operator
approves the corrected identity, diagonal construction, and core motion
language.

## Independent review findings

### Openbox unavailability is valid but not the sole blocker

The dedicated 1366x768 Openbox target was unavailable, so the required target
playback could not run without unauthorized host reconfiguration. That is a
genuine stop condition for the final target-host endurance gate. It does not
waive the animation-model, reference, CI, artifact, and operator-review defects
below.

### Current CI is not green for Phase 02

No dedicated Phase 02 workflow exists. The inherited Phase 01 workflow ran on
PR #9 and failed in contract closeout because the generated valid fixture for
`mon-animation-clip.schema.json` used a `clip_id` that violated the schema
pattern. Subsequent workflow steps were skipped. The branch therefore has a red
current workflow and no Phase 02 artifact publication.

### Exact native identity source was not available to Codex

The operator-approved native identity file is authority-bound to SHA-256:

`86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56`

The turnaround is authority-bound to:

`3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4`

The Architect independently re-verified both original operator uploads against
those hashes. Codex reported that it retrieved only a constructed derivative for
the identity source. A derivative cannot become the canonical identity input by
substitution. Codex must obtain the exact native files through durable project
transfer or stop at the reference gate with one targeted transfer request.

### The clip manifest uses direction as time

Each current clip contains eight frame references corresponding to N, NE, E,
SE, S, SW, W, and NW. There is no temporal frame sequence for each direction.
The Godot loader appends those eight directional images to one `SpriteFrames`
animation, causing the mon to rotate through views instead of perform a motion
over time.

The current `32 families x 8 directions = 256 images` count is a directional
pose catalog, not 256 temporal animation drawings. The 32-family completion
claim and 10,000-transition result are superseded as Phase 02 animation
evidence.

### Godot frame timing is incorrect

The current loader passes seconds-like values to `SpriteFrames.add_frame`.
Godot defines that argument as a relative frame duration. Absolute duration
depends on animation FPS and playing speed. The runtime must set an explicit
animation FPS and express frame holds as integer relative ticks on the 24 Hz
master grid.

### The generator is not reference-grounded or reliably deterministic

The current Pillow generator draws a simplified creature from generic ellipses,
polygons, and lines rather than deriving geometry from the approved reference
package. It also uses Python's process-randomized `hash()` in pose geometry, so
repeatability across independent interpreter processes is not guaranteed. Use a
stable project-defined digest or explicit authored values, not Python runtime
hash values.

The generator offsets visible body placement through bob, sway, and lean while
retaining a fixed metadata root. The current zero-root-drift claim therefore
does not prove that rendered root and planted-contact geometry are stable.

### Atlas and repository claims are incorrect

Current atlas pages arrange untrimmed 1024x1024 frames flush in a 4x4 page while
declaring a four-pixel gutter. This is not trim, extrusion, or gutter
reconstruction.

The branch also commits the bulk generated PNG corpus, duplicate Godot copies,
atlases, and pack archive to ordinary Git. This conflicts with the adopted
generated-asset policy. The final Phase 02 tree must retain authored sources,
manifests, validators, and selected review derivatives while producing the bulk
frame and pack corpus as deterministic workflow artifacts and local export
bundles.

Because current branch history already contains the bulk binaries, do not
rewrite or force-push history. Remove them from the final tree. The Architect
will use a squash merge if Phase 02 is later accepted so intermediate generated
blobs do not enter `main` history.

### Review publication is insufficient

The report references local `/home/...` paths and did not attach primary review
files to Notion or publish them through a Phase 02 workflow artifact. The
operator cannot approve visuals that are not durably accessible. The current
publication is not review-ready.

## Evidence disposition

### Retain

- Exact Godot 4.7.2 baseline and accepted Phase 01 foundation.
- Phase 02 schema and manifest direction.
- Layered `MonAvatar` scene hierarchy as a starting structure.
- Existing bridge and habitat integration direction.
- Deterministic ZIP metadata correction.
- QA, contact-sheet, transition-test, evidence, and clean-room tooling structure
  where it can be corrected.
- Negative results and rejected generated assets.

### Supersede as Phase 02 proof

- 256 unique body-animation-frame completion.
- 32 completed semantic animation families.
- Eight-direction temporal animation coverage.
- Zero-root-drift proof based only on manifest metadata.
- Four-pixel atlas gutter/extrusion claim.
- 10,000 real animation-transition proof.
- Five-second performance numbers as Godot runtime measurements.
- Identity fidelity based on the constructed derivative.
- Phase 02 CI completion.
- Operator-review readiness.

## Required correction A — exact reference gate

1. Retrieve the exact native identity and turnaround files from durable project
   authority.
2. Verify both hashes, dimensions, color mode, and transparency status.
3. Preserve the native files without recompression or mutation.
4. Commit them when within the ordinary-Git asset budget, or bind them through a
   durable versioned artifact with a committed manifest and local export/restore
   copy.
5. Do not use the constructed SVG derivative as a canonical identity source.
6. If either exact source remains unavailable, stop before regenerating bulk
   body art and return one targeted operator transfer request.

## Required correction B — identity-grounded construction and motion approval

Create an authored construction representation derived directly from the
approved sources. It must define stable proportions, palette roles, line and
shadow rules, head-spike map, eyes and pupils, mouth, hands and exact
finger/thumb count, feet and exact toe count, root, planted contacts, shadow
footprint, and perspective limits.

Publish accessible review files for:

- approved source references;
- six approved-view correspondence;
- four candidate diagonal views;
- anatomy and palette;
- silhouette and root/contact overlays; and
- a temporal core-motion sheet.

Every file must be attached or embedded in the Notion report or published as a
named GitHub Actions artifact with digest and direct PR/Issue reference. Local
filesystem paths are not publication.

## Required correction C — correct animation data model

Direction is a selection axis, not a temporal-frame index.

Define each runtime track by at least:

`stage + body_revision + family + direction + posture + variant`

Each track must contain an ordered temporal frame sequence with durations,
landmarks, contacts, events, entry/exit connectors, and interruption ranges.

Build a substantial operator-approval core pack containing real temporal
drawings:

- Three materially different idle/breath variants in all eight directions, at
  least six temporal drawings per track.
- Walk in all eight directions, at least eight temporal drawings per track.
- Run in all eight directions, at least six temporal drawings per track.
- Cardinal-to-diagonal and diagonal-to-cardinal orient/turn connectors with at
  least three temporal drawings per connector.
- Focused temporal proofs for sit/stand, lie/sleep/wake, listen, think,
  acknowledge, surprise, and sensor-degraded presentation.

Do not count direction changes, mirrored duplicates, metadata-only changes,
global translation, uniform scaling, or held-frame repetition as unique
temporal drawings.

This is the visual and motion approval gate. After operator approval, continue
the same Phase 02 directive to the complete 32-family library and final
target-host playback.

## Required correction D — Godot animation semantics

1. Set explicit animation FPS.
2. Represent 24 Hz timing-grid holds as relative duration ticks, not seconds
   passed to `add_frame`.
3. Load one temporal track per family, direction, posture, and variant.
4. Use actual `frame_changed`, loop, and completion behavior.
5. Return frame markers, contact events, interruption, completion, and
   degradation results from observed playback.
6. Implement direction, posture, affect, energy, stage, pack, and transition
   eligibility in the director.
7. Use a legal transition graph and authored transition tracks.
8. Implement real interruption and continuation behavior.
9. Implement controlled BodyA/BodyB handoff rather than simple visibility
   toggling.
10. Test missing/corrupt packs and recovery.

## Required correction E — root, contact, and identity QA

Validate rendered and source landmarks, not only declared metadata.

- Root remains exactly `(512,896)` in source space.
- Body bob and squash occur around the root; root itself does not translate.
- Declared planted contacts remain within two pixels during contact spans.
- Silhouette, body area, head, eye, mouth, hand, foot, palette, and alpha-edge
  measurements remain within reviewed bounds.
- Automated anatomy checks flag suspicious frames for operator disposition and
  never substitute for visual review.

## Required correction F — deterministic authoring and atlas packaging

- Remove Python runtime `hash()` from all geometry and asset-identity decisions.
  Use explicit authored IDs or a stable cryptographic digest.
- Prove byte-identical clean-process rebuilds under controlled tool versions.
- Trim transparent bounds losslessly.
- Extrude edge pixels and provide at least four real gutter pixels between
  packed regions.
- Record trim rectangles and reconstruct original source placement in Godot.
- Detect overlap, bleed, missing gutter, corrupt pack, and source-placement
  mismatch.

## Required correction G — repository and artifact policy

The final PR tree must:

- keep exact references, authored sources, clip specifications, manifests,
  validators, Godot resources, hashes, and selected review derivatives;
- remove the bulk generated full-canvas PNG corpus, duplicate runtime copies,
  atlases, and pack ZIP from ordinary Git;
- generate bulk assets in a dedicated immutable Phase 02 workflow;
- upload frame corpus, runtime packs, contact sheets, QA, and performance
  evidence as workflow artifacts with recorded SHA-256 digests; and
- preserve a local export/restore bundle independent of GitHub availability.

Do not configure Git LFS. Do not rewrite public branch history. Prepare for
squash merge at acceptance.

## Required correction H — dedicated Phase 02 CI

Add an immutable `phase02-embodiment` workflow that runs:

- approved-reference hash checks;
- deterministic clean-process generation;
- animation contract/schema/Rust/Godot drift checks;
- temporal-frame and unique-drawing accounting;
- root/contact/safety-region/anatomy/alpha QA;
- actual trim/extrude/gutter/atlas validation;
- Godot import and headless temporal playback;
- event/interruption/completion tests;
- missing/corrupt pack degradation and recovery;
- repository binary-budget check;
- artifact upload and digest capture; and
- evidence validation plus tamper-negative testing.

Repair the inherited Phase 01 workflow failure caused by the invalid generated
`mon-animation-clip` fixture. The current PR cannot be reviewed as green while
that workflow is failing.

## Required correction I — current-host evidence and final target blocker

Run headless and current-session development tests without changing host
configuration. Do not relabel the GNOME/mutter session as the dedicated Openbox
target.

The two-hour Openbox playback remains blocked until the actual target is
available. Record the exact minimum access requirement. Do not attempt display
reconfiguration, compositor changes, service changes, or physical hot-unplug.

After operator approval and Openbox availability, the final Phase 02
continuation must run the real 10,000 temporal-transition matrix and two-hour
continuous playback using one Godot process and one resident foundation
instance.

## Acceptance boundary for this continuation

This continuation passes only when:

1. Exact approved references are durably available and hash-verified, or one
   precise transfer blocker is returned before bulk regeneration.
2. Construction, diagonal, anatomy, palette, root/contact, and temporal
   core-motion materials are operator-accessible.
3. Direction and time are separated in manifests and runtime resources.
4. The core pack contains real temporal sequences and passes identity, root,
   and contact QA.
5. Godot timing, transitions, events, interruption, continuation, and
   BodyA/BodyB handoff are directly tested.
6. Asset generation is deterministic across clean processes.
7. Atlases use actual trim, extrusion, and gutter reconstruction.
8. Bulk generated assets are removed from the final ordinary-Git tree and
   published as versioned artifacts.
9. Dedicated Phase 02 CI and the inherited Phase 01 workflow are green.
10. Notion and GitHub contain directly accessible review materials.
11. Every broader count or performance claim unsupported by execution is
    removed or marked superseded.
12. Phase 03 and later remain closed.

## Publication discipline

Continue on `codex/p02-embodiment-001`, PR #9, and Issue #8. Merge current
`origin/main` normally. Do not rebase, force-push, rewrite history, create a
replacement PR, merge PR #9, or close Issue #8.

Use coherent implementation commits and at most one publication-reconciliation
commit. Preserve prior generated assets and claims as rejected or superseded
evidence while removing bulk binaries from the final tree.

Update the active task packet, `.agent/CURRENT.md`, `.agent/INDEX.md`,
append-only ledgers, Phase 02 Notion report and directive, PR #9, and Issue #8.
Leave the PR draft/open/unmerged and the issue open. Return one complete Codex
result and stop for Architect and operator review.

## Hard boundary

Do not implement or claim organism needs, drives, goals, autonomy,
autobiographical memory, learning, development, dreaming, camera/microphone
capture, VAD/STT/TTS, models, biometrics, contacts, notifications, spoken-help
recognition, live care behavior, medical capability, security certification,
product reliability, lifetime durability, availability, SLA, or Phase 03+
completion.

## Required result

Return `CODEX RESULT — COMPANION-P02-EMBODIMENT-001` with exact
reference-transfer status, corrected construction and temporal-track model,
real temporal-frame counts, identity/root/contact QA, Godot timing and playback
evidence, actual atlas/gutter evidence, artifact digests, dedicated CI runs,
accessible review publication, explicit Openbox blocker, all superseded claims,
and exact branch/PR/Issue/Notion state.
