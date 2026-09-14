# R06-C06 controller result

Status: `PASS — BOUNDED REPLAY-SAFE FIXED-STEP QUALIFICATION SUBMITTED FOR ARCHITECT REVIEW`

The frozen R05 source pack remains byte-identical (`1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`). The V2 intent contract uses UUID identity plus `intent_sequence`, explicit cancellation targeting, and a controller-owned 24 Hz semantic clock. Godot is a presentation adapter and consumes serialized schema-valid V2 objects.

Six left/right start→cruise→stop cases pass at -48/-96/-144 and +48/+96/+144 px/s. Presentation calibration is 0.5x/1.0x/1.5x while canonical displacement remains velocity/24. A 30 FPS and 60 FPS render cadence probe each produces 24 semantic ticks and identical final displacement. Mid-loop stop/cancel enters the stop track and never resumes cruise; actor position remains continuous.

The executable negative matrix covers duplicate/equal/lower replay, wrong cancellation target and replay, direction/facing/sign mismatch, missing/wrong-profile tracks, fixed-step loss/duplication, loop/root/phase reset, and ineligible/corrupt pack paths. Results are in `controller_locomotion_qualification.json` and are validated by `validate_r06_c06.py`.

Normal and quarter-speed Godot runs capture actual viewport images after `RenderingServer.frame_post_draw`; quarter speed changes render pacing, not semantic movement. This is bounded engineering/presentation evidence only. It does not claim physical grounding, organism autonomy, reliability, transition qualification, Openbox endurance, or Phase 02 acceptance.

## Hosted exact-head closeout — 2026-09-14

Implementation SHA `6ca691412b3da7efe9227191f5f34a9175883301` passed focused
R06 `34799648248`, Phase 01 `34799648246`, and inherited Phase 02
`34799648257`; PR-triggered runs `34799652134`, `34799652115`, and
`34799652259` also passed on the same SHA. R06 artifact `10331331019` has
digest `sha256:549b4af63f61dd5204d94d609365a70b584bda3f28f44ceb77818d4dfe889a3a`.
The final hosted run has zero Godot errors, strict render-boundary evidence,
actual normal/quarter playback, 30/60 FPS semantic equivalence, six velocity
cases, and 17 executable negative cases. The frozen pack SHA is unchanged.

## Corrected implementation-head closeout — 2026-09-14

The modulo phase observation now serializes a mathematically continuous loop
seam as `0.0` instead of a rounded `1.0`; controller movement and frozen source
bytes are unchanged. Implementation SHA
`941c231d4562177c1db02cd61fc0f0c085e6dae4` passed R06 `34800729601`, Phase 01
`34800729655`, and inherited Phase 02 `34800729662`; push-triggered R06
`34800727016` and inherited Phase 02 `34800727017` also passed. The corrected
local result SHA is
`a5c2923040e9d1c6df6d26139c2fd3cce7b21c8b58ba2cd8feb6811616834ea0`.
