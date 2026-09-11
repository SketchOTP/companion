# Phase 01 contracts

These Draft 2020-12 schemas and JSON fixtures define transport and persistence
shapes only. They do not describe a living organism, a sensor implementation,
or an emergency/care policy. Unknown fields are rejected at the service
boundary until a schema major is deliberately revised.

`fixtures/event-v1.json` is the canonical event vector used by the Rust tests
and bootstrap verification. Authoritative numeric fields are bounded integers
or fixed-point milli-units; floating point is rejected.

Phase 02 adds `mon-animation-clip.schema.json` and the corresponding fixture.

R04 adds `mon-authored-frame-pack-v1.schema.json`, the fail-closed landing
contract for immutable Architect-authored full-frame sources. Explicit Rust
types, its synthetic fixture, intake validator, and Godot importer agree on
approval, facing, posture, timing, landmarks, contacts, events, interruption
ranges, and provenance. Production eligibility is never inferred from names.
Clip manifests are presentation contracts: they describe authored raster
drawings, landmarks, timing, transitions, and overlays, not organism state or
care policy. `MonAnimationClip-v1` uses a fixed 24 Hz integer tick grid,
forbids root motion, rejects unknown fields, and binds every pack to a SHA-256
checksum.
