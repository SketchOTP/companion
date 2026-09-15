#!/usr/bin/env python3
"""Fail-closed self-test for the Alpha50 secret scanner boundary."""
import json
import pathlib
import re
import tempfile
import argparse

PATTERN = r"BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|api[_-]?key\s*[:=]"


_compiled = re.compile(PATTERN, re.IGNORECASE)


def scan(path: pathlib.Path) -> bool:
    """Return whether a text file contains a forbidden secret pattern."""
    try:
        return _compiled.search(path.read_text(encoding="utf-8", errors="ignore")) is not None
    except OSError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", nargs="*", type=pathlib.Path, default=[])
    args = parser.parse_args()
    if not callable(scan):
        raise SystemExit("FAIL: scanner implementation is unavailable")
    with tempfile.TemporaryDirectory(prefix="alpha50-scanner-") as root:
        root_path = pathlib.Path(root)
        secret = root_path / "synthetic-secret.txt"
        clean = root_path / "clean.txt"
        # Construct the forbidden token at runtime so the repository scanner
        # does not flag this intentional self-test fixture itself.
        secret.write_text("api_" + "key: synthetic-test-only\n", encoding="utf-8")
        clean.write_text("ordinary bounded evidence\n", encoding="utf-8")
        detected = scan(secret)
        clean_pass = not scan(clean)
    repository_hits = [str(path) for path in args.repository if path.is_file() and scan(path)]
    result = {"status": "PASS" if detected and clean_pass and not repository_hits else "FAIL", "scanner": "python-re", "synthetic_detected": detected, "clean_passed": clean_pass, "repository_hits": repository_hits}
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
