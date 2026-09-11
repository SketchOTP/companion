# HABITAT AND ASSET PACKS — COMPANION-P02-EMBODIMENT-001

## Habitat values

Record exact selected values and evidence for:

- Openbox output/screen identity;
- initial position and size;
- minimum and maximum size;
- logical content base size;
- content scale mode/aspect/stretch/filter;
- mon scale range;
- focus/input policy;
- visible-area clamp;
- saved geometry path and schema;
- target-missing fallback;
- resize behavior;
- bridge/Godot reconnect;
- simulated topology loss/restoration.

## Packs

Record boot-critical and on-demand pack composition, atlas dimensions, gutters,
trim/margin reconstruction, filtering/mipmap settings, disk size, decoded
texture memory, load latency, first-use stall, hashes, and corruption handling.

## Artifact policy

List what is committed, what is generated locally, what is published as a
versioned artifact, and how the complete asset bundle is exported/restored
without GitHub. Confirm ordinary-Git binary budget and no Git LFS change.

## Executed result

`godot/habitat_policy.md` and `embodiment_habitat.gd` lock a 640×360 logical
base, 960×540 initial window, 640×360 minimum, 1366×768 maximum, canvas-items
keep-aspect scaling, uniform raster scaling, target screen 0, visible-area
clamping, `user://` geometry persistence, and primary-screen fallback. The
metadata-only host probe observed an X11 desktop with two 3840×2160 outputs and
GNOME Shell/mutter framing rather than the dedicated 1366×768 Openbox target;
no display configuration was changed, so physical habitat and two-hour
playback remain unverified. The generated tree is 11 MB; no Git LFS was added.
