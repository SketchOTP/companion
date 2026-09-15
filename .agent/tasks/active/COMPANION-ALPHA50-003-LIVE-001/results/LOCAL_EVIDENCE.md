# Local Alpha50-003 evidence

- V2-only guard: `V2_ACCEPTANCE_GUARD_PASS`.
- `target/release/alpha50_qualification` produced `status=PASS`, 30 simulated
  days, 500 V2 serialization restart cases, V2 preference/correction/
  commitment/outcome causal flags, SQLite snapshot and clean-root backup
  restore.
- `scripts/alpha50_live_trace.py` produced `status=PASS` from checked-in
  `companion-core` and `godot-bridge` processes. The authenticated ordinary
  envelope was accepted, a V2 body intent and observed bridge result were
  durably recorded, and the restored identity was
  `a1fa5200-0000-0000-0000-000000000032`.
- Local live-trace JSON SHA-256 (run captured 2026-09-15):
  `d719cc992219c354c590affb3bb4223be697d68513b8260ff983e7daf99fd272`.
- Ordinary evidence fixture SHA-256:
  `5d7af6062efc1b53505a8d1c5e1aab5fbb794190ccb723bf60f0414428fe1acc`.

These are E3 candidate engineering observations. They do not claim production
Godot legal-transition qualification, multi-class failure coverage, care
process-loss independence, physical sensors, Openbox endurance, Alpha50
acceptance, or Phase 02 acceptance.

Additional exact-head checks after the inherited Phase 01 compatibility fix:

- Workspace tests: `cargo test --workspace --locked` — `PASSED` (25
  foundation-core and 6 foundation-services tests, plus binaries/docs).
- Clippy: `cargo clippy --workspace --all-targets --all-features --locked
  -- -D warnings` — `PASSED`.
- Schema/crosswalk/closeout/V2 guard — `PASSED` (22 schemas; 18 typed
  crosswalks; V2 acceptance guard).
- Local Phase 01 closeout — `PASSED` at 3000 cycles / seeds 17,23,41 after
  restoring the legacy fixture compatibility path outside Alpha live mode;
  duration was 304.303 seconds.
- Latest live-trace output SHA-256:
  `29a4249d4299e3be2b4f84fa8c8ef7f3a3c8c9953b9be96c4da2c4e32d6f428d`.
- Physical probe: `/dev/video0`, `/dev/video1`, and microphone/audio cards were
  observed (`E1_OBSERVED` inventory only); no semantic sensor capture was run.
- Target probe: current X11 is GNOME Shell/mutter at 7680x2160, not the
  dedicated 1366x768 Openbox target. Openbox endurance is therefore
  `BLOCKED`, with no host reconfiguration attempted.
