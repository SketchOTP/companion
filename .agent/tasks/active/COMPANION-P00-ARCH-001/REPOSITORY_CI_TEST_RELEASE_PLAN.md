# Repository, CI, Test, and Release Foundation Plan

Status: `COMPLETE — PROPOSED ONLY; NO SCAFFOLD, MANIFEST, OR WORKFLOW CREATED`

## Proposed source tree

```text
/
├── AGENTS.md
├── .agent/                  # Authority state and task evidence
├── .agents/                 # repository skills/instructions
├── .authority/
├── apps/
│   └── godot-body/          # Godot presentation only
├── services/
│   ├── companion-core/
│   ├── care-core/
│   ├── identity-consent-vault/
│   └── ops/
├── adapters/
│   ├── sensors/
│   ├── models/
│   └── notifications/
├── contracts/               # JSON Schemas, JCS/digest profiles, examples, compatibility fixtures
├── policies/                # reviewed care policy source; no secrets
├── assets/
│   ├── source/              # authored MON_FRAME_V1 source
│   └── manifests/           # asset provenance/rights; generated atlases excluded
├── migrations/              # immutable per-store migrations and fixtures
├── tests/
│   ├── unit/
│   ├── contract/
│   ├── integration/
│   ├── fault/
│   ├── privacy-security/
│   ├── golden/
│   └── acceptance/
├── tools/                   # project-owned build/validation helpers
├── docs/
└── release/                 # source templates for BOM/provenance; outputs excluded
```

This is a proposed boundary map, not authorization to create it.

## Authored, generated, and runtime separation

- Git tracks authored source, schemas, policies, migrations, fixtures, tests, asset source/manifests, and environment locks.
- Generated code, Godot imports, atlases, build/export outputs, coverage, BOMs, attestations, caches, and test results go to deterministic build directories or immutable release storage, not mixed with source.
- Runtime data uses local XDG directories; never repository/SSHFS. Tests use per-run local temporary roots with explicit fixtures and teardown.
- Secrets, credentials, personal data, biometric templates, real contacts, raw media, and private backups are never committed or placed in CI artifacts.

## Reproducible environment

- Pin Godot editor/export-template digest, the Architect-approved language toolchain selected through EXP-00, OS/container image digest where appropriate, all direct/transitive dependencies, schema/canonicalization/digest dialects, policy versions, and build tools.
- Resolve from locked, allowlisted sources; verify hashes/signatures before use; record offline cache provenance.
- Generate a human-readable version manifest and machine BOM. Clean builds must not depend on mutable user/global state.
- A developer setup script may diagnose prerequisites but cannot silently install/change host software.

## Branch, commit, and review rules

- Protected `main`; short-lived `codex/*` or feature branches; no force push.
- One directive/result lineage per coherent change; conventional, reviewable commits; Authority state updated with implementation evidence.
- Required independent review for architecture, care policy, privacy/security, migrations, dependency/rights, model/data/voice/assets, and release claims.
- Generated artifacts are rebuilt, not hand-edited. Failed tests/evidence remain append-only.
- CODEOWNERS or equivalent should require care/security/privacy and asset-rights review once roles exist.

## Test layers

| Layer | Required scope |
|---|---|
| Static | format/lint/type/schema/policy validation; secrets/private-data/forbidden-path scan; license headers |
| Unit/property | deterministic organism, memory projection, policy transitions, idempotency, fixed-point/numeric bounds, time and boundary values; randomized cases retain reproducible seeds |
| Contract | every IPC producer/consumer, `JCS-RFC8785-v1` golden bytes/digests, duplicate-key/Unicode/NaN/Infinity/numeric rejection, signature scope, schema-major rejection, additive compatibility, peer authorization |
| Persistence | migration, canonical replay hash, same/cross-boot sequence/causation, crash/checkpoint, pre/during/post-commit kill points, disk-full/read-only, backup/restore, corrupted-copy fail-closed |
| Integration | process graph with synthetic adapters; startup/shutdown/restart/degradation; direct producer→care safety path; companion stopped/forged/DB-absent negatives; duplicate safety idempotency; no shared writer |
| Godot | import/asset metadata, intent playback, window/display/focus/scaling, renderer fallback |
| Privacy/security | egress deny, log redaction, filesystem/socket modes, vault absent/locked/corrupt/unavailable/revoked and secret-taint/capability denial, threat fixtures, dependency scans |
| Safety | direct authorized safety input, care-owned receipt journal, deterministic scenario replay, false/missed/replay/media/fallback/ack states, producer outage→degraded coverage, companion cannot create/suppress transitions; simulation/shadow only |
| Resource/endurance | latency quantiles, per-process resource series, queue/store growth, leak/soak, suspend/resume |
| Acceptance | exact vertical-slice contract and end-goal/ADR/risk traceability; Architect visual and semantic review |

## Proposed CI matrix

No CI exists or is authorized yet. When authorized:

- fast presubmit on supported Linux: static, unit, retained-seed property, canonical-byte/digest contract, secret/privacy scan, deterministic replay;
- clean pinned Linux build: locked dependency restore, build, SBOM/license/provenance, zero untracked generated source;
- integration job: synthetic process graph, direct safety path/companion negative tests, vault-state denial, fault injection, persistence/backup/migration;
- Godot 4.7.2 job: headless import/schema plus display-capable self-hosted target-host tests separately;
- scheduled security/dependency/rights drift review and bounded endurance; never label queued/skipped target-host work as pass.

Camera/audio, GPU/display, suspend, power/noise, and actual host service tests cannot be proven by generic hosted CI. They require privacy-safe target-host directives and retained measurements.

## Roadmap Phase 01 foundation boundary

When separately authorized, Phase 01 may create the reproducible workspace, empty process shells, typed/canonical IPC, XDG test roots, logging/health/supervisor foundations, deterministic controls, CI, and provenance scaffolding described here. It may not implement the remembered-interaction/shadow-help behavior merely because those shells exist. EXP-00 blocks production `companion-core`, `care-core`, and `identity-consent-vault` implementation until the Architect approves a language/toolchain; language-neutral contracts and foundation work may proceed only within an explicit Phase 01 directive.

The remembered-interaction plus shadow-help work is a later cross-phase milestone requiring separately authorized Phase 02, 03, 04, and 10 contributions. Its completion would prove a bounded architecture integration only and would not complete any contributing roadmap phase.

## Artifacts and retention

- Presubmit: bounded logs/JUnit/schema reports retained long enough for review; no private payload.
- Accepted release candidate: source commit, build inputs, binary/assets, checksums/signatures, migrations, schemas/policies, test/evidence index, SPDX or CycloneDX BOM with separate model/data/voice/asset/service fields, vulnerability/license report, and SLSA 1.2-compatible provenance.
- Safety qualification and migration/restore/fault evidence is immutable and retention-governed. Raw test media is not retained unless licensed, synthetic, necessary, and explicitly authorized.

## Migration/release

- Every store schema has monotonic version, compatibility window, canonicalization/digest version, forward migration, preflight, consistent backup, resumption journal, and rollback/recovery procedure.
- Release candidates are built from clean reviewed commits, reproduce from declared inputs, sign artifacts/manifests, verify before install, stage separately, run compatibility/health checks, and retain last-known-good rollback.
- Code, policy, model, data, voice, asset, plugin, and service changes are independently visible; a code-only version cannot hide a model/policy change.
- Claims are generated from a reviewed capability/evidence matrix, not feature presence.

## Clean-clone acceptance

A fresh isolated checkout with only documented prerequisites must: verify locks/signatures; build without network after the declared restore stage; leave the checkout clean except documented ignored outputs; run all non-hardware tests; generate reproducible canonical event bytes/hashes or document unrelated nondeterminism; emit BOM/provenance/license reports; reject missing/unlocked inputs; and contain no personal/global-machine dependency. Target-host tests and Architect acceptance remain separate.

## Evidence-floor escalation

The cross-phase milestone's 100 replay/restart cases, 1,000 cycles, and 30-minute run are provisional minimum engineering floors. CI must distribute them across multiple seeds, organism/state boundaries, schema versions and invalid messages, persisted start states, boot epochs, and before/during/after-commit kill points; property/randomized failures retain exact seeds. These checks can expose deterministic recovery, bounded-loop, and immediate liveness/resource defects, but cannot establish statistical reliability, safety efficacy, long endurance, or an SLA. Separate later gates cover 24-hour/multi-day soak, target media, shadow safety, accessibility, controlled pilot, and operational evidence.
