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
mid-intake failure cleanup, and tamper rejection passed. Rust typed round-trip,
Godot playback, first-frame/render observation, world-contact measurement, and
hosted CI are `NOT RUN` locally because Cargo and Godot are unavailable; the
dedicated hosted workflow is `.github/workflows/phase02-embodiment-r06.yml`.

Status remains candidate integration only. Phase 02 is not accepted and no
transition or endurance campaign was started.
