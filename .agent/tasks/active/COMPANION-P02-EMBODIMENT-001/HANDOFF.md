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
