# COMPANION-P00-ENV-001 — Product-Contract Brief

Status: `COMPLETE_FOR_ARCHITECT_REVIEW`

Machine evidence narrows technical constraints but resolves none of the eleven operator/product decisions below. Each canonical identifier/title appears once in this crosswalk.

| RQ | Canonical status | Relevant environment evidence | Operator input still required | Downstream architecture affected | Blocks next package? |
|---|---|---|---|---|---|
| RQ-02 — First user population and household model | OPEN | **OBSERVED:** No machine fact identifies the intended user or household. Multiple displays and inputs do not imply multiple users. | Choose one primary qualification population, accessibility needs, household shape, safeguarding boundary, and whether minors are excluded. | Consent, accessibility, identity/biometrics, user data, evaluation cohort, safety policy | YES |
| RQ-03 — Intended product use and commercialization path | OPEN | **OBSERVED:** The host is a private Linux workstation; that does not establish research, pilot, consumer, or care-product intent. | Choose internal research, private prototype, supervised pilot, consumer product, or care-provider path and the permitted non-medical claims. | Regulatory/quality boundary, telemetry, evidence burden, support, licensing | YES |
| RQ-04 — Offline, cloud, compute, power, noise, and cost boundary | OPEN | **OBSERVED:** 8-core/16-thread CPU, 67.3 GB RAM, two 6 GiB NVIDIA GPUs, local NVMe, working OpenGL 4.6. **UNKNOWN:** model headroom, concurrent load, energy, noise, Vulkan, thermals under load. | Set the required offline survival level, cloud allowance, recurring-cost tolerance, power/noise limits, and acceptable degradation. | Process placement, model/service adapters, cache/persistence, scheduling, fallback policy | YES |
| RQ-05 — First caregiving scenario and escalation jurisdiction | OPEN | **OBSERVED:** Webcam plus separate USB/webcam/onboard audio inputs exist. **UNKNOWN:** sensor quality and safety fitness. Hardware does not choose a scenario or jurisdiction. | Choose the first qualified scenario, jurisdiction, claims boundary, check/acknowledgment timing, and escalation conditions. | Safety policy, sensor requirements, audit schema, verification sequence, validation plan | YES |
| RQ-07 — Multi-user identity, ownership, and relationship model | OPEN | **OBSERVED:** The workstation exposes multiple displays and input/output devices, but no evidence establishes household membership, ownership, or consent roles. | Define owner, additional household users, guests, trusted contacts, revocation, and relationship separation. | Identity, authorization, consent, memory partitioning, privacy, recovery | YES |
| RQ-08 — Voice, languages, wake word, and interruption model | OPEN | **OBSERVED:** Default mono USB mic supports 44.1/48 kHz; webcam mic supports 16 kHz; HDMI stereo output is default. **UNKNOWN:** far-field, AEC, latency, wake word, and barge-in. | Select language set, voice ownership/licensing expectations, activation model, interruption behavior, and privacy expectations for listening. | Audio boundary, VAD/STT/TTS interfaces, permissions, resource budgets, UX | YES |
| RQ-09 — Memory retention, export, backup, and deletion promises | OPEN | **OBSERVED:** Local ext4/NVMe has about 703 GB available; repository is on SSHFS. Capacity does not determine retention policy or durability. | Define retention periods, deletion semantics, export format, backup destination, restore promise, and treatment of safety/audit records. | Storage ownership, encryption, schema lifecycle, backup/restore, audit immutability | YES |
| RQ-10 — Notification and trusted-contact transport | OPEN | **OBSERVED:** No private network/account/contact data was collected. The host inventory does not select a transport or prove delivery. | Choose allowed contact channels, acknowledgment and retry rules, fallback path, contact enrollment/revocation, and outage behavior. | Notification adapter, secrets, consent, audit, delivery verification, safety failure states | YES |
| RQ-11 — Support lifetime and continuity promise | OPEN | **OBSERVED:** Ubuntu LTS, NVIDIA proprietary driver, two desktop managers, degraded systemd managers, 4.7.2 absent, 4.6 present, and split SSHFS/local storage create a nontrivial maintenance surface. | Choose supported lifetime, upgrade policy, offline continuity duration, owner export/restore guarantee, and service/vendor shutdown promise. | Version pinning, migrations, packaging, recovery, dependency policy, operational support | YES |
| RQ-12 — Canonical product name | PARTIALLY RESOLVED | **OBSERVED:** Repository name is fixed. The machine provides no relevant naming evidence. | Choose the product-facing name and any trademark/domain constraints when needed. | Branding, package/application identifiers, documentation | NO — may defer while stable internal identifiers are used |
| RQ-14 — Godot presentation mode and screen habitat | OPEN | **OBSERVED:** Three outputs exist across two logical X screens: two 4K/60 Hz GNOME-managed outputs and one 1366×768/59.96 Hz Openbox-managed output; text scale is 1.75 and work areas differ. | Choose target screen/output, full-screen world versus bounded habitat/window versus overlay, default creature size, movement bounds, persistence across display changes, and multi-monitor behavior. | Windowing, coordinate/scaling policy, focus/input, renderer affinity, placement persistence | YES |

## Recommended decision order

1. Fix the primary user/household and intended-use/claims boundary first; they govern safety, consent, privacy, accessibility, evidence, and commercialization obligations.
2. Choose the first caregiving scenario and jurisdiction, then the notification/acknowledgment boundary; this defines the safety contract before sensor or transport selection.
3. Set offline/cloud/cost/power/noise and support-lifetime promises; these govern process placement, model evaluation, packaging, continuity, and vendor-dependence rules.
4. Define multi-user ownership/consent and memory retention/export/deletion together because their data and revocation boundaries are coupled.
5. Decide voice/language/activation/interruption behavior after the privacy and offline boundaries are fixed, while retaining later acoustic qualification.
6. Decide the target display and habitat using the three-output/two-screen evidence before any Godot window contract is drafted.
7. Defer the product-facing name if needed; stable internal identifiers can support architecture work without prejudging branding.

## Operator question packet

1. Who is the single primary qualification population, what accessibility needs are mandatory, what household roles exist, and are minors explicitly out of scope?
2. Is the first outcome an internal research build, private prototype, supervised pilot, consumer product, or care-provider product, and what exact non-medical claims are permitted?
3. What must work with no network, what cloud use is acceptable, and what recurring cost, power, fan-noise, and graceful-degradation limits are acceptable?
4. Which first caregiving scenario and legal jurisdiction should be qualified, and what user/contact acknowledgment sequence is acceptable?
5. Who owns the creature and data, who else may interact, and how are guest access, trusted contacts, consent, and revocation handled?
6. Which languages are required, who owns/approves the voice, and should interaction use push-to-talk, explicit activation, wake word, continuous listening, or a staged combination?
7. What must be retained, exported, backed up, corrected, or deleted, for how long, and which safety/audit records have different rules?
8. Which trusted-contact transports are allowed, what counts as acknowledgment, and what retry/fallback behavior is required when delivery fails?
9. What support lifetime, upgrade path, offline continuity, export/restore, and vendor/service-shutdown promise should the project make?
10. Is the product-facing name required before architecture/package identifiers are fixed, or may naming remain deferred?
11. Which of the two 4K GNOME outputs or the separate 1366×768 Openbox output is the default habitat, and should the creature occupy a full-screen world, bounded window, or overlay?

## Technical decisions still owned by the Architect

- Exact process boundaries, IPC, persistence technology, build/package layout, renderer choice, GPU selection, camera mode, audio framework, speech stack, model candidates, notification adapter, service topology, and CI remain architecture/dependency decisions.
- The Architect should not treat absent diagnostics as absent capability, or generic specifications as workload evidence.
- Godot 4.7.2 availability requires a later bounded environment/dependency action; this directive neither installs it nor revises the version ruling.
