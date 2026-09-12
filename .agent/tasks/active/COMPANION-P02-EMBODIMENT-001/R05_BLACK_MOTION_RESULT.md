# CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R05-AUTHOR-002

## Verdict

PARTIAL / MOTION QUALITY GATE FAILED. Black-backed drawings and diagnostic
playback created. The requested complete smooth movements are not finished.
No visual approval request, finished-frame count, source-pack acceptance or
Phase 02 acceptance is made.

## Retrieval and preservation

ADEQUATE. Review 11, current kernel, exact selection, current Notion report and
directive, PR #9 and Issue #8 rechecked. Starting HEAD
6bef092cb402270b75cbc6703d4e8d5e9d4cc665; origin/main
d07620c4ab2c874e65db85ff9866197a5784563c already normally merged.
Secondary ext4 worktree only. Primary read-only status remains modified
AGENTS.md/.gitignore; unrelated secondary .gitignore/.ignore excluded.
Exact approved native hashes unchanged. No rebase, force-push or new branch.

## Work performed

51 built-in imagegen outputs: 23 background conversions, 4 front-presence keys,
8 start/stop keys, 8 turn keys and 8 constrained left-gait in-between attempts.
With the existing black front this is 52 drawings, not 52 accepted animation
drawings. New shading/geometry is candidate or rejected, not automatically
approved. Every generated original and exact-copy raw file is preserved.

The 52 images are 1254-square RGB, black-backed rather than MON_FRAME_V1 RGBA.
Perimeter maxima 1–2/255. Godot background is exactly black. No Photoroom,
billing action, new dependency, alpha shader, automatic cutout or anatomy
repair was used.

23 diagnostic sequences comprise eight separate construction stills, front
breathe/listen key studies, independent left/right gait/start/stop/turn studies,
two complete-action key-blocking sequences, and one failed 16-frame left
in-between diagnostic. Repeated keys are not counted as unique drawings.

## Visual observations and stop

The left in-between strip has insufficient leg progression between down and
passing keys (notably mid 1 and mid 5); it will jump into the passing pose.
The right 22.5-degree turn closely resembles the quarter master, and the 67.5
drawing remains too frontal before the profile endpoint. Front breathe/listen,
start/stop and turn studies remain sparse keys, below the complete motion floor.

These observations fail the motion gate. Remaining right/front/turn in-betweens
were NOT RUN using the failed interpolation approach. No smoothing, resampling,
crossfade or longer hold is represented as a new drawing. Review 11 key quality
remains the prerequisite for scaling; previous approved originals stay approved.

## Validation

- 13 focused review-timing/export/provider regression tests: PASSED.
- Exact-copy export of 52 sources, source hashes and black perimeter: PASSED.
- 23 normal/quarter GIF pairs and strips, duration readback: PASSED.
- Actual Godot 4.7.2 Xvfb/llvmpipe import and explicit review playback: PASSED.
- Actual frame zero post-draw/readback, exact observed frame order/completion,
  unchanged source hashes for all 23 sequences: PASSED.
- 24 FPS integer weights, two warmup render boundaries, 0.075s timing tolerance;
  maximum observed total-track error 0.008823s: PASSED.
- Zero final Godot ERROR lines; XIM/VSync and separate wrapper warnings retained.
- Godot missing-manifest and source-hash tamper negatives: PASSED (expected exit 1;
  no track was started). Exact negative results retained.
- First Godot attempt: FAILED, inferred-Variant parse error; explicit bool fixed.
  Original failed result retained. Preliminary wider timing test not final gate.
- Motion quality/continuity: FAILED.
- World contacts, MON_FRAME_V1 normalization, actual v2 intake/Rust/production
  runtime, full foundation regression, hosted art CI, Openbox/endurance: NOT RUN.
- No runtime/package promotion, no complete library, no Phase 03+ work.

## Artifacts and reproducibility

See [study README](../../../../assets/review/p02/author002/black-motion-studies/README.md).
The adjacent requests.json binds all 52 raw hashes and review order/ticks.
prompts.json retains all 51 tool prompts and source identities. export-result.json
binds the full local export; selected review GIFs/strips are committed. Bulk raw
PNGs/GIF sets remain in local XDG export outside ordinary Git.

Rebuild from the exact raw corpus with assemble_black_motion_studies.py followed
by export_black_motion_review.py. These generate review derivatives only.
Godot black_motion_review.gd is an explicit review player, not a production
intake fallback. No source artwork is procedurally regenerated.

Request SHA-256: 0b1e72352c86d95e13c051c9c5a5a4e9abc5a72d012fd31a56e7898fa4ab99af.
Full export result SHA-256: 70d6e238a4f0199364d21fbe6e3c2dce4d4d287b7b6f6c9d2b56172ab836bc0b.

Local portable archive: black-motion-studies-2026-09-12-v1.tar.gz.
Archive SHA-256: 2e13876b1d9e4f615419e0d234dfab286d5673258fd47f40df9beaeca05969f0.
The archive contains the preserved raw corpus and full local review set; it is
not a published production pack. Selected review derivatives are in this PR.

## Evidence ceiling / recommendation

E1 for generated visual observations; E3 for bounded Xvfb review execution,
not physical Openbox, quality, contact stability, reliability or product proof.
Retain black-format progress; correct the specific turn/in-between defects before
finishing all action sequences. Do not ask for approval of failed motion.

Architecture v1.0 remains adopted; Phase 01 accepted; Phase 02 active/unaccepted;
Phase 03+ closed. PR #9 remains draft/open/unmerged; Issue #8 open. Notion and GitHub
receive this partial result rather than a successful-art completion claim.
