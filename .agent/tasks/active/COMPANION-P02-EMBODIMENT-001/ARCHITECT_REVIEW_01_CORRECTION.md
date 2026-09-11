# Architect Review 01 — Source Recheck Correction

## Superseding clarification

After publishing Architect Review 01, the Architect re-read the complete current
`experiments/p02-embodiment/scripts/build_assets.py` at reviewed head
`9a65b8db032c97e13fce5d6a305989d32f2cc879`.

The review's statement that this file uses Python runtime `hash()` in geometry is
withdrawn. The reviewed file uses explicit family/direction indices and
trigonometric expressions; no `hash()` call was found in that file.

The deterministic-build requirement remains because exact clean-process output
must still be proven and all authoring inputs must be explicit and stable. The
remaining material findings and the continuation verdict are unchanged:

- the generator does not derive construction geometry from the exact approved
  native reference package;
- direction is used as temporal frame progression;
- visible body placement moves while fixed root/contact landmarks are declared;
- atlas gutter/extrusion is not physically implemented;
- bulk generated assets violate the adopted artifact policy;
- operator review material is not durably accessible;
- no dedicated Phase 02 workflow exists; and
- the inherited workflow is failing.

This correction supersedes only the Python `hash()` statement in
`ARCHITECT_REVIEW_01.md`, the associated current-state summary, the Notion
review, and the initial PR-body publication.
