# Godot 4.7.2 habitat boundary

## Black-background still review (operator request, 2026-09-12)

The project clear color and foundation background are black. Use the separate
`black_backdrop_review.gd` script for opaque candidate stills, never as a pack
loader fallback. In a private local copy of this Godot project run:

```sh
"$GODOT" --audio-driver Dummy --path "$REVIEW_PROJECT" --script res://black_backdrop_review.gd -- --image="$REVIEW_IMAGE"
```

For a bounded rendered test add `--self-test --capture="$REVIEW_CAPTURE"` after
the separator and use Xvfb for isolated rendering. All path variables must point
to the private local review copy/output (image input may be read-only). Use exact
Godot4.7.2. Headless without a rendering backend fails the render assertion.
`run_godot_qualification.py` remains the canonical diagnostic wrapper; supply
`--script black_backdrop_review.gd` and explicit `--script-arg` values.

This is one-frame review only: no timing/locomotion/intake claim. Existing
transparent source and approved-pack guards remain unchanged. Opaque sprites
can cover underlying layers; they are unsuitable for general layered compositing.

The project is a neutral, resizable, headless-validatable presentation shell.
The official Godot 4.7.2 Linux x86_64 binary is supplied by the private
qualification cache and is never committed. Geometry belongs in XDG state,
not this checkout. The shell deliberately contains no sprites, media capture,
speech, model inference, organism behavior, or care behavior.

R04-C01 accepts only a validated `MON_INGESTED_FRAME_PACK_V1`. Architect input
is a separate immutable `MON_AUTHORED_FRAME_SOURCE_PACK_V1`; intake enforces
operation-specific approval eligibility, approved-reference hashes, pack and
track digests, relationship uniqueness, path containment, and every source
hash. `MonAvatar` constructs 24 FPS `SpriteFrames` tracks from integer
1/24-second duration weights. Source PNGs remain outside Godot's generated
import cache and are loaded into derived `ImageTexture` objects without source
mutation.

## Superseded proof modes

R02/R03 procedural proof scripts and resources are retained only as negative
evidence. They are not imported by `MonAvatar`, are not a runtime fallback, and
must not be presented as candidate production art.

## R04 synthetic runtime gate

`r04_authored_pack_test.gd` uses an obviously geometric
`synthetic_test_only` pack. It proves exact track selection, a scene/render
commit observation before `started`, 24 Hz duration weights, event/completion
order, and fail-closed missing, ineligible, and hash-corrupt paths followed by
restoration. In headless mode, the bounded scene-tree observation is explicitly
labelled synthetic; physical display presentation remains a target-host gate.
`r04_identity_smoke_test.gd` loads the exact approved identity as a one-frame
import smoke fixture only; it is not candidate animation.
