#!/usr/bin/env python3
"""Semantic schema/Rust compatibility crosswalk.

This gate intentionally checks the contract surface, not product behavior.
Rust fields may contain additional optional fields, while every schema
required field must have a matching Rust field and compatible coarse type.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
mapping = {
    "event-envelope.schema.json": "EventEnvelope",
    "readiness.schema.json": "Readiness",
    "health.schema.json": "HealthSnapshot",
    "ordinary-observation.schema.json": "OrdinaryObservation",
    "safety-candidate.schema.json": "SafetyCandidate",
    "care-receipt.schema.json": "CareReceipt",
    "embodiment-intent.schema.json": "EmbodimentIntent",
    "vault-decision.schema.json": "VaultDecision",
    "backup-manifest.schema.json": "BackupManifest",
    "mon-animation-track.schema.json": "MonAnimationTrack",
}
text = (ROOT / "crates/foundation-core/src/contracts.rs").read_text(encoding="utf-8")
errors = []

def rust_fields(name):
    match = re.search(rf"pub struct\s+{name}\s*\{{(?P<body>.*?)\n\}}", text, re.S)
    if not match:
        errors.append(f"missing Rust type {name}")
        return {}
    return dict(re.findall(r"\s*pub\s+(\w+)\s*:\s*([^,]+),", match.group("body")))

def compatible(spec, rust_type):
    rust_type = rust_type.strip()
    if "format" in spec and spec["format"] == "uuid":
        return "Uuid" in rust_type
    typ = spec.get("type")
    if typ == "boolean": return rust_type == "bool"
    if typ == "integer": return any(token in rust_type for token in ("u8", "u16", "u32", "u64", "i32", "i64"))
    if typ == "object": return "Value" in rust_type or "Map" in rust_type
    if typ == "string": return "String" in rust_type or "str" in rust_type
    if isinstance(typ, list): return "Option" in rust_type
    if "anyOf" in spec: return "Option" in rust_type or "String" in rust_type
    return True

for schema_name, rust_name in mapping.items():
    schema = json.loads((ROOT / "contracts/schemas" / schema_name).read_text(encoding="utf-8"))
    fields = rust_fields(rust_name)
    for required in schema.get("required", []):
        rust_type = fields.get(required)
        if rust_type is None:
            errors.append(f"{schema_name}: missing required Rust field {required}")
        elif not compatible(schema.get("properties", {}).get(required, {}), rust_type):
            errors.append(f"{schema_name}: type mismatch {required}: {rust_type}")
    for key, spec in schema.get("properties", {}).items():
        if key in fields and not compatible(spec, fields[key]):
            errors.append(f"{schema_name}: type mismatch {key}: {fields[key]}")
    if schema.get("additionalProperties") is not False:
        errors.append(f"{schema_name}: additionalProperties must be false")

if errors:
    print("\n".join(f"ERROR {item}" for item in errors), file=sys.stderr)
    raise SystemExit(1)
print(f"contract_semantic_crosswalk_ok count={len(mapping)} required_fields_and_types=checked")
