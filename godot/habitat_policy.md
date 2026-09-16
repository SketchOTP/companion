# Bounded Openbox habitat policy — `MON_HABITAT_V1`

The target is the dedicated Openbox output `0` at the Phase 01 observed
1366×768 desktop. The logical base is 640×360; the initial window is 960×540,
with minimum 640×360 and maximum 1366×768. Canvas-items scaling, keep-aspect
policy, uniform mon scale, nearest filtering for authored raster pixels, and
visible-area clamping are explicit. Geometry is persisted in Godot `user://`
storage, never in the checkout or SSHFS.

The selected output is used when available. If topology injection reports it
absent, the shell falls back to the primary screen and marks `fallback_active`;
restoration reselects output 0 and reapplies bounded geometry. Bridge loss is a
degraded presentation state and reconnect is retried by the bridge adapter.
Physical monitor hot-unplug is not claimed by this deterministic topology test.
