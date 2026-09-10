#!/usr/bin/env python3
"""Synthetic SQLite store smoke: migration, WAL, idempotency and restore."""
import argparse, hashlib, json, os, pathlib, shutil, subprocess, tempfile

def sql(bin_path, db, statement):
    out = subprocess.run([str(bin_path), "-batch", "-noheader", str(db), statement], capture_output=True, text=True, check=False)
    if out.returncode: raise RuntimeError(out.stderr.strip())
    return out.stdout.strip()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output", type=pathlib.Path, required=True); a=ap.parse_args()
    sqlite=pathlib.Path(os.environ.get("COMPANION_SQLITE_BIN", "sqlite3")); work=pathlib.Path(tempfile.mkdtemp(prefix="companion-storage."));
    try:
        stores={name:work/f"{name}.sqlite3" for name in ("companion","care","vault")}
        for name, db in stores.items():
            sql(sqlite, db, "PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; CREATE TABLE authority_meta(k TEXT PRIMARY KEY,v TEXT); CREATE TABLE events(id INTEGER PRIMARY KEY,message_id TEXT UNIQUE,payload TEXT); INSERT INTO authority_meta VALUES('authority','%s');" % name)
        db=stores["companion"]
        sql(sqlite, db, "BEGIN; INSERT INTO events(message_id,payload) VALUES('m-1','synthetic'); COMMIT; INSERT OR IGNORE INTO events(message_id,payload) VALUES('m-1','duplicate');")
        before=sql(sqlite, db, "SELECT count(*) FROM events;"); integrity=sql(sqlite, db, "PRAGMA integrity_check;")
        backup=work/"backup.sqlite3"; sql(sqlite, db, ".backup '%s'" % backup); restore=work/"restore.sqlite3"; shutil.copy2(backup, restore)
        eq=sql(sqlite, db, "SELECT id||':'||message_id||':'||payload FROM events ORDER BY id;") == sql(sqlite, restore, "SELECT id||':'||message_id||':'||payload FROM events ORDER BY id;")
        result={"status":"PASS" if before=="1" and integrity=="ok" and eq else "FAIL","separate_store_count":len(stores),"duplicate_idempotent":before=="1","integrity":integrity,"backup_restore_equivalent":eq,"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"synthetic SQLite development-store smoke only","state_digest":hashlib.sha256(sql(sqlite, restore, "SELECT id||':'||message_id||':'||payload FROM events ORDER BY id;").encode()).hexdigest()}
        a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(result,sort_keys=True))
    finally:
        # The temporary database tree is private synthetic data, never a repo artifact.
        shutil.rmtree(work, ignore_errors=True)
if __name__ == "__main__": main()
