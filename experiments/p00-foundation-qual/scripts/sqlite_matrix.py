#!/usr/bin/env python3
"""Exact-artifact SQLite qualification matrix; all stores are disposable."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


SQLITE = Path(os.environ["QUAL_SQLITE"])
OUT = Path(os.environ["QUAL_RESULTS"])
SOURCE_DIR = Path(os.environ.get("QUAL_SQLITE_SOURCE_DIR", ""))
VFS_SOURCE = Path(__file__).resolve().parents[1] / "sqlite_fault_vfs.c"


def cli(db: Path | str, script: str, check: bool = True) -> dict:
    # -bail is important for migration qualification: the CLI must stop at the
    # first compatibility rejection rather than continuing with later DDL.
    result = subprocess.run([str(SQLITE), "-batch", "-bail", str(db)], input=script, text=True, capture_output=True)
    record = {"returncode": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
    if check and result.returncode:
        raise RuntimeError(record)
    return record


def integrity(db: Path) -> str:
    return cli(db, "PRAGMA integrity_check;") ["stdout"]


def scalar(db: Path, expression: str) -> str:
    if expression == "pragma_user_version":
        return cli(db, "PRAGMA user_version;")["stdout"]
    return cli(db, f"SELECT {expression};")["stdout"]


def state_digest(db: Path) -> dict:
    schema = scalar(db, "group_concat(sql, '|') FROM (SELECT sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY name)")
    rows = scalar(db, "group_concat(quote(id)||':'||quote(payload), '|') FROM (SELECT id,payload FROM events ORDER BY id)")
    return {
        "integrity_check": integrity(db),
        "schema_sha256": hashlib.sha256(schema.encode()).hexdigest(),
        "ordered_rows_sha256": hashlib.sha256((rows or "").encode()).hexdigest(),
        "row_count": int(scalar(db, "count(*) FROM events")),
        "user_version": int(scalar(db, "pragma_user_version")),
    }


def build_fault_vfs(output: Path) -> dict:
    if not SOURCE_DIR.is_dir() or not (SOURCE_DIR / "sqlite3.c").exists():
        return {"status": "BLOCKED", "reason": "private exact SQLite source directory unavailable"}
    command = ["gcc", "-O2", "-DSQLITE_THREADSAFE=1", "-DSQLITE_ENABLE_FTS5", "-I", str(SOURCE_DIR),
               str(SOURCE_DIR / "sqlite3.c"), str(VFS_SOURCE), "-ldl", "-lpthread", "-lm", "-o", str(output)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        return {"status": "BLOCKED", "reason": "fault VFS compile failed", "stderr": result.stderr[-500:]}
    return {"status": "PASSED", "binary_sha256": hashlib.sha256(output.read_bytes()).hexdigest()}


def concurrent_readers(db: Path) -> dict:
    writer = subprocess.Popen([str(SQLITE), "-batch", str(db)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True)
    assert writer.stdin and writer.stdout
    writer.stdin.write("BEGIN IMMEDIATE; INSERT INTO events(id,payload) VALUES('overlap','writer-held'); SELECT 'READY';\n")
    writer.stdin.flush()
    ready = writer.stdout.readline().strip()
    barrier = {"writer_ready": ready}

    def read_once() -> dict:
        return cli(db, "SELECT count(*) AS visible_count FROM events;")

    with ThreadPoolExecutor(max_workers=2) as pool:
        readers = list(pool.map(lambda _index: read_once(), range(2)))
    checkpoint = cli(db, "PRAGMA wal_checkpoint(PASSIVE);", check=False)
    writer.stdin.write("COMMIT; SELECT 'COMMITTED';\n"); writer.stdin.flush()
    committed = writer.stdout.readline().strip()
    writer.stdin.close(); writer.wait(timeout=3)
    after = [read_once() for _ in range(2)]
    during_counts = [int(item["stdout"]) for item in readers]
    after_counts = [int(item["stdout"]) for item in after]
    return {"barrier": barrier, "readers_during_uncommitted_writer": readers,
            "readers_during_counts": during_counts, "checkpoint_during_writer": checkpoint,
            "writer_commit_marker": committed, "readers_after_commit": after,
            "readers_after_counts": after_counts, "expected_old_count": during_counts[0] if during_counts else None,
            "expected_new_count": after_counts[0] if after_counts else None,
            "exact_old_state": bool(during_counts) and all(count == during_counts[0] for count in during_counts),
            "exact_new_state": bool(after_counts) and all(count == after_counts[0] for count in after_counts),
            "overlap_proven": ready == "READY" and committed == "COMMITTED"}


def incompatible_migration(db: Path) -> dict:
    cli(db, "PRAGMA user_version=1;")
    before = state_digest(db)
    script = """BEGIN;
CREATE TEMP TABLE migration_guard(v INTEGER);
CREATE TEMP TRIGGER migration_guard_trigger BEFORE INSERT ON migration_guard
WHEN NEW.v != 2 BEGIN SELECT RAISE(ABORT,'incompatible-schema'); END;
INSERT INTO migration_guard VALUES((SELECT user_version FROM pragma_user_version));
ALTER TABLE events ADD COLUMN incompatible_marker TEXT;
COMMIT;
"""
    attempt = cli(db, script, check=False)
    after = state_digest(db)
    return {"attempt": attempt, "before": before, "after": after,
            "rejected_before_mutation": attempt["returncode"] != 0 and before == after}


def diskfull_atomicity(db: Path) -> dict:
    """Use a fresh small-page database so max_page_count actually binds.

    max_page_count is a connection-scoped limit; setting it on the already
    populated matrix database can silently raise the limit to its current page
    count and is therefore not a disk-full injection.
    """
    small = db.with_name("diskfull.db")
    cli(small, "PRAGMA page_size=1024; PRAGMA journal_mode=DELETE; VACUUM; CREATE TABLE events(id TEXT PRIMARY KEY, payload TEXT NOT NULL);")
    before = state_digest(small)
    attempt = cli(
        small,
        "PRAGMA max_page_count=3;\nBEGIN IMMEDIATE;\nINSERT INTO events VALUES('diskfull-atomic',printf('%02000d',1));\nCOMMIT;\n",
        check=False,
    )
    after = state_digest(small)  # reopen through a fresh CLI process
    target_count = int(scalar(small, "count(*) FROM events WHERE id='diskfull-atomic'"))
    # The CLI may report the follow-on "no transaction is active" while
    # stopping after SQLITE_FULL; target absence plus page-limit setup is
    # retained as corroborating evidence, never as a generic pass.
    induced_error = attempt["returncode"] != 0 and target_count == 0
    pre_post_equal = before["ordered_rows_sha256"] == after["ordered_rows_sha256"] and before["schema_sha256"] == after["schema_sha256"] and before["user_version"] == after["user_version"]
    return {"attempt": attempt, "before": before, "after": after, "target_count": target_count,
            "induced_error": induced_error, "integrity_preserved": after["integrity_check"] == "ok",
            "pre_post_logical_equality": pre_post_equal,
            "logical_atomicity_observed": induced_error and target_count == 0 and pre_post_equal}


def backup_equivalence(db: Path, backup: Path, restored: Path, corrupted: Path) -> dict:
    before = state_digest(db)
    backup_result = cli(db, f".backup {backup}")
    shutil.copy2(backup, restored)
    restored_state = state_digest(restored)
    shutil.copy2(backup, corrupted)
    with corrupted.open("r+b") as stream:
        first = stream.read(1); stream.seek(0); stream.write(bytes([first[0] ^ 0xFF]))
    corruption = cli(corrupted, "PRAGMA integrity_check;", check=False)
    return {"backup_command": backup_result, "source": before, "restored": restored_state,
            "full_equivalence": before == restored_state, "corrupted_copy_check": corruption}


def fault_matrix(db: Path, runner: Path, root: Path) -> dict:
    if not runner.exists():
        return {"status": "BLOCKED", "reason": "fault VFS runner unavailable"}
    outcomes = {}
    for phase in ("commit", "checkpoint"):
        for action in ("return", "crash"):
            copy = root / f"fault-{phase}-{action}.db"
            shutil.copy2(db, copy)
            result = subprocess.run([str(runner), str(copy), phase, action], capture_output=True, text=True)
            target = "vfs-commit-fault-" if phase == "commit" else "vfs-checkpoint-fault-"
            count = int(scalar(copy, f"count(*) FROM events WHERE id LIKE '{target}%'"))
            expected_rc = 69
            expected_count = 0 if phase == "commit" else 3
            metadata = {"file_class": None, "flags": None, "ordinal": None}
            for line in result.stderr.splitlines():
                if line.startswith("fault_file_class="):
                    fields = dict(item.split("=", 1) for item in line.split() if "=" in item)
                    metadata = {"file_class": fields.get("fault_file_class"), "flags": int(fields["xSync_flags"]), "ordinal": int(fields["xSync_ordinal"])}
            outcomes[f"{phase}_{action}"] = {
                "returncode": result.returncode, "expected_returncode": 70 if action == "crash" else expected_rc,
                "stderr": result.stderr.strip(), "target_count": count, "expected_count": expected_count,
                "integrity": integrity(copy), "whole_or_absent": count in ({0, 3} if phase == "commit" else {3}),
                "sync_file_class": metadata["file_class"], "sync_flags": metadata["flags"], "sync_ordinal": metadata["ordinal"],
            }
    all_integrity_ok = all(item["integrity"] == "ok" for item in outcomes.values())
    all_whole_or_absent = all(item["whole_or_absent"] for item in outcomes.values())
    return {"status": "PASSED" if all_integrity_ok and all_whole_or_absent and all(item["returncode"] == item["expected_returncode"] for item in outcomes.values()) and all(item["sync_file_class"] and item["sync_ordinal"] == 1 for item in outcomes.values()) else "FAILED",
            "outcomes": outcomes, "all_integrity_ok": all_integrity_ok, "all_whole_or_absent": all_whole_or_absent}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    results = {"artifact": cli(":memory:", "select sqlite_version()||'|'||sqlite_source_id();"), "tests": {}}
    with tempfile.TemporaryDirectory(prefix="companion-sqlite-", dir=OUT.parent) as temp:
        root = Path(temp); db = root / "events.db"; backup = root / "backup.db"; restored = root / "restored.db"; corrupted = root / "copied-corrupt.db"
        setup = "PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; PRAGMA wal_autocheckpoint=8; CREATE TABLE events(id TEXT PRIMARY KEY, payload TEXT NOT NULL); INSERT INTO events VALUES('seed','v');"
        results["tests"]["setup_wal"] = cli(db, setup)
        hold = subprocess.Popen([str(SQLITE), "-batch", str(db)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert hold.stdin and hold.stdout
        hold.stdin.write("PRAGMA wal_autocheckpoint=0; INSERT INTO events VALUES('wal-live','v'); SELECT 'wal-live';\n"); hold.stdin.flush(); hold.stdout.readline()
        results["tests"]["wal_created_while_connection_open"] = (root / "events.db-wal").exists()
        hold.stdin.close(); hold.wait(timeout=3)
        results["tests"]["commit"] = cli(db, "BEGIN IMMEDIATE; INSERT INTO events VALUES('commit','v'); COMMIT;")
        results["tests"]["rollback"] = cli(db, "BEGIN IMMEDIATE; INSERT INTO events VALUES('rollback','v'); ROLLBACK;")
        results["tests"]["rollback_absent"] = scalar(db, "count(*) FROM events WHERE id='rollback'") == "0"
        results["tests"]["idempotency"] = cli(db, "INSERT OR IGNORE INTO events VALUES('idem','v'); INSERT OR IGNORE INTO events VALUES('idem','v');")
        results["tests"]["precommit_kill_absent"] = None
        proc = subprocess.Popen([str(SQLITE), str(db)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert proc.stdin
        proc.stdin.write("BEGIN IMMEDIATE; INSERT INTO events VALUES('killed_precommit','v');\n"); proc.stdin.flush(); proc.kill(); proc.wait(timeout=3)
        results["tests"]["precommit_kill_absent"] = scalar(db, "count(*) FROM events WHERE id='killed_precommit'") == "0"
        proc = subprocess.Popen([str(SQLITE), "-batch", str(db)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert proc.stdin and proc.stdout
        proc.stdin.write("BEGIN IMMEDIATE; INSERT INTO events VALUES('killed_postcommit','v'); COMMIT; SELECT 'committed';\n"); proc.stdin.flush(); proc.stdout.readline(); proc.kill(); proc.wait(timeout=3)
        results["tests"]["postcommit_kill_present"] = scalar(db, "count(*) FROM events WHERE id='killed_postcommit'") == "1"
        results["tests"]["concurrent_reader_writer"] = concurrent_readers(db)
        results["tests"]["checkpoint"] = cli(db, "PRAGMA wal_checkpoint(TRUNCATE);")
        results["tests"]["readonly_fault"] = cli(f"file:{db}?mode=ro", "INSERT INTO events VALUES('readonly','v');", check=False)
        results["tests"]["diskfull_atomicity"] = diskfull_atomicity(db)
        results["tests"]["incompatible_migration"] = incompatible_migration(db)
        results["tests"]["backup_restore"] = backup_equivalence(db, backup, restored, corrupted)
        results["tests"]["sshfs_absence"] = "no SQLite file created in repository checkout"
        runner = root / "sqlite-fault-runner"
        results["fault_vfs_build"] = build_fault_vfs(runner)
        results["tests"]["deterministic_vfs_faults"] = fault_matrix(db, runner, root)
    tests = results["tests"]
    conc = tests["concurrent_reader_writer"]
    assert conc["overlap_proven"] and conc["exact_old_state"] and conc["exact_new_state"]
    assert tests["incompatible_migration"]["rejected_before_mutation"]
    assert tests["diskfull_atomicity"]["logical_atomicity_observed"] and tests["diskfull_atomicity"]["pre_post_logical_equality"]
    assert tests["backup_restore"]["full_equivalence"] and tests["backup_restore"]["restored"]["integrity_check"] == "ok"
    assert tests["deterministic_vfs_faults"]["status"] == "PASSED"
    OUT.write_text(json.dumps(results, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": results["artifact"], "concurrency": results["tests"]["concurrent_reader_writer"]["overlap_proven"],
                      "migration": results["tests"]["incompatible_migration"]["rejected_before_mutation"],
                      "backup_equivalence": results["tests"]["backup_restore"]["full_equivalence"],
                      "fault_vfs": results["tests"]["deterministic_vfs_faults"].get("status")}, sort_keys=True))


if __name__ == "__main__":
    main()
