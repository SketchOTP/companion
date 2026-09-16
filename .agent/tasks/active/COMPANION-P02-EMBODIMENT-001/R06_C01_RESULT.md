# R06-C01 result — runtime selection derived from final playback

The frozen ZIP, manifest, and HTML hashes matched their Review 13 authority.
Runtime selection was derived from every manifest track whose group is not
`Diagnostics`; retry studies, historical blocking studies, and sheet
derivatives are excluded. The candidate pack contains 58 native 1254×1254 RGB
black-field assets, 24 playback tracks, and 283 frame slots. Source bytes are
copied unchanged and sidecars preserve observed source-space annotations. The
initial 68/26/303 derivation was superseded after explicit manifest inspection
identified two diagnostic tracks that must remain audit-only.

Local schema validation, immutable intake, fsync-backed staging/rename,
mid-intake failure cleanup, and tamper rejection passed. Cargo and Godot were
unavailable locally, so hosted execution was required. Hosted run
`34761173688` on head `a2826a546c700897bb049b1ce4defc354374f76a` passed the
Rust typed round-trip and the canonical Godot runner. Godot used Xvfb, Mesa
llvmpipe, and the Dummy audio driver; the observed render boundary was
`SubViewport.texture.get_image`, with zero Godot ERROR lines and one retained
V-Sync warning. The sanitized result and log hashes are committed in
`experiments/p02-embodiment/results/r06-c01/hosted-run-34761173688.json` and
the complete bundle is published as the workflow artifact.

Status remains candidate integration only. Phase 02 is not accepted and no
transition or endurance campaign was started. The earlier hosted head
`dfb41885559e279178a96f26594304c5a7f215b3` failed because headless fallback
readback dereferenced a null viewport texture and emitted
`ERROR: Parameter "t" is null.`; the canonical Xvfb path and null-safe guard
resolve that evidence-path defect without whitelisting engine errors.
