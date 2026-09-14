# R06-C06-C02 evidence correction (implementation pending hosted review)

The correction preserves the frozen R06 pack (`1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`) and C06-C01 behavior. The Godot qualification now uses monotonic absolute deadlines for review pacing, reports actual wall time including capture/readback, and keeps the pacing decomposition diagnostic-only.

Local Godot 4.7.2 evidence:

| side | normal wall ms | quarter wall ms | ratio |
| --- | ---: | ---: | ---: |
| left | 3033.866 | 12000.927 | 3.95565 |
| right | 3033.310 | 12000.134 | 3.95612 |

Each run contains four non-black frame-post-draw captures. Capture records bind semantic tick, actor position, track/frame, authored tick, track-derived phase, monotonic elapsed microseconds, source pack/frame hashes, and capture hash. The shared verifier independently loads the pack, recomputes duration totals/frame mapping/phase, and rejects a mutated pack duration (`pack_duration_binding`). The loaded profile cruise tracks total 32 authored ticks. `build_c06_capture_review.py` creates strips/GIFs solely from the actual checkpoint PNGs. The prior C06-C01 timing report is retained as superseded history; it is not rewritten.

Hosted focused R06, Phase 01, and inherited Phase 02 runs are required on one final implementation SHA. Legal-transition and Openbox work remain deferred pending Architect review.

## Hosted exact-head closeout — 2026-09-14

Implementation SHA `034690cab0f3b7a1bc297fed1bc0b1fa996d3511` passed focused
R06 `34843867410`, Phase 01 `34843867420`, and inherited Phase 02 `34843867429`.
Published R06 artifact `10346359655` has ZIP SHA-256
`e97561173a1bc48447fec13e498f21d0b4de49c5b3b5d34de3cba396f2ee6cfe`.
Hosted wall times are left `3078.224/12153.249 ms` (normal/quarter,
`3.94813665x`) and right `3078.854/12152.211 ms` (`3.94699164x`). The
capture media is sourced only from hosted Godot checkpoint PNGs. Frozen pack
SHA remains unchanged; no source PNG changed. C06-C02 is ready for Architect
review; transition and Openbox gates remain deferred.
