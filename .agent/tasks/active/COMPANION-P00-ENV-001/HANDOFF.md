# COMPANION-P00-ENV-001 — Handoff

Status: `COMPLETE_FOR_ARCHITECT_REVIEW`

## Directive result

- Verdict: `COMPLETE_FOR_ARCHITECT_REVIEW`.
- Retrieval confidence: `ADEQUATE`.
- Accepted pre-directive baseline: `ddb6b130ab6428a1f395cd223d309eeaa2ac7462`.
- Starting routing head: `2ea7b41d79f24f030ea3c3690dee00e8c2340671`.
- Result commit: `ef5b011bfd6e3f747e8bf8e8f06faebb21901d50`.
- Publication-evidence commit: the governance-only commit containing the final publication reconciliation.
- Architect acceptance: `NOT ASSIGNED`.

## Environment summary

- Ubuntu 24.04.5 LTS/X11; Ryzen 7 5800XT, 8 cores/16 threads; 67.3 GB RAM; 8.59 GB swap.
- GTX 1660 SUPER plus RTX 3050 6GB on NVIDIA 595.84; accelerated OpenGL 4.6 works; exact Vulkan capability is unknown because `vulkaninfo` is absent.
- Three connected outputs across two logical X screens: dual 4K/60 Hz GNOME surface and a separate 1366×768/59.96 Hz Openbox surface.
- One readable NexiGo UVC camera with MJPEG through 1080p30 and YUYV through 720p10; no active holder detected at inspection time.
- PipeWire/WirePlumber active; default USB mono microphone at 48 kHz and default HDMI stereo output at 48 kHz; no capture or playback validation.
- Repository is on SSHFS; system root is local ext4/NVMe with about 703 GB available.
- Godot 4.7.2 is selected but was not found. One unique pre-existing 4.6 stable binary content reports its version successfully.
- NTP is synchronized and automatic AC suspend action is disabled, but both system and user systemd managers report degraded; long-running and recovery behavior are unknown.

## Capability disposition

- Generic Godot Compatibility-renderer prerequisite: `SUPPORTED` by observed OpenGL 4.6/CPU/RAM/OS facts only.
- Selected Godot 4.7.2 executable: `BLOCKED` by absence and no-install boundary.
- Vulkan renderers: `UNKNOWN`.
- Camera and audio metadata paths: `OBSERVED`.
- Camera/audio quality, latency, concurrency, and Godot integration: `UNKNOWN`.
- Local inference headroom: `UNKNOWN`.
- Always-on operation: `DEGRADED / UNKNOWN`; service manager is degraded and recovery/soak evidence is absent.

## Operator decisions required

The complete evidence-backed eleven-record crosswalk is in `PRODUCT_CONTRACT_BRIEF.md`. Before architecture v1.0 approval, the operator still needs to define primary user/household, intended use/claims, offline/cloud/resource boundary, first caregiving scenario/jurisdiction, multi-user ownership/consent, voice/language/activation/interruption, retention/export/backup/deletion, notification transport/acknowledgment, support/continuity promise, and display habitat. Product naming may safely remain deferred if stable internal identifiers are retained.

## Architect decisions enabled

- Define a later engine-supply/version-verification action for the pinned 4.7.2 build without treating 4.6 as an automatic substitute.
- Preserve Compatibility rendering as an evidenced option and require exact Vulkan capability before considering Vulkan renderers.
- Require explicit logical-screen/output and scaling configuration in the presentation contract.
- Treat camera, audio, renderer, canonical state, and safety as separately degradable boundaries; exact technologies remain unselected.
- Separate SSHFS source/repository transport from local runtime state/cache assumptions.
- Require later health/recovery qualification for only the systemd units and session dependencies the architecture adopts.

## Remaining experiment requirements

- Exact Godot 4.7.2 launch/renderer/API behavior.
- Vulkan device/presentation query.
- Camera image quality/FOV/latency/load/sharing/reconnect.
- Microphone quality/noise/far-field/AEC/barge-in and speaker audibility/route switching.
- Concurrent rendering, sensor, speech, persistence, model, and safety resource use.
- Local-model benchmarks, thermal/power/noise measurements, storage latency, suspend/reboot/power-loss recovery, and long-run soak.

None is authorized by this directive.

## Publication and scope

- Notion report/directive: `PASSED` — updated and re-fetched with exact result SHA, review-pending state, closed product gate, and zero unknown blocks.
- GitHub Issue #2: `PASSED` — result comment `5598863339` added and issue re-fetched open for Architect review.
- Changed paths: `.agent/` only.
- Product implementation introduced: `NO`.
- System configuration changed: `NO`.
- Private media captured: `NO`.
- Dependency selected or installed: `NO`.
- Architecture v1.0 selected: `NO`.
- Contained deviation: one ephemeral diagnostic response exposed a hardware-serial field before sanitization; it was not retained or published in durable artifacts.

## Next action

Architect independently reviews the inventory, sanitization, crosswalk, and version/service/storage constraints, then accepts, continues, blocks, or rejects it. Acceptance of this inventory does not complete Roadmap Phase 00, authorize Godot installation, approve dependencies or architecture v1.0, or open Phase 01.
