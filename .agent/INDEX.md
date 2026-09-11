# Authority Project-State Index

## Canonical project

- Canonical project: https://app.notion.com/p/3d5833cb27ff8196814fdbae282f15ad
- End goal: https://app.notion.com/p/3d5833cb27ff81b09c20e2b52d537e1e
- Roadmap: https://app.notion.com/p/3d5833cb27ff81dd88faeb0c95b6f44e
- Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Visual bible: https://app.notion.com/p/3d5833cb27ff8108a3acf202fc268b6d
- Sprite contract: https://app.notion.com/p/3d5833cb27ff81989d95f604112e25ba
- Repository: https://github.com/SketchOTP/companion

## Current pointers

- R03 correction merge: `77ebc5c19285d97c467caedbcb3f7c3be083a4a0`
- R03 candidate source: `assets/source/p02/r03/mon_body_source_v2.json`
- R03 generated result: `experiments/p02-embodiment/results/r03/`
- R03 Godot playback: `godot/r03_temporal_playback_test.gd`

- Active roadmap phase: `02 — Mon Body, Habitat, and Sprite Pipeline`
- Phase acceptance: `NOT GRANTED`
- Active directive: `COMPANION-P02-EMBODIMENT-001-R03`
- Reviewed task head: `4a111435381ff2d364cd705edbb1d65da46ea886`
- R03 candidate head: `448ea93bb53f2f4f1742b5fdcc9837bc631464f4`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_03.md`
- Notion review: https://app.notion.com/p/3d8833cb27ff812f8102dbc79891053e
- Phase 02 directive: https://app.notion.com/p/3d8833cb27ff810e858acd029ac0ea05
- Phase 02 report: https://app.notion.com/p/3d8833cb27ff817d9d01d754ec852c10
- Pull request: `#9 — DRAFT / OPEN / UNMERGED`
- GitHub issue: `#8 — OPEN`
- Required branch: `codex/p02-embodiment-001`
- Required worktree: local ext4/NVMe secondary worktree
- Phase 03 and later: `CLOSED`

## Completed gates

- Canonical ingest: `.agent/tasks/completed/COMPANION-P00-INGEST-001/`
- Linux environment evidence: `.agent/tasks/completed/COMPANION-P00-ENV-001/`
- Architecture v1.0: `.agent/tasks/completed/COMPANION-P00-ARCH-001/`
- Foundation technology qualification: `.agent/tasks/completed/COMPANION-P00-QUAL-001/`
- Roadmap Phase 01 engineering foundation: `.agent/tasks/completed/COMPANION-P01-FOUNDATION-001/`
- Phase 01 merge: `fc31717bba8c4833736d1792d7a5fe1c6cca4900`

## Review 03 boundary

Retained:

- exact approved references and verified hashes;
- final-tree removal of prior generated bulk outputs;
- deterministic generation infrastructure;
- focused Phase 02 and inherited Phase 01 workflow success;
- initial facing/time separation design.

Rejected as proof:

- `MON_BODY_SOURCE_V1` production-body status;
- authoring-method comparison;
- 26 articulated temporal drawings;
- gait/contact and orientation behavior;
- rendered root/contact validation;
- schema/Rust/generated-track/Godot equivalence;
- 24 Hz timing correctness;
- current headless playback proof;
- operator-review readiness.

## R03 required package

1. `MON_BODY_SOURCE_V2` as a complete editable Godot-native layered body with explicit anatomy, pivots, source traceability, and neutral front/profile/front-left masters.
2. Genuinely articulated front-left idle, eight-phase walk, front↔front-left orientation pair, and listen→acknowledge reaction.
3. Exact contract alignment across schema, Rust, generated track data, fixtures, and Godot.
4. Explicit 24 FPS and integer 1/24-second relative duration weights.
5. Source- or render-derived root, contact, orientation, and anatomy evidence with tamper negatives.
6. Normal-speed and quarter-speed motion artifacts, frame strips, silhouette playback, root/contact playback, and event logs.
7. Focused CI that exercises the actual tracks, fails on unexpected Godot errors, and keeps inherited Phase 01 CI green.
8. Operator and Architect review before full-library or all-direction expansion.

## Authoring decision

Use existing Godot 4.7.2 layered 2D source nodes, bounded Skeleton2D/Bone2D deformation, AnimationPlayer timing, and discrete replacement drawings where identity-critical deformation requires them. Bake deterministic `MON_FRAME_V1` raster frames. Runtime remains raster sprite-frame based.

## Artifact and environment boundary

Keep source, manifests, validators, hashes, and selected review derivatives in Git. Keep bulk frame and pack output in workflow/local artifacts. The final Openbox endurance gate remains deferred until the editable body and motion proof are approved.

## Capability boundary

## R02 required package

### Authority and evidence reset

- merge current `origin/main` normally;
- ingest and verify exact approved references;
- preserve current output as rejected/superseded evidence;
- remove bulk generated corpus/atlases/pack from the final tree;
- replace regex-guessed contract samples with committed fixtures;
- restore inherited Phase 01 CI.

### Embodiment canon

- explicit visual-authority precedence matrix;
- bounded vector/path versus layered-raster comparison;
- neutral front, profile, and front-left construction candidate;
- anatomy, palette, silhouette, root/contact, and source-traceability overlays;
- pinned deterministic export with two clean-process identical results.

### Minimal motion proof

- one 6-8 drawing front-left idle/breathe loop;
- one eight-drawing front-left walk loop with planted contacts;
- one three-drawing front↔front-left orient connector pair;
- one listen/acknowledge temporal reaction;
- 1x and 0.25x playback plus frame strips and root/contact overlays.

### Focused contract and runtime proof

- direction separated from temporal progression;
- concrete track key:
  `stage + body_revision + family + direction + posture + variant`;
- explicit 24 FPS and integer relative-duration ticks;
- observed frame, event, loop/completion, interruption, and degradation logs;
- actual accepted Phase 01 transport path where the bridge boundary is claimed.

### Focused CI and publication

- inherited Phase 01 workflow green;
- focused Phase 02 proof workflow green;
- source-derived QA and tamper-negative evidence;
- accessible named review artifacts;
- no full-library, target-endurance, or product claims.

## Operator gate

R02 stops for one operator decision:

1. approve or reject the production construction;
2. select the authoring path; and
3. approve or reject the motion language.

Only an approved result unlocks all-eight-direction core motion, remaining
semantic families, final atlas/pack production, live 10,000-case transition
qualification, and two-hour Openbox playback.

## Evidence law

Every accepted claim must include induced stimulus, raw observation,
independent derived assertion, and a negative or tamper case. Identifier/count
coverage, metadata equality, hard-coded zero counters, and self-reported
performance constants are not capability evidence.

## Artifact policy

The final Phase 02 tree keeps exact references, authored source, construction and
track specifications, manifests, validators, Godot resources, hashes, and
selected review derivatives. Bulk generated frames, duplicate runtime copies,
atlases, and packs are workflow/local/release artifacts. Do not configure Git
LFS or rewrite public branch history. Eventual acceptance uses a squash merge.

## Openbox qualification

Accepted environment evidence observed a 1366x768 output on logical X screen 1.
Use explicit X `display.screen` addressing, such as the authorized
environment-equivalent of `DISPLAY=:0.1`, before declaring the target absent.
Do not alter display, compositor, service, audio, or power configuration.

## Protected-work rule

Do not commit, discard, reset, overwrite, stash, reformat, read into evidence,
copy, or reinterpret the operator-owned primary-worktree modifications.

## Hard boundary

Godot remains presentation-only. No organism, memory, learning, dreaming,
camera, microphone, speech, model, biometric, contact, notification, care,
security-certification, product-reliability, medical, emergency, SLA, or Phase
03+ capability is established.

## Historical records

- `CURRENT.md` — mutable current state
- `DIRECTIVES.md` — directive history
- `OUTCOMES.md` — result/evidence history
- `LEARNINGS.md` — durable learnings
- `RECORD.md` — decisions/milestones/reversals
- `REPO_MAP.md` — repository ownership map
- `EXTERNAL.md` — external source dispositions

## Current Review 02 gate

`COMPANION-P02-EMBODIMENT-001` is in the exact-reference, production-canon,
and minimal temporal-motion proof gate. Use `assets/source/p02/canon/` and
`assets/source/p02/proof-motion/` as the current candidate authority. The old
directional catalogue and broad core pack are superseded evidence only. The
focused `phase02-canon-motion-proof` workflow is the relevant CI path; operator
visual approval is still required.

## R02 result routing

The current task-branch result is `3d2ce3c45e32a110520c9fd1378113216188fb8b`
after normal merge `6e16c25` of Architect Review 02. Use
`assets/source/p02/canon/`, `assets/source/p02/proof-motion/`, and
`assets/source/p02/review/r02/` for the bounded six-track/front-left proof.
Local headless Godot proof passed in a temporary copy; vector rasterization,
dedicated Openbox playback, and operator visual approval remain pending.
The branch is useful source-transfer and CI progress plus negative evidence. No production embodiment, continuous aliveness, or Phase 03+ capability is accepted.
