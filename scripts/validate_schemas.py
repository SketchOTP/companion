#!/usr/bin/env python3
"""Dependency-free structural validation for the committed Phase 01 schemas."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
required = {"event-envelope.schema.json", "readiness.schema.json", "health.schema.json",
            "ordinary-observation.schema.json", "safety-candidate.schema.json", "care-receipt.schema.json",
            "embodiment-intent.schema.json", "vault-decision.schema.json", "backup-manifest.schema.json"}
errors = []
for name in sorted(required):
    path = ROOT / "contracts" / "schemas" / name
    try: doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: errors.append(f"{name}: {exc}"); continue
    if doc.get("$schema") != "https://json-schema.org/draft/2020-12/schema": errors.append(f"{name}: not Draft 2020-12")
    if doc.get("type") != "object" or doc.get("additionalProperties") is not False: errors.append(f"{name}: unsafe object policy")
try:
    event = json.loads((ROOT / "contracts" / "fixtures" / "event-v1.json").read_text(encoding="utf-8"))
    if event.get("schema_major") != 1: errors.append("event fixture schema_major")
    try:
        import jsonschema
        schema = json.loads((ROOT / "contracts" / "schemas" / "event-envelope.schema.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(event)
        print("jsonschema_event_ok")
    except ImportError:
        print("jsonschema_unavailable_structural_checks_only")
except Exception as exc: errors.append(f"fixture: {exc}")
if errors:
    for error in errors: print(f"ERROR {error}", file=sys.stderr)
    raise SystemExit(1)
print(f"schemas_ok count={len(required)} fixture=event-v1.json")
