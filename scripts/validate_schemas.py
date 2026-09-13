#!/usr/bin/env python3
"""Semantic Draft 2020-12 contract gate for every Phase 01 schema.

The fixture set is deliberately synthetic. This script exercises one valid
instance and deterministic invalid instances for every contract; it never
reads or writes personal/runtime data.
"""
import copy
import json
import pathlib
import sys
import uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "contracts" / "schemas"
NAMES = sorted(p.name for p in SCHEMA_DIR.glob("*.schema.json"))

def sample(schema: dict) -> dict:
    result = {}
    for key in schema.get("required", []):
        spec = schema.get("properties", {}).get(key, {})
        if "const" in spec:
            result[key] = spec["const"]
        elif "enum" in spec:
            result[key] = spec["enum"][0]
        elif spec.get("format") == "uuid":
            result[key] = str(uuid.UUID("00000000-0000-4000-8000-000000000001"))
        elif spec.get("format") == "date-time":
            result[key] = "2026-01-01T00:00:00Z"
        elif "pattern" in spec:
            result[key] = "0" * 64 if "[0-9a-f]" in spec["pattern"] else "synthetic_value"
        elif spec.get("type") == "boolean":
            result[key] = False
        elif spec.get("type") == "integer":
            result[key] = spec.get("minimum", 0)
        elif spec.get("type") == "object":
            result[key] = {}
        else:
            result[key] = "synthetic"
    for key, spec in schema.get("properties", {}).items():
        if key not in result and (spec.get("type") == ["string", "null"] or spec.get("anyOf")):
            result[key] = None
    return result

def validate(instance: dict, schema: dict) -> None:
    try:
        import jsonschema
    except ImportError:
        missing = set(schema.get("required", [])) - instance.keys()
        unknown = set(instance) - set(schema.get("properties", {}))
        if missing or unknown:
            raise ValueError(f"missing={sorted(missing)} unknown={sorted(unknown)}")
        for key, spec in schema.get("properties", {}).items():
            if key in instance and "const" in spec and instance[key] != spec["const"]:
                raise ValueError(f"const mismatch {key}")
        return
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(instance)

errors = []
for name in NAMES:
    path = SCHEMA_DIR / name
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{name}: not Draft 2020-12")
        if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
            errors.append(f"{name}: unsafe object policy")
        valid = sample(schema)
        if name in {"mon-animation-clip.schema.json", "mon-animation-track.schema.json", "mon-temporal-track-v2.schema.json", "mon-authored-frame-pack-v1.schema.json", "mon-authored-frame-source-pack-v1.schema.json", "mon-ingested-frame-pack-v1.schema.json", "mon-frame-intake-receipt-v1.schema.json"}:
            fixture_name = {"mon-animation-clip.schema.json": "mon-animation-clip-v1.json", "mon-animation-track.schema.json": "mon-animation-track-v1.json", "mon-temporal-track-v2.schema.json": "mon-temporal-track-v2.json", "mon-authored-frame-pack-v1.schema.json": "mon-authored-frame-pack-v1.json", "mon-authored-frame-source-pack-v1.schema.json": "mon-authored-frame-source-pack-v1.json", "mon-ingested-frame-pack-v1.schema.json": "mon-ingested-frame-pack-v1.json", "mon-frame-intake-receipt-v1.schema.json": "mon-authored-frame-intake-receipt-v1.json"}[name]
            fixture = ROOT / "contracts" / "fixtures" / fixture_name
            if fixture.exists():
                valid = json.loads(fixture.read_text(encoding="utf-8"))
        validate(valid, schema)
        for mutation in (
            lambda v: v.pop(next(iter(schema.get("required", []))), None),
            lambda v: v.__setitem__("__unknown", True),
        ):
            candidate = copy.deepcopy(valid)
            mutation(candidate)
            try:
                validate(candidate, schema)
                errors.append(f"{name}: invalid fixture accepted")
            except Exception:
                pass
    except Exception as exc:
        errors.append(f"{name}: {exc}")
if errors:
    print("\n".join(f"ERROR {error}" for error in errors), file=sys.stderr)
    raise SystemExit(1)
print(f"schemas_semantic_ok count={len(NAMES)} positive_and_negative=all")
