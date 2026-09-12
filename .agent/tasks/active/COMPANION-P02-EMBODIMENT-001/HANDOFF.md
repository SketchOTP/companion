# HANDOFF — COMPANION-P02-EMBODIMENT-001

## Latest disposition — operator rejection, 2026-09-12

R05-v1 visual review FAILED. All previews were rejected. Current work is PARTIAL:
preview timing and the cutout-provider adapter have focused regression tests,
but no replacement motion pack is ready. Read `R05_OPERATOR_REJECTION_01.md`
and `r05-v2-attempts.json`; do not request approval of old or new study images.
Previous handoffs below remain historical, not current visual acceptance.

Return the canonical result in this structure:

```text
# CODEX RESULT — COMPANION-P02-EMBODIMENT-001

## Verdict
## Retrieval confidence
## Protected-work verification
## Baseline / branch / worktree / PR state
## Reference-asset verification
## Construction model and candidate three-quarter views
## Authoring-pipeline decision
## Authored source and reproducibility result
## Animation-library coverage
## Unique-frame accounting
## Automated asset QA
## Visual QA and operator-review artifacts
## MonAvatar and layered-body result
## MonAnimationClip and animation-director result
## Embodiment intent/result bridge
## Habitat size, scale, screen, and recovery result
## Atlas and pack result
## 10,000-case intent/transition matrix
## Two-hour continuous playback result
## Performance and memory measurements
## Artifact/export/restore result
## CI and evidence validation
## Files and artifacts changed
## Dependencies and rights
## Failures and rejected assets
## Explicit deferrals
## Assumptions confirmed
## Assumptions disproven
## Deviations
## Notion publication
## GitHub publication
## Commits and remote equality
## Operator approvals required
## Recommendation to Architect
```

Include exact:

- branch base and every logical commit;
- reference/source/frame/pack/review/evidence hashes;
- clip/family/frame/direction/overlay counts;
- rejected and warning counts/reasons;
- selected habitat values;
- target-host performance distributions;
- transition and playback seeds/counts/events;
- CI run and artifact IDs;
- local export/restore result;
- repository binary payload;
- all non-passes and deferrals;
- PR and Issue #8 state;
- local/remote equality.

Do not state that the art, three-quarter views, animation library, or phase is
approved unless the operator and Architect explicitly approve it.

## R05-AUTHOR-001 bounded candidate handoff — 2026-09-12

The operator-authorized image-generation pass produced candidate pack
`05a17a00-0000-4000-8000-000000000001`, revision
`r05-author-001-bounded-v1`: 8 requested tracks, 33 frame occurrences, and 29
unique normalized frame hashes. Normal/quarter-speed, strip, silhouette, and
root/contact review media are committed and included in workflow artifact
`10298349112` (`sha256:9462bdb227d38b2d6051d6727bf4246b1d41f9bd6042305a1b422cead1ca945a`).

Local immutable intake, actual Rust 1.98.1 round-trip, exact Godot 4.7.2
import/cold/warm playback, rendered QA, export/restore, and tamper negatives
pass. After a first hosted run exposed an inherited 50 ms control-read race,
the scheduling-safe correction passed Phase 01 twice and Phase 02 twice on
exact head `b5c9e9a5e88de5fa08ec462bc209e7f24c909f1e`. The artwork remains
`candidate`; operator visual approval and Architect Phase 02 disposition are
required before scaling.

## R04 handoff contract

Return `CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R04` with the superseded
R03 paths, intake layout, Architect frame request, explicit schema/Rust type
inventory, source-preservation hashes, actual generated-pack Rust result,
Godot event order, failure/recovery matrix, hosted workflow/artifact IDs, and
final status `READY_FOR_ARCHITECT_FRAME_PACK`. Do not request visual approval;
no production frames have landed.

## Codex execution summary

The candidate implementation is ready for review with automated evidence, but
the phase is not self-accepted. Asset QA and the 10,000-case deterministic
transition matrix passed; the Godot 4.7.2 headless layered-avatar test passed.
The current session exposes two 3840×2160 X11 outputs with GNOME Shell/mutter,
not the dedicated Openbox target, so the required two-hour target-host run is
`NOT RUN`. New construction, diagonal views, frames, and motion remain pending
operator visual approval. No organism, memory, speech, perception, care, or
Phase 03+ capability was implemented or claimed.

## Reproducibility reconciliation — 2026-09-11

The pack writer now pins ZIP entry timestamps, platform metadata, and modes so
clean-room rebuilds are byte-identical. A clean-room rebuild and asset QA both
returned zero; the resulting pack SHA-256 is
`2ab74f5dbb56795a4807e837271ee8ad1eb14085e892f613604278e78ae6535f` and the
manifest SHA-256 is
`12e96358b1a8281950f8d2159cf30f6a924f5858d324d385c0f3d83e75b68a8f`.
The focused fix is published in commit
`6c81838899c943ea8d195230f9849140f0b54f5f`; target-host Openbox playback and
operator visual approval remain open gates.

The diagonal review-material correction is published at
`26571cbab782e5fc0ea712f577b8112767f05782`; the regenerated sheet contains all
four candidate views and the asset manifest remains green. Operator visual
approval and dedicated Openbox playback are still required.

## Architect Review 01 correction handoff — 2026-09-11

Exact native source transfer is now complete and verified:

- `assets/source/p02/references/identity-approved.png` — SHA-256
  `86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56`;
- `assets/source/p02/references/turnaround-approved.png` — SHA-256
  `3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4`.

New committed candidate sources are `construction_model_v2.json`,
`core-motion/temporal_tracks.json`, `core-motion/atlas_manifest.json`, and
`core-motion/manifest.json`.  The deterministic builder is
`experiments/p02-embodiment/scripts/build_core_motion.py`; the fail-closed
validator is `validate_core_motion.py`.  A fresh build produced 66 tracks and
334 drawings; the validator returned zero errors.  Full frames and atlas pages
are generated into private output and uploaded by
`.github/workflows/phase02-embodiment.yml`.

The Godot adapter now loads one temporal track per direction/family/posture/
variant, declares animation FPS 12, passes integer tick weights as relative
durations, emits observed frame/completion markers, and performs a bounded
BodyA/BodyB crossfade.  The package remains a visual candidate pending
operator and Architect review; no product capability is claimed.

## Architect Review 02 continuation handoff

The active result is now `MON_BODY_SOURCE_V1` plus a bounded
`MON_TEMPORAL_PROOF_V1` candidate: one `front_left` facing, six tracks, and 26
temporal drawings. Exact native reference hashes are bound in the canon and
proof manifests. Two clean private builds are byte-identical and the fail-closed
proof validator passes rendered canvas/root/safety checks. Review derivatives and
source files are committed under `assets/source/p02/canon/` and
`assets/source/p02/review/r02/`.

The raster candidate rendered; the vector candidate is explicitly unrun because
the host has no `resvg` rasterizer. The focused workflow stages the proof output
and exact Godot artifact in CI. Godot playback was not run locally because the
executable is absent, and the dedicated Openbox target remains unavailable.
Operator visual approval is the next gate; do not scale to eight directions or
the complete family library before that decision.

## R02 execution correction — 2026-09-11

The exact Godot 4.7.2 artifact was downloaded only to a private temporary
directory, hash-verified, and run in a temporary project copy with the
headless proof test; the observed result was `STATUS=0` with zero errors,
five frame markers, and one completion. This does not establish target-host
Openbox playback or visual approval. The committed focused workflow remains
the reproducibility path; no downloaded binary or generated full-frame corpus
is part of the repository tree.

Correction publication: `3d2ce3c45e32a110520c9fd1378113216188fb8b`, following
normal merge `6e16c25` of Architect Review 02 (`origin/main`
`7709aba7a777ab611da56a8e340f6bd17f7bf5b1`). The task branch remote equals
this head. PR #9 remains draft/open/unmerged and Issue #8 remains open.

## R03 correction handoff — 2026-09-11

Architect Review 03 is continued after normal merge
`77ebc5c19285d97c467caedbcb3f7c3be083a4a0`. The correction adds
`MON_BODY_SOURCE_V2` with an explicit editable Godot part hierarchy, a
deterministic part-pose raster bake, and five candidate temporal tracks:
`idle_breathe` (6), `walk` (8), two facing connectors (4 each), and
`listen_acknowledge` (6). The generated result contains 28 full-canvas frames
in private output with 25 unique pixel hashes; selected normal/quarter-speed,
silhouette, root/contact, and ordered-strip derivatives are committed under
`assets/source/p02/r03/review/`.

The v2 Draft 2020-12 track schema, Rust `MonTemporalTrackV2` type, committed
fixture, generated manifest, and Godot loader agree on facing as selection,
24 FPS, and integer relative duration weights. `validate_r03_motion.py` derives
root, contacts, safety bounds, source anatomy, checksums, temporal change, and
schema results and passes five deterministic tamper-negative mutations. The
Godot headless probe loads every generated PNG into `AnimatedSprite2D`, observes
actual frame-change signals for every track, checks 24 FPS configuration and
terminal playback state, and rejects a missing track; no `ERROR:` output was
observed. Godot emitted Bone2D leaf warnings only.

This remains a candidate proof, not operator or Architect approval. The Python
bake is explicitly a qualification-only mirror of the editable Godot source
because the dummy renderer cannot expose a readable SubViewport texture. Full
library, all-direction production, final atlas/pack scale, two-hour Openbox
playback, and operator visual approval remain deferred. Protected primary
`.gitignore`/`AGENTS.md` changes remain untouched.

## R03 publication reconciliation — 2026-09-11

The R03 candidate is published at `448ea93bb53f2f4f1742b5fdcc9837bc631464f4`,
after the normal Architect-review merge `77ebc5c19285d97c467caedbcb3f7c3be083a4a0`.
The remote task branch must remain equal to this candidate head. PR #9 remains
draft/open/unmerged and Issue #8 remains open; no visual approval or Phase 02
acceptance is claimed.

## Hosted CI correction — 2026-09-11

After publication, hosted runs exposed that the shared contract closeout did
not map the v2 temporal-track fixture, causing a false workflow failure. The
narrow fix `83909a894ad47e101bcf369b707f636624302a52` adds that mapping without
changing product scope. Focused Phase 02 run `34631901926` and inherited Phase
01 run `34631901998` now complete successfully. This does not change the
candidate-only visual or Openbox gates.

## R04 implementation handoff — 2026-09-11

Review 04 was incorporated by normal merge
`928ba4b8e52b8cadb9c8861ad066d2d8a91366a4`. Implementation commit
`652cf24368ad8fab03c0439da7e3ca3a75638657` and fail-closed CI correction
`7a79ddf9400a0d7cacd781d418fffdc625ec3c57` replace procedural production-art
selection with an immutable Architect-authored frame-pack boundary.

The landing contract is
`assets/source/p02/architect-frame-request-v1/ARCHITECT_FRAME_REQUEST_V1.md`;
the schema is `contracts/schemas/mon-authored-frame-pack-v1.schema.json`; the
evidence bundle is `experiments/p02-embodiment/results/r04/`. Exact source bytes
are copied into content-addressed and runtime locations without mutation.
Production packaging permits only `operator_approved`; review and synthetic
test operations are explicit. Rust validation requires the generated path.
Godot resolves and validates the exact track, loads and observes frame zero,
and only then emits `started`.

Focused hosted run `34656090767` passed and published artifact `10285600941`
with GitHub digest
`sha256:39c56c9d43968e870005065b6bebf19700791986c017496b1ea5a03e0e14ff1f`.
The inherited Phase 01 exact-head run must also complete successfully before
external handoff. PR #9 remains draft/open/unmerged and Issue #8 remains open.
No visual approval is requested. Subject to final exact-head validation and
publication, the bounded status is `READY_FOR_ARCHITECT_FRAME_PACK`.

## R04-C01 handoff

Review 05 is addressed by the source/ingested/receipt contract split and the
strongly typed authored-frame boundary documented in `R04_C01_CONTRACT.md`.
The Architect landing request is machine-checkable, while the only generated
pack is the synthetic `synthetic_r04_test_v1` calibration fixture. The intake
proves source-to-CAS/runtime byte equality and atomic publication; Rust consumes
the actual ingested `pack.json`; Godot validates the derived pack and observes
`first_frame_render_committed` before the director emits `started`. Negative
cases cover malformed source, hash, approval, landmark, contact, timing/event,
duplicate-asset, and missing-sRGB inputs. The result is bounded engineering
evidence only. After exact-head checks and publication, report exactly
`READY_FOR_ARCHITECT_FRAME_PACK`, leave PR #9 draft/open/unmerged and Issue #8
open, and stop for Architect review.

## Final R04-C01 publication — 2026-09-12

The focused implementation is `04570503c957e34e2ddcf2f1ab1cb1151a352b59` and
the committed sanitized bundle is `5d29b51e48073077abbdffad453226ce7e8cfddc`.
Local validation passed: schema/crosswalk, 20-case intake negatives, actual
generated-pack Rust round trip plus missing-path failure, Godot exact-track
playback and render-commit event order, export/restore, tamper negatives, and
the inherited 3,000-cycle Phase 01 regression (seeds 17/23/41; 309.685 s).
The final handoff is `READY_FOR_ARCHITECT_FRAME_PACK`. PR #9 remains
draft/open/unmerged and Issue #8 remains open; Architect and operator visual
approval are still required before any production frame pack is accepted.

## R04-C02 handoff — 2026-09-12

The C02 correction aligns the human and executable request and produces one
complete synthetic bounded profile (`phase02_bounded_motion_proof_v1`, 8
tracks, 31 frames). No production character pixels were generated. The
positive source pack passes Python schema/semantic validation, immutable
content-addressed intake, byte equality, local export/restore, and the full
19-case negative matrix. PNG checks now require one IHDR, RGBA8, zero
compression/filter/interlace flags, one explicit sRGB chunk, one terminal
IEND, and no trailing bytes. Intake fsyncs files/directories and uses a
same-filesystem atomic rename; the injected mid-intake failure leaves no
publishable destination.

The available local environment has neither Rust 1.98.1 nor the exact Godot
4.7.2 binary, so actual Rust round-trip and pinned Godot render-boundary gates
are `NOT RUN`/`BLOCKED`. A Godot 4.6 Xvfb smoke was not promoted to evidence.
The bounded status therefore remains `BLOCKED` pending hosted exact-tool
execution; `READY_FOR_ARCHITECT_FRAME_PACK` is not claimed. Phase 01 remains
accepted, Phase 02 remains active/unaccepted, PR #9 remains draft/open/unmerged,
and Issue #8 remains open.

## R04-C02 exact-tool rerun — 2026-09-12

The private Rust 1.98.1 toolchain and transient official Godot 4.7.2 artifact
were executed without system modification. The regenerated complete synthetic
profile passes exact Rust and Godot gates locally: 8 tracks/31 frames, typed
round-trip, missing-path failure, frame-post-draw observation, exact event and
24 Hz timing checks, corruption/ineligible/missing-track rejection, recovery,
export/restore, and 19 intake negatives. The independent validator passes with
all five tamper-negative mutations rejected. Hosted CI and remote publication
remain pending; no production or Phase 02 acceptance claim is made.

## R04-C03 diagnostic-parity handoff

The active correction uses one canonical runner for workflow and evidence
generation: `experiments/p02-embodiment/scripts/run_godot_qualification.py`.
It runs controlled import followed by consecutive cold/warm invocations and
retains `godot.stdout.log`, `godot.stderr.log`, `godot.engine.log`,
`xvfb-wrapper.log`, and `result.json` with exact version, exit code, display /
renderer summary, sanitized command, pack digest, channel hashes, exact error
and warning lines, wrapper diagnostics, cache digests, and semantic JSON.
Application `ERROR:` lines fail the single classifier; Xvfb warnings never enter
that channel. The local classifier matrix and Rust-backed C02 result validator
pass. The prior hosted exact line was lost by the superseded workflow, so the
first C03 hosted run must capture and publish it even on failure. Readiness is
not claimed until hosted cold/warm and one stability rerun are green. PR #9 and
Issue #8 remain open; Phase 02 remains unaccepted and no production art was
generated.

## R04-C03 final handoff — 2026-09-12

Normal authority merge is `8523692` from `origin/main`
`11e1139de780b44e37c6fa94f07e0ab8090ce7c1`. Correction commits are
`1a1dab092fc2b3051aba7eb39a251fbb4dea242b`,
`5e7edb105a2a1ac5e390018ee514c136543edbf6`, and
`e022d18c59a836272e1470ae4905e10641abfea2`; final local and remote task head
is `e022d18c59a836272e1470ae4905e10641abfea2`.

The superseded hosted run `34670268217` captured
`ERROR: Condition "status < 0" is true. Returning: ERR_CANT_OPEN` at
`drivers/alsa/audio_driver_alsa.cpp:97`; it was an ALSA initialization
diagnostic duplicated in stdout and the engine log, with empty stderr and
separate Xvfb warnings. The canonical runner now explicitly selects
`--audio-driver Dummy` and retains strict application-error classification.

Hosted Phase 02 run `34670472778` passed canonical import/cold/warm,
validation, and policy checks; stability job `103491224017` passed again.
Hosted Phase 01 rerun `34670472829` / job `103491215434` passed all checks.
Diagnostic artifacts: `10290328716`
(`sha256:4d8685f808a3b0dcc74ecbb1e837fb7726fe689663dbe7a5ba3a1afc8319a651`)
and `10290383849`
(`sha256:5970ba4a5745f0a11e5368c7ae585ec2bece1fa48bc888be086237e0d2cc2dbf`).
Local canonical evidence and tamper-negative validation pass. The bounded
handoff is `READY_FOR_ARCHITECT_FRAME_PACK`; this is not Phase 02 acceptance,
operator visual approval, or a production-art claim. PR #9 remains
draft/open/unmerged and Issue #8 remains open.

## R04-C04 readiness handoff update — 2026-09-12

Review 08 was merged normally in `e9915015a4df69f1af895ae33cefc97a7440c218`.
The only implementation change is the inherited Phase 01 readiness gate:
socket creation is now merely observed, explicit health is polled on a fixed
monotonic deadline, and stable readiness requires two complete samples separated
by a nonzero interval. The result contains the required sanitized startup trace,
timing fields, terminal reason, and bounded stderr tail. Focused synthetic tests
cover delayed convergence, deadline failure, and supervisor exit.

Local exact Rust checks and the resident probe pass. The final handoff remains
pending the required three same-head hosted Phase 01 passes and same-head Phase
02 pass. No production art, operator visual approval, or Phase 02 acceptance is
claimed.

## R04-C04 handoff — complete

Candidate SHA `e5f3bbb47f9f20d3e896956c9a1aabcd751cfd3b` passed hosted Phase 01
initial run `34674883461` / job `103502845478`, rerun #1 job `103503853827`,
and rerun #2 job `103504776796`. Phase 02 passed on the same SHA in run
`34674883457` / job `103502845517`; artifact `10292635102` is published with
digest `sha256:6efff4d21517c1983ddabfa86f9eaaf516ee60be0557625890d3ca7944f68fb8`.
The exact bounded status is `READY_FOR_ARCHITECT_FRAME_PACK`. This does not
accept Phase 02, approve visual identity, or authorize production art.

## R05-AUTHOR-001 candidate handoff

The bounded operator-review package is 8 tracks / 33 frame occurrences / 29
unique source hashes. Its image-generation sheets, source hashes, rejected
generations, deterministic MON_FRAME_V1 builder, source-pack manifest, selected
normal/quarter/silhouette/root-contact/strip media, and sanitized local evidence
are committed. Full normalized and ingested packs remain artifact output.

Local immutable intake, Rust 1.98.1, exact Godot 4.7.2 import/cold/warm playback,
rendered QA, export/restore, and five tamper negatives pass. All art remains
`candidate`; the operator must decide identity fidelity, anatomy, proportions,
gait/motion quality, facing transition, and listen/acknowledge readability.
Hosted exact-head CI and artifact publication remain required before the final
R05 return.

## 2026-09-12 — AUTHOR-002 superseding handoff

BLOCKED at Review11 anatomical key gate. Read R05_AUTHOR_002_KEY_GATE_RESULT.md
and R05_AUTHOR_002_STUDY_RESULTS.json before acting on any earlier completion
claim. 25 generated studies, zero promoted frames. Eight facings are provisional;
complete actions, v2 integration and contact QA NOT RUN. Do not request visual
approval. PR9 remains draft/open/unmerged; Issue8 remains open.
