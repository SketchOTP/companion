# COMPANION-ALPHA50-001 implementation record

This record appends the first integrated Alpha50 implementation on top of the
accepted Phase 01 foundation and R06 embodiment boundary. It does not accept a
roadmap phase or assign an overall completion percentage.

## Implemented bounded surfaces

- `foundation_core::organism` provides typed persistent identity/epoch,
  physiology variables, competing drives, goals, commitments, body-neutral
  intents, typed memory provenance, corrections/supersession, skill outcome
  updates, deterministic consolidation, abstaining retrieval, explicit
  commitment lifecycle, and model-free life stepping.
- `Store` owns an append-only companion `organism_snapshots` table in the
  existing SQLite authority store. Snapshots accelerate restart recovery; the
  event log remains canonical evidence.
- `companion-core` has an opt-in `COMPANION_ALPHA_LIFE=1` loop that restores a
  snapshot, advances state independently of Godot/model workers, emits a
  body-neutral intent, and snapshots again. Default Phase 01 behavior is
  unchanged.
- `alpha50_qualification` executes deterministic causal memory-to-action,
  30-day simulation, 500 restart round trips, snapshot restore, SQLite backup
  and clean-root restore, and integrity checks.
- `alpha50_transition_qualification.py` resolves only authored legal edges in
  the frozen R06 pack and retains raw sample cases plus graph-tamper evidence.
- `alpha50_sensor_probe.py` inventories existing Linux video/audio device APIs,
  records monotonic observation metadata, and explicitly reports degraded
  coverage when hardware is absent; raw media and semantic recognition are not
  implemented.
- `.github/workflows/alpha50.yml` runs the bounded organism, transition,
  sensor, direct-care, source-identity, and artifact-upload checks. Upload is
  unconditional on failure.

The retained restart campaign waits for two durable organism snapshots per
case rather than relying on a fixed startup sleep. This is qualification-harness
determinism; it does not alter production service startup timing.

## Evidence ceiling and remaining gates

Local and hosted checks are bounded engineering evidence (`E3_TARGET_TESTED`
unless explicitly marked otherwise). Transition qualification remains a
presentation resolver check; the dedicated 10,000-case live Godot campaign and
Openbox endurance require the existing exact target tooling and remain separate
from this local harness. No semantic vision, speech, TTS, notification,
medical, autonomy-product, reliability, or release claim is made.
