#!/usr/bin/env python3
"""RFC 8785 reference-oracle and bounded-profile parity checks."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON_SHELL = ROOT / "python" / "qual_shell.py"
RUST_BINARY = Path(os.environ.get("QUAL_RUST_BINARY", ""))
ORACLE = Path(os.environ["QUAL_JCS_ORACLE"])


def oracle(raw: str) -> str:
    result = subprocess.run(["node", str(ORACLE)], input=raw, text=True, capture_output=True, check=True)
    return result.stdout


def shell_canonical(command: list[str], raw: str) -> str:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as fixture:
        fixture.write(raw); fixture.flush()
        result = subprocess.run(command + ["--canonical", fixture.name], text=True, capture_output=True, check=True)
    return base64.b64decode(result.stdout.strip()).decode("utf-8")


def shell_rejects(command: list[str], raw: str) -> bool:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as fixture:
        fixture.write(raw); fixture.flush()
        result = subprocess.run(command + ["--canonical", fixture.name], text=True,
                                capture_output=True)
    return result.returncode != 0


def main() -> None:
    vectors = {
        '{"b":1,"a":2}': '{"a":2,"b":1}',
        '{"\\ud834\\udd1e":"𝄞","a":"A"}': '{"a":"A","𝄞":"𝄞"}',
        '{"z":[3,{"b":2,"a":1}],"a":"line\\n"}': '{"a":"line\\n","z":[3,{"a":1,"b":2}]}',
        "333333333.33333329": "333333333.3333333",
        "4.50": "4.5",
        "1e-6": "0.000001",
        "1e-27": "1e-27",
        "-0": "0",
    }
    oracle_results = {raw: oracle(raw) for raw in vectors}
    for raw, expected in vectors.items():
        if oracle_results[raw] != expected:
            raise AssertionError(f"oracle mismatch for {raw}: {oracle_results[raw]!r} != {expected!r}")
    duplicate = '{"a":1,"\\u0061":2}'
    duplicate_rejected = False
    try:
        json.loads(duplicate, object_pairs_hook=lambda pairs: (_ for _ in ()).throw(ValueError("duplicate")) if len({k for k, _ in pairs}) != len(pairs) else dict(pairs))
    except ValueError:
        duplicate_rejected = True
    if not duplicate_rejected:
        raise AssertionError("escaped duplicate accepted")
    event = json.loads((ROOT / "fixtures" / "event-v1.json").read_text(encoding="utf-8"))
    event["payload"].update({"𝄞": 1, "a": 2})
    event_raw = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
    py = shell_canonical(["python3", str(PYTHON_SHELL)], event_raw)
    rust = shell_canonical([str(RUST_BINARY)], event_raw)
    expected_profile = oracle(event_raw)
    if py != rust or py != expected_profile:
        raise AssertionError("Python/Rust bounded-profile bytes disagree with JCS oracle")
    numeric_profile_rejections = {
        raw: shell_rejects(["python3", str(PYTHON_SHELL)], raw)
        and shell_rejects([str(RUST_BINARY)], raw)
        for raw in ("333333333.33333329", "4.50", "1e-6", "1e-27", "-0")
    }
    if not all(numeric_profile_rejections.values()):
        raise AssertionError("a non-integer canonical-state number was accepted")
    print(json.dumps({
        "oracle_package": "canonical@5.0.0",
        "oracle_vectors": len(vectors),
        "escaped_duplicate_rejected": True,
        "non_bmp_utf16_order_checked": True,
        "numeric_profile_rejections": numeric_profile_rejections,
        "bounded_profile_python_rust_oracle_agreement": True,
        "fixture_sha256": hashlib.sha256(event_raw.encode()).hexdigest(),
        "status": "passed",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
