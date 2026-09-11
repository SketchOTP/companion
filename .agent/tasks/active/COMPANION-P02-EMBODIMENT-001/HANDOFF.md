# HANDOFF — COMPANION-P02-EMBODIMENT-001

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
