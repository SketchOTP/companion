# Godot 4.7.2 Artifact Qualification

Status: `COMPLETED — E1 OBSERVED ARTIFACT QUALIFICATION`

## Official provenance

- Official release announcement and archive rechecked: Godot `4.7.2-stable`, published 2026-08-18, built from commit `ed1daf0bf`.
- Standard artifact: `Godot_v4.7.2-stable_linux.x86_64.zip`, official Godot GitHub release asset, `77,860,424` bytes.
- GitHub release API published asset digest: `sha256:cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4`.
- Local SHA-256: `cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4` (`MATCH`).
- Cached binary identification: `4.7.2.stable.official.ed1daf0bf`.
- Godot is MIT-licensed. The selected archive contained the standard executable only; license text is represented by the official project/release sources rather than a separate archive notice file.

Record official release/archive/GitHub sources, release date and commit, exact artifact URL/name/size, official digest or signature evidence when available, locally computed digest, license/notices, archive contents, and retrieval time.

## Host-local handling

The archive and extracted binary are held only under a private local qualification cache. The executable is a 64-bit dynamically linked ELF; observed dynamic requirements were the Linux loader, `libc`, `libdl`, `libm`, `libpthread`, and `librt`. Existing Godot 4.6 was neither read as a substitute nor modified. No global PATH was changed. Removal is cache-directory deletion only after preserving the recorded digest/provenance evidence.

Record private XDG cache location in sanitized form, coexistence with existing Godot 4.6, dynamic-library inventory, permissions, and removal/rollback procedure. Do not modify 4.6 or global PATH.

## Permitted execution

Only `cached-godot --version` ran. It returned the exact version/build string above. No project, editor, window, renderer, display, import/export, plugin, template, or asset operation ran.

Record only the verified non-GUI version/build-identification command and output. No project, editor, display, renderer, import, export, template, plugin, or asset execution.

## Evidence ceiling and disposition

The official release page, archive listing, official GitHub release metadata, published GitHub asset digest, and matching local digest provide **source-correlated integrity evidence**. No independently verified signature chain was established, so this is not a general cryptographic authenticity certification. Recommend the exact cached artifact for a later Architect dependency decision only; it is not adopted or production-approved here.

State whether provenance is cryptographically verified, transport/source corroborated, or blocked. Recommend qualification disposition without adopting the artifact as a production dependency.
