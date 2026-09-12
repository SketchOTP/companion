# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001

## Objective

Complete Roadmap Phase 02 in one phase-sized implementation run. Deliver the
identity-locked mon body, deterministic sprite authoring/export/packaging
pipeline, substantial initial animation library, layered Godot avatar, semantic
animation director, bounded Openbox habitat behavior, automated/visual QA,
versioned artifacts, and target-host playback evidence.

This is not a scaffolding, static-sprite, one-idle-loop, or placeholder task.
Continue through internal commits until the full phase candidate is published or
one genuine stop condition is proven.

## Why this is next

Roadmap Phase 01 is accepted at the engineering-foundation boundary. The
largest next end-goal gap is visible embodiment: one stable creature identity,
controlled asset production, smooth causal animation, and a body-neutral Godot
adapter ready for later organism intents.

## Authoritative basis

Fetch and read the complete live content of:

- Canonical project:
  https://app.notion.com/p/3d5833cb27ff8196814fdbae282f15ad
- Complete end goal:
  https://app.notion.com/p/3d5833cb27ff81b09c20e2b52d537e1e
- Master roadmap:
  https://app.notion.com/p/3d5833cb27ff81dd88faeb0c95b6f44e
- Governance contract:
  https://app.notion.com/p/3d5833cb27ff81e2b3b2eabc70f9f6b3
- Architecture v1.0:
  https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Phase 01 acceptance:
  https://app.notion.com/p/3d8833cb27ff813a96e2f9d7b27b009f
- Approved visual bible:
  https://app.notion.com/p/3d5833cb27ff8108a3acf202fc268b6d
- R04 embodiment dossier:
  https://app.notion.com/p/3d5833cb27ff81d79680f362491287a7
- R10 sprite production contract:
  https://app.notion.com/p/3d5833cb27ff81989d95f604112e25ba
- Phase 02 directive:
  https://app.notion.com/p/3d8833cb27ff810e858acd029ac0ea05
- Phase 02 report:
  https://app.notion.com/p/3d8833cb27ff817d9d01d754ec852c10
- GitHub Issue #8:
  https://github.com/SketchOTP/companion/issues/8

Query the live Architecture Decision Ledger and Research Evidence Register.
Verify the Phase 01 acceptance and generated-asset storage records by exact ID,
title, status, rationale, consequence, and review trigger.

Directly inspect both approved visual attachments. Do not rely on descriptions:

1. `mon.visual_reference.v1` identity master.
2. `mon.turnaround_reference.v1` six-view reference.

Refresh the Notion page if signed attachment URLs expire.

## Known evidence

- Phase 01 merge baseline:
  `fc31717bba8c4833736d1792d7a5fe1c6cca4900`.
- Exact Godot: `4.7.2.stable.official.ed1daf0bf`.
- Habitat: bounded resizable Godot window on the dedicated 1366×768
  Openbox-managed output.
- Godot is a nonauthoritative body adapter.
- Phase 01 does not establish an organism, production sensor ingress, complete
  display recovery, security certification, or product reliability.

## Fixed visual identity

Preserve without exception unless the operator explicitly approves a revision:

- Original purple mon.
- Simple rounded unclothed body.
- Edge-spiked flame-shaped head.
- Black eye fields with white pupils.
- Small simple mouth.
- Exactly two fingers plus one thumb per hand.
- Exactly three toes per foot.
- Flat clean cel shading and controlled purple shadows.
- Transparent source-sprite background.
- No default clothing, accessories, symbols, patterns, muzzle, nose, teeth,
  horns, ears, extra anatomy, realistic musculature, painterly/3D/pixel-art
  treatment, or environment baked into a sprite.

## MON_FRAME_V1

- 1024×1024 source canvas.
- 8-bit RGBA PNG, sRGB, transparent background.
- Root `(512,896)`.
- Ground baseline `y=896`.
- Drawable safety region `x=64..960`, `y=32..960`.
- Source crop prohibited.
- Encoded screen translation prohibited.
- Root drift `0 px`.
- Planted-contact drift `<=2 px` unless explicitly dispositioned.
- Frame durations are integer multiples of `1/24 s`.
- Default body cadence: 12 drawings/s on the 24 Hz grid.
- Uniform runtime scaling only.

## Asset repository policy

Commit approved references, authored vector/pose/keyframe sources, clip specs,
manifests, validators, build tools, Godot resources, hashes, and selected review
derivatives. Generate the complete 1024×1024 PNG corpus and atlas packs
reproducibly and publish them as versioned artifacts/local export bundles rather
than inflating ordinary Git history.

Do not configure Git LFS. Do not commit an ordinary-Git binary over 25 MiB. Keep
the total new ordinary-Git binary payload below 100 MiB unless the Architect
explicitly approves otherwise.

## Scope

### 1. Authority and reference package

- Reconstruct current Git/Notion authority.
- Retrieve exact approved native references where possible.
- Verify their declared SHA-256 values and dimensions.
- Preserve canonical originals without recompression.
- Commit manifests with IDs, hashes, source authority, approval state, format,
  dimensions, transparency, and rights.
- Stop rather than substitute if a required reference is unavailable or its
  digest disagrees.

### 2. Construction model

Create an original project-authored construction model defining:

- Proportion grid and ratios.
- Palette and named color roles.
- Line/edge and shadow rules.
- Stable head-spike map and silhouette landmarks.
- Eye/pupil/mouth construction.
- Hand/finger/thumb and foot/toe construction.
- Root, baseline, shadow footprint, and attachment points.
- Squash/stretch/tilt/overlap/perspective limits.
- Correspondence across front/back/left/right/top/bottom.
- Candidate front-left/front-right/back-left/back-right views.

Generate reviewable construction, anatomy/palette, and eight-direction sheets.
The four three-quarter views are candidates until operator approval.

### 3. Authoring pipeline

Compare at least:

- layered vector/shape source with deterministic raster export;
- full-frame raster keyposes with controlled reference-based in-betweens.

Select the smallest identity-faithful deterministic pipeline. The authoring rig
may be vector-based, but runtime body animation must use raster sprite frames;
runtime skeletal deformation may not replace the requested frame library.

Implement:

- source-part or keypose library;
- per-frame pose/in-between definitions;
- deterministic MON_FRAME_V1 export;
- landmark sidecars;
- clip manifests;
- event/contact/timing tracks;
- alpha cleanup;
- lossless trim/extrude/atlas packaging;
- reproducible pack hashes;
- clean-room rebuild.

Prefer Godot-native or already-authorized tooling. Any new authoring-only tool
must be current, exact, locked, rights-reviewed, offline-capable after retrieval,
and must not become a runtime dependency by implication.

### 4. MonAnimationClip contract

Implement one versioned clip representation with:

- stable clip ID/version;
- body revision/stage;
- direction;
- start/end posture;
- behavior/action tags;
- affect/energy compatibility;
- loop mode/seam;
- per-frame durations;
- root-motion policy/expected node velocity;
- landmarks/contact spans;
- entry/exit connectors;
- interruptible ranges;
- event markers;
- overlays;
- repeat bounds/cooldown/rarity/recent-use suppression;
- pack/source revision/checksum.

Provide schema, Rust type, Godot resource/import form, fixtures, negative tests,
version/migration policy, and semantic drift validation.

### 5. Substantial initial library

Deliver at least:

- 32 semantic clip families;
- 256 unique authored body-frame sources after exact-duplicate removal,
  excluding eye/mouth overlays;
- eight manifest direction identifiers;
- full eight-direction coverage for neutral idle/breath, orient/turn, walk, and
  run;
- declared direction coverage and legal fallback for all other clips;
- 24 eye/gaze/blink overlays;
- 8 mouth-shape overlays;
- 3 materially different variants of the highest-frequency idle state.

Do not count global translation, uniform scale, metadata-only changes, exact
pixel duplicates, unapproved mirrored duplicates, or repeated held frames as
unique authored body frames.

Required behavior families include:

- idle/breath/blink/gaze;
- orientation and cardinal↔diagonal connectors;
- listen/think/acknowledge/speak-neutral/interrupted;
- greet-known presentation and observe-unknown presentation, without identity
  recognition;
- sit/lie/sleep/neutral-dream/wake/stretch;
- walk/run/hop/approach/retreat/stop;
- curiosity/inspect/hesitate/refuse/surprise/calm-joy/disappointment/tired/
  bored/attention-seek/self-play/practice/success/failure/goal-resume;
- sensor-degraded presentation;
- calm care check-in presentation without care policy.

Quality and transition coverage outrank decorative count.

### 6. Layered Godot body

Create:

```text
MonAvatar
├── Shadow
├── AccessoryBack
├── BodyA
├── BodyB
├── FaceOrEyes
├── MouthViseme
├── HeldObject
├── AccessoryFront
├── Effects
├── AnimationPlayer
└── MonAnimationDirector
```

Requirements:

- runtime raster frames and external SpriteFrames/clip resources;
- deterministic clip choice for tests;
- variation/recent-use suppression for normal mode;
- legal transition graph;
- authored transitions for incompatible silhouettes;
- interrupt/continuation behavior;
- frame events/contact/footfall markers;
- controlled BodyA/BodyB handoff;
- missing/corrupt pack degradation;
- no canonical organism, memory, identity, consent, secret, contact, or safety
  state in Godot.

### 7. Embodiment bridge

Use versioned local messages for:

- embodiment intent;
- acknowledgment;
- clip started;
- frame/event marker;
- interrupted;
- completed;
- failed/degraded;
- current visible body state.

Godot reports execution, not real-world action success. The bridge translates;
it does not choose organism goals or own creature truth.

### 8. Habitat

Explicitly select and test:

- initial/minimum/maximum window size;
- initial position;
- logical content base size;
- content scale mode/aspect/filter;
- mon runtime scale range;
- target screen/output;
- geometry persistence;
- visible-area clamping;
- resize behavior;
- focus/input policy;
- safe missing-output fallback;
- bridge/Godot restart reconnect;
- simulated topology loss/restoration.

Do not rely on Godot defaults. Physical hot-unplug remains deferred unless safe.

### 9. Packs and atlases

- Partition by stage/body revision/direction/behavior.
- Boot-critical synchronous pack.
- Likely-next asynchronous preload.
- Atlas pages <=4096×4096.
- >=4 px gutter/extrusion.
- Lossless initial import.
- Reconstruct source placement after trim.
- Mipmaps off unless evidence justifies them.
- Exact source→frame→clip→atlas→pack traceability.
- Detect missing/corrupt packs.
- Deterministic names/hashes.
- Local export and restore independent of GitHub.

### 10. Automated QA

Fail on:

- wrong canvas/bit depth/color/alpha;
- opaque source background;
- invalid/duplicate IDs;
- missing manifest/landmarks;
- root drift;
- safety-region overflow;
- invalid contacts/timing/frame numbering;
- illegal connectors;
- broken references/checksums;
- atlas overlap/gutter/bounds/bleed;
- duplicate frames counted as unique;
- untraceable source revision.

Warn and require disposition for near duplicates, centroid/area jumps,
eye/head jumps, palette drift, loop seam discontinuity, anatomy mismatch, alpha
halos, and excessive size/load/memory.

### 11. Visual review package

Generate from project-created assets only:

- identity/construction sheet;
- eight-direction sheet;
- palette/anatomy sheet;
- per-family contact sheets;
- transition sheet;
- eye/mouth overlay sheet;
- atlas/debug sheet;
- Godot viewport-only habitat stills;
- short motion artifact when an existing, provenance-recorded encoder is
  available, otherwise frame strips plus deterministic Godot playback.

Attach primary review files to the Notion result. Label previously approved
references, new construction candidates, new production candidates, automated
status, and operator approval state separately. Codex cannot self-approve art.

### 12. Performance and endurance

Run:

- >=10,000 deterministic semantic-intent/transition cases across retained seeds;
- >=2 hours continuously animated on the target host using one Godot process
  and one resident foundation instance.

During the playback run: resize, switch packs, interrupt clips, restart bridge,
exercise missing-pack degradation/recovery, and simulate target-display
loss/restoration.

Measure p50/p95/p99:

- frame time;
- pack load latency;
- intent/result latency;
- memory/resource growth.

Pass floors:

- zero invalid resource reference;
- zero root drift;
- zero safety-region overflow;
- zero illegal transition;
- zero unrecovered bridge disconnect;
- zero unbounded memory growth from pack switching;
- no post-warmup runtime pack-load stall >100 ms;
- no checkout/SSHFS runtime-state write;
- no embodiment AF_INET/AF_INET6 socket.

This is bounded engineering evidence, not product reliability.

### 13. CI and artifacts

CI must validate:

- authoritative reference hashes;
- source/manifest/clip schemas;
- frame generation and deterministic rebuild;
- automated frame QA;
- unique-frame accounting;
- atlas packaging;
- Godot import/headless playback;
- intent/result contracts;
- transition matrix;
- binary/repository budget;
- secrets/forbidden assets;
- evidence bundle and tamper-negative validation.

Publish versioned CI artifacts for full PNG frames, runtime packs, contact sheets,
motion review, QA, and performance results. Commit only the source, metadata,
selected review derivatives, and evidence allowed by the binary budget.

## Do not change

- Architecture v1.0 ownership.
- Companion/care separation.
- Godot 4.7.2.
- Bounded resizable Openbox habitat.
- Approved identity/anatomy.
- MON_FRAME_V1.
- Rust authoritative-service direction.
- Local XDG storage.
- Phase 01 evidence history.
- Protected primary SSHFS worktree.

## Required investigation

Before bulk production, record:

- exact reference retrieval/hash status;
- smallest identity-faithful authoring representation;
- derivation/review path for four three-quarter views;
- Godot PNG/SVG import and alpha-edge behavior;
- filtering/scaling quality at target sizes;
- atlas gutter/trim reconstruction;
- projected source/artifact/repository size;
- available optional encoders/tools;
- telemetry/cloud/license/reproducibility risks.

## External discovery

Use current primary sources. Recheck Godot 4.7 AnimatedSprite2D, SpriteFrames,
animation state APIs, import settings, window/screen/scaling, and GitHub binary
artifact guidance. Record exact source, version, integrity, license, maintenance,
offline behavior, transitive dependencies, and replacement cost for every new
tool.

## Authority boundaries

- companion-core requests body-neutral intents later; it does not choose files;
- Godot owns only current render/animation execution;
- godot-bridge translates/reports only;
- care-core is unaffected by animation/mood/effects;
- check-in presentation cannot create an incident;
- generation tools do not own canonical identity;
- asset manifests are not organism state or memory.

## Acceptance criteria

1. Exact references preserved or blocked before substitution.
2. Construction/palette/anatomy sheets and candidate diagonal views published.
3. Deterministic MON_FRAME_V1 rebuild from committed sources.
4. >=32 clip families and >=256 unique body-frame sources.
5. Required eight-direction coverage.
6. Eye and mouth overlay floors.
7. Canvas/root/alpha/region/timing/naming/landmark/checksum traceability pass.
8. Contacts, loops, transitions pass automated and visual QA.
9. Clip schema/Rust/Godot agreement.
10. Layered avatar/director consume semantic intents without organism logic.
11. Versioned bridge events/results work.
12. Explicit bounded Openbox size/scale/screen/persistence/fallback policy.
13. Pack loading has no broken references or unbounded stalls.
14. Generated packs reproduce and validate.
15. Visual review materials are attached and inspectable.
16. 10,000-case matrix passes.
17. Two-hour playback passes bounded criteria.
18. CI and artifact publication pass.
19. Local export/restore passes.
20. Notion/GitHub/PR/issue/artifact state agrees.
21. No Phase 03+ capability or claim.
22. Operator approval is pending or explicitly recorded, never self-asserted.

## Required validation

Report each as `PASSED`, `FAILED`, `BLOCKED`, `NOT RUN`, or `NOT APPLICABLE`.
At minimum validate protected work; reference hashes; rights; construction;
palette/anatomy/head silhouette; MON_FRAME_V1; landmarks; unique counts; timing;
contacts; loops; transition graph; clip contract; required coverage; layers;
intent/result; interrupt/continuation; pack degradation; atlases; reproducible
build; export/restore; explicit scaling/filter/screen/window; topology/reconnect;
Godot headless/target-host playback; 10,000 matrix; two-hour playback; frame/load/
memory latency; no checkout/SSHFS write; no network socket; binary budget;
artifacts/hashes; CI; evidence/tamper-negative; Notion attachments; PR/issue; and
Phase 03 closure.

## Prohibited implementation and claims

Do not implement or claim organism needs/drives/goals/personality/autonomy,
autobiographical memory, learning, development, dreaming, camera/microphone,
VAD/STT/TTS, model inference, biometrics, contacts, notifications, spoken-help,
live care, medical/emergency capability, security certification, production
reliability/lifetime/SLA, or Phase 03+ completion.

Do not configure Git LFS, use root/sudo, install system packages, modify host
displays/audio/services/power, or alter Godot 4.6.

## Stop and return to Architect if

Stop only when approved references cannot be retrieved/verified, available tools
cannot produce identity-faithful rights-cleared frames, a required tool falls
outside authority, diagonal construction drifts materially, MON_FRAME_V1 cannot
be generated/validated, Godot cannot import/play without architecture change,
artifact budget cannot be met, target testing would be unsafe, authority
conflicts, or protected work cannot remain untouched.

Return the single blocker, attempted alternatives, exact evidence, and minimum
Architect decision. Do not return avoidable broad questions.

## Required project updates

Complete the active packet, `.agent/CURRENT.md`, `.agent/INDEX.md`, append-only
ledgers, Notion result/directive, PR, Issue #8, visual attachments, artifact
manifests, and evidence. Preserve rejected art and failed approaches. Re-fetch
mutable records. Leave PR and issue open. Stop for Architect and operator visual
review.

## Required handoff

Return `CODEX RESULT — COMPANION-P02-EMBODIMENT-001` with retrieval/protected
work; baseline/branch/PR; reference hashes; construction and diagonal views;
pipeline decision; authored-source/reproducibility; clip/frame/direction counts;
QA/rejected assets; visual attachments; MonAvatar/director; clip contract;
bridge; habitat values; atlas/packs; 10,000 matrix; two-hour playback;
performance/memory; artifact/export/restore; CI/evidence; files/dependencies/
rights; deferrals/deviations; Notion/GitHub publication; commits/equality;
operator approvals; and Architect recommendation.

Do not report visual approval unless the operator explicitly provides it.

## R04-C03 superseding correction

Architect Review 07 retains all C02 contract/intake semantics and narrows the
remaining work to Godot diagnostic parity. Use one canonical runner for
controlled import, cold, warm, local, workflow, and evidence invocations. It
must retain Godot stdout/stderr/`--log-file` and separate Xvfb diagnostics,
record exact error lines and hashes, classify all application `ERROR:` output
fail-closed, and publish diagnostics on failure. Capture the prior hosted error
before any runtime change; do not generate production art, alter C02 contracts,
change Godot 4.7.2, or request visual approval. Final readiness remains gated
on two hosted passes and one stability rerun.

## R04-C04 readiness-race correction

Architect Review 08 supersedes only the inherited Phase 01 readiness probe.
Merge the review normally, then replace socket-exists/one-health-sample logic
with a fixed monotonic bounded poll of the explicit complete readiness
predicate. Require all five expected roles to be ready and healthy with
synthetic care coverage in two consecutive samples separated by a nonzero
interval. Record a sanitized startup trace and fail closed on timeout or
supervisor exit. Add deterministic delayed-ready, never-ready, and early-exit
tests, run the complete inherited Phase 01 verification, and prove three
same-SHA hosted Phase 01 passes plus a same-SHA Phase 02 pass. Do not alter
C02/C03, generate production art, modify the protected primary worktree, merge
PR #9, or close Issue #8.
