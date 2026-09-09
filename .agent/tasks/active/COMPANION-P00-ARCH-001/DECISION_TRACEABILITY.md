# Decision Traceability

Status: `COMPLETE — SEMANTIC CROSSWALK VALIDATED`

## External primary-source key

All external sources were retrieved on 2026-09-09 and are recommendation evidence, not product proof.

- **S01:** [JSON Schema Draft 2020-12 specification](https://json-schema.org/specification) — current released schema dialect.
- **S02:** [XDG Base Directory Specification 0.8](https://specifications.freedesktop.org/basedir/0.8/) — local config/data/state/cache/runtime placement and private local runtime directory.
- **S03:** [SQLite Write-Ahead Logging](https://www.sqlite.org/wal.html) — one-host WAL behavior, concurrency limits, network-filesystem prohibition, checkpointing, and 2026 WAL-reset fix.
- **S04:** [SQLite Online Backup API](https://www.sqlite.org/backup.html) — consistent snapshot/backup mechanism.
- **S05:** [systemd service documentation source](https://github.com/systemd/systemd/blob/main/man/systemd.service.xml), [execution sandbox documentation source](https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml), and [socket activation documentation source](https://github.com/systemd/systemd/blob/main/man/systemd.socket.xml) — restart/watchdog, least privilege, and local activation.
- **S06:** [NIST SP 800-218 SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) — secure lifecycle, requirements/design-decision tracking, provenance, vulnerability response.
- **S07:** [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — Govern/Map/Measure/Manage lifecycle; revision activity means recheck.
- **S08:** [NIST Privacy Framework](https://www.nist.gov/privacy-framework) — privacy risk management.
- **S09:** [Kentucky AG KCDPA guidance](https://www.ag.ky.gov/about/Office-Divisions/ODP/KCDPA/Pages/default.aspx) — January 1, 2026 effect and covered-consumer rights/sensitive-data consent.
- **S10:** [FTC Health Breach Notification Rule basics](https://www.ftc.gov/business-guidance/resources/health-breach-notification-rule-basics-business) — possible health-app/connected-device breach duties and 2024 amendments.
- **S11:** [FDA Digital Health Policy Navigator](https://www.fda.gov/medical-devices/digital-health-center-excellence/step-3-software-function-intended-maintaining-or-encouraging-healthy-lifestyle) — function/intended-use/claims boundary.
- **S12:** [CycloneDX 1.7 specification overview](https://cyclonedx.org/specification/overview/) — component, service, ML, dependency, vulnerability and provenance BOM capabilities.
- **S13:** [SPDX 3.0.1 specification](https://spdx.dev/use/specifications/) — code/model/dataset/license/provenance bill-of-materials vocabulary.
- **S14:** [SLSA 1.2 provenance](https://slsa.dev/spec/v1.2/provenance) — current approved build/source provenance concepts.
- **S15:** [Godot 4.7 Window](https://docs.godotengine.org/en/4.7/classes/class_window.html) — adopted bounded-window implementation surface.
- **S16:** [Godot Engine license](https://godotengine.org/license/) and live evidence E37 (exact 4.7.2 release) — engine rights and pinning; artifact verification remains open.

## End-goal pillar crosswalk

| Exact pillar | Architecture/slice/experiment linkage | Exact adopted/interim authority | Primary risks / unresolved contract | Environment and external support |
|---|---|---|---|---|
| **Persistent individual** | companion-core single writer; append-only events and deterministic projections; slice restart/replay/restore | ADR-04 **Use a hybrid persistent-organism architecture as the working direction — Interim**; ADR-05 **Do not allow a language model to own canonical identity, state, memory, or safety authority — Interim**; ADR-08 **Use append-only evidence with typed, temporal, versioned derived memories — Interim**; ADR-14 **Require local survival and owner-portable creature continuity — Interim** | RISK-05 **False or corrupted autobiographical memory**; RISK-08 **Cloud, subscription, vendor, model, or service shutdown**; RQ-09/RQ-11 open | Local ext4/NVMe available; SSHFS excluded. S02–S04. |
| **Autonomous life** | deterministic organism/world/arbitration modules; real two-drive slice; later organism experiments | ADR-04 Interim; ADR-06 **Maintain distinct homeostatic drives with explicit arbitration — Interim**; ADR-07 **Implement baby-like growth through developmental capability gates over safe pretrained priors — Interim** | RISK-10 **Runtime latency, heat, power, noise, or instability breaks continuous aliveness**; RISK-11 **Developmental gates produce either a fake infant or an unsafe/incompetent system**; RQ-04 open | Host CPU/RAM observed, concurrent capacity unknown; EXP-06/11. |
| **Embodied aliveness** | Godot-only adapter, body-neutral intents, bounded-window tests, MON_FRAME_V1 slice subset | ADR-13 **Make embodiment an engine-neutral adapter driven by causal intents — Interim**; ADR-23/25/27/28/29/36/37 Adopted; ADR-24 Godot 4.7.2 Interim; ADR-26 MON_FRAME_V1 Interim | RISK-10; RQ-04 open; production visual construction unfinished | Dedicated 1366×768 Openbox output, OpenGL observed, Vulkan/Godot 4.7.2 unknown. S15–S16; EXP-01–03. |
| **Grounded interaction** | sensor gateway emits uncertain evidence; model proposals bounded; real media absent slice | ADR-11 **Require perception systems to emit uncertain evidence rather than durable beliefs — Interim**; ADR-12 **Treat affect as a contextual hypothesis, never a directly observed fact or sole safety trigger — Adopted** | RISK-03 **Biometric misidentification or spoofing**; RISK-07 **Prompt injection or poisoned teaching through speech, screens, visitors, media, or demonstrations**; RQ-08 open | UVC/audio metadata observed; quality/latency/sharing unknown; EXP-07/08. |
| **Development and teaching** | versioned skill/development lifecycle, evidence-backed promotions/revocation; no online weights | ADR-07 Interim; ADR-10 **Prohibit uncontrolled online foundation-model weight updates in the first implementation — Interim** | RISK-07; RISK-11; RQ-07/RQ-08 open | Model/data choices deferred; live evidence E04 supports grounded teaching only as research. |
| **Memory and dreaming** | typed temporal projections, correction/abstention, synthetic namespace, false-promotion negative test | ADR-08 Interim; ADR-09 **Treat dreaming as governed offline consolidation, not factual experience — Adopted** | RISK-05; RQ-09 open | Local storage available, substrate unqualified; S03–S04; EXP-04/10. |
| **Caregiving utility** | separate care-core, deterministic named policy, incident/ack states, synthetic shadow-help path | ADR-03 **Keep the caregiving safety core architecturally independent from the companion — Adopted**; ADR-15 **Qualify named safety scenarios instead of building a generalized danger detector — Adopted**; ADR-35 **Use explicit spoken help request as the first caregiving scenario in Kentucky, United States — Adopted** | RISK-01 **Missed qualified emergency or distress event**; RISK-02 **False safety escalation and alarm fatigue**; RISK-13 **Check-in interaction is inaccessible to a user in distress or with disability**; RQ-08/RQ-10 open | Audio capability only metadata; S09–S11; EXP-08; live delivery prohibited. |
| **Privacy and security** | trust zones, one-writer stores, no default network, ephemeral media, future vault, consumer-rights seams | ADR-03/05/11/12/14/34 Adopted or Interim as stated; ADR-33 adult/single-owner Adopted | RISK-03; RISK-04 **Private camera, microphone, memory, or safety data exposure**; RISK-07; RISK-09 **Code, model, dataset, voice, asset, or plugin rights are incompatible**; RQ-07/RQ-09/RQ-10 | S02, S05–S10, S12–S14. |
| **Continuity and ownership** | local core, versioned export/backup/restore, adapter replacement, signed/staged update/rollback | ADR-14 Interim; ADR-27 Adopted; ADR-34 Adopted | RISK-08; RISK-14 **Model or software update silently changes qualified behavior**; RQ-09/RQ-11 | Local ext4/NVMe; recovery/systemd unknown. S03–S06, S12–S14; EXP-04/05/10/12. |
| **Human outcome** | healthy-disengagement requirements, accessible alternatives, claims evidence matrix, longitudinal later gate | ADR-12 Adopted; ADR-15 Adopted; ADR-33/34 Adopted | RISK-06 **Companion behavior creates unhealthy dependence, exclusivity, guilt, or social withdrawal**; RISK-13; RQ-07/RQ-08/RQ-11 | No human outcome is implemented or proven; Research E26–E28; Roadmap Phase 14. |

## Roadmap Phase 00–15 crosswalk

| Exact phase | This packet's durable contribution / future handoff | Key authority and risk linkage |
|---|---|---|
| **Phase 00 — Planning and product contract** | Options, recommendation, boundaries, RQ dispositions, first-slice contract, experiment/dependency/release plan | ADR-31/32 Adopted; RISK-12; all remaining RQs |
| **Phase 01 — Environment and engineering foundation** | Proposed module tree, exact Godot/store/supervisor entry experiments, clean-clone/CI contract | ADR-18 Adopted, ADR-21 Interim, ADR-22/23 Adopted, ADR-24 Interim; RISK-09/10/12/14 |
| **Phase 02 — Mon body, habitat, and sprite pipeline** | Godot-body boundary, MON_FRAME_V1, bounded-window and asset-rights gates | ADR-13/24/26 Interim, ADR-25/27–29/36/37 Adopted; RISK-10 |
| **Phase 03 — Organism kernel and autonomous life** | core component ownership, two-drive slice, deterministic replay | ADR-04/06 Interim; RISK-10/11 |
| **Phase 04 — Evidence, world model, and persistent memory** | evidence-before-belief, typed events/projections, SQLite candidate tests | ADR-05/08/11 Interim; RISK-05; RQ-09 |
| **Phase 05 — Speech presence and dialogue** | sensor/model interface and RQ-08 gate; no candidate approved | ADR-05/11 Interim; RISK-07/10/13; RQ-08 |
| **Phase 06 — Vision, identity, and social attention** | sensor gateway, future vault, unknown identity, no biometric first slice | ADR-11 Interim, ADR-12 Adopted; RISK-03/04/07; RQ-07 |
| **Phase 07 — Teaching, learning, and development** | versioned reversible skills and developmental promotion authority | ADR-07/10 Interim; RISK-07/11 |
| **Phase 08 — Sleep, dreaming, and lifelong consolidation** | synthetic namespace and factual-promotion prohibition | ADR-09 Adopted; RISK-05 |
| **Phase 09 — Personality, relationship, and rich daily life** | single-primary role default, relationship state in companion core, human-outcome controls | ADR-08 Interim, ADR-33 Adopted; RISK-06; RQ-07 |
| **Phase 10 — Caretaking core foundation** | independent care process/store, signed deterministic policy, shadow incident slice | ADR-03/15/35 Adopted; RISK-01/02/13; RQ-08/RQ-10 |
| **Phase 11 — Security, privacy, resilience, and owner continuity** | trust zones, vault seam, rights/BOM, update/migration/backup/restore, egress deny | ADR-14 Interim, ADR-34 Adopted; RISK-03/04/07/08/09/14; RQ-09/11 |
| **Phase 12 — Routine learning and qualified escalation** | policy/event interfaces preserve later scenario expansion; explicit-help remains first | ADR-15/35 Adopted; RISK-01/02/13; RQ-10 |
| **Phase 13 — Integrated alpha and content scale** | process topology, bounded queues, pack partitioning and full integration evidence shape | ADR-26 Interim, ADR-27 Adopted; RISK-10/12/14 |
| **Phase 14 — Longitudinal pilot and human validation** | preregistered claims, accessibility, dependence/healthy-disengagement, shadow metrics | ADR-15/33/34/35 Adopted; RISK-01/02/06/13 |
| **Phase 15 — Release qualification and operational launch** | signed release, SBOM/provenance, clean restore/rollback, counsel/claims gates | ADR-14 Interim, ADR-34 Adopted; RISK-08/09/14; RQ-09/10/11/12 |

## Semantic validation

- All 37 ADR rows were enumerated from the live ledger; every ADR cited above was compared to its exact title, status, rationale, consequence, and relationship.
- All 14 risk rows were read from the live risk register; each cited risk directly names the failure controlled by its associated architecture element.
- All open/partial RQs use their exact live title/status and are not marked resolved.
- The 10 exact end-goal pillars and all 16 exact roadmap phases appear once in the crosswalk.
- Accepted environment observations are never promoted into capacity claims; missing utilities are not missing capabilities.
- S01–S16 are current primary sources. They support standards/platform/legal design constraints, not runtime capability or legal conclusions.
