# COMPANION-P00-ENV-001 — Evidence Record

Status: `COMPLETE_FOR_ARCHITECT_REVIEW`

## Repository preflight

- Expected accepted baseline: `ddb6b130ab6428a1f395cd223d309eeaa2ac7462`.
- Directive/task-packet commit: `c06c796d9d54da4cdcf38296ee08c4f70fb3993d`.
- Starting routing head: `2ea7b41d79f24f030ea3c3690dee00e8c2340671`.
- Local `main` was clean at the accepted onboarding commit, then was fast-forwarded normally through the two governance-only directive commits.
- Initial working tree after synchronization: clean and equal to `origin/main`.
- Unexplained changes/divergence: none.
- Product/runtime paths present before execution: none.

## Authority reconstruction

- Re-fetched: canonical project, master roadmap, Open Decisions and Research Gaps, R09 deployment/hardware dossier, R10 Godot embodiment dossier, the live environment directive, and the pending coder report.
- Verified GitHub Issue #2 is open and preserves the no-self-acceptance and no-product-work boundary.
- No fetched authority changed the directive scope or invalidated the accepted ingest corpus.
- The repository directive ledger did not yet contain a dedicated environment-directive entry; this result appends it without rewriting history.
- Retrieval confidence: `ADEQUATE`.

## Inspection method

Probes emitted only selected, normalized fields. No general environment dump, host identity query, network inventory, persistent-device identifier query, media capture, screen capture, audio playback, package installation, privilege escalation, benchmark, or configuration change was used.

| Area | Interfaces/commands used | Result | Evidence class |
|---|---|---|---|
| OS/session | selected `/etc/os-release`, `uname`, `lscpu`, `free`, `ulimit`, selected `sysctl`, XDG session class, process command names, `xdpyinfo`, root-window properties | Completed with one loginctl-context limitation | E1_OBSERVED |
| Graphics | selected `lspci`, `nvidia-smi`, `glxinfo -B`, Vulkan loader/ICD file presence | OpenGL completed; exact Vulkan unknown because tool absent | E1_OBSERVED |
| Display | `xrandr` query/listmonitors/selected transforms, `xdpyinfo`, `_NET_WORKAREA`, read-only GNOME scaling keys | Three connected outputs across two X screens enumerated | E1_OBSERVED |
| Storage | `findmnt`, `df -B1`, `statfs`, `getconf`, selected `lsblk` chain | SSHFS repository and local ext4/NVMe system volume distinguished | E1_OBSERVED |
| Camera | device-node access metadata, `v4l2-ctl` capability/format/control/metadata queries, `fuser` exit status | Video and metadata nodes, formats, intervals, controls, and instantaneous holder state enumerated; no frames | E1_OBSERVED |
| Audio | package metadata, user-unit state, selected `pactl`/`wpctl`, ALSA list and stream metadata | Stack, defaults, current and advertised metadata enumerated; no recording/playback | E1_OBSERVED |
| Godot | PATH/package/app-entry/bounded-location discovery, `--version`, content-hash cardinality | 4.7.2 not found; one unique 4.6 stable binary content found | E1_OBSERVED |
| Tools | command presence and version queries | Presence/absence recorded without installation | E1_OBSERVED |
| Operations | selected `systemctl`, `timedatectl`, `/sys/power`, read-only GNOME power keys, cpufreq, power-supply/thermal metadata, sanitized sensors parser | Time/suspend/service/thermal visibility recorded; no state transition | E1_OBSERVED |

## Missing and blocked tooling

- `vulkaninfo`: absent. Exact Vulkan capability is `UNKNOWN`, not absent.
- `vainfo`: absent. VA-API capability is `UNKNOWN`, not absent.
- `smartctl`: absent. Drive-health telemetry is `UNKNOWN`, not absent.
- Compositor-specific Wayland utilities: absent and not relevant to the observed X11 session.
- Godot 4.7.2: not found. Installation was prohibited.
- Several developer tools are absent; presence was inventoried only and is not dependency approval.
- Camera video-node metadata-format query: `FAILED` with invalid argument because that node is video capture; the metadata-node query `PASSED` and returned UVC header metadata.
- Repository `lsblk` chain: `FAILED` because SSHFS is not a local block device; this establishes a storage-class boundary rather than missing storage.
- `wpctl --version`: `FAILED` because that option is unsupported; package metadata established WirePlumber and PipeWire versions.
- First sensor JSON parser: `FAILED`; it assumed every child was an object. A corrected type-checked parser `PASSED`. No fact was taken from the failed parser.
- One proposed temp-file display probe was rejected before execution because it included cleanup syntax. It was rerun as a pipe-only read and `PASSED`; no temp artifact was created.

## Privacy and sanitization validation

- Durable evidence stores no hostname, username, account identifier, home path, IP/MAC address, filesystem UUID, mount endpoint, persistent device identifier, credential, token, or unrelated personal file data.
- Device paths are limited to the directive-authorized `/dev/video0`, `/dev/video1`, and `/dev/media0` camera nodes.
- Audio node identifiers are normalized to functional device classes; application streams were not enumerated.
- Failed systemd unit identities were not collected; only aggregate counts and explicitly relevant unit states were retained.
- One live driver/audio metadata response exposed a hardware-serial field before filtering. It was discarded immediately, no raw output file was retained, and it is omitted from every repository and Notion artifact. This is recorded as a contained deviation.
- Camera frames/screenshots captured: `NO`.
- Microphone samples recorded: `NO`.
- Audible playback performed: `NO`.
- Media files added anywhere in the repository: `NO — PASSED`.

## Artifact validation

- `ENVIRONMENT_RAW.json` parse: `PASSED`.
- Required inventory categories: `PASSED — 10/10 nonempty`.
- Source/timestamp/status/confidence coverage and unique observation IDs: `PASSED`.
- Report and capability-matrix cross-check against raw key facts: `PASSED`.
- All eleven RQ entries exactly once in the intended crosswalk: `PASSED — 11/11`.
- Allowed capability status vocabulary and no pending rows: `PASSED`.
- Unsupported architecture/dependency selection: `PASSED — none found`.
- Exact current hostname/username/home path and live camera persistent-identifier scan: `PASSED — no durable matches`.
- MAC/UUID/private-endpoint/narrow-secret pattern scans: `PASSED`.
- Media absence and `.agent/`-only changed-path scope: `PASSED`.
- `git diff --check`: `PASSED`.
- Product/Godot/dependency/CI artifact absence: `PASSED`.

## Publication evidence

- Result commit: `ef5b011bfd6e3f747e8bf8e8f06faebb21901d50`.
- Normal result push and immediate local/remote equality: `PASSED`.
- Notion report/directive exact-result-SHA update and re-fetch: `PASSED`; zero unknown blocks and no pending-execution marker.
- GitHub Issue #2 result update/open state: `PASSED`; comment `5598863339`, issue `OPEN`.
- Publication-evidence commit: the governance-only commit containing this section.
- Final local/remote equality: required after publication-evidence push and reported in the canonical result.

## Evidence level

- Host and peripheral metadata: `E1_OBSERVED`.
- Sanitized artifact structure and semantic cross-check: `E3_TARGET_TESTED`.
- Product, renderer, camera stream, audio stream, local inference, caregiving, or always-on runtime capability: `NOT ESTABLISHED`.
