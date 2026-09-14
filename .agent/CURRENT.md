# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

## Latest Architect disposition

Architect Review 20 `CONTINUE — C06-C01 PARTIAL ACCEPTED`.

Retain the C06-C01 wire-range correction, one paused/manual presentation clock, authored-duration frame selection, real non-black translated Godot captures, replay/cancellation/fixed-step controller behavior, negative-evidence categorization, frozen source identity, and prior intake/Rust/render/compositor/failure/export boundaries.

Do not authorize legal-transition qualification yet.

Independent review of hosted artifact `10344096459` identified four remaining evidence defects:

1. Review 19 required quarter review at 4x review wall-time, but CI was weakened to accept `>=3.0x`; the exact artifact measures only about `3.17–3.18x`.
2. The submitted timing values do not match the exact hosted artifact even though the downloaded ZIP SHA-256 matches the submitted digest.
3. The shared phase verifier validates controller `animation_phase` based on hard-coded `AUTHORED_PROFILE_LOOP_TICKS := 32.0`, not phase independently derived from the loaded track's `duration_ticks`.
4. Capture records omit required source/timing identity fields, and the required actual-capture strip/GIF is absent.

Current authority:

- Architect Review 20: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_20.md`
- Notion Review 20: https://app.notion.com/p/3db833cb27ff81b4a078f4ab04a54b90
- Current Codex directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C02`
- Reviewed C06-C01 implementation: `de9d7c041cad3c28ecb2779e5afc11f1f2a0f3a4`
- Reviewed C06-C01 publication head: `84b1fcb12a89538a20f52efc1cc594173ab513e7`
- Hosted C06-C01 artifact: `10344096459`, digest `sha256:961f32864633d5ab45f121430d294bae538dc626c1abcac97488f333403b438f`
- Frozen visual task head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- Frozen R06 source-pack SHA-256: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`
- PR #9: draft/open/unmerged
- Issue #8: open
- Branch: `codex/p02-embodiment-001`

No new character artwork is authorized.

## Active objective

Execute `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C02` only:

1. normally merge current `origin/main` and preserve all accepted work/history;
2. restore real 4.0x review pacing using monotonic, deadline-based timing; hosted quarter/normal ratio must be `3.90..4.10` for left and right;
3. derive presentation loop ticks and phase from the loaded selected track's actual `duration_ticks`, with independent pack-backed verification rather than a duplicated controller constant;
4. bind every required capture to semantic tick, actor position, selected track/frame, authored tick, track-derived phase, monotonic review elapsed time, source pack/frame hashes, and capture hash;
5. preserve exact semantic equality between normal and quarter review checkpoints;
6. assemble strip/GIF only from actual Godot checkpoint PNGs;
7. add regression proving a 3.33x timing ratio fails validation;
8. reconcile the inaccurate C06-C01 reported timing values to the preserved hosted artifact;
9. keep focused R06 + Phase 01 + inherited Phase 02 green on one implementation SHA;
10. return to Architect before transition/Openbox qualification.

## Remaining Phase 02 gates

After C06-C02 passes without a new material defect: Architect decision on legal-transition campaign; then dedicated 1366x768 Openbox two-hour endurance; then final Phase 02 acceptance/PR merge decision.

Organism state, autobiographical memory, perception, speech, learning, development, dreaming, caregiving efficacy, production reliability, and Phase 03+ remain unaccepted.

## Protected work

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` modifications remain protected. Do not inspect, commit, reset, stash, overwrite, copy, or reformat them.
