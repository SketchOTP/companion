#!/usr/bin/env python3
"""Verify that independent Review 04 evidence mutations fail validation."""
import json, os, shutil, subprocess, tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
RESULTS = HERE.parents[1] / "results" / "phase01-review04"
VALIDATOR = HERE.parent / "validate_phase01_review04.py"

def mutate(root: Path, name: str) -> None:
    if name == "result_hash":
        path = root / "phase01_closeout.json"
        path.write_bytes(path.read_bytes() + b" ")
    else:
        filename, key, value = {
            "expected_outcome": ("phase01_closeout.json", ("categories", "valid_safety_candidate", "expected_status"), "rejected"),
            "rejection_reason": ("phase01_closeout.json", ("categories", "unknown_field", "expected_reason"), "wrong_reason"),
            "invalid_accepted": ("phase01_closeout.json", ("equations", "invalid_accepted"), 1),
            "acceptance_group": ("failure_matrix.json", ("groups", "startup_readiness", "status"), "FAIL"),
        }[name]
        path = root / filename
        value_obj = json.loads(path.read_text())
        target = value_obj
        for part in key[:-1]:
            target = target[part]
        target[key[-1]] = value
        path.write_text(json.dumps(value_obj, indent=2, sort_keys=True) + "\n")

def main() -> int:
    outcomes = {}
    for name in ("result_hash", "expected_outcome", "rejection_reason", "invalid_accepted", "acceptance_group"):
        with tempfile.TemporaryDirectory(prefix="companion-review04-tamper-") as temp:
            root = Path(temp)
            shutil.copytree(RESULTS, root, dirs_exist_ok=True)
            mutate(root, name)
            env = {**os.environ, "QUAL_REVIEW04_ROOT": str(root)}
            run = subprocess.run(["python3", str(VALIDATOR)], env=env, capture_output=True, text=True)
            outcomes[name] = run.returncode != 0
    print(json.dumps({"status": "PASS" if all(outcomes.values()) else "FAIL", "mutations": outcomes}, sort_keys=True))
    return 0 if all(outcomes.values()) else 1

if __name__ == "__main__":
    raise SystemExit(main())
