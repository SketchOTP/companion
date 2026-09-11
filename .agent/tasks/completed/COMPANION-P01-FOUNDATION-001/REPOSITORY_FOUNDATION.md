# Repository Foundation — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — AWAITING ARCHITECT REVIEW`

Document the implemented top-level layout, module ownership, authored/generated boundaries, bootstrap and clean-clone workflow, toolchain pins, build profiles, operator commands and repository exclusions.

Required proof:

- clean clone bootstrap and verification;
- locked debug/release builds;
- no undocumented manual edits;
- generated binaries/caches/runtime data excluded;
- canonical state never written into the checkout;
- protected primary worktree untouched;
- exact changed-path inventory and rationale.

## Implemented layout

`crates/foundation-core` owns contracts, canonicalization, IPC, paths, logging
and persistence; `crates/foundation-services` exposes six role binaries;
`contracts/` and `migrations/` are authored inputs; `godot/` is a neutral
presentation boundary; `scripts/` provides offline bootstrap, verification,
health, matrix, soak, artifact and SBOM commands; `assets/` reserves later
source/generated boundaries; and `evidence/` contains sanitized summaries.
Cargo.lock and rust-toolchain.toml pin the reproducible Rust inputs. Target,
Godot caches and runtime stores remain ignored or outside Git.
