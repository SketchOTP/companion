# Alpha50-003 live integration implementation

## 2026-09-15 candidate update

- Merged Architect Review 25 normally at merge commit `7d23b1f`.
- Replaced the Alpha qualification binary with a V2-only resident qualification;
  the acceptance source contains no historical `OrganismState` V1 instantiation.
- Added explicit typed V2 organism schema definitions for goals, commitments,
  memories/evidence references, and body-neutral intents, including the common
  signed-64 intent ceiling.
- Added `OrdinaryEvidenceV1` and its schema/fixture. Companion-core now exposes
  a separately addressed Unix ordinary-evidence socket with kernel peer-UID
  binding, generation/source/freshness checks, integrity digest, replay
  rejection, and durable event storage. Safety seqpacket transport remains
  independent.
- Extended the resident bridge to accept typed body intents and return an
  observed result. Companion records the result, applies V2 outcome learning,
  and snapshots state.
- Added `scripts/alpha50_live_trace.py`, which starts the checked-in companion
  and bridge services, sends an authenticated ordinary envelope, verifies the
  typed result/event path, restarts companion, and confirms a restored V2
  identity. No `ordinary-observation.json` is used.
- Added `scripts/alpha50_v2_guard.py` and workflow gates so Alpha acceptance
  fails closed if the binary regresses to V1 or if the resident trace is absent.

## Host disposition

Read-only inspection of the configured/default XDG roots found the canonical
companion authority database at `/home/sketch/.local/share/companion/data/companion.sqlite3`.
It contains only `authority_meta` and an empty `event_log`; no
`organism_snapshots` table/rows or V1 organism state were present. The database
was not modified.

## Evidence boundary

Local V2 qualification and the resident ordinary→V2→bridge-result trace pass.
The production Godot 10,000-case campaign, rich multi-class failure campaign,
care process-loss independence, and target hardware/Openbox evidence remain
unimplemented or blocked and are not claimed here.
