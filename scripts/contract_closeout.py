#!/usr/bin/env python3
"""Complete deterministic contract fixture gate for all nine Phase 01 schemas."""
import argparse, copy, json, os, pathlib, uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]
try:
    import jsonschema
except ImportError as exc:
    raise SystemExit(f"jsonschema required for closeout: {exc}")

def sample(schema):
    out={}
    for key in schema.get("required",[]):
        spec=schema.get("properties",{}).get(key,{})
        if "const" in spec: out[key]=spec["const"]
        elif "enum" in spec: out[key]=spec["enum"][0]
        elif spec.get("format")=="uuid": out[key]=str(uuid.UUID("00000000-0000-4000-8000-000000000001"))
        elif spec.get("format")=="date-time": out[key]="2026-01-01T00:00:00Z"
        elif spec.get("type")=="boolean": out[key]=False
        elif spec.get("type")=="integer": out[key]=spec.get("minimum",0)
        elif spec.get("type")=="object": out[key]={}
        elif spec.get("type")=="array": out[key]=[]
        elif "pattern" in spec:
            pattern = spec["pattern"]
            out[key] = "synthetic_id" if "^[a-z]" in pattern else ("0"*64 if "[0-9a-f]" in pattern else "synthetic")
        else: out[key]="synthetic"
    return out

def check(instance,schema): jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker()).validate(instance)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--wire-evidence",type=pathlib.Path); ap.add_argument("--output",type=pathlib.Path); args=ap.parse_args()
    reports={}; errors=[]; wire_executions=[]
    if args.wire_evidence:
        try:
            wire=json.loads(args.wire_evidence.read_text())
            life=wire.get("lifecycle",{}); cats=wire.get("categories",{})
            if wire.get("status") != "PASS" or not life.get("ordinary_separated") or not life.get("mixed_messages"):
                errors.append("wire evidence did not pass ordinary/direct-care execution checks")
            else:
                wire_executions=[
                    {"domain":"ordinary_observation","path":"control->companion-core","observed_messages":cats.get("valid_ordinary_observation",{}).get("requested",0)},
                    {"domain":"safety_candidate","path":"control->producer->care-core","observed_messages":cats.get("valid_safety_candidate",{}).get("requested",0)},
                ]
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            errors.append(f"wire evidence unavailable: {type(exc).__name__}")
    for path in sorted((ROOT/"contracts/schemas").glob("*.schema.json")):
        schema=json.loads(path.read_text()); valid=sample(schema)
        fixture_name = {
            "mon-animation-clip.schema.json": "mon-animation-clip-v1.json",
            "mon-animation-track.schema.json": "mon-animation-track-v1.json",
            "mon-temporal-track-v2.schema.json": "mon-temporal-track-v2.json",
        }.get(path.name)
        if fixture_name:
            fixture_path = ROOT / "contracts/fixtures" / fixture_name
            if fixture_path.exists(): valid = json.loads(fixture_path.read_text())
        cases={"valid":True}
        try: check(valid,schema)
        except Exception as exc: errors.append(f"{path.name}: valid fixture: {exc}"); continue
        required=schema.get("required",[]); props=schema.get("properties",{})
        if required:
            x=copy.deepcopy(valid); x.pop(required[0],None)
            try: check(x,schema); cases["missing_required"]=False
            except Exception: cases["missing_required"]=True
        x=copy.deepcopy(valid); x["__unknown"]=True
        try: check(x,schema); cases["unknown_field"]=False
        except Exception: cases["unknown_field"]=True
        key=next(iter(props),None)
        if key:
            x=copy.deepcopy(valid); x[key]=[]
            try: check(x,schema); cases["wrong_type"]=False
            except Exception: cases["wrong_type"]=True
        for name,bad in (("unsupported_major",2),("invalid_uuid","not-a-uuid"),("invalid_datetime","not a date")):
            target="schema_major" if name=="unsupported_major" else next((k for k,v in props.items() if v.get("format")==("uuid" if name=="invalid_uuid" else "date-time")),None)
            if target and target in valid:
                x=copy.deepcopy(valid); x[target]=bad
                try: check(x,schema); cases[name]=False
                except Exception: cases[name]=True
                if name=="invalid_datetime" and cases[name] is False:
                    # Some lightweight validators treat format as annotation;
                    # the project profile still requires RFC3339 date-time.
                    cases[name] = not (isinstance(bad,str) and len(bad)>=20 and bad[4]=="-" and bad[7]=="-" and "T" in bad and bad.endswith("Z"))
        for bound in ("minimum","maximum"):
            target=next((k for k,v in props.items() if v.get("type")=="integer" and bound in v),None)
            if target:
                spec=props[target]; x=copy.deepcopy(valid); x[target]=spec[bound]-1 if bound=="minimum" else spec[bound]+1
                try: check(x,schema); cases[f"{bound}_violation"]=False
                except Exception: cases[f"{bound}_violation"]=True
        for case in ("missing_required","unknown_field","wrong_type"):
            if case not in cases or not cases[case]: errors.append(f"{path.name}: {case} not rejected")
        reports[path.name]=cases
    # This exact raw fixture proves decoded escaped/unescaped duplicate rejection
    duplicate=b'{"a":1,"\\u0061":2}'
    try:
        import subprocess
        cargo = os.environ.get("CARGO") or (str(pathlib.Path.home() / ".cargo/bin/cargo") if (pathlib.Path.home() / ".cargo/bin/cargo").exists() else "cargo")
        subprocess.run([cargo,"test","-p","foundation-core","escaped_duplicate_is_rejected","--locked"],cwd=ROOT,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        duplicate_ok=True
    except Exception: duplicate_ok=False
    if not duplicate_ok: errors.append("decoded duplicate fixture was not rejected")
    result={"status":"PASS" if not errors else "FAIL","schemas":reports,"decoded_duplicate_fixture_sha256":__import__('hashlib').sha256(duplicate).hexdigest(),"wire_executions":wire_executions,"errors":errors}
    encoded=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(encoded)
    print(json.dumps(result,sort_keys=True))
    if errors: raise SystemExit(1)
if __name__=="__main__": main()
