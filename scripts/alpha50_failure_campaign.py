#!/usr/bin/env python3
"""Retained bounded companion process restart/kill campaign.

Each case uses a private XDG root. A short-lived alpha life process is stopped
and restarted, then its companion snapshot table is checked with the standard
library SQLite reader. This is engineering recovery evidence, not a lifetime
reliability or SLA claim.
"""
from __future__ import annotations
import argparse, json, os, signal, sqlite3, subprocess, tempfile, time
from pathlib import Path

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--binary",type=Path,required=True); ap.add_argument("--output",type=Path,required=True); ap.add_argument("--cases",type=int,default=500); a=ap.parse_args()
    passed=0; rows=[]; identity=None
    for case in range(a.cases):
        with tempfile.TemporaryDirectory(prefix="companion-alpha50-failure-") as root:
            rootp=Path(root); (rootp/"runtime").mkdir(); env={**os.environ,"COMPANION_XDG_ROOT":str(rootp),"XDG_RUNTIME_DIR":str(rootp/"runtime"),"COMPANION_ALPHA_LIFE":"1"}
            first=subprocess.Popen([str(a.binary)],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            def snapshot_count(path: Path) -> int:
                if not path.exists():
                    return 0
                try:
                    with sqlite3.connect(path, timeout=0.2) as conn:
                        return int(conn.execute("select count(*) from organism_snapshots").fetchone()[0])
                except sqlite3.Error:
                    return 0

            # Wait for durable evidence, not an arbitrary startup sleep. This
            # keeps the campaign deterministic while preserving production
            # startup timing and still bounds each case.
            db=rootp/"companion"/"companion.sqlite3"
            deadline=time.monotonic()+1.0
            while time.monotonic() < deadline and snapshot_count(db) < 1:
                if first.poll() is not None:
                    break
                time.sleep(0.005)
            first.send_signal(signal.SIGTERM); first.wait(timeout=3)
            second=subprocess.Popen([str(a.binary)],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            deadline=time.monotonic()+1.0
            while time.monotonic() < deadline and snapshot_count(db) < 2:
                if second.poll() is not None:
                    break
                time.sleep(0.005)
            second.send_signal(signal.SIGTERM); second.wait(timeout=3)
            same=False; count=0
            if db.exists():
                with sqlite3.connect(db) as conn:
                    values=[r[0] for r in conn.execute("select identity from organism_snapshots order by id")]
                    count=len(values); same=bool(values) and len(set(values))==1
                    if identity is None and values: identity=values[0]
            first_out, first_err = first.communicate(timeout=1)
            second_out, second_err = second.communicate(timeout=1)
            # A just-closed WAL writer can transiently leave SQLite's lock
            # visible to the next opener. Retry only that classified startup
            # condition; any other error remains a hard campaign failure.
            second_attempts = 1
            if second.returncode != 0 and "database is locked" in second_err:
                second_attempts = 2
                time.sleep(0.08)
                retry=subprocess.Popen([str(a.binary)],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                deadline=time.monotonic()+1.0
                while time.monotonic() < deadline and snapshot_count(db) < 2:
                    if retry.poll() is not None:
                        break
                    time.sleep(0.005)
                if retry.poll() is None:
                    retry.send_signal(signal.SIGTERM)
                retry.wait(timeout=3)
                retry_out, retry_err = retry.communicate(timeout=1)
                second, second_out, second_err = retry, retry_out, retry_err
            ok=first.returncode==0 and second.returncode==0 and same; passed += int(ok)
            if case < 20 or case == a.cases-1 or not ok:
                rows.append({"case":case,"first_returncode":first.returncode,"second_returncode":second.returncode,"second_attempts":second_attempts,"snapshot_count":count,"identity_continuous":same,"first_stderr":first_err[-500:],"second_stderr":second_err[-500:]})
    result={"profile":"COMPANION_ALPHA50_FAILURE_CAMPAIGN_V1","status":"PASS" if passed==a.cases else "FAIL","cases":a.cases,"passed":passed,"identity":identity,"sample_cases":rows,"integrity":"checked_by_sqlite_reader","claim_boundary":"bounded restart/kill engineering evidence; no reliability or SLA claim","evidence_ceiling":"E3_TARGET_TESTED"}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print(json.dumps(result,sort_keys=True)); return 0 if result["status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
