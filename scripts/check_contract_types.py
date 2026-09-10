#!/usr/bin/env python3
"""Deterministic schema/Rust crosswalk gate (no generated code)."""
import json, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
mapping={"event-envelope.schema.json":"EventEnvelope","readiness.schema.json":"Readiness","health.schema.json":"HealthSnapshot","ordinary-observation.schema.json":"OrdinaryObservation","safety-candidate.schema.json":"SafetyCandidate","care-receipt.schema.json":"CareReceipt","embodiment-intent.schema.json":"EmbodimentIntent","vault-decision.schema.json":"VaultDecision","backup-manifest.schema.json":"BackupManifest"}
text=(ROOT/"crates/foundation-core/src/contracts.rs").read_text(encoding="utf-8"); errors=[]
for schema, typ in mapping.items():
    doc=json.loads((ROOT/"contracts/schemas"/schema).read_text(encoding="utf-8"));
    if doc.get("$schema")!="https://json-schema.org/draft/2020-12/schema": errors.append(f"{schema}: schema draft")
    if not re.search(rf"struct\s+{typ}\b",text): errors.append(f"{schema}: missing Rust type {typ}")
if errors: print("\n".join(errors),file=sys.stderr); raise SystemExit(1)
print(f"contract_type_crosswalk_ok count={len(mapping)}")
