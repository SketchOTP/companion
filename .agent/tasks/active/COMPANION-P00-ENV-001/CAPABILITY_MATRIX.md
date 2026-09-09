# COMPANION-P00-ENV-001 — Capability Matrix

Allowed status values: `OBSERVED`, `SUPPORTED`, `DEGRADED`, `UNKNOWN`, `BLOCKED`.

| Capability area | Status | Direct evidence | Limitation / uncertainty | Architecture consequence |
|---|---|---|---|---|
| Linux OS and session | PENDING | Pending | Pending | Pending |
| CPU and memory | PENDING | Pending | No workload qualification yet | Pending |
| GPU and active driver | PENDING | Pending | Pending | Pending |
| OpenGL capability | PENDING | Pending | Pending | Pending |
| Vulkan capability | PENDING | Pending | Pending | Pending |
| Godot 4.7.2 availability | PENDING | Pending | Do not install | Pending |
| Connected display geometry | PENDING | Pending | `RQ-14` remains open | Pending |
| Webcam enumeration | PENDING | Pending | Metadata only | Pending |
| Webcam formats/resolutions/frame intervals | PENDING | Pending | No frame capture | Pending |
| Microphone enumeration/default | PENDING | Pending | No recording | Pending |
| Speaker enumeration/default | PENDING | Pending | No playback test | Pending |
| Audio routing/session manager | PENDING | Pending | Pending | Pending |
| Repository-volume storage | PENDING | Pending | No benchmark | Pending |
| Time and suspend observability | PENDING | Pending | Pending | Pending |
| Always-on service prerequisites | PENDING | Pending | No service changes | Pending |
| Local inference headroom | UNKNOWN | No benchmark authorized | Must not be inferred from hardware labels alone | Later benchmark required |
| Camera/audio concurrent runtime behavior | UNKNOWN | No capture or benchmark authorized | Metadata cannot prove concurrency | Later bounded experiment required |

Replace every `PENDING` value with an allowed status or a documented blocker before completion.
