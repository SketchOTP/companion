# R06-C06 replay-safe fixed-step controller qualification

This bounded qualification preserves the frozen R05 raster pack and adds a
versioned V2 locomotion command path. UUID intent IDs are ordered by an explicit
monotonic sequence; stale, duplicate, and replayed commands fail closed.
Canonical `MonRoot` movement runs at 24 semantic ticks per second, independent
of render cadence. Presentation gait rate is calibrated to commanded speed:
48 px/s = 0.5x, 96 px/s = 1.0x, and 144 px/s = 1.5x. Stop commands cancel the
currently active intent and enter the stop track without resuming cruise.

The Python result is semantic qualification. `godot/r06_c06_locomotion_test.gd`
consumes schema-valid serialized V2 intents and produces actual normal and
quarter-speed viewport captures plus movement/event traces. No source PNG is
edited, resampled, or regenerated.
