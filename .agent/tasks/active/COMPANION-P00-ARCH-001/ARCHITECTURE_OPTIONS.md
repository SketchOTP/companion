# Architecture Options

Status: `COMPLETE — PROPOSAL FOR ARCHITECT REVIEW`

## Evaluation frame

Both viable options preserve ADR-03, ADR-05, ADR-11, ADR-14, ADR-27, and ADR-34: a persistent non-LLM organism; evidence before belief; Godot as presentation only; a separate deterministic caregiving authority; local survival; and consumer-product controls from the foundation. Neither topology authorizes a dependency or proves target-host capacity.

| Criterion | Option A — cohesive core with isolated edges | Option B — fully decomposed local services |
|---|---|---|
| Shape | One transactional companion-core process owns organism, world, evidence ledger, memory projections, and learning lifecycle. Separate sensor, model, Godot, safety, notification-stub, and operations processes. | Separate world, organism, evidence, episodic memory, semantic memory, learning, planner, language, sensor, Godot, safety, audit, and operations services. |
| Authority | Few state owners; mutations cross one companion-core command boundary. Safety still has an independent owner and store. | Narrow owners per domain, but cross-domain workflows require distributed coordination and more authority arbitration. |
| Fault isolation | Untrusted/volatile edges and safety are isolated. A core crash pauses ordinary companion behavior but leaves its last committed state and safety process intact. | Maximum process isolation; individual noncritical services may restart independently. |
| Data consistency | Local ACID transactions can append evidence and advance derived projections atomically. | Requires sagas, idempotency, outbox/inbox, reconciliation, and eventual-consistency rules from day one. |
| IPC | Versioned JSON Schema envelopes over local Unix-domain sockets; low interface count. | Same protocol possible, but substantially more sockets, compatibility matrices, retries, and observability. |
| Deployment | Small user-service graph; viable on the accepted workstation after qualification. | Larger service graph, ordering, health, and upgrade surface; degraded systemd state is a larger blocker. |
| Security | Sensor/device and model processes have narrowly scoped privileges. Core remains high-trust but has no device or network access. | Narrowest theoretical privileges, offset by more interfaces and credential/authorization policy. |
| Observability | One canonical event sequence plus per-process structured logs and health. | Rich service-level visibility, but distributed correlation and partial-failure diagnosis are harder. |
| Recovery/update | One core schema/migration boundary plus separate safety store; staged adapter replacement. | Independent updates are possible, but mixed-version operation and rollback need extensive compatibility orchestration. |
| Testability | Deterministic core can be tested in-process; adapters use contract/replay tests; integrated slice remains manageable. | Strong unit isolation, but end-to-end and failure-state matrix grows sharply. |
| Resource use | Fewer runtimes, queues, duplicated caches, and DB connections. | More processes, serialization, duplicated working sets, supervision, and storage churn. |
| Migration | Component APIs preserve a later split when measurement justifies it. | Easy to scale components separately, but premature for one local host and one user. |
| Main failure mode | Core becomes too broad or accidentally absorbs model/safety/device authority. Prevent with explicit internal modules and capability tests. | Distributed complexity creates inconsistent personal state, message loss/duplication, and operational fragility before value is proven. |

## Recommendation

Recommend **Option A: cohesive transactional companion core with isolated privilege and failure domains**. It creates real separation where consequence demands it—caregiving policy/audit, sensors, models, renderer, external transport, and operations—while keeping mutually dependent organism and memory mutations under one serializable command/event authority. This is the smallest topology that satisfies the adopted constraints without inventing a distributed system.

Option B remains a credible migration target if experiments show one of these review triggers:

- a component must restart or upgrade independently to meet a measured safety or availability objective;
- a workload requires different hardware or resource scheduling;
- privilege analysis shows the cohesive core cannot be acceptably confined;
- database contention or release cadence cannot be controlled inside Option A;
- a second device or multi-owner deployment is adopted.

## Rejected alternatives

| Alternative | Disposition | Reason |
|---|---|---|
| Monolithic Godot application owns creature, memory, sensors, and safety | Rejected | Contradicts ADR-03 and ADR-27; renderer failure or asset reload could corrupt continuity or suppress safety. |
| LLM/persona as the creature | Rejected by ADR-19 | Cannot own durable truth, physiology, temporal identity, or deterministic safety. |
| Behavior-tree-only organism | Rejected by ADR-20 | Cannot alone provide developmental memory and durable individual continuity. |
| End-to-end RL-only organism | Rejected by ADR-20 | Uncontrolled learning, weak attribution/rollback, and unsafe data requirements. |
| Cloud control plane as canonical owner | Rejected for v1.0 | Conflicts with ADR-14 local survival and leaves RQ-04 unresolved. Optional cloud augmentation may later receive only scoped, minimized requests. |
| Shared database written by every process | Rejected | Duplicate authority, unsafe schema coupling, untestable privilege, and cross-process write races. Each store has one writer/owner. |

## Evidence basis

- Live ADRs 03–17, 19–21, 27, 33–37 and RISK-04, RISK-05, RISK-07, RISK-08, RISK-10, RISK-12, RISK-14.
- CoALA and Generative Agents support modular memory/action/planning, but do not validate this product.
- SQLite WAL permits concurrent readers and one writer on one host, but not network filesystems; its 2026 WAL-reset fix makes exact embedded-version verification mandatory.
- XDG Base Directory 0.8 requires local, private runtime directories suitable for Unix sockets.
- systemd supports restart/watchdog and service sandbox controls; the accepted host's degraded service state means these remain experiment-gated.

No option is adopted by this document.
