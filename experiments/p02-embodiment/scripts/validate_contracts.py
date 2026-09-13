#!/usr/bin/env python3
"""Draft 2020-12 and Rust-facing Phase 02 contract gate."""
from __future__ import annotations
import copy, json, sys, uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
try:
    import jsonschema
except ImportError:
    jsonschema=None

def sample(spec, root=None):
    root = root or spec
    if "$ref" in spec:
        target = root
        for part in spec["$ref"].removeprefix("#/").split("/"):
            target = target[part]
        return sample(target, root)
    if "anyOf" in spec:
        return sample(spec["anyOf"][0], root)
    if "oneOf" in spec:
        branch = dict(spec["oneOf"][0])
        branch.setdefault("required", spec.get("required", []))
        return sample(branch, root)
    if "const" in spec: return spec["const"]
    if "enum" in spec: return spec["enum"][0]
    if spec.get("format")=="uuid": return "00000000-0000-4000-8000-000000000001"
    if spec.get("format")=="date-time": return "2026-01-01T00:00:00Z"
    if "pattern" in spec:
        pattern = spec["pattern"]
        if "sources/sha256/" in pattern: return "sources/sha256/00/" + "0" * 64 + ".png"
        if "^runtime/frames/" in pattern: return "runtime/frames/test_pulse.png"
        if "[0-9a-f]" in pattern: return "0" * 64
        if "^frames/" in pattern: return "frames/test_pulse__front__neutral__v01__f000.png"
        if "frame\\\\.json" in pattern or "frame\\.json" in pattern: return "test_pulse__front__neutral__v01__f000.frame.json"
        if "__" in pattern and "\\.png" in pattern: return "test_pulse__front__neutral__v01__f000.png"
        if "\\.png" in pattern: return "test_pulse.png"
        if "track_id" in pattern: return "synthetic:test_pulse:front:neutral:1"
    typ=spec.get("type")
    if isinstance(typ,list): typ=next((x for x in typ if x!="null"),"string")
    if typ=="object" or "properties" in spec: return {k:sample(v, root) for k,v in spec.get("properties",{}).items() if k in spec.get("required",[])}
    if typ=="array":
        if spec.get("prefixItems"): return [sample(item, root) for item in spec["prefixItems"]]
        return [sample(spec.get("items",{}), root)]
    if typ=="integer": return spec.get("minimum", 0)
    if typ=="number": return spec.get("exclusiveMinimum", spec.get("minimum", 0)) + (1 if "exclusiveMinimum" in spec else 0)
    if typ=="boolean": return False
    return "synthetic"

def validate(value,schema):
    if jsonschema: jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker()).validate(value)
    else:
        missing=set(schema.get("required",[]))-set(value); unknown=set(value)-set(schema.get("properties",{}))
        if missing or unknown: raise ValueError(f"missing={missing} unknown={unknown}")

def main():
    errors=[]; tested=0
    for p in sorted((ROOT/"contracts/schemas").glob("*.schema.json")):
        schema=json.loads(p.read_text()); tested+=1
        if schema.get("$schema")!="https://json-schema.org/draft/2020-12/schema" or schema.get("additionalProperties") is not False: errors.append(f"unsafe {p.name}"); continue
        valid=sample(schema, schema)
        if p.name=="mon-animation-clip.schema.json": valid=json.loads((ROOT/"contracts/fixtures/mon-animation-clip-v1.json").read_text())
        try: validate(valid,schema)
        except Exception as e: errors.append(f"valid {p.name}: {e}"); continue
        if schema.get("required"):
            missing=copy.deepcopy(valid); missing.pop(schema["required"][0],None)
            try: validate(missing,schema); errors.append(f"missing accepted {p.name}")
            except Exception: pass
        unknown=copy.deepcopy(valid); unknown["__unknown"]=True
        try: validate(unknown,schema); errors.append(f"unknown accepted {p.name}")
        except Exception: pass
    result={"status":"PASSED" if not errors else "FAILED","schemas_tested":tested,"negative_cases":"missing_required_and_unknown_field","rust_fixture":"contracts/fixtures/mon-animation-clip-v1.json","errors":errors}
    print(json.dumps(result,sort_keys=True)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
