# EVIDENCE — COMPANION-P02-EMBODIMENT-001

## Source register

For every materially used external source or tool record title, owner, date,
URL, version/commit, integrity, license, maintenance, offline behavior,
transitive dependencies, evidence grade, established fact, limitation, project
inference, recommendation, and recheck trigger.

## Project evidence

Bind:

- reference files and hashes;
- construction source revision;
- authored source hashes;
- frame/landmark/clip manifests;
- rejected-frame records;
- pack/atlas hashes;
- QA reports;
- review-sheet hashes;
- Godot scene/resource hashes;
- contract fixtures/results;
- 10,000-case result;
- two-hour playback result;
- performance/memory result;
- CI runs/artifacts;
- export/restore result;
- final implementation commit and ancestry.

## Evidence ceiling

Separate direct observations, reproduced builds, target tests, operator visual
approval, hypotheses, and deferrals. Never treat generated art, automated QA, or
playback as operator approval or organism/product capability.

## Bound evidence package

- Reference metadata and inspected derivatives: `E1_OBSERVED`.
- Deterministic source/export/atlas/pack and automated QA: `E2_REPRODUCED`.
- Godot headless layered-avatar test and 10,000-case transition runner:
  `E3_TARGET_TESTED` (synthetic presentation only).
- Target-host Openbox habitat and two-hour playback: `NOT RUN` because the
  current session exposes a different display topology; no host settings were
  changed.
- Operator identity/motion approval: `PENDING`.

## Architect Review 01 correction evidence — 2026-09-11

The exact native references supplied through the Codex-accessible project
transfer were verified byte-for-byte before the new build:

- identity: `86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56`,
  1254×1254 RGBA;
- turnaround: `3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4`,
  1448×1086 RGB.

The previous 256-image directional catalog remains rejected historical
evidence.  The current candidate package is `MON_TEMPORAL_TRACKS_V1`: 66
independent tracks and 334 generated MON_FRAME_V1 drawings (166 byte-distinct
body outputs after duplicate removal), with idle A/B/C, walk, run, turn, and
focused proof tracks.  Direction is a track-selection key, not a temporal
frame index.  Core generation and validation are reproducible in private
outputs; the generated corpus and atlases are not part of ordinary Git.

The trim/extrude validator measured real 4 px reserved gutters and source
trim rectangles.  Automated rendered-pixel checks returned zero errors for
canvas, alpha, safety bounds, landmark root, and frame hashes.  These are
bounded `E2_REPRODUCED` candidate observations, not visual approval.

The dedicated Phase 02 workflow is now present but its hosted run and the
dedicated Openbox two-hour target run remain pending.  Godot headless playback
is not claimed locally because the exact 4.7.2 executable is not installed in
this worktree; the workflow stages it ephemerally after hash verification.

## Architect Review 02 — superseding bounded proof

Exact native reference evidence is directly available in Git and rechecked:
identity `86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56`
(1254×1254 RGBA) and turnaround
`3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4`
(1448×1086 RGB). The new `MON_BODY_SOURCE_V1` precedence model and six
front-left proof tracks are candidate evidence only. Two clean private builds
produced byte-identical output; `validate_motion_proof.py` passed with 6 tracks,
26 drawings, and 26 within-pack unique drawings. Review strips are committed
under `assets/source/p02/review/r02/` with hashes in their manifest.

The layered-raster candidate rendered the bounded proof. The layered-vector
candidate is explicitly `NOT_RUN_EXTERNAL_RASTERIZER_UNAVAILABLE` because
`resvg` is not installed; no dependency was adopted. Godot runtime event proof
and dedicated hosted workflow are pending execution, and operator visual
approval is not granted. The old 66-track/334-drawing and 32-family claims are
superseded as Phase 02 evidence.

## R03 correction evidence — 2026-09-11

### Reference and source

- Native identity reference SHA-256 `86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56` and turnaround SHA-256 `3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4` remain exact and unchanged.
- `MON_BODY_SOURCE_V2` is committed as JSON plus `godot/mon_body_source_v2.tscn`/`.gd`; the hierarchy contains bilateral arm/forearm/hand/finger01/finger02/thumb and thigh/lower-leg/foot/toe01/toe02/toe03 parts with pivots and source traceability.

### Rendered proof

- `build_r03_motion.py` produced five tracks and 28 deterministic 1024x1024 RGBA frames in `/tmp/companion-p02-r03-proof`; 25 frame pixel hashes are unique. A second clean build was byte-identical after timestamps were excluded from deterministic output.
- `validate_r03_motion.py` returned `PASS`. It checked Draft 2020-12 schema, frame hashes, root `[512,896]`, safety bounds, idle planted contacts, walk swing-foot displacement, facing endpoint differences, source-part coverage, 24 FPS, and track checksums.
- Tamper-negative mutations (root one pixel, duration zero, active-contact shift, endpoint hash reuse, missing bilateral digit) were each rejected.
- Review derivatives are normal and quarter-speed GIFs, silhouette and root/contact overlays, and ordered strips for all five tracks under `assets/source/p02/r03/review/`. They remain candidate art pending operator review.

### Godot and contracts

- `r03_temporal_playback_test.gd` loaded every actual generated PNG into `AnimatedSprite2D`, set animation speed to 24, applied integer duration ticks as relative weights, observed frame-change signals for every track, and checked once-track terminal state. It returned `PASS`; captured output contains no `ERROR:` lines and only expected Bone2D leaf warnings.
- `scripts/validate_schemas.py`, `scripts/check_contract_types.py`, `cargo fmt --all -- --check`, and `cargo test --workspace --locked` (with `R03_TRACKS_PATH` set) passed. Rust tests include generated-wrapper deserialization/re-serialization.

### Evidence ceiling and deferrals

These are bounded `E3_TARGET_TESTED` engineering observations. They do not
prove identity approval, production animation quality, full eight-direction or
32-family coverage, atlas/pack scale, Openbox behavior, runtime performance,
product capability, or any later roadmap phase. The full library and dedicated
Openbox endurance remain deferred until operator and Architect approval.
# R04 superseding evidence

The authoritative R04 evidence bundle is generated under
`experiments/p02-embodiment/results/r04/`. It binds exact approved-reference
hashes, byte-preserving source/CAS/runtime hashes, eight intake rejection
cases, required-path Rust round-trip results, Godot first-frame/event ordering,
corrupt-pack degradation/restoration, and local export/restore equivalence.
The validator consumes the result hashes and rejects semantic tampering.

R03 visual, rig, identity, and motion claims are `SUPERSEDED` and remain only
as negative evidence. R04 produces no production character pixels.

## R04 local and hosted result

- Implementation commit: `652cf24368ad8fab03c0439da7e3ca3a75638657`.
- Fail-closed CI correction: `7a79ddf9400a0d7cacd781d418fffdc625ec3c57`.
- Valid source intake: `PASSED`; both synthetic frames were byte-identical
  across input, CAS, and runtime copies.
- Negative intake cases: wrong dimensions, wrong mode, source-hash tamper,
  ineligible approval, missing landmark, contact tamper, duration tamper, and
  event-order tamper were each `REJECTED` for the expected reason.
- Actual generated-pack Rust round-trip: `PASSED`; missing required pack path
  returned nonzero.
- Godot: exact track selected, first frame observed before `started`, 24 Hz
  relative weights `[1,2]`, missing/ineligible/hash-corrupt rejection, and
  restoration recovery all `PASSED`; no unexpected `ERROR:` output.
- Evidence validator: `PASSED`; result-hash, byte-equality, rejection-reason,
  and event-order tampering each produced rejection.
- Clean-clone reproduction at implementation commit: `PASSED`; tracked diff
  remained empty.
- Focused Phase 02 hosted run `34656090767`: `PASSED`.
- Artifact `10285600941`,
  `phase02-embodiment-r04-e4ce8522624ac8e66cc727cb6d18d85b5b028903`,
  GitHub digest
  `sha256:39c56c9d43968e870005065b6bebf19700791986c017496b1ea5a03e0e14ff1f`.

Hosted run `34655914553` is preserved as a failed attempt: every substantive
R04 gate passed, but an over-broad historical private-path scan failed. Commit
`7a79ddf9400a0d7cacd781d418fffdc625ec3c57` scopes that check to the R04
surface and removes the hard-coded historical private path; it does not weaken
the source-intake or runtime gates.

Inherited Phase 01 run `34656090763` is also preserved as failed evidence. Its
resident closeout observed one `valid_ordinary_observation` as rejected because
the evidence loop could observe persistence before the companion process had
removed the shared marker file, permitting a later write/remove race. The
bounded correction requires both the exact event increment and marker removal
before another ordinary observation can be submitted. This tightens the
existing Phase 01 evidence barrier; it does not qualify the single-file handoff
as production sensor ingress. The corrected local 3,000-message matrix passed:
3,000 requested and observed, 396 accepted, 2,405 rejected, 199 duplicate,
zero invalid accepted, 2,802 care attempts, 198 care outcomes, and 198 ordinary
companion events with zero ordinary care rows.

Evidence ceiling remains `E3_TARGET_TESTED` for the synthetic intake/runtime
boundary. No production character pixels, accepted body, approved animation,
visual aliveness, target-host endurance, or Phase 02 acceptance is claimed.

## 2026-09-11 — R04-C01 authored-pack contract correction

Review 05 rejected the prior `READY_FOR_ARCHITECT_FRAME_PACK` claim because
orientation endpoints, occluded landmarks, request completeness, PNG profile,
identity/reuse rules, atomic publication, and runtime integrity were not
represented fail-closed. The correction adds separate source/ingested/receipt
schemas, typed Rust records, a bounded request-profile validator, direct PNG
IHDR/sRGB/alpha/safety checks, unique source identities, staged atomic intake,
pack and relationship verification in Godot, and a render-commit acknowledgment.

The synthetic fixture is intentionally geometric and is not candidate art. The
valid intake, ten negative cases, actual ingested-pack Rust round trip (including
nonzero missing-path failure), local export/restore, and Godot exact-track,
ineligible, corrupt, and recovery checks are bounded `E3_TARGET_TESTED`
evidence. No production frame pack, body, visual approval, or Phase 02
acceptance is inferred. R02/R03 visual assets and claims remain superseded.

## R04-C01 final evidence binding — 2026-09-12

Implementation commit: `04570503c957e34e2ddcf2f1ab1cb1151a352b59`; bundle
commit: `5d29b51e48073077abbdffad453226ce7e8cfddc`. Result files are hash-bound
in `experiments/p02-embodiment/results/r04/provenance.json` and the independent
validator returns `PASSED`; its tamper-negative mutations all return rejected.
Observed bundle timestamps are `2026-09-12T00:57:59.400413Z` through
`2026-09-12T00:58:02.880248Z`. Source fixture SHA-256 is
`2571a6c3069562900121902b074c374170c360d39ef9428a5d43c238383943d7` and
ingested fixture SHA-256 is
`01c88a1adadea41b5d9cbd7eb24c49208ad346475e58e6debda3d23ab9e49c2f`.
Evidence ceiling remains synthetic `E3_TARGET_TESTED`; no production art,
visual approval, or Phase 02 acceptance is inferred.

## R04-C02 request/profile correction — 2026-09-12

The executable request is now keyed by complete role tuples and matches the
published request: three `neutral_construction` roles (`front`, `right`, and
`front_left`), `idle_breathe/front_left`, `walk/front_left`, both orientation
connectors, and `listen_acknowledge/front_left`. The positive synthetic
`phase02_bounded_motion_proof_v1` pack contains 8 tracks and 31 calibration
frames. It exercises one valid same-track held drawing (`reuse_of` with the
same source hash and two ticks), an occluded profile eye landmark, and a
not-applicable object landmark. Intake is byte-preserving and fsync-backed;
an injected pre-rename failure leaves no output directory.

The C02 negative matrix rejects right/left profile mismatch, missing and
duplicate neutral roles, endpoint/facing and required-event errors, invalid
reuse, wrong dimensions/mode/hash, iCCP-only and duplicate-sRGB claims,
malformed chunk order, trailing PNG data, stale output, and injected
mid-intake failure. Schema and Python semantic validation pass. Rust and the
exact Godot 4.7.2 render-boundary run are `NOT RUN` in this checkout because
those executables are unavailable; no readiness or production claim is made.
The available Godot 4.6/Xvfb run was used only as a local syntax/behavior
smoke and is not evidence for the pinned 4.7.2 artifact.

## R04-C02 exact-tool evidence rerun — 2026-09-12

The private existing Rust 1.98.1 toolchain and transient official Godot 4.7.2
artifact were used without host modification. The full synthetic profile passed
locally through exact Rust typed round-trip and missing-path rejection, exact
Godot 4.7.2 playback with `RenderingServer.frame_post_draw`, first-frame event
order, 24 Hz weights, walk/listen markers, missing/ineligible/corrupt/recovery
cases, export/restore, and the 19-case intake negative matrix. The result
bundle was regenerated and `validate_r04_results.py --tamper-negative` returned
`PASSED`; all five mutations were rejected. Evidence remains synthetic and
bounded; hosted CI, remote publication, and Architect review are still needed.

## R04-C03 diagnostic-parity evidence — 2026-09-12

Review 07 was merged normally at `11e1139de780b44e37c6fa94f07e0ab8090ce7c1`.
The superseded hosted run did not retain its exact `ERROR:` line, so the line
cannot be reconstructed and no runtime change was made from speculation. The
new canonical runner is `scripts/run_godot_qualification.py`; each run writes
separate stdout, stderr, Godot `--log-file`, Xvfb wrapper, and structured
`result.json` outputs, with SHA-256 hashes and exact application error/warning
arrays. Local import/cold/warm runs used Godot
`4.7.2.stable.official.ed1daf0bf` under Xvfb/Mesa llvmpipe and recorded zero
Godot application `ERROR:` lines. The wrapper contained only xkbcomp warnings,
which remain separate diagnostics. Classifier tests passed for all seven cases,
including a synthetic stderr-only failure. Hosted cold/warm execution and its
always-published diagnostic artifact remain required evidence.

## R04-C03 final hosted evidence — 2026-09-12

The first C03 hosted run `34670268217` retained the exact diagnostic after the
upload-condition fix: `ERROR: Condition "status < 0" is true. Returning:
ERR_CANT_OPEN` at `drivers/alsa/audio_driver_alsa.cpp:97`, duplicated in
stdout and the Godot engine log, with empty stderr and separate Xvfb xkbcomp
warnings. This is a host audio-backend initialization diagnostic, not an image
fixture error. The canonical runner was then corrected to select Godot's
explicit `Dummy` audio driver while preserving fail-closed error classification.

At exact head `e022d18c59a836272e1470ae4905e10641abfea2`, Phase 02 run
`34670472778` passed import/cold/warm, semantic validation, policy checks, and
always-upload diagnostics; stability job `103491224017` passed again. Phase 01
rerun `34670472829` / job `103491215434` passed all inherited checks, including
the 3,000-cycle closeout. Cold/warm used Godot
`4.7.2.stable.official.ed1daf0bf`, exit `0`, zero application errors, and
`RenderingServer.frame_post_draw`. Cold hashes: stdout
`4951db8a7a462c908040e3c693ee2f25ad62b5f9eb34f12985d06565d21c5f70`, stderr
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, engine
`c540f86b2ae357057d13f35c647a211c72bfba004829b3b44536bb3e95e6eb9a`, Xvfb
`b987a262609a3720f450ab6815ed90b2069dd47b7b012959ca19c325aebf5d55`.
Published artifacts are `10290328716`
(`sha256:4d8685f808a3b0dcc74ecbb1e837fb7726fe689663dbe7a5ba3a1afc8319a651`)
and `10290383849`
(`sha256:5970ba4a5745f0a11e5368c7ae585ec2bece1fa48bc888be086237e0d2cc2dbf`).
Evidence remains bounded synthetic E3 target testing; no production art or
Phase 02 acceptance claim follows.

## R04-C04 readiness evidence — local

The inherited probe's one-shot startup decision was replaced by
`wait_for_stable_readiness()`. The predicate requires a live supervisor, all
five expected roles, every role ready and healthy, and synthetic care coverage.
The fixed timeout is 5,000 ms, the poll interval is 50 ms, and two consecutive
complete-ready samples are required. A local resident run returned `PASS` with
the socket observed at approximately 50 ms, all roles and readiness observed in
that sample, and stable readiness after a nonzero interval. The sanitized trace
contains only role names, booleans, care coverage, timing, and error classes;
the stderr tail was empty.

Focused synthetic tests returned delayed-ready `PASS` after four samples,
never-ready expected `FAIL` with `readiness_timeout`, and early supervisor exit
expected `FAIL` with `supervisor_exited_before_stable_readiness`. The local Rust
1.98.1 format, clippy, tests, and release build also pass. Full hosted exact-SHA
stability evidence remains required before this handoff is accepted.

## R04-C04 hosted exact-head evidence — 2026-09-12

The fixed readiness gate passed the initial hosted Phase 01 run
`34674883461` / job `103502845478`, same-head rerun #1 job `103503853827`,
and same-head rerun #2 job `103504776796`, all on
`e5f3bbb47f9f20d3e896956c9a1aabcd751cfd3b`. The exact same SHA passed Phase
02 run `34674883457` / job `103502845517`; artifact `10292635102` was
published with digest
`sha256:6efff4d21517c1983ddabfa86f9eaaf516ee60be0557625890d3ca7944f68fb8`.
Hosted evidence is E4 regression-protected for the readiness probe and E3
target-tested for the bounded phase result. No Phase 02 acceptance, production
art, operator visual approval, security certification, or reliability claim
follows.
