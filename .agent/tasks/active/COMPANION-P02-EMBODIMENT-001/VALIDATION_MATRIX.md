# VALIDATION MATRIX — COMPANION-P02-EMBODIMENT-001

Report only `PASSED`, `FAILED`, `BLOCKED`, `NOT RUN`, or `NOT APPLICABLE`.

1. Protected primary worktree unchanged.
2. Clean local secondary worktree.
3. Phase 01 acceptance/merge reconstructed.
4. Mandatory Notion/GitHub authority available.
5. Both approved visual references inspected directly.
6. Exact reference dimensions/hashes.
7. No external copyrighted creature art.
8. Construction model complete.
9. Palette lock.
10. Anatomy and head-spike invariants.
11. Candidate diagonal views labeled for approval.
12. Authoring approach evidence and rights.
13. Deterministic MON_FRAME_V1 export.
14. 1024×1024 RGBA/sRGB/alpha.
15. Root/baseline/safety region.
16. Landmarks and contacts.
17. Frame timing and numbering.
18. Unique-frame accounting.
19. >=32 clip families.
20. >=256 unique body-frame sources.
21. Required eight-direction coverage.
22. >=24 eye/gaze/blink overlays.
23. >=8 mouth overlays.
24. Idle variant coverage.
25. Clip schema/Rust/Godot agreement.
26. Transition graph and connectors.
27. Loop seams and contact drift.
28. Interrupt/continuation.
29. Frame/event markers.
30. Layer order and body handoff.
31. Missing/corrupt pack degradation.
32. Atlas dimensions/gutter/overlap/bleed.
33. Source→pack traceability.
34. Reproducible pack build.
35. Local export/restore.
36. Explicit window/base/scale/filter settings.
37. Target-screen placement.
38. Geometry persistence and resize.
39. Simulated topology loss/restoration.
40. Bridge/Godot reconnect.
41. Headless Godot validation.
42. Target-host Openbox playback.
43. Review sheets generated.
44. Review artifacts attached to Notion.
45. 10,000-case transition matrix.
46. Two-hour continuous playback.
47. Frame-time distribution.
48. Pack-load latency.
49. Intent/result latency.
50. Memory/resource growth.
51. No checkout/SSHFS runtime write.
52. No embodiment AF_INET/AF_INET6 socket.
53. Ordinary-Git binary budget.
54. Generated artifact hashes.
55. CI result/artifact IDs.
56. Evidence manifest/validator.
57. Tamper-negative test.
58. Failed/rejected assets preserved.
59. Notion/PR/Issue synchronization.
60. Remote branch equality.
61. PR open/unmerged.
62. Issue #8 open.
63. Phase 03+ closed.
64. No prohibited capability or claim.
65. Operator visual approval correctly pending or recorded.
# Architect Review 01 correction — current validation (2026-09-11)

Local Python syntax/schema/contract checks and the private core-motion build
returned zero errors.  A second clean-process build was byte-identical in the
generated manifest, track definitions, frame corpus, and atlas pages.  Godot
4.7.2 headless and hosted Phase 02 CI are not run in this worktree because the
artifact is not installed; the workflow downloads it ephemerally after hash
verification.  Openbox two-hour playback remains `NOT RUN`.
# R03 validation matrix

| Property | Positive observation | Tamper-negative |
| --- | --- | --- |
| Root | rendered track landmarks remain `[512,896]` | one-pixel root mutation rejected |
| Planted contact | idle and active contacts remain on baseline | contact shift rejected |
| Swing foot | walk rendered x/y displacement across phases | frozen/shifted contact rejected |
| Anatomy | bilateral hierarchy includes every digit/toe | removed digit rejected |
| Facing | connector endpoint frame hashes differ | endpoint reuse rejected |
| Timing | Godot `SpriteFrames` speed 24, integer weights | zero duration/schema mutation rejected |
| Track selection | every generated family starts; missing family is rejected | nonexistent track never emits start |
| Schema/Rust | actual v2 tracks validate and round-trip | malformed field/schema mutation rejected |

R03 status is bounded `E3_TARGET_TESTED` candidate evidence; operator visual
approval, complete library, Openbox endurance, and later phases remain deferred.
# R04 superseding validation matrix

| Check | Required result |
|---|---|
| Valid synthetic intake | PASSED; exact source/CAS/runtime bytes |
| Wrong dimensions / mode / hash | REJECTED with exact reason |
| Ineligible approval | REJECTED before presentation |
| Missing landmark | REJECTED |
| Contact / duration / event tamper | REJECTED |
| Missing required Rust pack path | nonzero |
| Actual generated-pack Rust round trip | PASSED |
| Exact Godot track | frame zero presented before `started` |
| Missing/corrupt pack | failed/degraded; no `started` |
| Restored pack | exact track starts |
| Clean clone and hosted CI | required before handoff |

## R04 executed result

| Check | Status | Observation |
|---|---|---|
| Valid source intake | `PASSED` | input, content-addressed, and runtime bytes/hash equal for both synthetic frames |
| Wrong dimension | `PASSED` | rejected as `wrong_dimensions` |
| Wrong mode | `PASSED` | rejected as `wrong_mode` |
| Source-hash tamper | `PASSED` | rejected as `source_hash_mismatch` |
| Approval-state rejection | `PASSED` | rejected as `approval_ineligible` |
| Missing landmark | `PASSED` | rejected as `landmark_missing` |
| Contact tamper | `PASSED` | rejected as `contact_invalid` |
| Duration tamper | `PASSED` | rejected as `duration_invalid` |
| Event-order tamper | `PASSED` | rejected as `event_order_invalid` |
| Missing generated-pack path | `PASSED` | Rust validator returned nonzero |
| Actual generated-pack Rust round trip | `PASSED` | required exported path consumed; one typed track reserialized |
| Godot exact-track selection | `PASSED` | exact synthetic track selected at 24 FPS |
| First-frame acknowledgment order | `PASSED` | `first_frame_presented` observed before `started` |
| Missing track | `PASSED` | `track_missing`; no `started` |
| Ineligible pack | `PASSED` | `approval_ineligible`; no `started` |
| Corrupt frame | `PASSED` | `frame_hash_mismatch`, degraded |
| Restoration | `PASSED` | restored exact pack emitted `started` after frame-zero presentation |
| Result validator tamper negatives | `PASSED` | hash, byte equality, rejection reason, and event order each rejected |
| Clean clone at implementation commit | `PASSED` | complete R04 evidence plus Cargo/contract checks; tracked diff empty |
| Focused Phase 02 hosted run | `PASSED` | run `34656090767`; artifact `10285600941` |
| Inherited Phase 01 hosted run | `FAILED` | run `34656090763` exposed an intermittent ordinary-observation marker race |
| Corrected 3,000-message local matrix | `PASSED` | 3,000/3,000 exact accounting; 198/198 ordinary observations persisted with the consumption barrier |

The failed inherited run is not converted to a pass. Final reconciliation and
new exact-head hosted Phase 01 validation remain required. Production art, animation,
Openbox endurance, and Phase 02 acceptance remain `NOT RUN`.

## R05-AUTHOR-001 local validation

| Check | Status | Evidence |
| --- | --- | --- |
| Review 10 / ADR-57 authority | `PASSED` | live authority reconciled; candidate authorship authorized |
| Exact reference hashes | `PASSED` | identity and turnaround hashes match |
| Bounded request equation | `PASSED` | 8 tracks / 33 occurrences / 29 unique hashes |
| Clean-process pack determinism | `PASSED` | source-tree digest equality |
| MON_FRAME_V1 PNG/intake | `PASSED` | 33/33 byte-identical review intake |
| Rust actual-pack round trip | `PASSED` | actual path returned 0; missing path returned nonzero |
| Godot import/cold/warm | `PASSED` | exact 4.7.2; zero application errors |
| All requested Godot tracks | `PASSED` | eight exact requested roles started |
| Marker order | `PASSED` | footfalls, facing changes, attention/acknowledge/settled |
| Production eligibility | `PASSED` | candidate rejected for production |
| Corruption and recovery | `PASSED` | `frame_hash_mismatch`, then restored `started` |
| Rendered bounds/contact QA | `PASSED` | zero safety/perimeter/drift failures |
| Semantic tamper negatives | `PASSED` | 5/5 rejected |
| Local export/fresh restore | `PASSED` | full restored hash equality |
| Hosted Phase 01 | `FAILED` | run `34695095049` passed but duplicate run `34695094043` failed with late `BrokenPipeError`; mixed evidence supersedes a pass |
| Hosted Phase 02 / artifact | `PASSED` | run `34695095027`; artifact `10298790129`, digest `sha256:b4c802a0fa20bb2f2e8652bc4d56cbf8887766929412c3abd1debac32c8e82f1` |
| Delayed control-frame regression | `PASSED` | 150 ms delayed send exceeds superseded 50 ms window and completes under bounded framing |
| Complete local Phase 01 after correction | `PASSED` | all 12 groups and exact 3,000-message closeout pass with exact Godot 4.7.2 configured |
| Operator visual approval | `NOT RUN` | candidate package not self-approved |
| Phase 02 acceptance | `NOT RUN` | requires Architect review and later gates |
