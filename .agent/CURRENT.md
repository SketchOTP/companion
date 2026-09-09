# Current Project State

## Current stage

Planning Phase 02 — Master Delivery Roadmap remains active.

Roadmap Phase 00 — Planning and Product Contract remains active. `COMPANION-P00-ENV-001` has completed independent Architect review and is accepted. The environment-evidence packet is archived. Product implementation remains closed.

## Current objective

Resolve the operator-dependent product-contract decisions that materially determine safety, privacy, evaluation, embodiment, and architecture v1.0. No Codex directive is currently active. Do not install or run Godot 4.7.2, select dependencies, run media/workload benchmarks, draft architecture v1.0 as approved, create application or asset work, or begin Phase 01 without a new bounded Architect directive.

## Directive state

- Active directive: `NONE`
- Last completed directive: `COMPANION-P00-ENV-001`
- Last directive verdict: `ACCEPTED — ENVIRONMENT EVIDENCE QUALIFIED`
- Completed task packet: `.agent/tasks/completed/COMPANION-P00-ENV-001/`
- Architect review: `.agent/tasks/completed/COMPANION-P00-ENV-001/ARCHITECT_REVIEW.md`
- Notion directive: https://app.notion.com/p/3d6833cb27ff81e6ab93e37fc851b49d
- Notion coder report: https://app.notion.com/p/3d6833cb27ff8159b66fdebeb690be90
- Notion Architect review: https://app.notion.com/p/3d6833cb27ff81c596a4dbe116099a75
- Codex result commit: `ef5b011bfd6e3f747e8bf8e8f06faebb21901d50`
- Codex publication head reviewed: `c41176bf0b682ca55871e3636d143cf98c150747`
- Product implementation authorization: `CLOSED`

## Accepted environment evidence

- Host: Ubuntu 24.04.5 LTS, x86_64, X11; Ryzen 7 5800XT with 8 physical cores/16 threads; approximately 67.3 GB RAM.
- Graphics: GTX 1660 SUPER and RTX 3050 6GB on NVIDIA 595.84; direct OpenGL 4.6 observed. Exact Vulkan device/presentation capability remains unknown.
- Display: three outputs across two logical X screens—two 3840×2160/60 Hz GNOME-managed outputs and one 1366×768/59.96 Hz Openbox-managed output. The target habitat remains an operator decision.
- Camera: one readable UVC webcam with enumerated MJPEG through 1080p30 and YUYV through 720p10. No frame was captured; quality, latency, field of view, sharing, and integrated behavior remain unknown.
- Audio: PipeWire/WirePlumber active; default USB mono microphone at 48 kHz and default HDMI stereo output at 48 kHz. No audio was recorded or played; acoustics, latency, echo cancellation, wake behavior, and barge-in remain unknown.
- Storage: repository on network-backed SSHFS; local system storage on ext4/NVMe with substantial free space. Canonical runtime state must not use the repository volume by assumption.
- Godot: selected 4.7.2 build was not found. A pre-existing Godot 4.6 stable binary was observed but is not an approved substitute.
- Operations: time synchronization is active and automatic AC suspend is disabled; system and user systemd managers reported degraded. Adopted service topology, failure causes, recovery, power, thermal behavior, and endurance remain unqualified.

## Evidence disposition

- Host/peripheral metadata: `ACCEPTED — E1_OBSERVED`.
- Sanitized artifact structure, privacy validation, and eleven-RQ crosswalk: `ACCEPTED — E3_TARGET_TESTED` for those evidence artifacts only.
- Product/runtime capability: `NOT IMPLEMENTED / NOT ACCEPTED`.
- Generic Godot Compatibility-renderer prerequisite: `SUPPORTED` only at the official simple-project specification level.
- Companion workload, exact Godot 4.7.2 runtime, Vulkan, media quality/latency, local inference, always-on recovery, and safety behavior: `NOT ESTABLISHED`.

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

## Accepted privacy deviation and control improvement

One transient diagnostic response exposed a hardware-serial field before filtering. The value was immediately discarded and is absent from durable GitHub and Notion records. The deviation is accepted as contained. Future machine probes must use source-level field allowlists and pre-reviewed bounded commands wherever practical; post-processing redaction is only a secondary control.

## Current blockers

- Roadmap Phase 00 and its implementation-opening package are incomplete.
- Operator decisions affecting target users, claims, caregiving scenario/jurisdiction, ownership/consent, cloud/offline boundary, voice, retention, notifications, support, and screen habitat remain unresolved.
- Godot 4.7.2 supply and exact runtime verification remain unauthorized and incomplete.
- No production dependency beyond the existing Godot/Godot-version rulings is approved.
- Architecture v1.0, Phase 01, and product implementation remain closed.

## Next Architect decision point

Obtain a focused operator ruling on the first high-coupling product decisions: primary user/household, intended use and claims, first caregiving scenario and jurisdiction, and the default screen habitat. Then resolve or deliberately defer the remaining contract decisions in dependency order before issuing architecture v1.0 work.
