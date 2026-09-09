# Current Project State

## Current stage

Planning Phase 02 — Master Delivery Roadmap is active.

Roadmap Phase 00 — Planning and Product Contract remains active. `COMPANION-P00-ENV-001` remains the active bounded directive. Codex has completed the privacy-sanitized host/peripheral inventory and product-contract evidence for publication and independent Architect review. Product implementation remains closed.

## Current objective

Publish and independently review the environment evidence. Do not install Godot 4.7.2, resolve operator choices, select dependencies, draft architecture v1.0 as final, run workload/media benchmarks, or begin product implementation without a new or continued bounded directive.

## Directive state

- Active directive: `COMPANION-P00-ENV-001`
- Directive status: `CODEX RESULT PREPARED — PUBLICATION / ARCHITECT REVIEW PENDING`
- Issuer: Architect
- Verified pre-directive baseline: `ddb6b130ab6428a1f395cd223d309eeaa2ac7462`
- Directive publication commit: `c06c796d9d54da4cdcf38296ee08c4f70fb3993d`
- Starting routing head: `2ea7b41d79f24f030ea3c3690dee00e8c2340671`
- Codex result commit: `PENDING_PUBLICATION`
- Notion directive: https://app.notion.com/p/3d6833cb27ff81e6ab93e37fc851b49d
- Required Notion report: https://app.notion.com/p/3d6833cb27ff8159b66fdebeb690be90
- GitHub issue: https://github.com/SketchOTP/companion/issues/2
- Active task packet: `.agent/tasks/active/COMPANION-P00-ENV-001/`
- Last completed directive: `COMPANION-P00-INGEST-001`
- Last accepted outcome: `COMPANION-P00-INGEST-001-ARCHITECT-ACCEPTANCE-02`
- Product implementation authorization: `CLOSED`

## Current observed environment evidence

- Host: Ubuntu 24.04.5 LTS, kernel 7.0.0-31-generic, x86_64, X11; Ryzen 7 5800XT with 8 cores/16 threads; about 67.3 GB RAM and 8.59 GB swap.
- Graphics: GTX 1660 SUPER plus RTX 3050 6GB on NVIDIA 595.84; accelerated OpenGL 4.6 observed; exact Vulkan capability unknown because the loader/ICD exists but `vulkaninfo` is absent.
- Display: three connected outputs across two logical X screens—two 3840×2160/60 Hz GNOME outputs and one 1366×768/59.96 Hz Openbox output. `RQ-14` remains an operator decision.
- Camera: one readable NexiGo N60 UVC webcam with separate video/metadata nodes; MJPEG through 1920×1080/30 fps and YUYV through 1280×720/10 fps; no holder at inspection time; no frames captured.
- Audio: PipeWire 1.0.5/WirePlumber 0.4.17 active; default USB mono microphone at 48 kHz and default HDMI stereo output at 48 kHz; no recording or playback test.
- Storage: repository on network-backed SSHFS; system root on local ext4/NVMe with about 703 GB available; no benchmark.
- Godot: selected 4.7.2 build not found in inspected installation surfaces; one unique pre-existing 4.6 stable binary content is represented by two entries and accepted `--version`. This does not revise the 4.7.2 ruling.
- Operations: NTP synchronized and automatic AC suspend action disabled; both system and user systemd managers report degraded, while key inspected services remain active. Recovery, power, noise, load thermals, and long-run stability are unqualified.

## Evidence classification

- Host/peripheral metadata: `E1_OBSERVED`.
- Sanitized artifact structure, RQ crosswalk, and consistency validation: `E3_TARGET_TESTED`.
- Generic Godot Compatibility-renderer prerequisite: `SUPPORTED` only at the published simple-project specification level.
- Companion workload, local inference, camera/audio stream quality, concurrent execution, safety behavior, and always-on operation: `NOT ESTABLISHED`.
- Retrieval confidence: `ADEQUATE`.
- Architect acceptance: `NOT ASSIGNED`.

## Canonical open and partially resolved decisions

- `RQ-02 — First user population and household model`: open.
- `RQ-03 — Intended product use and commercialization path`: open.
- `RQ-04 — Offline, cloud, compute, power, noise, and cost boundary`: open.
- `RQ-05 — First caregiving scenario and escalation jurisdiction`: open.
- `RQ-07 — Multi-user identity, ownership, and relationship model`: open.
- `RQ-08 — Voice, languages, wake word, and interruption model`: open.
- `RQ-09 — Memory retention, export, backup, and deletion promises`: open.
- `RQ-10 — Notification and trusted-contact transport`: open.
- `RQ-11 — Support lifetime and continuity promise`: open.
- `RQ-12 — Canonical product name`: partially resolved; repository name fixed, product-facing name open.
- `RQ-14 — Godot presentation mode and screen habitat`: open.

## Directive boundaries preserved

- No elevated access, package installation, driver/permission/service/display/audio/power change, media capture, playback, benchmark, or disruptive state transition occurred.
- No product source, Godot project, asset, dependency, manifest, CI, deployment, model, dataset, voice, database implementation, biometric operation, notification, or safety integration was introduced.
- No architecture or operator decision was silently resolved.
- One ephemeral diagnostic response exposed a hardware-serial field before filtering; it was immediately discarded and is absent from every repository and Notion artifact. This remains recorded as a contained privacy-handling deviation.

## Current blockers

- Independent Architect review of the inventory result is not yet performed.
- Godot 4.7.2 is selected but not currently available on the host under the inspected surfaces; installation is not authorized.
- Vulkan device/presentation capability is unknown because the existing diagnostic stack lacks `vulkaninfo`.
- Both systemd managers report degraded; relevant failure causes and adopted service topology remain unqualified.
- All eleven product-contract records remain open or partially resolved; the machine evidence informs but does not answer them.
- Roadmap Phase 00, architecture v1.0, dependency selection, Phase 01, and product implementation remain closed.

## Next Architect decision point

Review the sanitized raw inventory, report, capability matrix, eleven-RQ product-contract brief, architecture constraints, privacy deviation, validation evidence, Notion report, GitHub Issue #2, and exact result commit. Accept, continue, block, or reject without inferring product authority.
