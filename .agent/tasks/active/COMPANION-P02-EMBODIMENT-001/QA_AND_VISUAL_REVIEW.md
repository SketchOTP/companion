# QA AND VISUAL REVIEW — COMPANION-P02-EMBODIMENT-001

## Automated QA

Record pass/fail/warning counts and artifact links for canvas/format/alpha,
root/baseline, safety bounds, landmarks, naming, numbering, timing, contacts,
loop seams, transitions, checksums, atlas packing, duplicates, palette, silhouette,
anatomy, alpha halos, and repository budget.

## Visual QA

Publish and link:

- identity/construction sheet;
- eight-direction sheet;
- palette/anatomy sheet;
- per-family contact sheets;
- transition sheet;
- eye/mouth overlay sheet;
- atlas/debug sheet;
- viewport-only habitat stills;
- motion reel or deterministic playback alternative.

For every item record whether it is an approved reference, a new candidate,
automatically passed, Architect-reviewed, operator-approved, rejected, or
pending. Preserve rejected frames and reasons.

## Operator gate

Codex cannot self-approve identity or animation quality. List exact operator
questions and the minimum review artifact needed for each. Do not conflate
technical validation with visual approval.

## Executed result

Automated asset QA passed: 256/256 decodable RGBA frames, 256 unique hashes,
32 families, eight directions, 24 eye overlays, eight mouth overlays, safety
region and zero-root-drift metadata, valid pack and atlas dimensions. Contract
QA passed for all ten schemas with valid, missing-required, and unknown-field
cases. Review derivatives include construction diagonal candidates, palette /
anatomy, eight-direction, family, transition, eye, and mouth sheets. They are
new candidates pending operator review; automated QA is not visual approval.
# Architect Review 01 correction — review package (2026-09-11)

The committed review set now includes native six-view correspondence, diagonal
candidates, proportion/root grid, anatomy/palette, pose/shadow limits, and the
temporal core/idle-variant sheets.  `validate_core_motion.py` checks rendered
canvas, alpha, safety bounds, root landmarks, hashes, track floors, atlas
placement, and overlap.  All new construction, diagonal, motion, and identity
decisions remain pending operator visual approval.
# R03 review gate

The R03 validator checks rendered pixels and source hierarchy rather than
declared metadata alone: 1024x1024 RGBA canvas, safety bounds, fixed root,
planted idle contacts, walk swing displacement, facing endpoint differences,
anatomy coverage, frame/track hashes, schema, and 24-FPS timing. Five
tamper-negative mutations fail closed. Review derivatives for all five tracks
are committed under `assets/source/p02/r03/review/`; operator approval is still
pending and no full-library review may be requested.
