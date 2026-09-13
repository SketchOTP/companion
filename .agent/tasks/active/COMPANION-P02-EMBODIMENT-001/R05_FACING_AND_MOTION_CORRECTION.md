# Operator correction: front-facing presence and profile locomotion

## Status and authority

2026-09-12. Operator visual requirement recorded; motion planning only, not a
new accepted pack. Retrieval confidence ADEQUATE for this correction. No new
pixels, runtime changes, or visual approval are claimed in this record.

The operator rejects front-left as the universal presentation. For this flat
screen habitat, ordinary rest and interaction should face the viewer. Leftward
and rightward travel should face the corresponding full profile, with deliberate
turns into travel and back toward the viewer. Quarter and back views must exist
for meaningful orientation rather than substituting for every action.

This supersedes the front-left-heavy artistic target, not historical test
results. Review 10 candidate-authorship permission remains effective. Phase 02
is unaccepted; Phase 03+ stays closed. Existing R05-v1 art remains rejected.

## Actual defect found

At c64b9743a34cf31b73e8e8e5f508821c90730f40,
`intake_authored_frame_pack.py:191-229` requires front-left idle, walk and
listen/acknowledge and only front/front-left orientation. Its request profile
is `phase02_bounded_motion_proof_v1`. The R05 builder also constructs those
tracks. This is a written/executable coverage defect, not only prompt quality.

Keep that accepted synthetic fixture as a historical engineering regression.
Do not relabel old images, weaken its validator, or pretend a new side-on pack
passes its old eight-track requirement. A separately versioned request table,
matching written request, fixture and tests is necessary for the corrected
pack. This record specifies the visual intent; it does not assert that the
new executable request profile already exists.

## Coordinate and action vocabulary

- Facing is the body silhouette relative to the viewer. `left` means the nose
  direction points screen-left; `right` points screen-right. It is not the
  creature's anatomical left/right.
- Gaze is eye/head attention and may change without turning the torso.
- Travel is screen displacement: none, left, right. No default diagonal-depth
  walk is implied by a flat habitat. Any future depth travel needs an explicit
  habitat/scale model.
- Posture is standing, sitting, lying, etc.; facing does not replace posture.
- Gait phase identifies the anatomical support/swing leg, not whichever foot
  happens to appear on the left of the image. Track it through occlusion.
- Transition intent states why a facing/posture changes. A clip name cannot
  serve as evidence that the rendered body actually changes facing.

## Complete coverage map for planning, not a generation order

| Area | Necessary drawings and connections | Facing policy |
| --- | --- | --- |
| Construction | Neutral silhouette/face/limb correspondence in all eight facings | front, front-right, right, back-right, back, back-left, left, front-left |
| Rest/presence | Complete inhale/exhale, settle, weight shifts, blink, gaze, small head turns and return | Front by default; other facings only for deliberate orientation |
| Attention/response | Look, attention lead, listen hold, acknowledge, settle; greeting/refusal/surprise as later presentations | Front; targeted look may lead into a justified turn |
| Lateral locomotion | Anticipation, first step, alternating stride loop, last step/deceleration, profile stand | Independently checked left and right profile |
| Turns | Front to each profile and return through its quarter view; profile to back and return through back-quarter; deliberate 180-degree reversal | Whole-body ordered facing progression; no one-frame flip |
| Posture connectors | Stand/sit, sit/stand, sit/lie, lie/sleep, wake/rise, stretch/settle | Declared source/end facing and compatible posture |
| Other movement | Run start/loop/stop, walk/run change, hop anticipation/takeoff/flight/landing/recovery | Travel-matched facing; landing and support phase explicit |
| Action connectors | Inspect/reach/retract, gesture/recover, self-play/practice response and return | No assumed teleport to a standard pose |
| Interruptions | Mid-step stop, interrupted turn, interrupted gesture, resume or finish-to-rest | Preserve current support leg and visible facing |
| Degradation | Missing-pack safe hold, interrupted presentation and recovery | Last valid compatible pose, not random front-left fallback |

Back views support a turn-away, not permanent avoidance of the viewer. Looking
over a shoulder is not the same action as rotating the entire body. Not every
family needs eight duplicate tracks: declare its supported facings and an
authored connector or explicit unavailable result for unsupported requests.

## First bounded replacement proof

Demonstrate two complete, continuous actions before scaling the library:

```text
front rest -> gaze left -> anticipation -> front-left turn -> left profile
-> walk start -> full alternating walk cycles -> decelerate/plant -> profile rest
-> turn through front-left -> front -> settle/full breath

front rest -> gaze right -> anticipation -> front-right turn -> right profile
-> walk start -> full alternating walk cycles -> decelerate/plant -> profile rest
-> turn through front-right -> front -> settle/full breath
```

Also plan a turn-away/return study with back-quarter and back correspondence;
do not manufacture it by horizontal mirroring of the asymmetric approved head.
Independent left/right source review is required. A return turn need not be a
reversed outbound sequence: anticipation and settling have different timing.

The full planning map is not authorization to generate the entire 32-family
library now. The first bounded sequence is a proposed replacement review scope,
not a claim that the old request contract accepts it.

## Authored timing and physical continuity

Provisional drawing budgets, to be revised from playback rather than counted
as quality: front breathing 16-24 drawings over a complete 3-4 second cycle;
profile stride 16-24 drawings per full two-step cycle; each 90-degree body turn
8-12 drawings including anticipation/settle; each start/stop 6-10 drawings;
front listen/acknowledge 16-24 drawings with a readable listening hold. All
durations remain integer 24 Hz ticks. These are targets, not completed counts
or newly adopted validator limits. Holds extend duration; they are not unique
drawings. Timing, spacing and identity continuity matter more than the count.

Walk key order on each profile: anatomical left contact, down, passing, up;
anatomical right contact, down, passing, up; then reconnect to the first pose.
Add in-betweens only after these keys visibly exchange the legs correctly.
The swing foot clears the floor; support changes visibly; arms counter-swing;
head/torso weight response is bounded; hands retain the same fingers and thumb
through occlusion. Starts and stops connect to a specific support-leg phase.
Stopping cannot snap a passing foot onto the ground. Reversing direction requires
deceleration/plant, a deliberate turn, and a new first step.

For idle, torso expansion AND contraction must be visible, with delayed small
arm/head follow-through and planted feet. Acknowledgment follows attention and
a listening hold, then settles. Neither action is an endlessly looped nod.

## Source root is not a world-space planted foot

The source root remains (512,896); actor translation stays outside PNG pixels.
For an in-place treadmill walk, a support foot moves backward relative to the
root while world translation moves the body forward. Grounding must evaluate
the composition, not hardcode a constant local foot point:

```text
world_contact(t) = actor_position(t)
                 + uniform_scale * (source_contact(t) - source_root)
```

Idle contacts can be stationary in both spaces. Translating locomotion generally
cannot keep a foot fixed relative to BOTH actor and ground. Before implementing
this in the contract, reconcile R10's contact reference frame with the Architect;
do not silently reinterpret the accepted two-pixel contact check or shorten
contacts to single frames to make it vacuous. Keep source-root, local landmarks,
stance intervals, intended stride distance and observed world slip distinguishable.

## Visual and runtime review gates for the replacement

- Eight-facing construction correspondence checked against exact references;
  no new anatomy or unapproved mirror assumed correct.
- Frame strips identify anatomical limbs and gait phases through overlap.
- Both complete travel-and-return sequences play at normal and quarter speed;
  direction changes correspond to actual silhouette changes.
- Profile walk never falls back to front-left; front idle never selects a
  diagonal track. An unavailable exact track reports unavailable, not success.
- First/last posture, support leg and facing match connectors; no seam jerk,
  mid-step reset, unsolicited turn, or infinite one-shot animation.
- Cutouts inspected on black, white, gray and saturated contrast backdrops;
  no green fringe or transparent-edge halo accepted on transport success alone.
- Smoothness, hand stability and identity are visual gates; pixel hashes and
  green CI do not establish them. No request to approve the rejected package.
- Full-library generation and target-host endurance remain outside this planning
  correction. Replacement art/intake/playback are NOT RUN this turn.

## External discovery and evidence

REFERENCE only: Adobe's walk-cycle guide, rechecked 2026-09-12,
https://www.adobe.com/creativecloud/animation/discover/animation-walk-cycle.html .
Its contact/crossover and whole-body weight discussion supports planning gait
keys before in-betweens. No Adobe software, new dependency or donor character
asset is adopted. This plan's facing policy comes from the operator, not Adobe.

Repository profile defect: E1_OBSERVED. New motion quality: NOT RUN.
Protected primary status-only inspection retained its AGENTS.md/.gitignore
modifications; secondary .gitignore/.ignore remain untouched. No runtime or
contract code is changed by this planning record.
