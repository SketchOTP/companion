# COMPANION-P00-ENV-001 — Architecture Implications

Status: `COMPLETE_FOR_ARCHITECT_REVIEW`

This document converts observed environment facts into constraints and preserved options for later architecture v1.0. It does not select dependencies, define final module boundaries, or qualify workload capacity.

## Host/runtime constraints

- **OBSERVED:** x86_64 Ubuntu 24.04 LTS, 8 physical cores/16 threads, 67.3 GB RAM, two 6 GiB NVIDIA GPUs, systemd 255.
- **INFERRED:** The host can support ordinary native Linux development and a simple Godot Compatibility-renderer workload at the generic specification level.
- **UNKNOWN:** Total companion workload fit, process concurrency, latency, contention, power, noise, thermal ceiling, and long-running behavior.
- Later architecture must preserve explicit resource budgets and degraded modes rather than assigning components from hardware labels alone.

## Graphics and Godot constraints

- **OBSERVED:** Accelerated OpenGL 4.6 is available with no software renderer detected. This preserves a Compatibility-renderer option.
- **UNKNOWN:** Exact Vulkan capability because the loader/ICD is present but no Vulkan capability tool is installed. Forward+ and Mobile renderer paths remain unqualified.
- **OBSERVED:** The selected 4.7.2 build is unavailable; one unique pre-existing 4.6 stable binary content is represented by two filesystem entries.
- Architecture v1.0 may preserve renderer fallback and GPU-selection seams, but it may not claim exact 4.7.2 behavior until that build is supplied and tested under separate authority.

## Display and habitat constraints

- **OBSERVED:** The host is not a single-display surface: two 4K outputs form a 7680×2160 GNOME work area, while a separate 1366×768 output is managed by Openbox on another logical X screen.
- The presentation boundary must identify logical screen, connector, usable work area, scale, focus/input behavior, display removal/reconnect behavior, and placement persistence.
- Preserved option classes are full-screen on one selected output, a bounded habitat/window, or an overlay. None is adopted here.
- `RQ-14` must decide the default habitat and size before an exact window contract or visual occupancy target can be approved.

## Camera boundary implications

- **OBSERVED:** One UVC camera exposes separate video and metadata nodes. The video node supports compressed 1080p30 and lower-bandwidth/raw alternatives; controls are visible and the node is accessible.
- **UNKNOWN:** Capture quality, FOV, latency, sustained stability, multiple-client sharing, and concurrent camera/audio/render behavior.
- The later sensor boundary must enumerate and select formats deliberately, expose permission/device-busy/degraded states, and avoid assuming the highest listed mode is the correct runtime mode.
- Godot CameraServer support is a generic API fact, not proof that this device works through the selected engine build.

## Audio boundary implications

- **OBSERVED:** PipeWire/WirePlumber is the active graph. The default microphone is a dedicated USB mono input at 48 kHz, distinct from the webcam's 16 kHz mono microphone. Default output is HDMI stereo at 48 kHz; onboard analog endpoints also exist.
- The architecture must not assume microphone/camera co-location, speaker audibility, echo cancellation, or that current default devices remain stable.
- A later audio contract needs explicit device selection/fallback, format conversion boundaries, route-change handling, mute/degraded state, and permission failure reporting.
- VAD, wake word, STT, TTS, echo cancellation, and interruption behavior remain unselected and require operator/product decisions plus later acoustic evidence.

## Persistence and storage implications

- **OBSERVED:** The Git working tree is on SSHFS; the operating-system volume is local ext4/NVMe.
- Repository transport, source checkout, runtime state, model cache, audit evidence, and backup are separate storage concerns. Architecture must not assume SSHFS semantics or availability are appropriate for live canonical state.
- Local ext4/NVMe capacity preserves a local-storage option, but durability, backup, encryption, migration, export, restore, and power-loss behavior remain unqualified.
- No database, storage engine, or retention policy is selected.

## Always-on and recovery implications

- **OBSERVED:** NTP is synchronized and automatic AC suspend action is disabled, but both system and user systemd managers report degraded. Core inspected units remain active.
- **UNKNOWN:** Causes of unrelated failed units, reboot recovery, session-login dependency, display-server restart behavior, suspend/resume recovery, power-loss recovery, UPS coverage, and long-running stability.
- Later service design must define visible startup/degraded/recovery states and qualify only its own relevant units without assuming the wider manager is healthy.
- A desktop session is currently required for observed display/audio metadata; architecture must decide which components may run without a logged-in graphical session.

## Evidence gaps requiring later experiments

- Exact Godot 4.7.2 launch and renderer selection.
- Vulkan device/presentation capability.
- Camera image quality, lighting/FOV, latency, format cost, device sharing, and disconnect/reconnect.
- Microphone quality, noise floor, far-field speech, playback audibility, route switching, echo cancellation, and barge-in.
- Concurrent rendering, perception, speech, persistence, and model resource use.
- Local inference latency, memory/VRAM use, throughput, contention, and fallback.
- Repository versus local-volume build/cache/runtime behavior.
- Suspend/resume, logout/login, reboot, power-loss, service restart, long-run soak, thermal, power, and noise behavior.

Every item above requires a later bounded directive; none is authorized by this inventory.

## Options preserved

- Compatibility rendering now; Vulkan renderers only after capability execution.
- Full-screen, bounded-window, or overlay habitat on an explicitly selected output.
- Dedicated USB microphone or webcam microphone after acoustic/placement testing, with explicit fallback.
- Compressed or raw camera modes selected from later measured quality/load evidence.
- Local runtime state on local storage with repository transport kept separate; exact persistence/backup technology remains open.
- User-session services or split system/user service topology after privilege, privacy, and recovery requirements are decided.
