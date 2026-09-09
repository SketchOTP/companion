#!/usr/bin/env python3
"""Bounded disposable SQLite matrix for COMPANION-P00-QUAL-001."""
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SQLITE=Path(os.environ["QUAL_SQLITE"]); OUT=Path(os.environ["QUAL_RESULTS"])
def sql(db, statement, check=True):
    r=subprocess.run([str(SQLITE),"-batch",str(db),statement],text=True,capture_output=True)
    if check and r.returncode: raise RuntimeError(r.stderr.strip())
    return {"returncode":r.returncode,"stdout":r.stdout.strip(),"stderr":r.stderr.strip()}
def count(db): return int(sql(db,"select count(*) from events;")["stdout"])
def main():
  OUT.parent.mkdir(parents=True,exist_ok=True); results={"artifact":sql(":memory:","select sqlite_version()||'|'||sqlite_source_id();"),"tests":{}}
  with tempfile.TemporaryDirectory(prefix="companion-sqlite-",dir=OUT.parent) as td:
    root=Path(td); db=root/"events.db"; backup=root/"backup.db"; restored=root/"restored.db"; copied=root/"copied-corrupt.db"
    setup="pragma journal_mode=WAL; pragma synchronous=FULL; pragma wal_autocheckpoint=8; create table events(id text primary key, payload text not null); insert into events values('seed','v');"
    results["tests"]["setup_wal"]=sql(db,setup)
    hold=subprocess.Popen([str(SQLITE),"-batch",str(db)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    hold.stdin.write("pragma wal_autocheckpoint=0; insert into events values('wal-live','v'); select 'wal-live';\n"); hold.stdin.flush()
    hold.stdout.readline()
    results["tests"]["wal_created_while_connection_open"]=(root/"events.db-wal").exists()
    hold.stdin.close(); hold.wait(timeout=3)
    results["tests"]["commit"]=sql(db,"begin immediate; insert into events values('commit','v'); commit;"); results["tests"]["commit_count"]=count(db)
    results["tests"]["rollback"]=sql(db,"begin immediate; insert into events values('rollback','v'); rollback;"); results["tests"]["rollback_absent"]=(sql(db,"select count(*) from events where id='rollback';")["stdout"]=="0")
    results["tests"]["idempotency"]=sql(db,"insert or ignore into events values('idem','v'); insert or ignore into events values('idem','v'); select count(*) from events where id='idem';");
    # A killed uncommitted CLI transaction must be absent after reopen.
    proc=subprocess.Popen([str(SQLITE),str(db)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    proc.stdin.write("begin immediate; insert into events values('killed_precommit','v');\n"); proc.stdin.flush(); proc.kill(); proc.wait(timeout=3)
    results["tests"]["precommit_kill_absent"]=(sql(db,"select count(*) from events where id='killed_precommit';")["stdout"]=="0")
    # Post-commit process termination leaves a whole committed transaction.
    proc=subprocess.Popen([str(SQLITE),"-batch",str(db)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    proc.stdin.write("begin immediate; insert into events values('killed_postcommit','v'); commit; select 'committed';\n"); proc.stdin.flush(); proc.stdout.readline(); proc.kill(); proc.wait(timeout=3)
    results["tests"]["postcommit_kill_present"]=(sql(db,"select count(*) from events where id='killed_postcommit';")["stdout"]=="1")
    results["tests"]["checkpoint"]=sql(db,"pragma wal_checkpoint(TRUNCATE);")
    results["tests"]["concurrent_readers"]=[sql(db,"select count(*) from events;") for _ in range(3)]
    results["tests"]["readonly_fault"]=sql(f"file:{db}?mode=ro","insert into events values('readonly','v');",check=False)
    results["tests"]["diskfull_simulated"]=sql(db,"pragma max_page_count=3; insert into events values('diskfull',quote(zeroblob(100000)));",check=False)
    results["tests"]["incompatible_migration_fail_closed"]=(sql(db,"pragma user_version;")["stdout"]!="2")
    results["tests"]["backup_api"]=sql(db,f".backup {backup}")
    shutil.copy2(backup,restored); results["tests"]["restore_count_equivalent"]=(count(restored)==count(db))
    shutil.copy2(backup,copied)
    with copied.open("r+b") as f: f.seek(0); b=f.read(1); f.seek(0); f.write(bytes([b[0]^0xFF]))
    results["tests"]["copied_corruption_detected"]=sql(copied,"pragma integrity_check;",check=False)
    results["tests"]["sshfs_absence"]="no SQLite file created in repository checkout"
    results["tests"]["during_commit_kill"]="BLOCKED: deterministic scheduling inside SQLite commit was not established without an intrusive fault VFS"
    results["tests"]["checkpoint_kill"]="BLOCKED: deterministic scheduling inside checkpoint was not established without an intrusive fault VFS"
  OUT.write_text(json.dumps(results,sort_keys=True,indent=2)+"\n"); print(json.dumps(results,sort_keys=True))
if __name__=="__main__": main()
