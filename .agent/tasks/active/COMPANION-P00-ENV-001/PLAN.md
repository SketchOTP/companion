# COMPANION-P00-ENV-001 — Execution Plan

## Checkpoint 1 — Reconstruct authority and repository state

- Read `AGENTS.md`, Authority skill, mandatory kernel, active directive, and this packet.
- Re-fetch the canonical project, roadmap, open-decision queue, R09, R10, and the live Notion directive/report.
- Fetch `origin/main`, verify the expected baseline or explain a later governance-only fast-forward, and confirm the working tree is clean.
- Stop on unexplained product work, divergence, or changed authority that alters scope.

## Checkpoint 2 — Define privacy-safe evidence handling

- Establish a temporary private workspace outside the repository for command output.
- Define redaction and normalization before collecting evidence.
- Record commands and versions separately from sanitized results.
- Never retain media content; use metadata and capability enumeration only.

## Checkpoint 3 — Inspect host and session

- Observe distribution, kernel, architecture, session/display server, desktop/compositor, CPU topology/features, memory/swap, and safely available system limits.
- Classify missing tools separately from missing capabilities.

## Checkpoint 4 — Inspect graphics, display, and storage

- Observe GPU model/driver, active rendering path, OpenGL/Vulkan availability, software-rendering conditions, display outputs/modes/scaling, and repository-volume storage facts.
- Do not run sustained benchmarks or change display configuration.

## Checkpoint 5 — Inspect camera and audio metadata

- Enumerate webcam device metadata, driver, formats, resolutions, frame intervals, controls, and access state without capturing a frame.
- Enumerate the active audio stack, input/output devices, defaults, routing, and available metadata without recording or playing audio.
- Record contention, permission, and observability limits explicitly.

## Checkpoint 6 — Inspect Godot and existing development tools

- Locate existing Godot executables and report exact version/build and non-invasive launch/version behavior.
- Record relevant installed tool versions without treating presence as approval.
- Do not install, update, create a Godot project, or choose dependencies.

## Checkpoint 7 — Build the evidence products

- Populate `ENVIRONMENT_RAW.json` from sanitized observations.
- Produce the report and capability matrix with fact/inference/unknown/operator-choice labels.
- Build the eleven-RQ product-contract crosswalk.
- State architecture implications as constraints/options only.

## Checkpoint 8 — Validate

- Parse and validate JSON.
- Check source/timestamp/status/confidence coverage.
- Cross-check summaries against raw observations.
- Run privacy, secret, path, media-file, and changed-scope scans.
- Confirm all eleven RQs and all required inventory categories appear exactly once in their intended records.
- Run `git diff --check` and inspect the complete diff.

## Checkpoint 9 — Publish

- Update `.agent` current/directive/outcome records and the Notion coder report.
- Commit and normally push the focused result.
- Re-fetch Notion and GitHub Issue #2, verify final SHA agreement, leave the issue open, and return the canonical result for Architect review.

## Stop conditions

Stop rather than improvise when a useful probe requires elevated access, installation, configuration change, private-media capture, disruptive output, external upload, exposure of private identifiers, or resolution of an operator choice.
