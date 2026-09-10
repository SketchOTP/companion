#!/usr/bin/env python3
"""Assert the synthetic packet crosses the supervisor's real child socket."""
import argparse, json, os, pathlib, subprocess, tempfile
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output", type=pathlib.Path, required=True); a=ap.parse_args()
    root=pathlib.Path(tempfile.mkdtemp(prefix="companion-care.")); env=os.environ.copy(); env["COMPANION_XDG_ROOT"]=str(root); env["COMPANION_SKIP_COMPANION"]="1"
    proc=subprocess.run([env.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor"),"--once"],env=env,capture_output=True,text=True,timeout=30)
    lines=proc.stdout.splitlines(); accepted=any('"care_receipt"' in line for line in lines); duplicate=any('"duplicate":true' in line for line in lines); ready={role:any(f'"process":"{role}"' in line and '"event":"ready"' in line for line in lines) for role in ("care-core","identity-consent-vault","sensor-gateway","godot-bridge")}
    no_companion=not any('"process":"companion-core"' in line and '"event":"ready"' in line for line in lines)
    result={"status":"PASS" if proc.returncode==0 and accepted and duplicate and all(ready.values()) and no_companion else "FAIL","returncode":proc.returncode,"roles_ready":ready,"actual_socket_packet":accepted,"duplicate_idempotency":duplicate,"companion_store_optional":no_companion,"claim_boundary":"synthetic direct-care transport only","evidence_ceiling":"E3_TARGET_TESTED"}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True))
if __name__ == "__main__": main()
