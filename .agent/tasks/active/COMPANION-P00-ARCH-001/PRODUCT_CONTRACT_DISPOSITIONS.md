# Product-Contract Dispositions

Status: `COMPLETE — PROPOSED DISPOSITIONS; NO RQ RESOLVED`

| RQ — exact live title/status | Proposed disposition | Why unresolved / needed authority | Safe bounded default for Phase 01/02 |
|---|---|---|---|
| **RQ-04 — Offline, cloud, compute, power, noise, and cost boundary — OPEN** | **RESEARCH/EXPERIMENT REQUIRED**, then operator ruling | The accepted host inventory cannot prove concurrent capacity or acceptable household cost/power/noise. Privacy, recurring cost, and cloud tolerance are operator product choices. | Build a local-only core and disabled replaceable cloud adapter. No selected model size, cloud dependency, workload-capacity claim, or final hardware inference. Run EXP-02/06/09/11. |
| **RQ-07 — Multi-user identity, ownership, and relationship model — OPEN** | **OPERATOR RULING REQUIRED** | ADR-33 fixes one primary adult plus configured caregivers/contacts and unknown visitors, but not caregiver access, visitor memory, shared/private memories, delegation, transfer, dispute, or recovery authority. | One primary owner authority; no minor enrollment; no co-equal owner; unknown visitors have no durable personal memory; caregivers have no general memory access. Implement roles only after a signed matrix. |
| **RQ-08 — Voice, languages, wake word, and interruption model — OPEN** | **OPERATOR RULING REQUIRED**, followed by research/experiment | Required languages, voice identity/rights, wake word, far-field use, accessibility, interruption expectations, and latency are product experience choices. | First slice has no real audio/voice/model. Use synthetic schema fixtures. Do not select VAD/ASR/TTS/KWS or claim speech coverage until decisions and EXP-08. |
| **RQ-09 — Memory retention, export, backup, and deletion promises — OPEN** | **OPERATOR RULING REQUIRED**, informed by storage/restore experiments and counsel | Lifetime, raw-media policy, deletion across derived/backups/audit, owner custody, RPO/RTO, and exceptions define trust and architecture. | No raw-media retention. Keep test fixtures synthetic. Design typed provenance/correction/deletion tombstone/export seams; set no public lifetime/RPO/RTO promise. Run EXP-04/10. |
| **RQ-10 — Notification and trusted-contact transport — OPEN** | **DEFER WITH SAFE BOUNDED DEFAULT** | Channel, recipient devices, jurisdiction, vendor, cost, acknowledgment, retries and outage behavior require operator selection and legal/security evaluation. | Deterministic offline stub only; no credentials, contacts, SDK, network, or delivery. Maintain separate `provider_accepted`, `delivered`, and `acknowledged` states. |
| **RQ-11 — Support lifetime and continuity promise — OPEN** | **OPERATOR RULING REQUIRED**, informed by restoration and business analysis | Creature lifespan, update/support duration, end-of-service, key recovery, replacement body and vendor obligations cannot be inferred technically. | Local portable versioned format and replaceable adapters from day one; no “forever” promise. EXP-10 proves a bounded restore mechanism, not a commercial support term. |
| **RQ-12 — Canonical product name — PARTIALLY RESOLVED 2026-09-08** | **DEFER WITH SAFE BOUNDED DEFAULT** | Repository `SketchOTP/companion` is fixed; public name needs originality/trademark and claims review. | Use “Companion” or the canonical descriptive title only as internal working labels; do not create release branding, domains, user-facing marks, or trademark claims. |

## Proposed operator questions after evidence narrows the space

1. RQ-07: exact caregiver capabilities; private/shared memory; authority transfer/recovery; visitor retention.
2. RQ-08: languages and accessibility modes; wake-word versus explicit control; interrupt/barge-in expectations; acceptable synthetic/licensed voice direction.
3. RQ-09: no-raw-media default confirmation; owner deletion/export scope; backup custody; target RPO/RTO; audit/legal exceptions.
4. RQ-11: minimum supported lifetime, offline grace/end-of-service, update cadence, key escrow/recovery, replacement-body promise.
5. RQ-04 only after resource evidence: acceptable cloud use/data classes, recurring cost, household power/noise, and graceful-degradation requirements.
6. RQ-10 only before live safety work: preferred recipient channel and definition of acknowledged assistance.

The Architect—not this packet—records any resulting resolution in Notion and a new adopted ADR.
