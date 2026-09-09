# COMPANION-P00-ARCH-001 — Authority Context Acknowledgment

Status: `COMPLETED — GATE PASSED; ARCHITECTURE SYNTHESIS AUTHORIZED BY PREFLIGHT`

## 1. Retrieval confidence

- Confidence: `ADEQUATE`
- Retrieval completed at: `2026-09-09T10:04:24-04:00`
- Current local `HEAD`: `6559cec1beaf27bf958c2b9517b0717f04c83ea9`
- Current `origin/main`: `6559cec1beaf27bf958c2b9517b0717f04c83ea9`
- GitHub Issue #3 state: `OPEN`
- Material unavailable/truncated sources: `NONE`

Every required Notion fetch reported complete page content; the two ledgers were queried in faithful rows mode and returned `has_more=false`.

## 2. Mandatory live-source verification

| Authority | Status | Retrieved marker | Material change from bridge |
|---|---|---|---|
| Canonical project | PASSED | `2026-09-09T13:11:42.620Z` | None |
| Complete operational end goal | PASSED | `2026-09-08T19:03:28.691Z` | None |
| Master roadmap | PASSED | `2026-09-09T13:12:24.145Z` | None |
| Single-source-of-truth governance contract | PASSED | `2026-09-09T12:03:12.606Z` | None |
| Operator Decision Packet 01 | PASSED | `2026-09-09T11:47:59.205Z` | None |
| Open Decisions and Research Gaps | PASSED | `2026-09-09T11:42:06.728Z` | None |
| R05 — Caretaking Safety Core | PASSED | `2026-09-09T11:29:39.778Z` | None |
| R06 — Privacy, Security, Compliance, and Resilience | PASSED | `2026-09-09T11:29:57.271Z` | None |
| R10 — Godot Sprite Embodiment and Asset Production Contract | PASSED | `2026-09-09T11:42:55.100Z` | None |
| Mon Visual Design Bible V1 | PASSED | `2026-09-09T07:31:51.863Z`; both images directly inspected | None |
| Accepted Linux environment review | PASSED | `2026-09-09T10:39:34.626Z` | None |
| Active Architecture directive | PASSED | parent `2026-09-09T13:10:24.930Z`; full `2026-09-09T13:10:37.794Z` | None |
| Required Coder Architecture Report | PASSED | `2026-09-09T13:10:49.306Z` | Pending template as expected |
| Architecture Decision Ledger and ADR-33 through ADR-37 | PASSED | 37 rows; `has_more=false` | Live count is 37: 21 adopted, 14 interim, 2 rejected |
| Research Evidence Register and current totals | PASSED | 46 rows; `has_more=false` | Live count is 46: 33 Grade A, 11 Grade B, 2 Grade C |
| GitHub Issue #3 | PASSED | live issue and all three comments fetched; open | None |
| Repository root, `AGENTS.md`, Authority skill, current state, and Git status | PASSED | `HEAD=origin/main=6559cec...`; clean; only root `AGENTS.md` applies | None |

## 3. Exact adopted decision acknowledgment

| Decision | Exact live title and status | Codex interpretation | Source verified |
|---|---|---|---|
| ADR-33 | **Target one adult primary user with support needs in a single-primary-user household model for iteration one — Adopted** | One adult 18+ is the primary user and authority. Configured trusted caregivers/contacts have explicit limited roles; unknown visitors get limited context. Minors and co-equal owners are out of scope. | PASSED |
| ADR-34 | **Develop toward a consumer product from the start under a narrow non-medical companion and trusted-contact assistance claim — Adopted** | Security, privacy, recovery, rights, quality, and evidence are product foundations, while diagnosis, guaranteed detection, prevention-of-harm, medical monitoring, and emergency-service replacement claims remain prohibited. | PASSED |
| ADR-35 | **Use explicit spoken help request as the first caregiving scenario in Kentucky, United States — Adopted** | The first scenario begins with explicit speech and is governed for Kentucky; qualification progresses through simulation, recorded replay, and shadow mode. Live contact delivery is separately gated. | PASSED |
| ADR-36 | **Use the separate 1366×768 Openbox output as the iteration-one mon display — Adopted** | The dedicated Openbox-managed display is the target, but placement, focus, scaling, display removal, and recovery still require target-host qualification. | PASSED |
| ADR-37 | **Use a bounded resizable Godot habitat window on the dedicated Openbox display — Adopted** | The default is a normal bounded resizable window, not fullscreen or overlay. Initial/min/max geometry, aspect/scaling, focus, persistence, and display-loss behavior are architecture/test work. | PASSED |

## 4. Foundational invariant acknowledgment

1. **Ground zero.** ADR-01 prohibits importing prior-project substance by default; only current Companion authority and fresh evidence govern.
2. **Split authority.** ADR-02 and the governance contract make Notion authoritative for project meaning/status, while GitHub holds versioned artifacts and technical evidence; both must reconcile.
3. **Persistent organism, bounded models.** ADR-04 and ADR-05 separate canonical organism state, memory, control, and safety from any language model. Models can propose typed outputs but cannot own truth or authority.
4. **Uncertain perception.** ADR-11 requires timestamped, source- and quality-bearing evidence. Sensor/model output never mutates durable belief directly.
5. **Typed memory.** ADR-08 requires temporal, versioned, correction-aware memory classes and explicit abstention when evidence is inadequate.
6. **Dream/fact separation.** ADR-09 makes synthetic dream material hypothetical unless a governed promotion links it to real evidence.
7. **Renderer isolation.** ADR-13 and ADR-27 make Godot an engine-neutral embodiment adapter. Renderer crash, replacement, or asset reload must not corrupt organism, memory, consent, or safety state.
8. **Safety independence.** ADR-03 and ADR-15 require a separate, deterministic-at-policy, auditable caregiving authority operating on named scenarios, never companion mood or improvisation.
9. **Continuity.** ADR-14 requires local survival and owner-portable identity/state/memory/policy with export, backup, restore, and vendor-replacement seams.
10. **Artifact-specific rights.** ADR-17 and RISK-09 require separate provenance and rights review for code, models, weights, datasets, voices, assets, plugins, and services.
11. **Consumer foundation.** ADR-34 makes security, privacy, recovery, controlled updates, observability, consumer rights, and evidence Phase-01 foundations, not release cleanup.

## 5. Approved mon and embodiment acknowledgment

The identity master and six-view turnaround were directly inspected. The canonical mon is an original purple, simple-bodied 2D character with an edge-spiked flame-like head, black eye fields with white pupils, simple mouth, two fingers plus one thumb on each hand, three toes on each foot, simple anatomy, and flat cel shading. The turnaround fixes front, back, left, right, top, and bottom identity-defining silhouettes. Identity master: native `1254×1254 RGBA`, SHA-256 `86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56`. Turnaround: native `1448×1086 RGB`, SHA-256 `3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4`.

`MON_FRAME_V1` uses a `1024×1024 RGBA` source canvas, root `(512,896)`, 24 Hz timing grid, fixed naming, landmarks, transition metadata, layered overlays, partitioned packs, and build-time trimming. Godot `4.7.2` is the selected baseline; installed Godot `4.6` is not an approved substitute. The target is the adopted 1366×768 Openbox display in a bounded resizable window. Unresolved work includes normalized transparent production frames, pose/expression/construction sheets, exact clip/transition coverage, window sizing/scaling/focus/recovery behavior, and all runtime quality/performance tests.

## 6. Accepted environment and explicit unknowns

### Accepted observations

- Ubuntu 24.04.5, x86_64/X11, Ryzen 7 5800XT (8C/16T), about 67.3 GB RAM.
- NVIDIA GTX 1660 SUPER and RTX 3050 6 GB, driver 595.84, direct OpenGL 4.6.
- Three outputs across two X screens; the separate 1366×768 Openbox display is adopted.
- A UVC webcam exposes metadata; PipeWire/WirePlumber and ALSA enumerate a USB mono microphone and HDMI stereo output.
- The repository checkout is SSHFS. Local ext4/NVMe storage exists for later runtime state.
- Godot 4.6 is present; selected Godot 4.7.2 is absent.
- System and user systemd state was degraded during inventory.

### Not established

- Godot 4.7.2 availability, artifact authenticity, or host behavior.
- Vulkan availability or correct GPU/device selection because `vulkaninfo` was absent.
- Camera image quality, latency, frame delivery, privacy indicator behavior, or sharing/contention.
- Microphone intelligibility, latency, echo cancellation, media/replay resistance, VAD/ASR performance, or barge-in.
- Concurrent workload headroom or safe model size.
- User-service startup, watchdog, suspend/resume, crash-loop, or recovery behavior.
- Sustained power, thermal, fan-noise, storage-growth, or endurance behavior.

Canonical live state, databases, WALs, sockets, and locks must not be placed on the SSHFS repository checkout. Use a local filesystem and XDG locations after implementation is authorized.

## 7. Remaining product-contract records

| RQ | Exact title/status | Unresolved consequence | Proposed disposition type only |
|---|---|---|---|
| RQ-04 | **Offline, cloud, compute, power, noise, and cost boundary — OPEN** | Determines model sizes, service/network boundaries, recurring cost, privacy, latency, graceful degradation, and hardware sufficiency. | RESEARCH/EXPERIMENT REQUIRED |
| RQ-07 | **Multi-user identity, ownership, and relationship model — OPEN** | Requires roles, enrollment, visitor behavior, private/shared memory, caregiver permissions, and authority rules beyond the adopted single-primary model. | OPERATOR RULING REQUIRED |
| RQ-08 | **Voice, languages, wake word, and interruption model — OPEN** | Determines languages, accessibility, voice rights, latency, far-field coverage, wake-word need, echo cancellation, and barge-in. | OPERATOR RULING REQUIRED |
| RQ-09 | **Memory retention, export, backup, and deletion promises — OPEN** | Determines storage scale, raw-media rules, deletion semantics, backup ownership, RPO/RTO, and continuity obligations. | OPERATOR RULING REQUIRED |
| RQ-10 | **Notification and trusted-contact transport — OPEN** | Determines channel/vendor, acknowledgment, retries, idempotency, outage behavior, cost, and continuity. | DEFER WITH SAFE BOUNDED DEFAULT |
| RQ-11 | **Support lifetime and continuity promise — OPEN** | Determines support/update term, end-of-service migration, key recovery, replacement body, and backup promises. | OPERATOR RULING REQUIRED |
| RQ-12 | **Canonical product name — PARTIALLY RESOLVED** | Repository `SketchOTP/companion` is fixed; public/product name needs originality and trademark screening. | DEFER WITH SAFE BOUNDED DEFAULT |

No row is resolved by this acknowledgment.

## 8. Active objective in Codex's own words

This directive must turn accepted product, research, host, visual, safety, and governance facts into a decision-ready Architecture v1.0 proposal: credible topology alternatives, one recommended component/process design, single owners for every authority/state class, typed interfaces and data paths, privacy/threat/claims controls, dependency and rights dispositions, recovery/update/test/release plans, and a bounded experiment queue. It is the critical path because Phase 01 cannot safely initialize around assumed process, persistence, device, or claims boundaries.

A meaningful first vertical slice is a restartable, user-visible closed loop spanning simulated evidence, deterministic organism change, durable event/memory handling, body-neutral intent, a real Godot adapter on the adopted display, and a simulated spoken-help incident through an independently governed safety policy and stub notification acknowledgment. It is not a static window or chatbot. The Architect must independently review and adopt, revise, or reject the package before Phase 01 or product work opens.

## 9. Hard-prohibition acknowledgment

This directive does **not** authorize Godot installation or execution; Godot 4.6 substitution; product/Godot source or sprite production; dependencies, manifests, CI workflows, deployment, database implementation, models, datasets, voices, or media capture/playback; benchmarks or host changes; biometric enrollment, notification integration, or safety runtime; architecture self-approval; Phase 01; or any product-capability claim.

## 10. Contradictions, stale records, and changes

- Material contradiction found: `NONE`
- Stale snapshot found: previous 32-ADR/44-evidence onboarding counts are historical, not current; the live ledgers contain 37/46.
- Live count changes: `ADR 37 = 21 adopted, 14 interim, 2 rejected; evidence 46 = 33 A, 11 B, 2 C; review states 33 Reviewed, 12 Candidate, 1 Needs Deep Review.`
- Required Architect clarification: `NONE TO COMPLETE THIS PLANNING DIRECTIVE`; remaining operator choices are explicitly dispositioned, not assumed.

## 11. Gate result

- Mandatory sources verified: `PASSED`
- ADR-33 through ADR-37 semantics verified: `PASSED`
- Foundational invariants understood: `PASSED`
- Environment limits understood: `PASSED`
- Remaining RQs understood: `PASSED`
- Hard boundary understood: `PASSED`
- Retrieval confidence: `ADEQUATE`
- Architecture synthesis authorized by this preflight: `YES`

This preflight authorizes Codex to produce the requested proposal only. It is not Architect acceptance of Architecture v1.0.
