# R06-C06-C03 final locomotion timing and phase closeout

## Verdict

The C06-C03 correction closes the two Review 21 defects without changing any
approved source pixels. The exact hosted implementation head is
`49d9d65e08b9c9410d8013266ed5a5a5194ff8c5`; focused R06, Phase 01, and the
inherited Phase 02 workflows are green on that SHA. Legal-transition and
Openbox qualification remain deferred pending Architect review.

## Authority and source identity

- Review 21 authority: `origin/main` `4853ae92d98b46371cd6c7066ba20653d0e09ecf`.
- Frozen R06 source pack: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.
- Hosted artifact ID: `10352161425`.
- Hosted artifact ZIP SHA-256: `87765dcfa5b06c1c5be16fcf85a5ba806be29dcfcb4dc224da95b84d59dc183a`.

No source PNG changed. The prior C06-C02 artifact `10346359655` and its
approximately `3.95x` full-run values remain preserved as historical evidence;
the earlier weak intermediate-checkpoint and phase-reset claims are superseded.

## Timing origin and observation

Both runs use one monotonic review epoch immediately before the cruise intent.
Each checkpoint elapsed value is sampled immediately after the paced
`RenderingServer.frame_post_draw` observation and before viewport readback and
PNG save overhead. The exact 4.0 review deadline is used; startup and capture
overhead are not used to redefine the semantic timing.

| side | checkpoint | normal usec | quarter usec | ratio |
| --- | --- | ---: | ---: | ---: |
| left | first_cruise | 552681 | 2176958 | 3.93891 |
| left | second_loop_cruise | 1383568 | 5509631 | 3.98219 |
| left | stop | 2507576 | 10008704 | 3.99139 |
| left | full run (ms) | 2507.576 | 10008.704 | 3.99139 |
| right | first_cruise | 550547 | 2176129 | 3.95267 |
| right | second_loop_cruise | 1384045 | 5508197 | 3.97978 |
| right | stop | 2507976 | 10007981 | 3.99046 |
| right | full run (ms) | 2507.976 | 10007.981 | 3.99046 |

All required ratios are within `[3.90, 4.10]`. Normal and quarter checkpoint
sets match exactly in semantic tick, actor position, track, frame, authored
tick, derived phase, and source-frame identity. The quarter run differs only in
monotonic review wall time.

## Pack-derived authored progression

The loaded left/right cruise tracks each sum to 32 authored ticks (`8 frames ×
4 ticks`). Presentation phase is derived from the loaded duration array and
the advancing authored cursor, modulo 32. The observed cruise sequence advances
cursor `0..47`, maps frame/tick from the actual pack, wraps `31 → 32` to phase
`0.96875 → 0.0`, and continues through the second loop without reset. The
qualified checkpoints are:

```text
first_cruise        cursor 12, phase 0.375, actor x left 220 / right 420
second_loop_cruise  cursor 32, phase 0.0,   actor x left 140 / right 500
stop                stop-track cursor 11,  phase 0.458333...
```

`verify_c06_trace.py` independently reloads the runtime pack, recomputes
duration totals, frame mapping, source hashes, and phase. Its negative matrix
rejects a pack-valid sequential jump (`authored_progression`) and an explicit
unexpected phase reset (`authored_phase_reset`); the legitimate modulo seam
passes.

## Rendered evidence and media

The 16 hosted Godot checkpoint PNGs (left/right × normal/quarter × four
checkpoints) are all non-black, translated, and frame-post-draw observed. Each
capture contains capture index, semantic tick, actor root, track/frame,
authored tick/cursor/loop total, track-derived phase, monotonic observed time,
source-pack SHA, source-frame SHA, capture SHA, and non-black status.

The media manifest is `b71bea469f92fbca3822b9b231d224970b8680417d4ab2f935f8b70c10e12ec1`.
Actual-capture review media hashes:

- left strip `7678fc588897e1fdfab327866a30362b1fc6e32dcd64795d5047e4eb52e29ddf`;
  GIF `75689fbd0bf823782a3a6f36779a327acfd45c7afb8ef8d68b64ed6132310d2f`.
- right strip `1e8ecf04186c5728b473250cc69d616983f0c687edd666a4cffaf72212bbc71b`;
  GIF `f3c67b821e09a6f411deb65a8c7919d23431abcf6eceb53dcd69cdfc2ee6d8b0`.

## Negative evidence and regressions

The scheduler/trace verifier positive result is `PASS` with independent
rejections for fixed-step tick loss/duplication, hidden root reset, loop
recenter, pack duration/source-duration mutation, pack-valid sequential jump,
unexpected phase reset, and black capture. Controller-path, loader/resolver,
and signed-64 wire-boundary negatives remain green. The timing verifier rejects
an artificial `3.33x` total and a bad intermediate checkpoint ratio.

Hosted runs on the exact implementation SHA:

- focused R06: `34853256541` — PASS;
- Phase 01: `34853256563` — PASS;
- inherited Phase 02: `34853256770` — PASS.

The final branch publication commit is this implementation SHA; no generated
art or runtime source bytes were added by C06-C03.
