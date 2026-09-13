# R06-C04 result — runtime-transform locomotion requalification

Status: `BLOCKED` / Architect decision required. No approved source PNG was
modified.

Implementation merge head before C04 edits: `c26dcefa8fb455662f3f0b1b749b02be5eb0c9d4`.
Current source pack SHA: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.
Result SHA: `57155563762502f9fa42c089f31cd622b1cbd7df971c56f0bb448b254b457d6f`.

The actual runtime transform is native 1254x1254, centered anchor `(627,627)`,
offset `(0,0)`, scale `0.5`, and MonRoot `(320,320)`: `world = MonRoot +
0.5*(source_pixel-(627,627))`. Persistent near/far correspondence is tracked
through crossings; screen-X identity is not used for handoffs.

Under that transform, accepted left loop anchors alternate
`+140.0,-174.5,+85.0,-159.5` and right loop anchors alternate
`-115.0,+184.5,-143.0,+168.0`; the first handoff is opposite the requested
direction for each side. Actor-root nets are `-218.0 px` left and `+189.0 px`
right, but alternating touchdown progression, phase-hint ambiguity, and maximum
planted slips of `27.0 px`/`18.0 px` fail the ≤2 px criterion. This is a
preserved geometric contradiction, not a claim of Phase 02 acceptance.

Independent negative tests are built from a passing baseline and reject each
mutated semantic property alone. C04 hosted workflows, transition qualification
and Openbox endurance are not run after the required stop condition.
