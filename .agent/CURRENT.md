# Current Project State

## Black motion targeted retry — 2026-09-12

Seven new imagegen trials do not complete the12 required action tracks. A late
gait edit swaps the support leg; a localized repair improves one overlap only.
Four inhale intermediates fail gradual contour progression (268,276,277,277,
273,277px through endpoints). NEEDS_ARCHITECT_DECISION on a controllable temporal
authoring route; no further defective bulk generation or visual approval request.
See active R05_BLACK_MOTION_RETRY_RESULT.md and black-motion-retry review evidence.
Black-background and original approval boundaries remain unchanged.

## Black motion continuation — 2026-09-12

51 new imagegen outputs plus the prior black front image are preserved as 52
black-backed drawings. Key studies cover all eight facings, front presence and
both lateral actions. **Complete animation remains INCOMPLETE / visual gate
FAILED:** several in-betweens do not progress toward the next passing key, and
turn angles jump. No automatic approval transfer from the unchanged original
operator selection. Further bulk interpolation stopped; no finished pack claim.

Review export and Godot playback of 23 diagnostic sequences pass bounded checks,
not motion-quality or contacts. See active `R05_BLACK_MOTION_RESULT.md` and
`assets/review/p02/author002/black-motion-studies/README.md`. Opaque review mode
does not weaken MON_FRAME_V1 or the historical transparent intake contracts.

## Operator black-background request — 2026-09-12

Godot clear color and foundation backdrop now black. One separately generated
black-backed front candidate passes an actual Xvfb still-render check. Original
approved images unchanged. This removes cutout dependency for the still preview,
not transparent-pack intake. See `R05_BLACK_BACKDROP_RESULT.md` in the active
packet. Full gait conversion/actions remain unfinished; no Phase02 acceptance.

## Latest continuation — clean-source preparation blocked, 2026-09-12

After operator `proceed`, generated five missing right gait roles, one targeted
passing-foot repair and one failed alpha extraction. Prior approved selection
is unchanged. Six Photoroom calls returned HTTP402 without output; built-in
fallback returned RGB/no alpha. No new frames promoted. See active packet
`R05_AUTHOR_002_CONTINUATION_RESULT.md` and `R05_AUTHOR_002_CONTINUATION_RESULTS.json`.
Raw key-study strips/GIFs are diagnostics only. Restore authorized cutout access
before source preparation; do not weaken alpha/intake gates or change billing.

## Latest operator visual approval — 2026-09-12

The operator expressly approved **the construction sheet and the latest corrected
gait poses**. Exact selection: eight construction facings and eleven latest gait
keys in `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_AUTHOR_002_OPERATOR_SELECTION.json`.
See `R05_AUTHOR_002_OPERATOR_APPROVAL.md` for the quoted clarification and scope.
This supersedes the coder's visual non-acceptance for those selected images.
Superseded repairs remain excluded. Complete actions, edge cleanup, normalization,
source/world contacts and v2 intake/runtime remain unfinished, not passed.
No source pack, full motion library or Phase02 acceptance is implied.

## Historical execution before operator approval — 2026-09-12

Review11 was merged normally. 25 reference-based outputs (10 construction,
15 gait/repair attempts) were generated and self-reviewed. The key set still
fails stable limb/hand/foot correspondence, including independently repeated
left/right passing-foot defects. Review11's anatomical key-pose stop condition
is reached. **BLOCKED; zero promoted frames; no visual approval request.**
See `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_AUTHOR_002_KEY_GATE_RESULT.md`
and `R05_AUTHOR_002_STUDY_RESULTS.json`. Eight-facing studies are provisional,
not locked. Full actions, v2 intake/runtime and world-contact QA are NOT RUN.
Previous planning-only and rejected-art records below remain historical.

## Latest operator disposition — 2026-09-12

The operator additionally rejects universal front-left facing. Current visual
planning is front-facing rest/interaction, full-profile left/right travel, and
deliberate whole-body turns with quarter/back correspondence. See
`tasks/active/COMPANION-P02-EMBODIMENT-001/R05_FACING_AND_MOTION_CORRECTION.md`.
This correction is recorded, not implemented: old front-left request fixtures
remain historical engineering coverage, not the replacement art specification.

All R05-v1 previews are **REJECTED**, not awaiting approval. Cutout contamination,
motion/hand defects and overly fast looping were reported by the operator.
The current correction is recorded in
`tasks/active/COMPANION-P02-EMBODIMENT-001/R05_OPERATOR_REJECTION_01.md`.
Codex candidate authorship remains authorized. Replacement motion is **NOT READY**;
new generated studies are not counted as a completed pack. Prior technical passes
below are historical and do not override the operator's rejection.

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

R05-v1 and superseded repair attempts remain rejected. The selected AUTHOR-002
construction/key artwork now has operator visual approval, not complete animation
or source-pack qualification. Review11 still governs the motion model.

## Current authority

- Architect Review 11:
  `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_11.md`
- Notion Review 11:
  https://app.notion.com/p/3d9833cb27ff818c89ebe1aca70cf28b
- Current bounded Codex directive:
  `COMPANION-P02-EMBODIMENT-001-R05-AUTHOR-002`
- PR #9: `DRAFT / OPEN / UNMERGED`
- Issue #8: `OPEN`
- Branch: `codex/p02-embodiment-001`

## Operator-facing policy

Ordinary rest, breathing, listening, acknowledgement and social presence default to `front`.

Screen-left locomotion uses true `left` profile. Screen-right locomotion uses true `right` profile. Quarter and back facings exist for deliberate whole-body turns/orientation and may not substitute for every action.

All eight neutral construction facings are required: `front`, `front_right`, `right`, `back_right`, `back`, `back_left`, `left`, `front_left`.

Left/right production art must be independently reviewed. Blind horizontal mirroring is not accepted.

## Contact-coordinate policy

`MON_FRAME_V1` source root remains fixed at `(512,896)` and source PNGs encode no world translation.

For stationary clips, planted-contact drift is evaluated in source space. For translating locomotion, world grounding is evaluated after combining source landmarks with the 24 Hz actor/MonRoot translation plan:

```text
world_contact(t) = actor_root_world(t)
                 + uniform_scale * (source_contact(t) - source_root)
```

During a declared planted span, composed world-contact drift must remain within 2 px. A support foot is not required to remain fixed relative to both source root and world. Contact spans may not be shortened to a single frame to make QA vacuous.

## Active objective

Codex executes `COMPANION-P02-EMBODIMENT-001-R05-AUTHOR-002` only:

1. merge current `origin/main` normally;
2. preserve R05-v1 and rejected-study evidence;
3. create versioned request profile `phase02_presence_lateral_motion_proof_v2` without weakening v1;
4. implement source-vs-world contact QA;
5. produce eight-facing neutral construction candidates;
6. gate generation on correct left/right gait key poses before in-betweens;
7. produce front-facing breathe and listen/acknowledge;
8. produce complete left and right front→quarter→profile turn/start/walk/stop→quarter→front actions;
9. use transparent generation or approved Photoroom RGBA cutout tooling without green chroma production backgrounds;
10. normalize promoted frames to `MON_FRAME_V1`;
11. pass actual v2 source/ingested/receipt, Rust and Godot validation;
12. publish complete-action normal/quarter-speed, strip, silhouette, edge, and contact review media;
13. return for operator/Architect review before library scale.

## Motion requirements

Profile walk keys must visibly include anatomical-left contact/down/passing/up and anatomical-right contact/down/passing/up before in-betweens. Swing feet clear the floor; support legs alternate; arms counter-swing; torso/head response stays bounded; hands keep exactly two fingers plus thumb; feet keep exactly three toes.

Front breathing must show a complete inhale and exhale. Listen/acknowledge must show attention lead, a readable listening hold, acknowledgement and settle rather than a rapid repeated nod.

## Retained engineering evidence

Retain:

- accepted Phase 01 foundation;
- C02/C03/C04 authored-frame intake/runtime/readiness engineering;
- Review 10 Codex candidate-art authorization;
- R05 review-timing correction;
- completion-aware preview playback;
- operator-authorized Photoroom cutout adapter and negative cutout evidence;
- exact approved references and hashes;
- all R05-v1/replacement negative results.

No previous green CI result overrides the operator's visual rejection.

## Not accepted

- normalized/operator-approved production source pack;
- accepted complete motion language (selected construction/static keys are approved);
- visual aliveness;
- complete 32-family/eight-direction library;
- 10,000 live transition qualification;
- Openbox endurance;
- Phase 02 completion;
- organism, autobiographical memory, perception, speech, learning, dreaming, care efficacy, production reliability or Phase 03+ capability.

## Protected work

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` modifications remain protected. Do not inspect them for evidence, commit, reset, stash, overwrite, copy, or reformat them.
