# Godot 4.7.2 habitat boundary

The project is a neutral, resizable, headless-validatable presentation shell.
The official Godot 4.7.2 Linux x86_64 binary is supplied by the private
qualification cache and is never committed. Geometry belongs in XDG state,
not this checkout. The shell deliberately contains no sprites, media capture,
speech, model inference, organism behavior, or care behavior.

The Phase 02 workflow stages the generated `MON_TEMPORAL_TRACKS_V1` artifact
under `godot/assets/p02-core/` for ephemeral import and headless playback. A
local run may do the same from the private output of
`build_core_motion.py`; the generated corpus is intentionally absent from the
ordinary-Git tree. `MonAvatar` loads one SpriteFrames animation per temporal
track at an explicit 12 FPS and reports observed frame/completion markers.
