# Qualification Results Matrix

Status: `COMPLETED — SYNTHETIC QUALIFICATION SUMMARY`

| Workstream | Candidate/configuration | Evidence level | Functional result | Security/reliability result | Rights/provenance | Recommendation | Architect decision needed |
|---|---|---|---|---|---|---|---|
| Python 3.12 | Existing CPython 3.12.3 | E3 | Frozen shell/negatives pass; median request 7.40 ms | No product/security claim | PSF stdlib; no third-party deps | Comparator only; patch-lag review required | Yes — language adoption |
| Rust stable | Isolated Rust 1.98.1 | E3 | Same digest/negatives pass; median request 1.30 ms | Static ownership model; not system proof | MIT/Apache-2.0; locked qualification crates | Recommend Rust candidate | Yes — language adoption |
| IPC weak baseline | 0600 pathname/UID/message field | E3 | Same-user valid injection accepted | Insufficient by demonstrated attack | N/A | Reject | No |
| IPC candidate 1 | Private seqpacket + generation | E3 | Valid/direct/duplicate tests pass | Bounded tests only | stdlib/Linux primitives | Candidate, superseded by C2 | Yes — mechanism adoption |
| IPC candidate 2 | C1 + generation capability + nondumpable | E3 | Valid accepted; missing capability/stale/spoof rejected | Does not cover root/full account/authorized producer | stdlib/Linux primitives | Recommend later implementation experiment | Yes |
| Godot 4.7.2 artifact | Standard Linux x86_64 | E1 | Published digest matched; `--version` exact | No renderer/display qualification | MIT; official release source | Later dependency decision candidate | Yes |
| SQLite exact build | 3.53.4 amalgamation CLI | E3 partial | Most bounded WAL/backup/fault checks pass | Commit/checkpoint kill gaps block acceptance | Public domain source; system toolchain | Blocked — more evidence | Yes |
| systemd user supervision | systemd 255 transient units | E3 | Start/stop/exit/restart visibility pass | No persistent/production policy test | system component | Candidate feasible | Yes |
| direct supervisor comparator | Parent observes child | E1 | Child exit observed | No restart/status lifecycle | stdlib | Inferior evidence surface | No |

## Phase 01 readiness

Language-neutral contracts/fixtures/XDG/logging/test controls are ready only for a later directive. Authoritative-service implementation is blocked on Architect language and IPC decisions. SQLite remains blocked on the missing deterministic commit/checkpoint fault evidence. Godot and systemd have qualification evidence but no adopted dependency/supervisor. The IPC trust and persistence gaps remain capable of forcing architecture change.

## Prohibited inference

A recommendation or bounded passing test is not production adoption, product capacity, safety efficacy, release readiness, or permission to merge/open Roadmap Phase 01.
