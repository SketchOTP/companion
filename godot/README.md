# Godot 4.7.2 habitat boundary

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
