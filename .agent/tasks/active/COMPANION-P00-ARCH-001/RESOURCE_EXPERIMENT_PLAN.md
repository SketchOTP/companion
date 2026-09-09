# Resource and Experiment Plan

Status: `COMPLETE — PLANNED ONLY; NO EXPERIMENT EXECUTION AUTHORIZED`

Experiments are ordered by architectural rewrite risk and privacy. Each uses a fresh bounded task directive, fixed protocol, no personal media, and exact negative evidence. Hardware specifications never substitute for measured concurrent behavior.

| ID | Priority / phase gate | Question and bounded method | Measures / pass decision | Output / stop condition |
|---|---|---|---|---|
| EXP-01 | P0 — Phase 01 entry | Can the exact Godot 4.7.2 Linux build be obtained from an official release and independently verified without replacing 4.6? Inventory official artifact, hashes/signatures if published, executable metadata, dependency linkage; do not launch until separately authorized. | Exact version/build, source URL, digest, signature/provenance, coexistence plan. Pass only when authenticity and rollback are documented. | Supply record. Stop on absent official artifact, unverifiable provenance, or forced host mutation. |
| EXP-02 | P0 — architecture/renderer | Does Vulkan enumerate correctly and which GPU/display path serves the Openbox output? Metadata first, then separately authorized minimal renderer probe with OpenGL fallback. | driver/device/extensions, renderer selection, present path, errors. No capacity claim. | GPU matrix. Stop on software renderer, wrong GPU, or display-stack mutation need. |
| EXP-03 | P0 — slice | Does Godot 4.7.2 honor bounded resizable window placement, min/max geometry, aspect/scaling, focus, input, persistence, screen removal, and restart on the adopted output? Use synthetic visuals only. | placement success 100/100 starts; no clipping/focus trap; defined fallback; recovery ≤ slice threshold. | Window behavior report and selected technical policy. Stop on compositor/display changes or privacy capture need not authorized. |
| EXP-04 | P0 — persistence | Which local store/journal configuration preserves event/projection integrity under concurrent reads, checkpoints, kill/power-loss simulation, disk full, migration, and backup? Compare fixed SQLite candidate with one credible alternative if SQLite fails. | 0 partial commits/corruption; deterministic replay; bounded checkpoint; backup/restore equivalence; exact library includes 2026 WAL-reset fix. | Storage ADR candidate. Stop if candidate version is affected or local filesystem cannot satisfy locking/fsync. |
| EXP-05 | P0 — operations | Can user services supervise the proposed graph despite currently degraded systemd? Use synthetic no-device processes and reversible user units only under separate authority. | ordered start/stop, watchdog, backoff, crash-loop visibility, suspend/resume, logout/reboot semantics; 100 restart injections. | Supervisor decision. Stop before system services/elevation or policy changes. |
| EXP-06 | P0 — slice/resource | What is the headroom of the minimal slice under concurrent Godot, core, care, store, and stubs? | per-process CPU/RSS/GPU/VRAM/I/O; latency quantiles; no swap pressure/unbounded growth; 30-minute then bounded soak. | Slice resource envelope only. Stop on thermal/noise or host-impact threshold. |
| EXP-07 | P1 — before real perception | What camera modes, latency, quality, privacy indicators, hotplug, and exclusive/shared ownership are usable? Use consented artificial targets; no household imagery retained. | frame delivery/jitter/drop, format conversion, contention, hotplug, ephemeral-buffer proof. | Camera adapter decision. Stop on personal capture, device permission/default change, or unexplained sharing. |
| EXP-08 | P1 — before real speech/help | What microphone/speaker path supports intelligibility, echo control, VAD/ASR/barge-in and replay/media-audio discrimination? Use licensed synthetic/test utterances, no personal voice. | capture/playback latency, drop, SNR, false/miss matrices, echo/replay behavior, degraded coverage. | Audio topology and later candidate benchmark. Stop before ambient recording, personal voice, or live claim. |
| EXP-09 | P1 — RQ-04 | What combination of selected model candidates fits concurrent latency, memory, privacy, cost, power, and noise constraints? Only after RQ-08 and dependency/rights gates. | per-model quality/latency/resources, cloud bytes/cost, graceful fallback. | Informs RQ-04; cannot resolve operator cost/privacy preference. |
| EXP-10 | P1 — backup/continuity | Does encrypted export restore onto a fresh local directory/replacement body with identical identity and policy semantics? | RPO/RTO, manifest/hash match, key-recovery success, event/projection equivalence. | Informs RQ-09/RQ-11. Stop if recovery requires undisclosed vendor or missing key. |
| EXP-11 | P1 — power/household fit | What are wall power, thermal, fan-noise, suspend/recovery, and storage-growth characteristics under the qualified concurrent workload? | calibrated wall power, temperatures/throttling, acoustic method, state growth, resume correctness. | Informs RQ-04 and later release constraints. Stop on hardware safety threshold. |
| EXP-12 | P1/P2 — endurance | Can a qualified subset run 24 h, then multi-day, without state drift, leak, queue growth, renderer freeze, or missed health signal? | time series, injected failures, zero silent degradation, bounded data growth. | E5 candidate only after production-like configuration. |

## Experiment doctrine

- Freeze versions, configs, seeds, datasets/fixtures, artifact rights, start/end state, and abort thresholds before running.
- Use local ext4/NVMe for live state; SSHFS holds only source and immutable copied results.
- Separate warmup, idle baseline, isolated component, and integrated concurrency.
- Report `PASSED`, `FAILED`, `BLOCKED`, `NOT RUN`, or `NOT APPLICABLE`; retain partial/negative evidence.
- Avoid privileged changes. A missing utility is not missing capability.
- No benchmark may choose a product promise. RQ-04, RQ-08, RQ-09, and RQ-11 retain operator policy decisions.
- Phase 01 may not start until EXP-01/02/03/04/05 protocols and stop limits are approved; execution may be sequenced within Phase 01 only if the Architect explicitly allows it.

## Resource budgets

The slice contract's latency and leak thresholds are initial qualification gates, not final product SLAs. Absolute CPU/GPU/VRAM/storage/power/noise budgets remain `UNKNOWN` until EXP-02/06/11. Model budgets remain `UNKNOWN` until RQ-08 and artifact-specific candidates are selected.
