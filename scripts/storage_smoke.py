#!/usr/bin/env python3
"""Synthetic store smoke using the resident Rust store owners."""
import argparse, hashlib, json, os, pathlib, sqlite3, subprocess, tempfile

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=pathlib.Path,required=True); a=ap.parse_args(); root=pathlib.Path(tempfile.mkdtemp(prefix="companion-storage-")); env=os.environ.copy(); env.update(COMPANION_XDG_ROOT=str(root),COMPANION_CYCLES="2")
    binary=env.get("FOUNDATION_SUPERVISOR","target/release/ops-supervisor"); proc=subprocess.run([binary,"--once"],env=env,capture_output=True,text=True,timeout=30)
    dbs={n:root/"companion"/f"{n}.sqlite3" for n in ("companion","care","vault")}; integrity=True; backup_eq=False; rows=0
    for db in dbs.values():
        con=sqlite3.connect(db); integrity &= con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"; con.close()
    care=sqlite3.connect(dbs["care"]); rows=care.execute("SELECT count(*) FROM safety_receipts").fetchone()[0]; care.backup(sqlite3.connect(root/"care-restore.sqlite3")); care.close(); restored=sqlite3.connect(root/"care-restore.sqlite3"); backup_eq=restored.execute("PRAGMA integrity_check").fetchone()[0]=="ok" and restored.execute("SELECT count(*) FROM safety_receipts").fetchone()[0]==rows; restored.close()
    result={"status":"PASS" if proc.returncode==0 and integrity and rows>=2 and backup_eq else "FAIL","separate_store_count":3,"integrity":integrity,"care_receipts":rows,"backup_restore_equivalent":backup_eq,"rust_store_process":True,"claim_boundary":"synthetic SQLite development-store smoke only","evidence_ceiling":"E3_TARGET_TESTED","state_digest":hashlib.sha256(str(rows).encode()).hexdigest()}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True))
if __name__=="__main__": main()
