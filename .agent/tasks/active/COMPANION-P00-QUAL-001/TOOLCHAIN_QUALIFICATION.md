# Toolchain Qualification — Python 3.12 versus Rust

Status: `COMPLETED — E3 TARGET-TESTED SYNTHETIC COMPARISON`

## Candidate provenance

- **Python candidate:** unchanged `/usr/bin/python3`, CPython `3.12.3`, supplied by the Ubuntu `python3-minimal` package. It reports OpenSSL `3.0.13` and bundled `sqlite3` `3.45.1`; that SQLite library was not used as the exact SQLite qualification candidate. Python 3.12.14 documentation was current at source recheck, so the target interpreter is an older patch within the 3.12 line and requires an explicit support/update review before any adoption. The Python standard library is PSF-licensed; this harness has no third-party Python dependency.
- **Rust candidate:** Rust `1.98.1` (`rustc 1.98.1 (48a229cea 2026-09-01)`, Cargo `1.98.1`) installed only beneath the private qualification cache using `RUSTUP_HOME` and `CARGO_HOME`. The official release announcement records that 1.98.1 fixes the 1.98.0 vtable miscompilation. The local rustup-init SHA-256 was recorded in private evidence; no global PATH, profile, package, or existing Cargo state changed. Rust and rustup are dual MIT/Apache-2.0.
- **Qualification-only Rust crates:** `serde_json 1.0.151` and `sha2 0.10.9`, with exact transitive checksums in committed `Cargo.lock`. Their registry licenses must be rechecked before any reuse; neither is production-approved. The locked build is offline-reproducible after its initial cache population.

Record exact interpreter/compiler, package/toolchain source, release/security status, licenses, digests, standard/native dependencies, and isolated setup.

## Frozen parity contract

Both shells are disposable, synthetic programs under `experiments/p00-foundation-qual/`. They implement the same one-message AF_UNIX length-prefixed envelope, duplicate-key/invalid-value/schema-major rejection, `JCS-RFC8785-v1` fixture canonicalization, SHA-256 digest, fixed-point update, boot/sequence/causation fields, idempotency outcome, bounded queue declaration, payload-minimized log marker, and controlled one-request process lifecycle. They neither implement Companion organism, memory, care policy, contacts, media, nor any live safety behavior.

Fixture `event-v1.json` SHA-256: `569b94e68f93f70e040c62d5d53610624cdea61f6296f6de84d8fff18d6b8e5f`.

Both candidates produced canonical digest `04d5a59aa1251deb262f7ed787b2d1a22346ce00c2e09d5943c1ef332b0b3f3e` for the frozen event and passed duplicate-key, `NaN`, lone-surrogate, and unsupported-major negative vectors. The fixture contains no floating-point values; this is a cross-language target check of the selected profile surface, not a complete JCS conformance certification.

Describe the identical non-product service-shell behavior, schemas, fixtures, canonicalization profile, synthetic state, IPC, logging, fault, and packaging rules.

## Results

Twelve synthetic self-test and one-request process samples per candidate were retained privately. Medians:

| Candidate | Self-test median | AF_UNIX request round-trip median | Direct third-party dependencies | Native dynamic surface |
|---|---:|---:|---:|---|
| CPython 3.12.3 | 27.60 ms | 7.40 ms | 0 | system CPython/runtime libraries |
| Rust 1.98.1 | 1.04 ms | 1.30 ms | 2 direct / locked transitive graph | `libc`, `libgcc_s` |

Rust debug binary was approximately 8.0 MB; the isolated Rust toolchain/cache and debug target directory were materially larger than the script-only Python shell. The Python shell was shorter and relied only on the installed standard library; the Rust shell required the lock, toolchain, and a larger dependency surface but supplied static typing and ownership checking. Locked Rust rebuild succeeded offline. No RSS/CPU steady-state comparison was performed beyond these short startup/request samples, so claims about sustained resource behavior are `UNKNOWN`.

Record functional parity, deterministic/golden-vector results, retained seeds, startup distributions, RSS, CPU, artifact/environment size, dependency surface, offline reproduction, isolation, update/rollback, testability, complexity, and failed attempts.

## Recommendation

**Recommendation to Architect: RUST for the first authoritative-service implementation decision, subject to a later explicit adoption.** The bounded shell gave identical selected semantic outcomes with substantially lower sample startup/request timing and a stronger language-level memory-safety model. This does not establish production security, throughput, maintainability, or a final language decision; the Rust dependency and toolchain footprint, Python 3.12.3 patch lag, and lack of sustained RSS/CPU evidence remain material.

Language-neutral Phase 01 work—repository layout, schemas, canonical fixtures, XDG policy, logging/health contracts, and test controls—does not depend on this recommendation. Implementation of `companion-core`, `care-core`, and `identity-consent-vault` remains blocked pending Architect adoption.

Recommend Python, Rust, a narrowly bounded split, or blocked follow-up. Do not self-adopt the result. State which Phase 01 work remains language-neutral.
