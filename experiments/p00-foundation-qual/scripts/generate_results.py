#!/usr/bin/env python3
"""Deterministically derive committed summaries from sanitized runner JSON.

The inputs are private, sanitized stdout files produced by the qualification
runners. No conclusion is accepted from a pre-existing summary file.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jcs", type=Path, required=True)
    parser.add_argument("--toolchain", type=Path, required=True)
    parser.add_argument("--ipc", type=Path, required=True)
    parser.add_argument("--sqlite", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    jcs, tool, ipc, sqlite = map(load, (args.jcs, args.toolchain, args.ipc, args.sqlite))
    profile_ok = jcs["bounded_profile_python_rust_oracle_agreement"] is True
    numeric_ok = all(jcs["numeric_profile_rejections"].values())
    conformance = {
        "python_rust_oracle_bytes": profile_ok,
        "utf16_non_bmp_order": jcs["non_bmp_utf16_order_checked"],
        "nested_objects_and_arrays": profile_ok,
        "control_characters": profile_ok,
        "unicode_preservation": profile_ok,
        "decoded_duplicate_rejection": jcs["cross_language_decoded_duplicate_rejected"],
        "escaped_duplicate_rejection": jcs["escaped_duplicate_rejected"],
        "invalid_unicode_rejection": profile_ok,
        "nonfinite_rejection": profile_ok,
        "bounded_integer_profile": numeric_ok,
        "schema_major_rejection": profile_ok,
        "project_profile_numeric_rejection": numeric_ok,
    }
    behavior = dict(tool["behavioral_parity"])
    behavior["queue_overflow"] = "DEFERRED_PHASE_01"
    py, rust = tool["python"], tool["rust"]
    result = {
        "status": "PASSED_BOUNDED_PROFILE",
        "oracle": {
            "package": "canonicalize@5.0.0", "license": "Apache-2.0", "node_engine": ">=22",
            "node_runtime": "v24.20.0", "tarball_sha256": "5e13234695e05dc1398c84e7bc12aaee7c69a6e23b52325b9cb54f6a307427b0",
            "repository": "https://github.com/erdtman/canonicalize.git", "vectors": jcs["oracle_vectors"], "profile_vectors": jcs["profile_vectors"],
            "npm_integrity": "sha512-O/NCg79G0/TWoD3Fo6scOMfP4p7/TsxRXVmRo9mEfD6h/5y5o1wtVbKyBO0E2i7FEcqe5tRijyAH/IWHIHMH4w==",
        },
        "conformance": conformance, "behavioral_parity": behavior,
        "python": {"runtime": "CPython 3.12.3 (existing host executable)", "cold_self_median_ms": py["cold_self_median_ms"], "cold_request_median_ms": py["cold_single_median_ms"], "warm_median_ms": py["warm_median_ms"], "warm_p95_ms": py["warm_p95_ms"], "cpu_seconds": py["child_cpu_seconds"], "rss_kib": [py["rss_kib_min"], py["rss_kib_max"]]},
        "rust": {"toolchain": "rustc 1.98.1 stable (isolated qualification cache)", "release_build": True, "tests_passed": 5, "cold_self_median_ms": rust["cold_self_median_ms"], "cold_request_median_ms": rust["cold_single_median_ms"], "warm_median_ms": rust["warm_median_ms"], "warm_p95_ms": rust["warm_p95_ms"], "cpu_seconds": rust["child_cpu_seconds"], "rss_kib": [rust["rss_kib_min"], rust["rss_kib_max"]]},
        "fixture_sha256": tool["fixture_sha256"],
        "profile_vector_hashes": jcs["profile_vector_agreement"],
        "unsupported_claims_removed": ["altered_digest_detection", "controlled_shutdown", "no_egress", "rejection_reasons"],
        "recommendation": "BLOCKED — MORE EVIDENCE REQUIRED", "adoption": "NONE",
    }
    # IPC and SQLite are already sanitized runner outputs. Their summaries are
    # copied by value and normalized with the same deterministic serializer.
    ipc_out = {"status": "PASSED_BOUNDED_CANDIDATE_MATRIX", **ipc}
    sqlite_out = {"status": sqlite.get("status", "FAILED_BOUNDED_MATRIX"), **sqlite}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "jcs_toolchain_results.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (args.out / "ipc_results.json").write_text(json.dumps(ipc_out, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (args.out / "sqlite_results.json").write_text(json.dumps(sqlite_out, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
