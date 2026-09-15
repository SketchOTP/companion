# Connected Listen → Acknowledge candidate

Operator requested missing drawings and a connected front-facing action on black.
The built-in image-generation tool made 18 reference-based edits. Thirteen were
selected and five rejected; three prior poses supply rest, listening hold, and
acknowledgment. This is candidate review artwork, not an approved motion pack.

- `prompts.json`: exact generation instructions, input/output identities.
- `selection.json`: selected ordering, tick weights and rejection explanations.
- `source_evidence.json`: all 21 raw source hashes, dimensions, modes, disposition.
- `requests.json`: 17 playback slots / 16 distinct drawings, 116 ticks at 24 Hz.
- `compiled_result.json`: assembled asset hashes and review artifact identities.

The portable export includes original `authoring/raw/` bytes and all rejected
outputs. Bulk PNGs and ZIP are outside ordinary Git. None were resized, cropped,
warped, recolored, or re-encoded by the preparation/compiler scripts. Canvas
display scaling does not modify source files. The source frames are 1254×1254
RGB black-background studies, not 1024×1024 MON_FRAME_V1 RGBA intake sources.

The clip presents attention, a listening hold, one acknowledgment, follow-through,
and return to front rest. Hands/feet were visually inspected; exact planted-contact
drift and anatomical stability have not been quantitatively qualified. Distinct
hashes prove distinct files, not motion quality. Operator approval remains open.

Rebuild using the original exported raw bytes and existing study/retry bundles:

```sh
python3 experiments/p02-embodiment/scripts/prepare_listen_review.py \
  --root "$LISTEN" --selection assets/review/p02/author002/listen-ack-connected/selection.json
python3 experiments/p02-embodiment/scripts/compile_black_review.py \
  --studies "$STUDIES" --retry "$RETRY" --sheets assets/review/p02/author002/black-sequence-sheet \
  --listen "$LISTEN" --out "$NEW_OUTPUT"
python3 -m unittest discover -s experiments/p02-embodiment/scripts -p 'test_*listen_review.py' -v
python3 -m unittest discover -s experiments/p02-embodiment/scripts -p test_compile_black_review.py -v
```

`STUDIES`, `RETRY`, and `LISTEN` identify separate private local exports;
`NEW_OUTPUT` must not already exist. Generation itself is not deterministic;
reassembly uses retained exact source bytes. Open the generated `index.html`
and choose Listen → Ack, normal or quarter speed. Repeated front-rest source is
an intentional hold/return, not another unique drawing.

Final export ZIP SHA-256:
`45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b`.

No production approval, full-library completion, or Phase 02 acceptance implied.
