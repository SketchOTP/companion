# Architect Review 10 — Operator Override Authorizes Codex Candidate Sprite Authorship

## Verdict

`OPERATOR OVERRIDE ACCEPTED — CODEX CANDIDATE ART AUTHORSHIP AUTHORIZED`

- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACCEPTED`
- Roadmap Phase 02: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 03 and later: `CLOSED`
- Branch: `codex/p02-embodiment-001`
- PR: `#9 — DRAFT / OPEN / UNMERGED`
- Issue: `#8 — OPEN`
- Notion review: https://app.notion.com/p/3d9833cb27ff8179a60dc64d5ab6b5ac

## Operator ruling

The operator expressly authorizes the AI coder and approved image-generation
tooling to design and create the sprite sheets, poses, positions, frames and
animations required for Phase 02.

This ruling supersedes Review 04/09 only where those reviews prohibited Codex
from creating production character pixels or held Codex until Architect-authored
art existed.

The override does not transfer architectural acceptance, roadmap-transition
authority, product capability authority, organism state, memory, consent,
secrets, tools or safety decisions to Codex.

## Updated visual-authorship boundary

- **Operator** — final visual authority. Approves or rejects identity,
  construction, pose language, animation quality and motion language.
- **AI Architect** — strategic and acceptance authority. Defines evidence,
  reviews candidate output, detects drift and accepts/rejects the Phase 02 gate.
- **Codex / approved image-generation tooling** — may create candidate
  identity-critical sprite pixels, source poses, in-betweens, overlays and
  animation frames from the exact approved references.
- **Godot** — nonauthoritative presentation/runtime adapter.

All generated art remains `candidate` until explicit operator approval.

## Source authority

Codex must ground candidate generation in the exact approved reference assets:

```text
confident_purple_ghost_mascot.png
SHA-256 86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56

purple_monster_turnaround_sheet.png
SHA-256 3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4
```

Unrelated character art and previously rejected procedural placeholder geometry
must not be substituted as identity evidence.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R05-AUTHOR-001

## Objective

Create the first operator-reviewable, reference-grounded candidate sprite pack
using approved image-generation tooling, then pass that exact pack through the
accepted authored-frame intake/runtime boundary.

## Why this is next

The pre-art engineering gate is accepted and the operator has now explicitly
authorized Codex to own candidate sprite-sheet creation. The smallest decisive
next action is therefore a bounded candidate-art pack, not more infrastructure
work and not full-library scale.

## Authoritative basis

Read and reconcile:

1. canonical project and end goal;
2. Architecture v1.0;
3. R04 embodiment research;
4. R10 sprite-production contract;
5. approved visual bible;
6. exact approved references;
7. Architect Reviews 04–10;
8. adopted authored-frame contracts from R04-C01/C02;
9. current `.agent/` authority;
10. PR #9 and Issue #8.

## Scope

Generate candidate source art for the bounded review pack:

- neutral front construction;
- neutral profile construction;
- neutral front-left construction;
- front-left idle/breathe: 6–8 frames;
- front-left walk: 8 frames;
- front → front-left orientation: at least 4 frames;
- front-left → front orientation: at least 4 frames;
- listen → acknowledge: 6 frames.

Codex may use image generation, reference-based image editing and iterative
regeneration to achieve identity consistency and real temporal pose changes.

Do not scale to the complete 32-family/eight-direction library in this directive.

## Candidate art requirements

Every accepted-for-review source frame must be brought into conformance with:

```text
MON_FRAME_V1
1024 x 1024
8-bit RGBA PNG
sRGB
transparent background
root = (512, 896)
baseline = 896
safety x=64..960, y=32..960
24 Hz timing grid
approval_state = candidate
```

The art must preserve the approved creature's:

- purple palette family;
- flame/edge-spiked head silhouette;
- black eye fields with white inner eye shapes;
- simple mouth language;
- exactly two fingers plus one thumb per hand;
- exactly three toes per foot;
- simple integrated body proportions;
- flat/cel-shaded rendering language.

## Motion requirements

### Idle/breathe

Use real temporal pose variation: visible torso expansion/contraction, bounded
head/spike follow-through and arm response. Root and planted feet remain stable.

### Walk

Use real gait phases, including contact/down/passing/up. Legs and feet must
articulate, arms counter-swing, the swing foot must move, and planted-contact
drift must remain within the accepted tolerance after normalization.

### Orientation

The start and end images must visibly correspond to front and front-left facing.
Do not satisfy this with scale-only deformation.

### Listen → acknowledge

Attention should lead through the face/head, followed by posture response,
settling and acknowledgment. Decorative marks may supplement the action but may
not constitute it.

## Generation discipline

- Reference-driven generation/editing is authorized.
- Text-only unrelated character generation is prohibited as final candidate
  evidence.
- Codex may reject and regenerate frames freely before publication.
- Do not silently repair anatomy after intake; rejected art is regenerated at
  the source-generation stage.
- Preserve negative and rejected generations as bounded review evidence where
  useful, but do not flood ordinary Git with bulk binary candidates.

## Intake and validation

For the selected candidate pack:

1. build the immutable Architect/Codex source-pack manifest and sidecars;
2. mark every asset `candidate`;
3. run the accepted source-pack validator;
4. run atomic intake to the ingested pack and receipt;
5. run actual Rust round-trip against the ingested pack;
6. load and play the exact requested tracks in Godot 4.7.2;
7. publish deterministic normal-speed and quarter-speed motion review media;
8. publish ordered strips, silhouette views and root/contact overlays;
9. retain exact source and artifact hashes.

## Visual QA

Do not rely only on automated counts. Review and publish evidence for:

- silhouette consistency;
- head-spike topology;
- face/eye consistency;
- hand and foot anatomy;
- proportion drift;
- palette/shading drift;
- root/contact stability;
- walk mechanics;
- orientation endpoint fidelity;
- loop seams;
- listen/acknowledge readability.

## Acceptance criteria

This directive passes only when:

- the bounded candidate pack exists;
- all required frame counts and tracks are present;
- the source art is recognizably grounded in the approved mon references;
- anatomy invariants are preserved;
- the tracks contain real temporal pose changes;
- the exact candidate pack passes source/ingested/receipt validation;
- Rust and Godot consume the actual candidate pack;
- review artifacts are directly accessible;
- Phase 01 and focused Phase 02 CI remain green;
- no art is labeled approved before operator review.

Passing this directive does **not** accept Phase 02. It produces the candidate
visual package for Architect and operator review.

## Prohibited claims

Do not claim:

- operator-approved visual identity;
- approved motion language;
- complete Phase 02;
- complete eight-direction/full-library coverage;
- visual aliveness;
- Openbox endurance;
- organism behavior;
- memory, speech, vision, learning, dreaming or care capability;
- Phase 03 progress.

## Stop and return to Architect if

- the approved references cannot be accessed or verified;
- image generation cannot maintain identity/anatomy after bounded iteration;
- the existing intake contract cannot represent the generated frames truthfully;
- a new dependency or 3D production pipeline appears necessary;
- protected operator work cannot be preserved;
- current `origin/main` cannot be merged normally.

## Required project updates

Continue only on `codex/p02-embodiment-001`, PR #9 and Issue #8. Merge
`origin/main` normally first. Update the active task packet, `.agent/CURRENT.md`,
`.agent/INDEX.md`, append-only ledgers, Notion directive/report, PR #9 and Issue
#8. Leave PR #9 draft/open/unmerged and Issue #8 open.

## Required handoff

Return:

```text
# CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R05-AUTHOR-001
```

with the generated candidate asset inventory, source hashes, rejected-candidate
summary, visual QA findings, motion review media, intake/Rust/Godot evidence,
CI runs, artifact hashes and the explicit operator decisions required.

## Capability boundary

This ruling changes who may author candidate art. It does not change the accepted
product capability boundary. Roadmap Phase 02 remains active and unaccepted.