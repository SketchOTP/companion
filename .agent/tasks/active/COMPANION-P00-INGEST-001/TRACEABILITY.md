# COMPANION-P00-INGEST-001 — End-Goal and Roadmap Traceability

Source abbreviations: **Canonical** = Ground-Zero Canonical Project; **End Goal** = Complete Operational Definition; **Roadmap** = Planning Phase 02 Master Delivery Roadmap; **R01–R10** = Research Phase 01 domain pages; **ADR-N** and **SRC-N** = live database records.

## End-goal acceptance pillars

| Pillar | Canonical source(s) | Roadmap phase(s) that build it | Major linked risk(s) | Current proof/status | Gap before end-goal acceptance |
|---|---|---|---|---|---|
| Persistent individual | Canonical; End Goal §§1,9; R01; R02; ADR-01, ADR-31 | 03, 04, 08, 11, 13–15 | RISK-01, 04, 11, 14 | Adopted requirement; no implementation | Canonical state, tested persistence, migration, restore, and longitudinal identity evidence |
| Autonomous life | End Goal §2; R01; ADR-02, 03 | 03, 07–09, 13–15 | RISK-01, 02, 12 | Architecture principle adopted; implementation absent | Deterministic multi-drive life, durable goals/actions, developmental and longitudinal qualification |
| Embodied aliveness | End Goal §3; R04; R10; Visual Bible; ADR-14, 23–29 | 02, 03, 09, 13–15 | RISK-03, 10 | Host/engine/style/identity/turnaround adopted and visually inspected | Production construction sheets, sprite pipeline, semantic clips, causal integration, perceptual tests |
| Grounded interaction | End Goal §4; R03; R04; ADR-07–09 | 04–06, 09, 13–15 | RISK-02, 07, 09 | Evidence-first rules adopted; concrete dependencies open | Qualified audio/vision/identity stack, uncertainty handling, grounding and end-to-end tests |
| Development and teaching | End Goal §5; R01; R03; ADR-03, 12 | 03, 05–07, 09, 13–15 | RISK-02, 12 | Developmental-gate and bounded-learning hypotheses recorded | Learning curriculum, mastery/correction/rollback design, efficacy and safety evidence |
| Memory and dreaming | End Goal §6; R02; ADR-04–06 | 04, 07–09, 11, 13–15 | RISK-04, 05, 14 | Typed/temporal/synthetic-separation principles adopted; storage open | Schema, consolidation/forgetting, synthetic isolation, correction, scale, backup/restore qualification |
| Caregiving utility | End Goal §7; R05; ADR-10, 11, 17 | 10, 12–15 | RISK-06, 07, 09, 13 | Independent named-scenario authority adopted; scenario/operator decisions open | Chosen scenario, evidence envelope, accessible check-in, consented contacts, delivery/ack and pilot outcomes |
| Privacy and security | End Goal §8; R06; Governance; ADR-08, 15 | 01, 04–07, 10–15 | RISK-05, 07, 08, 14 | Local-first/least-privilege constraints adopted; controls unimplemented | Threat model, data map, consent/retention, encryption, access, supply-chain and red-team evidence |
| Continuity and ownership | End Goal §9; R06; ADR-15, 16 | 01, 04, 08, 11, 13–15 | RISK-04, 08, 11, 14 | Portability/local survival adopted; no operational proof | Versioned backup/export/restore/migration, rollback, vendor replacement and disaster tests |
| Human outcome | End Goal §10; R07; R05; ADR-13, 31 | 09, 12–15 | RISK-06, 12, 13 | Ethical relationship and measurable-outcome requirements adopted | Metrics, non-manipulation review, longitudinal pilot, accessibility, benefit/false-alert evidence |

## Roadmap phase coverage

| Phase | Required outcome in own words | Depends on | Produces evidence for | Current status/authorization | Canonical source |
|---|---|---|---|---|---|
| 00 — Planning and product contract | Freeze traceable product, architecture, interfaces, risks, test strategy, data/security plan, asset plan, and backlog | End Goal; research; operator rulings | Every pillar's planned acceptance path | **ACTIVE**; ingest is first gate; product work closed | Roadmap Phase 00; directive |
| 01 — Environment and engineering foundation | Establish reproducible repo, tooling, quality gates, observability, configuration, and safe dev runtime | Accepted Phase 00 package | Privacy, continuity, future regression evidence | **NOT AUTHORIZED** | Roadmap Phase 01; R09 |
| 02 — Mon body, habitat, and sprite pipeline | Produce standards-conformant anatomy, frames, semantic clips, layers, atlases, loading, and habitat | Phase 01; Visual Bible; R10 | Embodied aliveness | **NOT AUTHORIZED**; habitat/construction choices open | Roadmap Phase 02; R10 |
| 03 — Organism kernel and autonomous life | Implement renderer-independent canonical organism time, needs, drives, goals, actions, temperament, and development | 01; contracts from 00 | Persistent individual; autonomy | **NOT AUTHORIZED** | Roadmap Phase 03; R01 |
| 04 — Evidence, world model, and persistent memory | Build provenance-bearing evidence, world claims, typed temporal memory, correction, and persistence | 01, 03 | Grounding; memory; continuity | **NOT AUTHORIZED**; storage open | Roadmap Phase 04; R02–R04 |
| 05 — Speech presence and dialogue | Add interruptible VAD/STT/TTS and grounded dialogue without granting model authority | 03, 04 | Grounded interaction; teaching | **NOT AUTHORIZED**; stack open | Roadmap Phase 05; R03 |
| 06 — Vision, identity, and social attention | Add consented identity and uncertain face/pose/gesture/object evidence | 03–05 | Grounded interaction; privacy | **NOT AUTHORIZED**; stack/retention open | Roadmap Phase 06; R03, R06 |
| 07 — Teaching, learning, and development | Teach bounded words, objects, counts, gestures, actions and lessons with mastery/correction | 03–06 | Development; autonomy | **NOT AUTHORIZED** | Roadmap Phase 07; R01, R03 |
| 08 — Sleep, dreaming, and lifelong consolidation | Add consolidation, forgetting, synthetic dreaming isolation, and long-horizon maintenance | 03, 04, 07 | Memory/dreaming; continuity | **NOT AUTHORIZED** | Roadmap Phase 08; R02 |
| 09 — Personality, relationship, and rich daily life | Integrate temperament, rituals, play and shared history without manipulation | 02–08 | Human outcome; embodied/autonomous life | **NOT AUTHORIZED** | Roadmap Phase 09; R07 |
| 10 — Caretaking core foundation | Implement an independent deterministic policy/audit boundary for named scenarios | 01, 04, 06; operator scenario ruling | Caregiving; safety architecture | **NOT AUTHORIZED**; first scenario open | Roadmap Phase 10; R05 |
| 11 — Security, privacy, resilience, and owner continuity | Harden least privilege, consent, encryption, updates, rollback, backup/export/restore and vendor replacement | 01–10 | Privacy; continuity | **NOT AUTHORIZED** | Roadmap Phase 11; R06 |
| 12 — Routine learning and qualified escalation | Learn routines under evidence coverage and qualify staged accessible escalation/contact acknowledgment | 04, 06, 10, 11; contact decisions | Caregiving utility; human outcome | **NOT AUTHORIZED**; contacts/evidence envelope open | Roadmap Phase 12; R05 |
| 13 — Integrated alpha and content scale | Integrate all authorities, scale content, test degradation/performance, and close cross-system gaps | 01–12 | All pillars at integrated target level | **NOT AUTHORIZED** | Roadmap Phase 13; End Goal |
| 14 — Longitudinal pilot and human validation | Run consented long-horizon evaluation of continuity, benefit, safety, false alerts, relationship and recovery | 13; approved protocol/population | Human outcome and operational/longitudinal proof | **NOT AUTHORIZED**; protocol/population open | Roadmap Phase 14; End Goal §10 |
| 15 — Release qualification and operational launch | Establish release claims, operations, support, incident response, recovery and owner-control evidence | 14 and all prior exit criteria | End-goal acceptance | **NOT AUTHORIZED** | Roadmap Phase 15; End Goal |

## Cross-cutting constraints

| Constraint | Applies to phases | Canonical authority | How compliance is evidenced | Current status |
|---|---|---|---|---|
| Notion remains project source of truth | 00–15 | Governance; ADR-19 | Live link traversal, reconciliation, Notion result publication | Adopted; ingest verified |
| Companion and caregiving authority remain separate | 00, 03–15 | End Goal; R05; ADR-10 | Interface ownership, policy tests, audit and failure isolation | Adopted; unimplemented |
| LLM cannot own canonical state, memory, tools, or safety | 00, 03–15 | R01–R06; ADR-01, 07 | Architecture boundaries, capability controls and degraded-mode tests | Adopted; unimplemented |
| Perception remains evidence with uncertainty | 00, 04–07, 10–15 | R03; ADR-08 | Confidence/provenance/abstention schemas and calibration tests | Adopted; unimplemented |
| Dream generation cannot become external fact | 00, 04, 08, 11, 13–15 | R02; ADR-06 | Synthetic tag isolation and negative write-path tests | Adopted; unimplemented |
| Core identity and continuity have a local path | 00, 01, 03–15 | End Goal; R06; ADR-15, 16 | Offline/degraded operation, backup/export/restore/migration tests | Adopted; unimplemented |
| Code, models, data, voices, assets, and services need separate rights review | 00–15 | Governance; R06; ADR-20 | Provenance/license inventory and approval records | Adopted; only governance assets present |
| Approved visual identity and `MON_FRAME_V1` are preserved | 00, 02, 09, 13–15 | Visual Bible; R10; ADR-23–29 | Hash/metadata, frame validators and perceptual review | Adopted; references inspected, production assets absent |
| Attachment must not be optimized through manipulation | 00, 03, 05, 07, 09, 12–15 | R07; ADR-13 | UX/policy review, telemetry constraints, human-study measures | Adopted; unimplemented |
| Product claims require matching qualification evidence | 00–15 | End Goal; Governance; ADR-31 | Authority evidence ladder, traceable exit criteria and release review | Adopted; this ingest is E2 only |

## Traceability conclusion

Every end-goal pillar has at least one owning roadmap phase and a planned progression to integrated, longitudinal, and release evidence. Every roadmap phase supports one or more end-goal pillars; none is an orphan. No acceptance pillar lacks a planned evidence path, but all product paths remain future work. Open choices—especially architecture/dependencies, habitat/construction art, caregiving scenario/contact flow, privacy retention, shipping population, and longitudinal protocol—must be resolved by later bounded authority before their dependent phases can claim completion.
