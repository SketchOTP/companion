# GODOT AVATAR AND ANIMATION DIRECTOR — COMPANION-P02-EMBODIMENT-001

## MonAvatar

Document the final scene tree, external resources, layer order, body handoff,
landmark use, pack loading, and missing/corrupt-pack behavior.

## MonAnimationDirector

Document and test:

- semantic intent input;
- eligibility filtering;
- deterministic selection mode;
- normal variation and recent-use suppression;
- transition graph;
- posture/direction connectors;
- interrupt ranges and continuation;
- event markers;
- completion/failure result;
- no canonical organism logic.

## Bridge

Record exact versioned messages and observed sequences for acknowledgment, clip
start, frame/event, interruption, completion, and failure/degradation.

## Validation

Include 10,000-case retained-seed transition results, illegal-transition count,
selection latency, bridge round-trip latency, and tamper-negative evidence.

## Executed result

`godot/main.tscn` contains the required layered `MonAvatar` tree. The avatar
loads `SpriteFrames` from the generated raster manifest and alternates BodyA /
BodyB; `MonAnimationDirector` performs deterministic seed-based selection,
recent-use suppression, legal connector fallback, interruptible semantic
intents, and versioned results. `EmbodimentBridge` emits versioned intent,
frame, completion, interruption, and degradation-shaped events. The headless
Godot 4.7.2 test reports a live `gaze` intent and visible body state. Missing
manifest/empty clips degrade explicitly. Canonical state and care policy are
not present in these scripts.
