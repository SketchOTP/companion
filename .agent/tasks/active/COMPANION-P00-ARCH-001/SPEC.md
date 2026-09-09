# COMPANION-P00-ARCH-001 — Operative Specification

Status: `ISSUED — ACTIVE; CONTEXT-BRIDGE ACKNOWLEDGMENT REQUIRED`

## Authority

- Notion directive: https://app.notion.com/p/3d6833cb27ff8183a210e560883d96ab
- Required Notion report: https://app.notion.com/p/3d6833cb27ff8141837fdaa087841324
- GitHub Issue #3: https://github.com/SketchOTP/companion/issues/3
- Verified baseline: `db33d8a597f79a01e569482dc00583dcf50249f9`
- Directive publication commit: `704325baa95e490710441a468625d2e74f9a343c`
- Acceptance authority: Architect

## Conversation-isolation rule

Codex cannot see the operator–Architect ChatGPT conversation. The live Notion hierarchy, this repository, and GitHub Issue #3 are the complete execution bridge. No unpublished chat statement may be assumed.

Before substantive architecture work, Codex must:

1. Read `AUTHORITY_CONTEXT_BRIDGE.md`.
2. Re-fetch every mandatory live source named in that file.
3. Complete `AUTHORITY_CONTEXT_ACKNOWLEDGMENT.md` with exact source-backed decisions, open questions, environment limits, hard prohibitions, and current objective.
4. Record retrieval confidence as `ADEQUATE`, `UNCERTAIN`, or `INSUFFICIENT`.
5. Stop and report if confidence is not `ADEQUATE` or if any material source conflict remains unresolved.

This preflight is part of the directive acceptance criteria. A complete architecture packet with a faulty or missing acknowledgment cannot pass.

## Objective

Produce a decision-ready Architecture v1.0 package and measurable first vertical-slice contract. Compare credible alternatives, recommend one architecture, define authority/process/data boundaries, dispose remaining RQs without unauthorized resolution, evaluate only necessary dependencies and rights, define threat/privacy/claims controls, and establish repository/CI/test/release and experiment plans.

## Adopted operator decisions that must govern the work

- One adult primary user aged 18 or older who may have support needs; single-primary-user authority model; explicitly configured trusted caregivers/contacts; no minors in iteration one.
- Consumer-product development from the start under a narrow non-medical claim: a persistent digital companion with configurable check-in and trusted-contact assistance.
- Explicit spoken help request is the first caregiving scenario; first jurisdiction is Kentucky, United States; qualification begins in simulation, recorded replay, and shadow mode before live delivery.
- Iteration one runs on the accepted Linux PC and existing webcam, microphone, connected speakers, and dedicated 1366×768 Openbox-managed output.
- The default presentation is a bounded resizable Godot application window on that Openbox output.
- Godot 4.7.2 is the selected baseline but was not found on the host; Godot 4.6 is not an approved substitute.
- The mon is the operator-approved original flat cel-shaded purple 2D sprite character governed by the visual bible and `MON_FRAME_V1` contract.
- Godot is the body/presentation adapter, not the owner of organism truth, memory, biometrics, credentials, consent, contacts, or safety policy.
- The caregiving core remains separately governed, deterministic at the policy boundary, auditable, and immune to companion mood or improvisation.
- Core identity, organism state, memory, consent, essential interaction, safety policy, backup, export, and restore require a local survival path.

These summaries do not replace the live decision records. Codex must verify ADR-33 through ADR-37 and the underlying canonical pages.

## Required outputs

Complete every file in this packet and the dedicated Notion report. Use the live Notion directive as the full contract.

Additional mandatory context artifacts:

- `AUTHORITY_CONTEXT_BRIDGE.md` — Architect-issued source and decision bridge; preserve as issued and note any live-source changes in the acknowledgment.
- `AUTHORITY_CONTEXT_ACKNOWLEDGMENT.md` — Codex-completed preflight proof before architecture synthesis.

## Hard boundary

Planning/evidence only. No product source, Godot project, sprites, dependency or package installation, manifest, CI workflow, deployment, database implementation, models/data/voices, media capture/playback, benchmark, biometric enrollment, notification integration, safety runtime, architecture self-approval, Phase 01, or product capability.

## Completion

Commit and normally push only `.agent/` planning/evidence changes, update Issue #3 without closing it, and return the canonical `CODEX RESULT`. Completion remains provisional until independent Architect review.

The final handoff must explicitly state that Codex cannot see the chat, identify the canonical sources it actually re-fetched, and report whether every context-acknowledgment item passed.
