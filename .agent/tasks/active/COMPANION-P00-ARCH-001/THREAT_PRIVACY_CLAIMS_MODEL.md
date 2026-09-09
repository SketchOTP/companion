# Threat, Privacy, and Claims Model

Status: `COMPLETE — PRELIMINARY; COUNSEL AND TARGET TESTING REQUIRED`

This is an engineering threat/claims model, not legal advice. It applies the adopted adult/Kentucky/nonmedical scope and preserves uncertainty about statutory applicability.

## Protected assets and actors

Assets: creature identity and autobiographical memory; household audio/video evidence; routines, relationships, preferences, health-like and distress information; consent; biometric templates; trusted contacts and credentials; incident policy/audit; update/signing material; availability and recovery.

Actors: primary adult owner/user; configured caregiver/contact; unknown visitor; malicious visitor/co-resident; remote attacker; compromised dependency/model/service; provider/operator insider; accidental media source; faulty sensor/model; maintenance agent; lost/stolen backup.

Trust zones and single owners are defined in `PROCESS_PRIVILEGE_DATA_BOUNDARIES.md`. Ambient media, memory, incidents, biometrics, contacts, and secrets are high-sensitivity data; synthetic model/dream output is untrusted.

## Priority abuse/misuse cases

| Threat | Consequence | Required control | Required evidence |
|---|---|---|---|
| Spoofed/replayed help phrase from TV, phone, recording, adversary, or generated voice | false escalation, alarm fatigue | source/quality/replay metadata; bounded confirmation; accessible fallback; incident dedupe; never voice alone for identity; shadow mode | representative replay/media/adversarial matrix; false alerts/user-day; trace review |
| Missed spoken help due to noise, distance, accent, atypical speech, outage, or disability | delayed help | visible coverage state; multiple accessible response paths; retry/timeout; explicit limitations; no silence=danger assumption | target-population accessibility and degraded-audio tests; sensitivity/latency by condition |
| Companion mood/model prose triggers care | unsafe authority coupling | care accepts only versioned policy inputs from allowed producers; reject free-form text/mood | capability and negative contract tests |
| Visitor teaches poison/prompt injection through speech/screen/demo | data exfiltration or behavioral corruption | provenance, role/consent checks, typed tools, reversible skill lifecycle, model sandbox, no direct store/tool authority | multimodal adversarial suite and rollback proof |
| Biometric false match/spoof | cross-person memory/contact leak | no biometrics in first slice; later explicit enrollment, unknown result, quality/liveness, vault, no sole safety authority | target-camera demographic/condition/spoof validation and legal review |
| Raw media or memory leaks through logs/cloud/support | severe privacy harm | ephemeral raw media; payload-free logs; default no network; data minimization; user-initiated scoped diagnostics; access audit | data-flow inspection, egress test, log scan, penetration test |
| Unauthorized deletion/export/contact change | identity loss, stalking, coercion | owner authentication, role matrix, step-up confirmation, recovery delay where appropriate, immutable audit | abuse-case tests, recovery and appeal workflow |
| Malicious/buggy update or dependency | silent behavior/safety regression | signed artifacts, separate BOMs, provenance, staged update, compatibility gates, rollback, policy/model review | clean build, signature, SBOM, regression/canary/rollback evidence |
| Corrupt memory or synthetic dream promoted as fact | relationship harm | append-only evidence, temporal correction, source linkage, synthetic namespace, abstention | contradiction/false-memory/crash/migration tests |
| Vendor/cloud shutdown | creature loss | local survival, portable versioned export, replacement adapters/body | offline test and replacement restore |
| Repeated crash/watchdog loop | unavailable or misleading system | bounded backoff, failure latch, visible degraded coverage, last-known-good rollback | service fault matrix and operational alert proof |
| Caregiver overreach/coercion | autonomy/privacy loss | explicit limited roles, per-purpose access, private/shared memory policy, owner-visible audit/revocation | operator ruling on RQ-07 and user research |

## Consent and data lifecycle

- Ambient sensing is off until an explicit purpose, role, indicator, retention rule, and accessible pause/delete path exist.
- Consent is versioned and purpose-specific; absence/expiry revokes acquisition, not merely downstream use.
- Unknown visitors are not enrolled and receive limited context. Minors are excluded from iteration one; discovery of minor-directed use triggers immediate product/legal review.
- Raw media is ephemeral by default. Retention requires a separate adopted policy; derived evidence retains source/model/version/quality without silently preserving raw content.
- Correction appends a superseding version; it does not erase audit. User deletion must define whether the request removes source data, derived memories, backups, and incident/legal records and must expose exceptions.
- Export/backup must be owner-controlled, encrypted, manifest-driven, and restorable. Key recovery cannot rely solely on the vendor.
- Every third-party/model/service flow needs purpose, fields, region, retention, training-use prohibition, subprocessors, deletion, incident, and shutdown analysis before approval.

## Kentucky and federal implications

The Kentucky Consumer Data Protection Act took effect January 1, 2026 and provides covered consumers access, correction, deletion, portability, opt-out, and sensitive-data consent rights. Applicability depends on thresholds/exemptions and exact data flows; the architecture should implement a data inventory and rights workflow without claiming the statute necessarily applies.

The FTC Health Breach Notification Rule may cover certain health apps, connected devices, PHR vendors/related entities and service providers; the 2024 amendments clarify coverage and unauthorized disclosure. Companion data may become health-like through check-ins, distress, routines, or integrations even under a nonmedical claim. HIPAA is not assumed merely because data is sensitive; entity/flow analysis is required.

FDA treatment is function- and intended-use-specific. The adopted narrow nonmedical companion/check-in/trusted-contact claim must stay unrelated to diagnosis, cure, mitigation, prevention, treatment, clinical monitoring, or medical management unless separately classified. Interface behavior, labeling, marketing, and technical function must remain consistent.

### Mandatory counsel/review triggers

- any Kentucky consumer pilot, paid/public distribution, or KCDPA-threshold/applicability decision;
- collection/inference of health-like, biometric, precise location, disability, routine, or distress data;
- live notification/contact delivery, emergency-services routing, or caregiver portal/access;
- children/minors, co-equal owners, employer/insurer/health-provider access, or expansion outside Kentucky;
- medical/detection/prevention/monitoring/accuracy claims;
- cloud processing, cross-border transfer, vendor training use, staff/support access, or targeted advertising/sale/profiling;
- deletion exceptions, incident retention, backup/key recovery, breach, or security incident;
- public product name/trademark and voices/assets/models/datasets with unclear commercial rights.

## Claims boundary

Permitted direction, only after evidence: “persistent digital companion with configurable check-in and trusted-contact assistance.” Even this sentence does not prove a released capability today.

Prohibited unless separately qualified/classified:

- detects/prevents emergencies, falls, self-harm, illness, or danger;
- guarantees response, delivery, acknowledgment, or safety;
- continuously medically monitors, diagnoses, treats, mitigates, or replaces clinicians/emergency services;
- knows identity, emotion, intent, consent, or distress with certainty;
- is conscious/sentient, never forgets, cannot die, or will be supported forever;
- is private/secure/offline/accessibile/bias-free without scoped evidence;
- is suitable for children or all populations.

Every future claim maps to a versioned feature, intended population/use/environment, evidence level, exclusions, degraded state, and owner. Unsupported claims fail release review.

## Spoken-help deterministic policy boundary

Candidate input must include producer, schema/policy version, timestamp/freshness, transcript or intent evidence, confidence/quality, channel health, and replay/media flags. The policy records accepted/rejected reason, attempts confirmation through configured accessible channels, avoids duplicate incidents, and separately models `detected`, `confirmed`, `queued`, `provider_accepted`, `delivered`, `acknowledged`, `failed`, `expired`, and `closed`. Companion content cannot suppress or manufacture transitions. In shadow mode no external delivery occurs.

## Degraded coverage

Loss of microphone, model, care process, policy integrity, storage, clock quality, contact configuration, or transport produces a specific visible and auditable coverage state. The system never presents normal check-in assistance while its qualifying path is unavailable. A user-accessible non-voice fallback is required before live qualification.

## Evidence gates

Threat model review; dependency and model/data/voice/asset/service rights; static and dynamic security testing; IPC/privilege penetration; egress/log privacy tests; deletion/export/restore exercises; accessible scenario testing; replay/media spoof tests; false/missed trigger estimates in shadow mode; update/rollback exercise; incident response tabletop; and product/counsel sign-off before any pilot or claim.
