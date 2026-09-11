# Phase 01 dependencies and rights

| Component | Version / identity | Purpose | Rights / status |
|---|---|---|---|
| Rust toolchain | 1.98.1 | Authoritative foundation services | Rust/LLVM licenses; adopted baseline |
| serde / serde_json | locked in Cargo.lock | Contract encoding | MIT/Apache-2.0; development dependency |
| sha2 | locked in Cargo.lock | Event digest | MIT/Apache-2.0; development dependency |
| libc | locked in Cargo.lock | Narrow Unix IPC calls | MIT/Apache-2.0; development dependency |
| thiserror, tracing, uuid | locked in Cargo.lock | Errors, logs, identifiers | MIT/Apache-2.0; development dependency |
| SQLite | exact 3.53.4 external artifact | Synthetic development stores | Public domain; release qualification remains conditional |
| Godot | 4.7.2 official Linux x86_64 SHA-256 cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4 | Neutral habitat validation | MIT; not committed, not a product capability |

Cargo.lock is committed for reproducibility. No model, speech, camera,
biometric, notification, or cloud dependency is present. No dependency is
approved beyond the Phase 01 foundation baseline until the Architect reviews
this phase result.
