# Phase 02 evidence bundle — candidate

This bundle contains sanitized, deterministic outputs from the Phase 02
embodiment candidate. It contains no private media, hostnames, usernames,
credentials, runtime stores, or screenshots.

| Evidence | Result | Ceiling |
|---|---|---|
| `asset_validation.json` | 256 unique RGBA frames, 32 families, overlays and pack valid | E2_REPRODUCED |
| `contract_validation.json` | ten Draft 2020-12 schemas and negative cases | E2_REPRODUCED |
| `godot_headless.json` | layered avatar/director scene and visible state | E3_TARGET_TESTED |
| `transition_matrix.json` | 10,000 cases, seeds 17/23/41, zero illegal transitions | E3_TARGET_TESTED |
| `target_host_probe.json` | metadata-only X11 topology and WM observation | E1_OBSERVED |
| `playback_smoke.json` | five-second synthetic smoke | E1_OBSERVED |

The ≥2-hour dedicated Openbox target-host playback is `NOT RUN`: the active
session exposes dual 3840×2160 outputs under GNOME Shell/mutter rather than the
authorized dedicated 1366×768 Openbox target. This is an explicit limitation,
not a pass or product claim.
