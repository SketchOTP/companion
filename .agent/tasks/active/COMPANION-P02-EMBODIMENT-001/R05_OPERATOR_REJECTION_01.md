# R05 operator visual rejection and bounded corrective investigation

## Status

PARTIAL. Retrieval confidence ADEQUATE. The operator rejected every R05-v1
preview. There is no qualified replacement animation pack and no request for
visual approval. Review 10 candidate-authorship authorization remains in force.
Architecture v1.0 is adopted, Phase 01 accepted, Phase 02 unaccepted, and later
phases closed. PR9 stays draft/open/unmerged and Issue8 open.

## Preserved boundary

Starting head: `d0440d2df83d0d344eac9a2f8c907e464d358ff0`.
Fetched main: `8b5f18e48b124e16b0af87c76b02f2080e5121ad`; normal merge was
already up to date. Local ext4 secondary worktree used. Protected primary status
was inspected only; its AGENTS.md and .gitignore modifications were untouched.
Secondary .gitignore modification and untracked .ignore were also preserved.

## What the operator rejected

- Green edge contamination on the old cutouts.
- Fast upward idle motion without a convincing complete exhale.
- Twitchy walk, repeated leading leg, glitching hand.
- Orientation presented as rapid head shaking.
- Listen/acknowledge presented as rapid bob/flick with a distorted hand.
- Too few usable temporal drawings and insufficient smoothness throughout.

## Confirmed implementation defects and corrections

The review builder forced 84 ms per drawing instead of using duration_ticks.
It set infinite looping even for completion=once. It also exported binary-alpha
GIF previews of antialiased RGBA frames. The corrected review helper uses the
24 Hz source timing, cumulative nearest-centisecond rounding (at most 5 ms
boundary error), four-times-slower quarter speed, completion-aware looping, and
a declared neutral review backdrop. Source pixels and source timing are not
changed by review generation. Six focused tests pass.

The old pack's eight two-tick idle frames still describe only 2/3 second; this
fix does not turn them into a slow breath. New source timing and motion must be
authored and validated together. A loop/seam must not be inferred from counts.

## iHero/provider investigation

Read-only inspection identified remove.bg and Photoroom adapters. No iHero job,
order, notification, or model pipeline was run or changed. A small stdlib upload
adapter was implemented from official API documentation; only the explicitly
selected provider key is read, never logged. It is offline source-authoring
tooling, not a runtime dependency. No new package was installed.

- remove.bg live attempt: FAILED, HTTP 402; no output artifact was accepted.
- Photoroom: three live HTTP 200 RGBA outputs, original dimensions retained.
- API-response bytes preserved exactly; original generation bytes untouched.
- Two ordinary mocked test methods and one three-case validation method pass:
  exact response preservation; HTTP failure without output/key logging; wrong
  dimensions, RGB-only result, and wholly opaque result rejection.
- Live provenance includes input/output SHA-256, dimensions, mode and alpha.
  Dimensions equality is NOT geometry equality. An early local probe used the
  overly broad key geometry_unchanged; that assertion is withdrawn. The helper
  and all current records use dimensions_preserved only.

Official sources: https://www.remove.bg/api and
https://docs.photoroom.com/remove-background-api-basic-plan/quickstart-guide .
Provider use follows the operator's explicit request to use iHero's cutout API.
Original art and approved references only were uploaded; no personal data.

## New generation studies — not a replacement pack

Eight reference-conditioned generation attempts were inspected. Dense walk
sheets still repeat the wrong leg; opposite contact keys differ but their
in-betweens do not preserve convincing leg correspondence. A single passing
pose lifts the wrong intended leg. One breathing sheet drifts toward frontal
facing. A new neutral rest image is a study, not an approved construction.
The latest sixteen-drawing breathing sheet has inconsistent placement, still
requires motion/art review, and has not been promoted to source-pack content.
Hashes and dispositions are in `r05-v2-attempts.json` beside this record.

Photoroom cutouts were composited over white, black, gray and magenta. In all
three samples the test found zero pixels with alpha>8 and green exceeding both
red and blue by >12. This is a narrow green-contamination check, not universal
edge QA. Each sample had six nonzero-alpha perimeter samples (maximum alpha
1 or 2); these outputs are NOT MON_FRAME_V1 intake-ready unchanged. No automatic
anatomy repair or image-band warping was performed.

## Remaining art work

The operator's request for more frames is retained. Proposed bounded authoring
targets are 16 idle drawings over a full approximately four-second breath,
16 or more alternating gait drawings, 12 drawings per one-shot orientation,
and at least 16 listen/acknowledge drawings with attention, pause, nod and settle.
These are targets, not observed or completed counts. Before source-pack use,
make an explicit versioned request-profile update; do not silently weaken the
accepted old bounded-profile validator or change expected counts from output.

Hand/foot anatomy and paired gait key continuity remain unresolved. Additional
raw generations must not be called smooth animation merely because hashes differ.
Do not submit this study set for approval or scale the full library.

## Evidence

- Review timing tests: PASSED (6 tests, E2_REPRODUCED).
- Cutout adapter tests: PASSED (3 methods, 5 scenarios, E2_REPRODUCED).
- Historical builder integration: PASSED. All eight preview tracks were rebuilt;
  every source-frame byte and pack.json byte matched the retained old pack.
  GIF completion and summed durations were independently read back and matched
  track ticks within 5 ms. This is not a new visual pass.
- Three live Photoroom cutouts: PASSED bounded transport/format observation,
  E3_TARGET_TESTED; visual/normalization acceptance NOT GRANTED.
- New gait/motion selection: FAILED current authoring gate, E1_OBSERVED.
- New pack intake/Rust/Godot: NOT RUN, no selected replacement pack.
- Full runtime/soak/art acceptance: NOT RUN, no new claim.
- Historical exact-reference and foundation evidence retained without rerun.

Selected contrast-sheet SHA-256:
`7c3e72bf72219a852cd8ef9aa68cc3f2f73eae3cafcb484e2aa7526802909caa`.

The old generated-art CI job remains only a rejected-source engineering
regression and its artifact is named rejected-v1. No hosted green result can
reverse the visual rejection. New helper tests do not make live provider calls.
