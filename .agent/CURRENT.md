# Current Project State

## Current stage

Planning Phase 02 — Master Delivery Roadmap remains active.

Roadmap Phase 00 — Planning and Product Contract remains active. The canonical ingest and Linux environment inventory are accepted. Operator Decision Packet 01 is partially resolved: three high-coupling product decisions are adopted and the dedicated display is selected. Product implementation remains closed.

## Current objective

Obtain the remaining habitat-mode ruling for the selected 1366×768 Openbox-managed output: borderless full-screen habitat, bounded resizable habitat window, or transparent desktop overlay. After that ruling is recorded, close Decision Packet 01 and issue the next bounded Roadmap Phase 00 directive for architecture v1.0 options and the first vertical-slice contract. Do not install or run Godot 4.7.2, select dependencies, run media/workload benchmarks, create product or asset work, approve architecture v1.0, or begin Phase 01 without explicit later authority.

## Directive and operator-gate state

- Active coder directive: `NONE`
- Active task packet: `NONE`
- Active operator gate: https://app.notion.com/p/3d6833cb27ff817a8972cecb1b877260
- Operator-gate status: `PARTIALLY RESOLVED — HABITAT MODE PENDING`
- Last completed directive: `COMPANION-P00-ENV-001`
- Last directive verdict: `ACCEPTED — ENVIRONMENT EVIDENCE QUALIFIED`
- Completed environment packet: `.agent/tasks/completed/COMPANION-P00-ENV-001/`
- Environment Architect review: `.agent/tasks/completed/COMPANION-P00-ENV-001/ARCHITECT_REVIEW.md`
- Environment acceptance commit: `19140d1076bd6cbd23f25b76b54f9637acec8d84`
- Previous operator-gate routing commit: `d3a3ed4998587510ae4cab828b9e6ff0bff1ea25`
- Product implementation authorization: `CLOSED`

## Adopted operator rulings — 2026-09-09

- `RQ-02 — First user population and household model`: **RESOLVED**. Iteration one targets one adult primary user aged 18 or older who may have support needs, using a single-primary-user authority model with explicitly configured trusted caregivers/contacts. Minors are out of scope.
- `RQ-03 — Intended product use and commercialization path`: **RESOLVED**. Develop toward a consumer product from the start under the narrow non-medical claim: a persistent digital companion with configurable check-in and trusted-contact assistance. Diagnosis, guaranteed emergency detection, prevention of harm, continuous medical monitoring, and replacement for emergency services remain excluded unless separately qualified and classified.
- `RQ-05 — First caregiving scenario and escalation jurisdiction`: **RESOLVED**. The first scenario is an explicit spoken help request. The first jurisdiction is Kentucky, United States. Qualification begins with simulation, recorded replay, and shadow mode before live trusted-contact delivery.
- `RQ-14 — Godot presentation mode and screen habitat`: **PARTIALLY RESOLVED**. The dedicated iteration-one mon display is the separate 1366×768 Openbox-managed output. The default habitat mode remains open.

## Current canonical counts

- Research evidence: `46` records — `33` Grade A, `11` Grade B, `2` Grade C.
- Architecture decisions: `36` records — `20` adopted, `14` interim, `2` rejected.
- Decision/research-gap queue: `14` items — `6` resolved, `2` partially resolved, `6` open.

## Accepted environment evidence

- Host: Ubuntu 24.04.5 LTS, x86_64, X11; Ryzen 7 5800XT with 8 physical cores/16 threads; approximately 67.3 GB RAM.
- Graphics: GTX 1660 SUPER and RTX 3050 6GB on NVIDIA 595.84; direct OpenGL 4.6 observed. Exact Vulkan device/presentation capability remains unknown.
- Display: two 4K/60 Hz GNOME-managed outputs and one 1366×768/59.96 Hz Openbox-managed output. The Openbox output is now selected for the mon.
- Camera: one readable UVC webcam with enumerated MJPEG through 1080p30 and YUYV through 720p10. Quality, latency, field of view, sharing, and integrated behavior remain unknown.
- Audio: PipeWire/WirePlumber active; default USB mono microphone at 48 kHz and default HDMI stereo output at 48 kHz. Acoustics, latency, echo cancellation, wake behavior, and barge-in remain unknown.
- Storage: repository on network-backed SSHFS; local system storage on ext4/NVMe. Canonical runtime state must not use the repository volume by assumption.
- Godot: selected 4.7.2 build was not found. A pre-existing 4.6 stable binary is not an approved substitute.
- Operations: system and user systemd managers reported degraded. Adopted service topology, recovery, power, thermal behavior, and endurance remain unqualified.

## Current evidence and compliance implications

- Kentucky consumer-product development triggers a product-specific applicability review of the Kentucky Consumer Data Protection Act before a Kentucky consumer pilot or release. Applicability is not assumed solely from the project description.
- Selecting the Openbox output does not select a window mode. Godot 4.7 supports fullscreen, borderless, transparent, focus, and passthrough behaviors; on Linux X11, exclusive fullscreen bypasses the compositor. No exclusive mode is implied.
- Future machine probes must use source-level field allowlists and pre-reviewed bounded commands wherever practical; post-processing redaction is only a secondary control.

## Remaining open and partially resolved decisions

- `RQ-04 — Offline, cloud, compute, power, noise, and cost boundary`: open.
- `RQ-07 — Multi-user identity, ownership, and relationship model`: open beyond the adopted single-primary-user baseline.
- `RQ-08 — Voice, languages, wake word, and interruption model`: open.
- `RQ-09 — Memory retention, export, backup, and deletion promises`: open.
- `RQ-10 — Notification and trusted-contact transport`: open.
- `RQ-11 — Support lifetime and continuity promise`: open.
- `RQ-12 — Canonical product name`: partially resolved; repository name fixed, public product name open.
- `RQ-14 — Godot presentation mode and screen habitat`: partially resolved; Openbox output selected, habitat mode open.

## Current blockers

- Operator selection of the Openbox habitat mode.
- Roadmap Phase 00 architecture v1.0, process/privilege/data boundaries, first vertical-slice contract, dependency and rights shortlist, threat/privacy models, measurable acceptance thresholds, and repository/CI/test/release rules remain incomplete.
- Godot 4.7.2 supply, exact runtime verification, Vulkan verification, media/workload benchmarks, dependency selection, Phase 01, and all product implementation remain closed.

## Next operator decision point

Choose one default mode for the selected Openbox display:

- `A` — borderless full-screen habitat
- `B` — bounded resizable habitat window
- `C` — transparent desktop overlay
