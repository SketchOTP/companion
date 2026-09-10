# Contracts and Canonicalization — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — AWAITING ARCHITECT REVIEW`

Document every implemented Phase 01 schema and matching Rust type, compatibility rule, extension policy, canonical byte profile, digest scope and golden fixture.

Required contracts:

- canonical event envelope;
- lifecycle/readiness;
- health/degraded state;
- ordinary observation;
- safety candidate;
- care receipt;
- embodiment intent/result;
- vault decision stub;
- backup/export manifest shell.

Required proof:

- JSON Schema Draft 2020-12 validation;
- duplicate decoded-key, Unicode, number and schema-major rejection;
- deterministic JCS/digest golden vectors;
- Rust/schema compatibility;
- malformed/unknown-variant negative tests;
- retained property-test seeds;
- no unsupported RFC 8785 or product claims.

## Implemented contract profile

Nine schemas and matching Rust structs are committed. The encoder rejects
duplicate decoded keys (including escaped equivalents), nonfinite/fractional
numbers and unsupported schema majors; object members are sorted by decoded
UTF-16 units and SHA-256 covers the resulting canonical event bytes. The
profile is intentionally integer/fixed-point bounded and is not a claim of a
general-purpose RFC 8785 implementation or product semantics.
