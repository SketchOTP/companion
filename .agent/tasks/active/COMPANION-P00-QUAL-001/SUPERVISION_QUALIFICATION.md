# Supervision Qualification

Status: `PENDING CODEX EXECUTION`

## Manager diagnosis

Record sanitized system/user manager state, relevant failed-unit classification, whether failures are Companion-relevant, and commands used. Do not expose unrelated private service details or repair anything.

## Transient synthetic probe

When safe, record transient user-service start/stop, child exit detection, bounded restart/backoff, crash-loop visibility, environment isolation, status collection, cleanup, and all failures. Do not install persistent units.

## Comparator

Compare systemd user supervision with a minimal direct qualification supervisor at the evidence level only.

## Disposition

Recommend a Phase 01 experiment direction or return `BLOCKED`. Do not adopt or install a production supervisor.
