# C01 implementation record — 2026-09-15

Status: `CONTINUE / PARTIAL IMPLEMENTATION`; Architect acceptance is not claimed.

Implemented in the current candidate tree:

- ordinary evidence is emitted by the checked-in `sensor-gateway` child through
  the supervisor, with a separately provisioned HMAC domain, peer credentials,
  producer generation, freshness and durable message-id replay checks;
- sequence exhaustion refuses new body intents instead of re-emitting the
  signed-64 maximum and marks the V2 body-output capability degraded;
- the bridge now invokes the configured Godot 4.7.2 runner and accepts a result
  only when Godot reports the frozen pack, a successful track run, and an
  observed `RenderingServer.frame_post_draw` boundary;
- the Alpha workflow runs the production legal graph in Godot for 10,000 raw
  cases and independently verifies the resulting trace; the historical
  Python-owned qualification is no longer an acceptance step;
- evidence manifest hashing excludes the manifest itself and publishes a
  separate manifest digest.

Local evidence:

- `cargo test --workspace --locked`: PASSED (26 foundation-core, 6
  foundation-services, all binaries and doc tests).
- Python syntax and `git diff --check`: PASSED.
- Resident authenticated ordinary ingress and durable replay: PASSED.
- The exact Godot 4.7.2 binary is not installed on this host. A separately
  labelled Godot 4.6 exploratory run under Xvfb exercised the bridge and
  produced a PASS causal trace, but it is not acceptance evidence for the
  required 4.7.2 runtime. The exact-version causal loop and 10,000-case
  process campaign are therefore NOT RUN locally.

Remaining C01 work is not silently promoted: rich V2 goals/development/
consolidation, paired production causal controls, restart-remembered behavior
through real Godot, multi-class failures, care process-loss independence,
resident clean-root restore, and the hosted exact-head regressions remain
required before an Alpha handoff.
