# COMPANION-P00-ENV-001 — Capability Matrix

Allowed status values: `OBSERVED`, `SUPPORTED`, `DEGRADED`, `UNKNOWN`, `BLOCKED`.

Status: `COMPLETE_FOR_ARCHITECT_REVIEW`

| Capability area | Status | Direct evidence | Limitation / uncertainty | Architecture consequence |
|---|---|---|---|---|
| Linux OS and session | OBSERVED | Ubuntu 24.04.5 LTS, x86_64, kernel 7.0.0-31, X11, two logical X screens | Login-session properties unavailable in execution context | Treat X11 and two window-manager surfaces as the actual presentation baseline |
| CPU and memory | OBSERVED | Ryzen 7 5800XT, 8 cores/16 threads, 67.3 GB RAM, 8.59 GB swap | No concurrent workload benchmark | Hardware labels cannot select model size or prove headroom |
| GPU and active driver | OBSERVED | GTX 1660 SUPER plus RTX 3050 6GB; proprietary NVIDIA 595.84 | Display-to-GPU affinity was not proven | Later runtime must identify its actual adapter and screen explicitly |
| OpenGL capability | SUPPORTED | Direct rendering and OpenGL 4.6 on both exposed NVIDIA contexts | Godot 4.7.2 not installed | Generic Godot Compatibility-renderer prerequisite is supported, not workload-qualified |
| Vulkan capability | UNKNOWN | Vulkan loader and NVIDIA ICD present | `vulkaninfo` unavailable; exact API/features/presentation unexecuted | Do not select Forward+ or Mobile renderer from this inventory |
| Godot 4.7.2 availability | BLOCKED | Selected version absent from all inspected installation surfaces | Installation prohibited by directive | Exact engine launch and integration evidence require later authority |
| Existing Godot executable | OBSERVED | Two entries with identical content report Godot 4.6 official stable and pass `--version` | Version differs from selected baseline; no project launched | Treat only as pre-existing tooling, not the approved implementation engine |
| Connected display geometry | OBSERVED | Three outputs across 7680×2160 and 1366×768 logical X screens; normal orientation; 60/59.96 Hz | Effective app scale and target output unresolved | `RQ-14` must choose screen, habitat, size, and scaling behavior |
| Webcam enumeration | OBSERVED | One readable UVC webcam; video, metadata, and media nodes; no holder detected | Instantaneous holder check cannot prove future availability | Sensor ownership and visible degraded state need explicit design |
| Webcam formats/resolutions/frame intervals | OBSERVED | MJPEG through 1080p30; YUYV through 720p10; control metadata available | No frame capture, quality, FOV, latency, or multi-client test | Later experiment must select a mode from measured quality/latency/load evidence |
| Microphone enumeration/default | OBSERVED | Default USB mic is mono S16_LE at 48 kHz; 44.1/48 kHz advertised | No recording, signal-quality, latency, or far-field test | Input selection cannot be based on enumeration alone |
| Speaker enumeration/default | OBSERVED | Default HDMI stereo sink is S32_LE at 48 kHz; analog sink also visible | No audible playback or route confirmation | Output selection and failure detection require later playback evidence |
| Audio routing/session manager | OBSERVED | PipeWire 1.0.5, WirePlumber 0.4.17, active Pulse compatibility; defaults visible | Active-stream owners omitted; AEC/barge-in/concurrency unknown | Preserve an audio adapter boundary and explicit degraded states |
| Repository-volume storage | DEGRADED | Network-backed SSHFS with about 1.10 TB available | No local block-device semantics or benchmark | Do not assume repo mount latency/durability is suitable for live state or caches |
| Local system storage | OBSERVED | ext4 on local NVMe, about 703 GB available | No health, latency, throughput, or power-loss evidence | Local persistence remains feasible as an option but unqualified operationally |
| Time and suspend observability | OBSERVED | NTP synchronized; freeze/mem and deep sleep exposed; no automatic AC suspend action | Suspend/resume not exercised | Runtime must tolerate wall-clock and sleep transitions; recovery remains unproven |
| Always-on service prerequisites | DEGRADED | systemd/user managers work and key units are active | Both managers report degraded with 48/20 failed-unit counts; causes not collected | Do not assume clean service-manager state; qualify relevant units later |
| Thermal and power visibility | DEGRADED | GPU temperature and CPU governor visible | No CPU temperature, load thermals, host battery, UPS, energy, or noise evidence | Resource and shutdown policies require later measurement/operator input |
| Local inference headroom | UNKNOWN | No benchmark authorized | CPU/GPU/RAM specifications do not prove model fit or concurrency | Later model-specific bounded benchmarks are required |
| Camera/audio concurrent runtime behavior | UNKNOWN | Metadata-only device enumeration | No capture, playback, Godot, or concurrent-load test | Later bounded integration experiment is required |

`SUPPORTED` here means only that directly observed facts meet the cited generic prerequisite. It does not mean the companion workload, target engine build, or integrated system has passed.
