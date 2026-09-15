#!/usr/bin/env python3
"""Fail-closed self-test for the Alpha50 secret scanner boundary."""
import json
import pathlib
import shutil
import subprocess
import tempfile

PATTERN = r"BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|api[_-]?key\s*[:=]"


def scan(path: pathlib.Path) -> bool:
    result = subprocess.run(["rg", "-nI", PATTERN, str(path)], capture_output=True, text=True)
    return result.returncode == 0


def main() -> None:
    if shutil.which("rg") is None:
        raise SystemExit("FAIL: rg scanner is unavailable")
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
    result = {"status": "PASS" if detected and clean_pass else "FAIL", "scanner": "rg", "synthetic_detected": detected, "clean_passed": clean_pass}
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
