# Supervision Qualification

## Correction-cycle disposition

The Architect accepted the bounded transient systemd-user probes at
`E3_TARGET_TESTED`; this workstream was not rerun because host service-manager
state did not materially change. No persistent unit, restart, or host policy
was modified. The retained result is feasibility evidence only and does not
select a production supervisor.

Status: `COMPLETED — E3 TRANSIENT USER-SERVICE FEASIBILITY CHECK`

## Manager diagnosis

The user manager reported `degraded` with 20 failed units, but a sanitized name check found zero Companion-named failures. This establishes unrelated host noise as the observed explanation only; it does not identify or repair those units. `systemd --user` was available (`255`) with a user runtime directory and bus address.

Record sanitized system/user manager state, relevant failed-unit classification, whether failures are Companion-relevant, and commands used. Do not expose unrelated private service details or repair anything.

## Transient synthetic probe

No persistent unit was created. A collected transient service with a synthetic environment marker started and stopped successfully. A controlled child exit returned status `42`. A transient restart-on-failure service reported `Result=exit-code`, `NRestarts=2`, and failed active/sub states before it was stopped and reset. This establishes ordered execution, child-exit observation, bounded restart/backoff visibility, environment injection, status collection, and cleanup for the tested user-manager surface.

When safe, record transient user-service start/stop, child exit detection, bounded restart/backoff, crash-loop visibility, environment isolation, status collection, cleanup, and all failures. Do not install persistent units.

## Comparator

A minimal direct parent process observed a child exit (`23`) but provided only caller-owned lifecycle observation; it has no independently observed restart accounting, unit status, or user-manager cleanup semantics. This is an evidence comparison, not a production supervisor selection.

Compare systemd user supervision with a minimal direct qualification supervisor at the evidence level only.

## Disposition

**Recommendation to Architect: systemd user supervision is host-feasible as a later Phase 01 candidate.** The degraded user-manager state did not block transient synthetic probes and no Companion-relevant failed unit was observed. Persistent unit installation, production policy, and supervisor adoption remain unapproved.

Recommend a Phase 01 experiment direction or return `BLOCKED`. Do not adopt or install a production supervisor.
