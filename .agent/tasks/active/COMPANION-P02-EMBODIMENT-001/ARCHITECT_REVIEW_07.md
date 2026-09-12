# Architect Review 07 — C02 Local Pass; Hosted Godot Diagnostic Parity Investigation

## Verdict

`INVESTIGATE — C02 SEMANTICS RETAINED; READY_FOR_ARCHITECT_FRAME_PACK BLOCKED BY HOSTED GODOT EVIDENCE DISCREPANCY`

- Reviewed branch: `codex/p02-embodiment-001`
- Reviewed head: `1d7ea24295b505c6beb0f612a6b248a6f8d5edfb`
- PR: `#9 — DRAFT / OPEN / UNMERGED`
- Issue: `#8 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACCEPTED`
- Roadmap Phase 02: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 03 and later: `CLOSED`
- Canonical Notion review:
  https://app.notion.com/p/3d9833cb27ff81109a7add09837f7b2b

C02 materially completed the requested contract, intake, and bounded synthetic-pack work locally and through the direct hosted Godot gate. The remaining blocker is narrower: the direct hosted Godot gate and the sanitized evidence runner are separate executions with different diagnostic-capture semantics. The second path reports an `ERROR:` but does not preserve the exact line, while the first path passes.

## Retained C02 evidence

Do not repeat unless inputs change:

- exact approved visual references and hashes;
- source/ingested/receipt contract split;
- complete positive `phase02_bounded_motion_proof_v1` pack with 8 tracks / 31 frames;
- exact request-profile semantics and endpoint/event validation;
- exact PNG/sRGB structural validation;
- same-track reuse semantics;
- fsync-backed staged publication and atomic rename;
- actual generated-pack Rust validation and missing-path rejection;
- local Godot 4.7.2 playback with `RenderingServer.frame_post_draw` observation;
- local semantic validator and tamper negatives;
- Phase 01 hosted run `34667692938` success;
- Phase 02 direct Godot step success in run `34667692926`.

These remain bounded synthetic engineering evidence. `READY_FOR_ARCHITECT_FRAME_PACK` is not accepted until the hosted discrepancy is resolved.

## Independent diagnosis

### 1. The failure is isolated to the hosted evidence path

Phase 02 run `34667692926` passed the direct Godot exact-track/degradation/recovery gate and failed only in `Generate and validate sanitized evidence` with `unexpected Godot ERROR output`. No artifact was uploaded because artifact publication is downstream of the failing validator.

### 2. The two gates are not evidence-equivalent

The direct workflow invokes Godot and redirects only application stdout into files before grepping those files for `ERROR:`. Application stderr is not part of that grep.

`run_r04_evidence.py` launches a second Godot process, captures both stdout and stderr, separates Xvfb/xauth output with `xvfb-run -e`, and marks any `ERROR:` in Godot stdout/stderr as unexpected.

Therefore a direct pass and evidence-run failure are possible even when the underlying code is unchanged.

### 3. The exact diagnostic was lost

The evidence runner stores a count and boolean but not the exact captured `ERROR:` lines. It stores truncated stdout but not complete stderr. The failing workflow also skips artifact publication.

The current evidence does not justify classifying the line as harmless wrapper noise or as a product defect. The exact error must be retained before changing runtime behavior.

### 4. Fail-closed policy is correct

Do not weaken or remove `unexpected Godot ERROR output`. Unknown Godot errors remain failures until captured and classified.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R04-C03

## Objective

Identify and resolve the hosted-only Godot diagnostic discrepancy through one canonical Godot evidence runner. Return `READY_FOR_ARCHITECT_FRAME_PACK` only when the exact hosted path passes twice with no unknown Godot error hidden or ignored.

## Scope

### A. Preserve C02 semantics

Do not reopen authored-pack schema, request-profile, PNG, fsync/atomic-intake, or visual-authorship design unless the captured Godot diagnostic directly proves a defect there.

### B. Create one canonical Godot evidence runner

Both the direct workflow gate and `run_r04_evidence.py` must use the same runner and classification policy. Capture separately Godot stdout, Godot stderr, Godot `--log-file`, Xvfb/xauth diagnostics from `xvfb-run -e`, exit code, exact Godot version, display/rendering summary, sanitized command/arguments, and SHA-256 of retained logs. Retain exact Godot `ERROR:` lines, not only a count.

### C. Eliminate duplicate pass definitions

Remove the current stdout-only direct gate versus stdout+stderr evidence gate mismatch. Prefer one authoritative Godot execution per evidence set. If more than one invocation is retained for stability, each invocation must use the same runner, capture policy, inputs, and assertions.

### D. Cold/warm reproduction

After one explicit controlled Godot import step, run the canonical qualification twice consecutively in the same hosted workspace: cold then warm. Record `.godot` cache existence and sanitized tree digest before/after each run.

### E. Diagnose before modifying runtime

If an actual Godot `ERROR:` is captured, preserve the exact line/context, classify its origin, fix it only when evidence identifies a project-controlled cause, then rerun cold/warm. Do not whitelist or regex-ignore an unknown error. Wrapper-only diagnostics must remain in the wrapper channel.

### F. Fixture lifecycle investigation

Inspect SubViewportContainer/SubViewport/avatar/director/texture cleanup only if the exact diagnostic implicates lifecycle/resource cleanup. Do not change cleanup speculatively first.

### G. Always publish diagnostics

Add a sanitized diagnostic artifact step with `if: always()` or equivalent so stdout, stderr, engine log, Xvfb diagnostics, structured classification, and hashes survive validator failure.

### H. Classifier tests

Test synthetic channels proving Godot stderr `ERROR:` fails, Godot stdout `ERROR:` fails, Xvfb-only diagnostics remain separate, and no unknown Godot error can be suppressed by the direct gate.

## Required validation

- canonical runner classifier tests;
- cold hosted Godot qualification pass;
- warm hosted Godot qualification pass;
- empty actual-Godot `ERROR:` list in both accepted runs;
- complete existing event/timing assertions retained;
- diagnostic artifact published even for an intentionally failing classifier fixture;
- Phase 01 hosted CI green;
- Phase 02 semantic validator green;
- one additional hosted rerun after the first green result;
- `git diff --check` and private-data scan.

## Stop and return to Architect if

The exact diagnostic is a reproducible Godot/X11/renderer error that cannot be removed without weakening render observation, changing an approved dependency, or altering host configuration. Return the exact line, context, reproduction, official upstream evidence, and minimum Architect decision required. Do not whitelist it.

## Prohibited work

No production character pixels, operator visual review, art/3D dependency, sprite-library expansion, final atlas work, Openbox endurance, Phase 03 work, PR merge, or Issue closure.

## Acceptance criteria

C03 passes only when one canonical runner defines Godot diagnostics for direct CI and evidence generation; exact Godot error lines are retained; diagnostics survive failures; cold and warm hosted qualifications pass with no actual Godot `ERROR:` lines; Phase 01 and Phase 02 workflows are green; a second hosted rerun reproduces green; and no unknown diagnostic is ignored or whitelisted. Final status may then be `READY_FOR_ARCHITECT_FRAME_PACK`.

## Required handoff

Return `CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R04-C03` with the exact hosted diagnostic if reproducible, root-cause classification, canonical runner description, cold/warm structured results, stdout/stderr/Godot-log/Xvfb hashes, classifier negative matrix, event/timing result, CI and rerun IDs, diagnostic artifact IDs/digests, publication reconciliation, and final readiness status.

## Capability boundary

A passing C03 proves only that the bounded synthetic authored-frame intake/runtime gate is regression-protected and diagnostically trustworthy. It does not accept production art, Phase 02, visual aliveness, or product capability.
