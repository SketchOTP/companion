# COMPANION-P00-ENV-001 — Environment Report

Status: `COMPLETE_FOR_ARCHITECT_REVIEW`

Retrieval confidence: `ADEQUATE`

## Executive summary

- **OBSERVED:** The iteration-one host is Ubuntu 24.04.5 LTS on x86_64 with an 8-core/16-thread Ryzen 7 5800XT, about 67.3 GB RAM, two NVIDIA GPUs using driver 595.84, three connected display outputs across two logical X screens, one UVC webcam, and an active PipeWire/WirePlumber audio stack.
- **OBSERVED:** The repository resides on network-backed SSHFS, while the system root is local ext4 on NVMe with about 703 GB available. These filesystems must not be treated as interchangeable runtime/storage targets.
- **OBSERVED:** Accelerated OpenGL 4.6 is working. The Vulkan loader and NVIDIA ICD are present, but `vulkaninfo` is unavailable, so exact Vulkan capability remains `UNKNOWN`.
- **OBSERVED:** The selected Godot 4.7.2 baseline is not installed in the inspected surfaces. Two entries with identical content report Godot 4.6 stable and accept `--version`; no project was opened or created.
- **UNKNOWN:** Metadata does not qualify concurrent Godot, camera, audio, speech, model, memory, and safety workloads. It also does not establish camera/image quality, audio quality, latency, echo cancellation, power, noise, thermals under load, suspend recovery, or long-running stability.

## Host and session

- **OBSERVED:** Ubuntu 24.04.5 LTS, kernel 7.0.0-31-generic, x86_64, UEFI boot, glibc 2.39.
- **OBSERVED:** AMD Ryzen 7 5800XT, 8 physical cores, 16 logical CPUs, SSE4.2/AVX/AVX2/FMA/AES/SHA support, no AVX-512.
- **OBSERVED:** 67,303,972,864 bytes RAM and 8,589,930,496 bytes swap; roughly 40.25 GB RAM was available during collection.
- **OBSERVED:** Active session type is X11 under Ubuntu GNOME. The X server exposes two logical screens with GNOME Shell on screen 0 and Openbox on screen 1.
- **UNKNOWN:** `loginctl` session properties were unavailable because the execution shell lacked a login-session identifier. This is a tool-context limitation, not evidence that no desktop session exists.

## Graphics and display

- **OBSERVED:** NVIDIA GeForce GTX 1660 SUPER and GeForce RTX 3050 6GB, both using the `nvidia` kernel driver; each reports 6 GiB VRAM.
- **OBSERVED:** Direct rendering is enabled and the X server exposes OpenGL 4.6 through both GPUs. No software renderer appeared in `glxinfo`.
- **UNKNOWN:** Exact Vulkan version, device features, and presentation support. A Vulkan loader and NVIDIA ICD exist, but the diagnostic utility is absent.
- **OBSERVED:** Logical X screen 0 is 7680×2160 across two normal-orientation 3840×2160 outputs at 60 Hz. DP-0 is primary; the usable work area is 7614×2104.
- **OBSERVED:** Logical X screen 1 is 1366×768 on one normal-orientation HDMI output at 59.96 Hz; usable work area is 1366×722 and no primary flag is exposed.
- **OBSERVED:** RandR transforms are identity. GNOME text scaling is 1.75 and its integer scaling key is automatic/default.
- **UNKNOWN / OPERATOR INPUT REQUIRED:** Effective in-application scale, target X screen/output, desired on-screen size, movement area, and full-screen versus bounded-window versus overlay habitat. These directly constrain `RQ-14` but do not resolve it.

## Storage and always-on operation

- **OBSERVED:** Repository volume: `fuse.sshfs`, about 1.10 TB available. It is network-backed FUSE, not a local block device. No throughput or latency benchmark was run.
- **OBSERVED:** System root: ext4 on a non-rotating 1 TB-class NVMe SSD, about 703 GB available. No benchmark or health query was run.
- **OBSERVED:** systemd 255 is PID 1. Both system and user managers report degraded; 48 system units and 20 user units were failed at the collection instant. Failed-unit identities were not collected because they may disclose unrelated system activity.
- **OBSERVED:** Time synchronization is enabled and synchronized. Logind, D-Bus, the graphical target, PipeWire, PipeWire Pulse compatibility, and WirePlumber are active.
- **OBSERVED:** Kernel power metadata exposes `freeze` and `mem`, with deep sleep selected. GNOME's AC idle action is `nothing`; actual suspend/resume was not exercised.
- **DEGRADED:** Thermal visibility is incomplete. GPU temperatures were observable at the inventory instant, but no CPU temperature or kernel thermal zones were exposed.
- **UNKNOWN:** Power-loss recovery, UPS coverage, reboot/session recovery, suspend recovery, workload thermals, power/noise, and long-running stability.

## Webcam

- **OBSERVED:** One NexiGo N60 FHD UVC webcam using `uvcvideo` exposes a video node, a UVC metadata node, and a media node. All are readable by the current process; no current device holder was detected at the observation instant.
- **OBSERVED:** MJPEG supports 320×240 through 1920×1080 at 30/25/15 fps. YUYV supports up to 800×600 at 30/25/15 fps, 1024×576 at 20/15/10 fps, and 1280×720 at 10/5 fps.
- **OBSERVED:** Controls include brightness, contrast, saturation, white balance, gain, power-line frequency, sharpness, exposure, pan, tilt, autofocus, and zoom.
- **UNKNOWN:** Field of view, image quality, lighting tolerance, latency, exclusive versus shared access, Godot feed behavior, and sustained or concurrent operation.
- **OBSERVED:** No camera frame or screenshot was captured, retained, or transmitted.

## Microphone and speakers

- **OBSERVED:** PipeWire 1.0.5, WirePlumber 0.4.17, and PulseAudio compatibility are active.
- **OBSERVED:** Default input is a running, unmuted USB microphone using mono S16_LE at 48 kHz; hardware metadata advertises 44.1 and 48 kHz. The webcam also exposes mono S16_LE at 16 kHz, and onboard analog stereo input is visible.
- **OBSERVED:** Default output is a running, unmuted HDMI digital stereo sink using S32_LE at 48 kHz. Onboard analog stereo output is also visible.
- **UNKNOWN:** Audible output, signal quality, room acoustics, far-field pickup, latency, acoustic echo cancellation, wake word, interruption/barge-in, and simultaneous capture/playback behavior.
- **OBSERVED:** No audio was recorded and no test audio was played. Application stream ownership was not enumerated to avoid unrelated private activity.

## Godot and existing tools

- **OBSERVED:** Godot 4.7.2 was not found in PATH, Debian packages, Flatpak, Snap, desktop entries, or bounded common executable locations. Installation was prohibited and not attempted.
- **OBSERVED:** Two filesystem entries in bounded user locations have one shared content hash and report `4.6.stable.official.89cea1439`; `--version` exited successfully.
- **INFERRED:** The CPU, RAM, Linux vintage, local free storage, dedicated GPUs, and working OpenGL 4.6 exceed Godot's generic recommended baseline for a simple Compatibility-renderer project. The official documentation explicitly warns that actual project scope and competing workloads require testing; this inference does not qualify this companion workload.
- **UNKNOWN:** Forward+/Mobile renderer eligibility until Vulkan capability is executed, and all behavior of the selected 4.7.2 build until that exact version is made available under later authority.
- **OBSERVED:** Git, Bash, GCC/G++, Make, Python, Node/npm, Docker CLI, FFmpeg, GStreamer, jq, ripgrep, camera/audio diagnostics, NVIDIA/OpenGL diagnostics, and XRandR tools are present. Presence is not dependency approval.
- **OBSERVED:** Several other tools are absent, including `vulkaninfo`, `vainfo`, `smartctl`, Clang, CMake, Ninja, Rust/Cargo, Java, and compositor-specific Wayland utilities. Absence of a utility is not absence of the corresponding hardware capability.

## Material constraints for architecture v1.0

1. The selected engine version is not currently runnable; architecture cannot cite a local 4.7.2 launch until a later directive authorizes how that exact build is supplied.
2. The display habitat must explicitly select a logical X screen/output and scaling policy; “the monitor” is not a singular target on this host.
3. A Compatibility-renderer path has generic host support; a Vulkan renderer path remains unverified.
4. Sensor boundaries must account for one video node plus a distinct metadata node, multiple audio inputs, a default microphone separate from the webcam microphone, and currently running default audio nodes.
5. Repository-on-SSHFS and local-runtime-on-ext4/NVMe must be treated as different failure/performance domains.
6. Always-on service design cannot assume a healthy systemd baseline or complete thermal/power visibility; relevant unit health and recovery behavior need later bounded qualification.

## Discrepancies and blocked observations

- Canonical selection: Godot 4.7.2. Live installation: only Godot 4.6 discovered. This is a version-availability gap, not a change to the adopted engine ruling.
- `vulkaninfo`, `vainfo`, and `smartctl` are unavailable. Their absence narrows evidence; it does not disprove Vulkan, hardware video, or drive-health capability.
- One camera metadata command does not apply to the video-capture node and returned an invalid-argument status; the same command succeeded on the metadata node.
- A first sensor JSON filter failed on a non-object field; a corrected filter ran successfully. No source fact was inferred from the failed parser.
- Media capture, playback, benchmarks, suspend/reboot/power-loss exercises, and concurrent-load tests were blocked by directive, not attempted.

## Privacy and sanitization

Only selected fields were retained. Host/account names, private paths, network addresses, filesystem identifiers, persistent device identifiers, audio node identifiers, unrelated application streams, and failed-unit names are absent from durable artifacts. One live driver/audio metadata response exposed a hardware-serial field before filtering; it was immediately discarded, no raw output file was retained, and the value is absent from the repository and Notion report. This containment is preserved as a deviation rather than hidden.

## Sources

- Canonical directive: https://app.notion.com/p/3d6833cb27ff81e6ab93e37fc851b49d
- Research anchor R09: https://app.notion.com/p/3d5833cb27ff8146b6dee00af9a071d8
- Research anchor R10: https://app.notion.com/p/3d5833cb27ff81989d95f604112e25ba
- Godot 4.7 system requirements: https://docs.godotengine.org/en/4.7/about/system_requirements.html
- Godot 4.7 CameraServer: https://docs.godotengine.org/en/4.7/classes/class_cameraserver.html
- Godot 4.7 AudioStreamMicrophone: https://docs.godotengine.org/en/4.7/classes/class_audiostreammicrophone.html
- Linux V4L2 function reference: https://docs.kernel.org/userspace-api/media/v4l/user-func.html
- WirePlumber `wpctl`: https://pipewire.pages.freedesktop.org/wireplumber/man/wpctl.html
- X.Org RandR: https://www.x.org/Projects/XRandR/
