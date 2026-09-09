# Foundation Qualification Harnesses

This directory is disposable qualification infrastructure for
`COMPANION-P00-QUAL-001`. It is **not** the Companion runtime, a product
module, or a production service design. Its dependencies are qualification-only
and are not production-approved. Passing any test here does not establish a
product, security, reliability, or safety capability.

The committed sources and fixtures define repeatable synthetic checks. Binaries,
downloaded toolchains, Godot archives, SQLite sources/builds, databases, WAL
files, raw measurements, and temporary sockets belong in the private local
qualification state/cache roots, never in Git.

The harnesses use no personal data, media, contacts, credentials, model calls,
or live safety behavior. They only exercise frozen synthetic envelopes so that
toolchain, canonicalization, local IPC, and local-storage candidates can be
compared before any product implementation is authorized.
