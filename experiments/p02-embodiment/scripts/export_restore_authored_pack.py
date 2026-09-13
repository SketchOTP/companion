#!/usr/bin/env python3
"""Deterministic local export/restore check for an already-intaken frame pack."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_manifest(root: Path) -> dict[str, str]:
    return {path.relative_to(root).as_posix(): digest(path) for path in sorted(root.rglob("*")) if path.is_file()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--restore", type=Path, required=True)
    args = parser.parse_args()
    source = args.intake.resolve()
    before = tree_manifest(source)
    args.archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name in sorted(before):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, (source / name).read_bytes(), compresslevel=9)
    if args.restore.exists():
        shutil.rmtree(args.restore)
    args.restore.mkdir(parents=True)
    with zipfile.ZipFile(args.archive) as bundle:
        bundle.extractall(args.restore)
    after = tree_manifest(args.restore)
    if before != after:
        raise SystemExit("restored content-addressed pack differs")
    print(json.dumps({"status": "PASSED", "archive_sha256": digest(args.archive), "files": len(before), "restored_hashes_equal": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
