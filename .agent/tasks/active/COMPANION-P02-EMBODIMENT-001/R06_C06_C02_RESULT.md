# R06-C06-C02 evidence correction (implementation pending hosted review)

The correction preserves the frozen R06 pack (`1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`) and C06-C01 behavior. The Godot qualification now uses monotonic absolute deadlines for review pacing, reports actual wall time including capture/readback, and keeps the pacing decomposition diagnostic-only.

Local Godot 4.7.2 evidence:

| side | normal wall ms | quarter wall ms | ratio |
| --- | ---: | ---: | ---: |
| left | 3033.866 | 12000.927 | 3.95565 |
| right | 3033.310 | 12000.134 | 3.95612 |

Each run contains four non-black frame-post-draw captures. Capture records bind semantic tick, actor position, track/frame, authored tick, track-derived phase, monotonic elapsed microseconds, source pack/frame hashes, and capture hash. The shared verifier independently loads the pack, recomputes duration totals/frame mapping/phase, and rejects a mutated pack duration (`pack_duration_binding`). The loaded profile cruise tracks total 32 authored ticks. `build_c06_capture_review.py` creates strips/GIFs solely from the actual checkpoint PNGs. The prior C06-C01 timing report is retained as superseded history; it is not rewritten.

Hosted focused R06, Phase 01, and inherited Phase 02 runs are required on one final implementation SHA. Legal-transition and Openbox work remain deferred pending Architect review.
