# Current Project State

## Current stage

Planning Phase 02 — Master Delivery Roadmap remains active.

Roadmap Phase 00 — Planning and Product Contract remains active. The canonical ingest, Linux environment inventory, and Operator Decision Packet 01 are complete. Product implementation remains closed.

## Current objective

Issue the next bounded Roadmap Phase 00 directive for architecture v1.0 options and the first vertical-slice contract. That directive must convert accepted environment evidence and adopted operator rulings into decision-ready architecture, process/data/privilege boundaries, repository expansion rules, dependency evaluation criteria, measurable acceptance thresholds, and deliberate dispositions for the remaining product-contract questions. It must not install Godot, select dependencies by assumption, run media/workload benchmarks, create product source/assets, approve architecture v1.0, or open Phase 01 by implication.

## Directive and gate state

- Active coder directive: `NONE`
- Active task packet: `NONE`
- Operator Decision Packet 01: `COMPLETE`
- Operator decision page: https://app.notion.com/p/3d6833cb27ff817a8972cecb1b877260
- Last completed coder directive: `COMPANION-P00-ENV-001`
- Last coder-directive verdict: `ACCEPTED — ENVIRONMENT EVIDENCE QUALIFIED`
- Completed environment packet: `.agent/tasks/completed/COMPANION-P00-ENV-001/`
- Environment acceptance commit: `19140d1076bd6cbd23f25b76b54f9637acec8d84`
- Initial operator-ruling publication: `0a4912cef63b5d4d64f8ab2f9abd7d18e7619906`
- Final habitat-ruling publication: `PENDING_PUBLICATION`
- Product implementation authorization: `CLOSED`

## Adopted operator rulings — 2026-09-09

- `RQ-02 — First user population and household model`: **RESOLVED**. Iteration one targets one adult primary user aged 18 or older who may have support needs, using a single-primary-user authority model with explicitly configured trusted caregivers/contacts. Minors are out of scope.
- `RQ-03 — Intended product use and commercialization path`: **RESOLVED**. Develop toward a consumer product from the start under the narrow non-medical claim: a persistent digital companion with configurable check-in and trusted-contact assistance. Diagnosis, guaranteed emergency detection, prevention of harm, continuous medical monitoring, and replacement for emergency services remain excluded unless separately qualified and classified.
- `RQ-05 — First caregiving scenario and escalation jurisdiction`: **RESOLVED**. The first scenario is an explicit spoken help request. The first jurisdiction is Kentucky, United States. Qualification begins with simulation, recorded replay, and shadow mode before live trusted-contact delivery.
- `RQ-14 — Godot presentation mode and screen habitat`: **RESOLVED**. The mon uses a bounded resizable Godot habitat window on the separate 1366×768 Openbox-managed output. Full-screen and transparent-overlay modes are not iteration-one defaults.

## Current canonical counts

- Research evidence: `46` records — `33` Grade A, `11` Grade B, `2` Grade C.
- Architecture decisions: `37` records — `21` adopted, `14` interim, `2` rejected.
- Decision/research-gap queue: `14` items — `7` resolved, `1` partially resolved, `6` open.

## Accepted environment evidence

- Host: Ubuntu 24.04.5 LTS, x86_64, X11; Ryzen 7 5800XT with 8 physical cores/16 threads; approximately 67.3 GB RAM.
- Graphics: GTX 1660 SUPER and RTX 3050 6GB on NVIDIA 595.84; direct OpenGL 4.6 observed. Exact Vulkan device/presentation capability remains unknown.
- Display: two 4K/60 Hz GNOME-managed outputs and one 1366×768/59.96 Hz Openbox-managed output. The Openbox output and bounded resizable window mode are selected for the mon.
- Camera: one readable UVC webcam with enumerated MJPEG through 1080p30 and YUYV through 720p10. Quality, latency, field of view, sharing, and integrated behavior remain unknown.
- Audio: PipeWire/WirePlumber active; default USB mono microphone at 48 kHz and default HDMI stereo output at 48 kHz. Acoustics, latency, echo cancellation, wake behavior, and barge-in remain unknown.
- Storage: repository on network-backed SSHFS; local system storage on ext4/NVMe. Canonical runtime state must not use the repository volume by assumption.
- Godot: selected 4.7.2 build was not found. A pre-existing 4.6 stable binary is not an approved substitute.
- Operations: system and user systemd managers reported degraded. Adopted service topology, recovery, power, thermal behavior, and endurance remain unqualified.

## Product and architecture consequences

- Consumer-product engineering must include rights, security, privacy, update, support, recovery, and evidence practices from Phase 01 rather than treating them as pre-release cleanup.
- Kentucky applicability analysis must cover KCDPA thresholds/exemptions and other relevant federal/state privacy, biometric, recording, health-like-data, and consumer-protection obligations before a Kentucky pilot or release.
- Spoken-help qualification must cover accidental media playback, replay/spoofing, uncertain speaker identity, confirmation, accessible fallback, cancellation, false activation, degraded audio, trusted-contact acknowledgment, and immutable audit.
- The bounded resizable habitat must define initial/minimum/maximum geometry, content scaling, aspect behavior, mon occupancy, placement persistence, focus/input behavior, selected-screen recovery, and response to display removal or geometry change.
- Future machine probes must use source-level field allowlists and pre-reviewed bounded commands wherever practical; post-processing redaction is only a secondary control.

## Remaining open and partially resolved decisions

- `RQ-04 — Offline, cloud, compute, power, noise, and cost boundary`: open.
- `RQ-07 — Multi-user identity, ownership, and relationship model`: open beyond the adopted single-primary-user baseline.
- `RQ-08 — Voice, languages, wake word, and interruption model`: open.
- `RQ-09 — Memory retention, export, backup, and deletion promises`: open.
- `RQ-10 — Notification and trusted-contact transport`: open.
- `RQ-11 — Support lifetime and continuity promise`: open.
- `RQ-12 — Canonical product name`: partially resolved; repository name fixed, public product name open.

## Current blockers

- Roadmap Phase 00 architecture v1.0, process/privilege/data boundaries, first vertical-slice contract, dependency and rights shortlist, threat/privacy models, measurable acceptance thresholds, and repository/CI/test/release rules remain incomplete.
- The remaining product-contract decisions must be resolved or deliberately deferred without creating an immediate redesign risk.
- Godot 4.7.2 supply, exact runtime verification, Vulkan verification, media/workload benchmarks, dependency selection, Phase 01, and all product implementation remain closed.

## Next Architect action

Publish the final habitat ruling, then issue a bounded architecture-options directive to Codex. The next directive must produce decision artifacts and evidence only; it does not open product implementation.
