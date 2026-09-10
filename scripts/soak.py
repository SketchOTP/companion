#!/usr/bin/env python3
"""Supervised synthetic soak. Default is the required 60 minutes."""
import argparse, hashlib, json, pathlib, subprocess, time, os
def main():
    p=argparse.ArgumentParser(); p.add_argument("--duration-seconds", type=int, default=3600); p.add_argument("--interval", type=int, default=10); p.add_argument("--output", type=pathlib.Path, required=True); a=p.parse_args()
    if a.duration_seconds < 3600: raise SystemExit("duration must be at least 3600 seconds for the Phase 01 floor")
    start=time.time(); samples=[]; failures=[]; binary=pathlib.Path(os.environ.get("FOUNDATION_SUPERVISOR", "target/release/ops-supervisor"))
    while time.time()-start < a.duration_seconds:
        proc=subprocess.run([str(binary)], capture_output=True, text=True, timeout=30)
        if proc.returncode: failures.append({"returncode":proc.returncode})
        samples.append({"elapsed_seconds":round(time.time()-start,3), "stdout_sha256":hashlib.sha256(proc.stdout.encode()).hexdigest()})
        time.sleep(a.interval)
    result={"status":"PASS" if not failures else "FAIL", "started_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(start)),
            "ended_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()), "duration_seconds":a.duration_seconds,
            "samples":len(samples), "failures":failures, "evidence_ceiling":"E3_TARGET_TESTED", "claim_boundary":"synthetic engineering soak only"}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True))
if __name__ == "__main__": main()
