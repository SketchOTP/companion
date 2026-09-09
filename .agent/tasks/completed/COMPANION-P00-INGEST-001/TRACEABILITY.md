# COMPANION-P00-INGEST-001 — End-Goal and Roadmap Traceability

Source abbreviations: **Canonical** = Ground-Zero Canonical Project; **End Goal** = Complete Operational Definition; **Roadmap** = Planning Phase 02 Master Delivery Roadmap; **R01–R10** = Research Phase 01 domain pages. Statuses below are live Architecture Decision Ledger statuses, not inferred maturity.

## Canonical semantic reference key

### Architecture decisions cited

- `ADR-02 — Use Notion as the single source of truth for project meaning and status — Adopted`
- `ADR-03 — Keep the caregiving safety core architecturally independent from the companion — Adopted`
- `ADR-04 — Use a hybrid persistent-organism architecture as the working direction — Interim`
- `ADR-05 — Do not allow a language model to own canonical identity, state, memory, or safety authority — Interim`
- `ADR-06 — Maintain distinct homeostatic drives with explicit arbitration — Interim`
- `ADR-07 — Implement baby-like growth through developmental capability gates over safe pretrained priors — Interim`
- `ADR-08 — Use append-only evidence with typed, temporal, versioned derived memories — Interim`
- `ADR-09 — Treat dreaming as governed offline consolidation, not factual experience — Adopted`
- `ADR-10 — Prohibit uncontrolled online foundation-model weight updates in the first implementation — Interim`
- `ADR-11 — Require perception systems to emit uncertain evidence rather than durable beliefs — Interim`
- `ADR-12 — Treat affect as a contextual hypothesis, never a directly observed fact or sole safety trigger — Adopted`
- `ADR-13 — Make embodiment an engine-neutral adapter driven by causal intents — Interim`
- `ADR-14 — Require local survival and owner-portable creature continuity — Interim`
- `ADR-15 — Qualify named safety scenarios instead of building a generalized danger detector — Adopted`
- `ADR-16 — Use explicit help requests and declared check-in deadlines as first safety-validation candidates — Interim`
- `ADR-22 — Run iteration one on the existing Linux PC and existing peripherals — Adopted`
- `ADR-23 — Use Godot as the iteration-one embodiment engine — Adopted`
- `ADR-24 — Pin Godot 4.7.2 stable as the initial implementation baseline — Interim`
- `ADR-25 — Represent the mon as an original project-authored 2D sprite system — Adopted`
- `ADR-26 — Adopt MON_FRAME_V1 and a layered semantic sprite-clip pipeline — Interim`
- `ADR-27 — Keep Godot embodiment separate from canonical state and caregiving authority — Adopted`
- `ADR-28 — Adopt Mon Visual Reference V1 as the canonical iteration-one identity — Adopted`
- `ADR-29 — Approve the six-view turnaround sheet as an authoritative visual reference — Adopted`
- `ADR-31 — Adopt the complete operational end goal as the project completion baseline — Adopted`
- `ADR-32 — Begin Planning Phase 02 and govern delivery through the 16-phase master roadmap — Adopted`

### Risks cited

- `RISK-01 — Missed qualified emergency or distress event`
- `RISK-02 — False safety escalation and alarm fatigue`
- `RISK-03 — Biometric misidentification or spoofing`
- `RISK-04 — Private camera, microphone, memory, or safety data exposure`
- `RISK-05 — False or corrupted autobiographical memory`
- `RISK-06 — Companion behavior creates unhealthy dependence, exclusivity, guilt, or social withdrawal`
- `RISK-07 — Prompt injection or poisoned teaching through speech, screens, visitors, media, or demonstrations`
- `RISK-08 — Cloud, subscription, vendor, model, or service shutdown`
- `RISK-09 — Code, model, dataset, voice, asset, or plugin rights are incompatible`
- `RISK-10 — Runtime latency, heat, power, noise, or instability breaks continuous aliveness`
- `RISK-11 — Developmental gates produce either a fake infant or an unsafe/incompetent system`
- `RISK-13 — Check-in interaction is inaccessible to a user in distress or with disability`
- `RISK-14 — Model or software update silently changes qualified behavior`

## End-goal acceptance pillars

| Pillar | Canonical source(s) and relevant decisions | Roadmap phase(s) that build it | Major linked risk(s) | Current proof/status | Gap before end-goal acceptance |
|---|---|---|---|---|---|
| Persistent individual | Canonical; End Goal §§1,9; R01; R02; ADR-04, ADR-08, ADR-14, ADR-31 | 03, 04, 08, 11, 13–15 | RISK-05, RISK-08, RISK-14 | End goal adopted; architecture/memory/continuity decisions remain Interim; no implementation | Canonical state, memory-integrity, restart/migration equivalence, update safety, restore, and longitudinal identity evidence |
| Autonomous life | End Goal §2; R01; ADR-04, ADR-06, ADR-07, ADR-31 | 03, 07–09, 13–15 | RISK-10, RISK-11 | Hybrid, drive, and developmental directions are Interim; no implementation | Deterministic multi-drive life, durable goals/actions, coherent interruption, developmental promotion, and longitudinal qualification |
| Embodied aliveness | End Goal §3; R04; R10; Visual Bible; ADR-13, ADR-22, ADR-23, ADR-24, ADR-25, ADR-26, ADR-27, ADR-28, ADR-29 | 02, 03, 09, 13–15 | RISK-09, RISK-10, RISK-14 | Host, engine, 2D identity, turnaround, and separation adopted; version/pipeline/causal-intent details include Interim decisions | Construction references, normalized life set, rights evidence, causal integration, load/latency/soak tests, and perceptual review |
| Grounded interaction | End Goal §4; R03; R04; ADR-11, ADR-12, ADR-22, ADR-31 | 04–06, 09, 13–15 | RISK-03, RISK-07, RISK-10, RISK-13 | Uncertain-evidence direction is Interim; affect limit and host are adopted; dependencies remain open | Qualified audio/vision/identity stack, spoof/adversarial/accessibility coverage, grounding, uncertainty calibration, and end-to-end tests |
| Development and teaching | End Goal §5; R01; R03; ADR-07, ADR-10, ADR-11 | 03, 05–07, 09, 13–15 | RISK-07, RISK-11, RISK-14 | Developmental gates, controlled learning, and perception boundary are Interim; no implementation | Curriculum, teachable-skill lifecycle, mastery/correction/rollback, poisoned-teaching resistance, leakage/generalization, and update regression evidence |
| Memory and dreaming | End Goal §6; R02; ADR-08, ADR-09, ADR-14 | 04, 07–09, 11, 13–15 | RISK-04, RISK-05, RISK-08, RISK-14 | Dream/fact separation adopted; memory and continuity designs Interim; storage remains open | Typed schema, correction/supersession, synthetic isolation, false-memory benchmark, privacy, scale, migration, and restore qualification |
| Caregiving utility | End Goal §7; R05; ADR-03, ADR-11, ADR-12, ADR-15, ADR-16 | 10, 12–15 | RISK-01, RISK-02, RISK-03, RISK-13 | Separation, affect limit, and named-scenario rule adopted; perception and first scenario candidates Interim; RQ-05/RQ-10 open | Selected scenario/jurisdiction, evidence coverage, sensitivity/false-alert targets, accessible check-in, consented transport, delivery/ack, audit, and pilot outcomes |
| Privacy and security | End Goal §8; R06; Governance; ADR-03, ADR-05, ADR-08, ADR-11, ADR-12, ADR-14 | 01, 04–07, 10–15 | RISK-03, RISK-04, RISK-07, RISK-08, RISK-14 | Boundaries are adopted or Interim; controls unimplemented; retention/identity choices open | Threat/data/privilege model, consent/retention, biometric spoof testing, encryption/access, injection defense, supply-chain review, recovery, and incident exercise |
| Continuity and ownership | End Goal §9; R06; ADR-14, ADR-27, ADR-31 | 01, 04, 08, 11, 13–15 | RISK-05, RISK-08, RISK-14 | Renderer separation and end goal adopted; local survival/portability Interim; no operational proof | Versioned backup/export/restore/migration, key recovery, offline/vendor replacement, update rollback, and replacement-body tests |
| Human outcome | End Goal §10; R05; R07; ADR-03, ADR-07, ADR-12, ADR-15, ADR-31 | 09, 12–15 | RISK-01, RISK-02, RISK-06, RISK-11, RISK-13 | Ethical, safety, and outcome requirements adopted or bounded Interim; no longitudinal evidence | Population/protocol, non-manipulation and accessibility review, well-being/benefit measures, false-alert burden, longitudinal pilot, and release claims evidence |

## Roadmap phase coverage

| Phase | Required outcome in own words | Depends on | Produces evidence for | Current status/authorization | Canonical source |
|---|---|---|---|---|---|
| 00 — Planning and product contract | Freeze traceable product, architecture, interfaces, risks, test strategy, data/security plan, asset plan, and backlog | End Goal; research; operator rulings | Every pillar's planned acceptance path | **ACTIVE**; ingest correction gate active; product work closed | Roadmap Phase 00; ADR-31; ADR-32; directive |
| 01 — Environment and engineering foundation | Establish reproducible repo, tooling, quality gates, observability, configuration, and safe development runtime | Accepted Phase 00 package | Privacy, continuity, future regression evidence | **NOT AUTHORIZED** | Roadmap Phase 01; R09 |
| 02 — Mon body, habitat, and sprite pipeline | Produce standards-conformant construction references, frames, semantic clips, layers, atlases, loading, and the selected screen habitat | Phase 01; Visual Bible; R10; presentation-mode decision | Embodied aliveness | **NOT AUTHORIZED**; screen habitat and supporting construction work remain open | Roadmap Phase 02; R10 |
| 03 — Organism kernel and autonomous life | Implement renderer-independent canonical organism time, needs, drives, goals, actions, temperament, and development | 01; accepted Phase 00 contracts | Persistent individual; autonomy | **NOT AUTHORIZED** | Roadmap Phase 03; R01 |
| 04 — Evidence, world model, and persistent memory | Build provenance-bearing evidence, world claims, typed temporal memory, correction, and persistence | 01, 03 | Grounding; memory; continuity | **NOT AUTHORIZED**; retention/storage contracts open | Roadmap Phase 04; R02–R04 |
| 05 — Speech presence and dialogue | Add interruptible VAD/STT/TTS and grounded dialogue without granting model authority | 03, 04; voice/language/wake/interruption decision | Grounded interaction; teaching | **NOT AUTHORIZED**; interaction model and stack open | Roadmap Phase 05; R03 |
| 06 — Vision, identity, and social attention | Add consented identity and uncertain face/pose/gesture/object evidence | 03–05; user/household and identity-authority decisions | Grounded interaction; privacy | **NOT AUTHORIZED**; population, multi-user, and retention rules open | Roadmap Phase 06; R03; R06 |
| 07 — Teaching, learning, and development | Teach bounded words, objects, counts, gestures, actions, tricks, and lessons with mastery/correction | 03–06 | Development; autonomy | **NOT AUTHORIZED** | Roadmap Phase 07; R01; R03 |
| 08 — Sleep, dreaming, and lifelong consolidation | Add consolidation, forgetting, synthetic-dream isolation, and long-horizon maintenance | 03, 04, 07 | Memory/dreaming; continuity | **NOT AUTHORIZED** | Roadmap Phase 08; R02 |
| 09 — Personality, relationship, and rich daily life | Integrate temperament, rituals, play, and shared history without manipulation | 02–08; household/relationship model | Human outcome; embodied/autonomous life | **NOT AUTHORIZED** | Roadmap Phase 09; R07 |
| 10 — Caretaking core foundation | Implement an independent deterministic policy/audit boundary for a selected named scenario | 01, 04, 06; scenario/jurisdiction decision | Caregiving; safety architecture | **NOT AUTHORIZED**; first scenario open | Roadmap Phase 10; R05 |
| 11 — Security, privacy, resilience, and owner continuity | Harden least privilege, consent, encryption, updates, rollback, backup/export/restore, and vendor replacement | 01–10; retention and support-lifetime promises | Privacy; continuity | **NOT AUTHORIZED** | Roadmap Phase 11; R06 |
| 12 — Routine learning and qualified escalation | Learn routines under evidence coverage and qualify staged accessible escalation/contact acknowledgment | 04, 06, 10, 11; scenario, population, and notification decisions | Caregiving utility; human outcome | **NOT AUTHORIZED**; transport/acknowledgment and accessibility constraints open | Roadmap Phase 12; R05 |
| 13 — Integrated alpha and content scale | Integrate all authorities, scale content, test degradation/performance, and close cross-system gaps | 01–12 | All pillars at integrated target level | **NOT AUTHORIZED** | Roadmap Phase 13; End Goal |
| 14 — Longitudinal pilot and human validation | Run consented long-horizon evaluation of continuity, benefit, safety, false alerts, relationship, and recovery | 13; selected population/intended use and approved evaluation protocol | Human outcome and operational/longitudinal proof | **NOT AUTHORIZED**; population, use, and protocol open | Roadmap Phase 14; End Goal §10 |
| 15 — Release qualification and operational launch | Establish release claims, operations, support, incident response, recovery, and owner-control evidence | 14 and all prior exit criteria; product name and support promise | End-goal acceptance | **NOT AUTHORIZED** | Roadmap Phase 15; End Goal |

## Cross-cutting constraints

| Constraint | Applies to phases | Canonical authority | How compliance is evidenced | Current status |
|---|---|---|---|---|
| Notion remains project source of truth | 00–15 | Governance; ADR-02 | Live link traversal, ID/title reconciliation, Notion result publication | Adopted; focused re-fetch verified |
| Companion and caregiving authority remain separate | 00, 03–15 | End Goal; R05; ADR-03 | Process/privilege ownership, policy tests, immutable audit, and failure isolation | Adopted; unimplemented |
| LLM cannot own canonical state, memory, tools, or safety | 00, 03–15 | R01–R06; ADR-05 | Typed proposal boundaries, capability controls, persistence ownership, and degraded-mode tests | Interim constraint; unimplemented |
| Perception remains evidence with uncertainty and affect remains hypothesis | 00, 04–07, 10–15 | R03; ADR-11; ADR-12 | Confidence/provenance/abstention schemas, calibration, corroboration, and negative escalation tests | Interim/adopted boundary; unimplemented |
| Dream generation cannot become external fact | 00, 04, 08, 11, 13–15 | R02; ADR-09 | Synthetic tagging, isolation, and negative factual-write-path tests | Adopted; unimplemented |
| Core identity and continuity have a local path | 00, 01, 03–15 | End Goal; R06; ADR-14 | Offline/degraded operation, backup/export/restore/migration and vendor-replacement tests | Interim constraint; unimplemented |
| Code, models, data, voices, assets, and services need separate rights review | 00–15 | Governance; R06; RISK-09 | Provenance/license inventory and artifact-level approval records | Required; only governance assets present |
| Approved visual identity and `MON_FRAME_V1` are preserved | 00, 02, 09, 13–15 | Visual Bible; R10; ADR-25; ADR-26; ADR-28; ADR-29 | Hash/metadata, frame validators, anatomy checks, and perceptual review | Adopted/Interim pipeline; production assets absent |
| Attachment must not be optimized through manipulation | 00, 03, 05, 07, 09, 12–15 | R07; RISK-06 | UX/policy review, prohibited-metric checks, red-team studies, and longitudinal measures | Required; unimplemented |
| Product claims require matching qualification evidence | 00–15 | End Goal; Governance; ADR-31 | Authority evidence ladder, traceable exit criteria, pilot evidence, and release review | Adopted; corpus enumeration remains E2 and this focused semantic correction reaches E3; no product evidence exists |

## Traceability conclusion

Every end-goal pillar has at least one owning roadmap phase and a planned path toward integrated, longitudinal, and release evidence; every phase supports at least one pillar. The corrected references distinguish adopted decisions from Interim directions and tie each risk only to a substantive failure mode. The eleven RQ records retain their canonical meanings. Architecture/dependency selection, evaluation-protocol design, and unfinished visual construction references remain legitimate Phase 00 or production-planning work, but they are not substituted for unrelated RQ identifiers. All product evidence paths remain future work and unauthorized.
