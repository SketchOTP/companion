# Godot Habitat Foundation — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — AWAITING ARCHITECT REVIEW`

Document the exact Godot 4.7.2 project shell for the approved bounded resizable habitat on the dedicated 1366×768 Openbox-managed output.

Required implementation and proof:

- verified artifact bootstrap without replacing Godot 4.6;
- configurable screen/output selection;
- bounded resizable window and content-scaling policy;
- geometry persistence outside the repository;
- safe visible fallback when target display is missing or changes;
- `godot-bridge` handshake, reconnect and degraded-state behavior;
- visible foundation health status;
- neutral non-production placeholder only;
- headless project validation;
- target-host window test that does not capture or expose private desktop content;
- Godot absence/disconnect/reconnect tests.

Do not generate/import production sprites or implement media, speech, model, organism or care behavior.

## Implemented neutral shell

`godot/project.godot` and `main.tscn` define a bounded resizable 640x360
viewport with canvas scaling and a neutral status screen. The exact cached
Godot 4.7.2 artifact passed `--headless --path godot --editor --quit`; a local
X11/Openbox probe observed the titled 640x360 window at the requested bounded
position and terminated it without screenshot or media capture. No geometry is
written by the shell and no production asset or bridge behavior is present.

## Review 01 continuation

The neutral Godot script now models explicit connecting/connected/degraded/
disconnected/incompatible bridge states, a versioned bridge marker, configurable
target-screen selection, bounded geometry, visible-area clamping, and persisted
window geometry. `godot-bridge` writes a local versioned handshake state under
the private runtime root. Renderer, media, sprite, and production embodiment
behavior remain out of scope; target-host display-loss recovery is still
unqualified until exercised.

## Architect Review 02 continuation

`godot-bridge` now creates a private runtime UDS and serves the versioned
`companion-foundation-v1` handshake. The Godot 4.7 shell uses
`StreamPeerUDS`, configurable `COMPANION_TARGET_SCREEN`, persisted output/
position/size, and explicit disconnected/incompatible/degraded states. The
headless smoke observed handshake success and a clean degraded run after bridge
termination. Target-host display-loss recovery and production embodiment remain
unqualified.
