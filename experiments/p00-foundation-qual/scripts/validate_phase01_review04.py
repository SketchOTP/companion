#!/usr/bin/env python3
"""Fail-closed semantic validator for the Phase 01 Review 04 evidence."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RESULTS = Path(os.environ.get("QUAL_REVIEW04_ROOT", Path(__file__).resolve().parents[1] / "results" / "phase01-review04"))
FIXTURE = ROOT / "experiments" / "p00-foundation-qual" / "fixtures" / "event-v1.json"
RESULT_FILES = ("phase01_closeout.json", "failure_matrix.json", "contract_closeout.json", "godot_bridge.json", "regression900.json")
PRIVATE = re.compile(r"/(?:home|srv|tmp|run)/|(?:username|hostname|serial(?:[-_ ]?number)?|secret|capability[-_ ]?(?:bytes?|material|token|value))", re.I)
EXPECTED = {
    "valid_safety_candidate": ("direct-care", "accepted", "accepted"),
    "duplicate_safety_candidate": ("direct-care", "duplicate", "duplicate"),
    "replay_safety_candidate": ("direct-care", "rejected", "replay_rejected"),
    "malformed_frame": ("direct-care", "rejected", "malformed_frame"),
    "duplicate_decoded_key": ("direct-care", "rejected", "duplicate_decoded_key"),
    "unsupported_schema_major": ("direct-care", "rejected", "unsupported_schema_major"),
    "unknown_field": ("direct-care", "rejected", "unknown_field"),
    "invalid_uuid": ("direct-care", "rejected", "invalid_uuid"),
    "invalid_datetime": ("direct-care", "rejected", "invalid_datetime"),
    "stale_generation": ("direct-care", "rejected", "stale_generation"),
    "invalid_mac": ("direct-care", "rejected", "invalid_mac"),
    "stale_mac": ("direct-care", "rejected", "stale_mac"),
    "unauthorized_sender": ("direct-care", "rejected", "unauthorized_sender"),
    "forbidden_companion_state": ("direct-care", "rejected", "forbidden_companion_state"),
    "valid_ordinary_observation": ("ordinary", "accepted", "ordinary_observation"),
}

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load(name: str) -> dict:
    value = json.loads((RESULTS / name).read_text(encoding="utf-8"))
    if PRIVATE.search(json.dumps(value, sort_keys=True)):
        raise AssertionError(f"private value in {name}")
    return value

def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)

def validate() -> dict:
    manifest = json.loads((RESULTS / "manifest.json").read_text(encoding="utf-8"))
    require(not PRIVATE.search(json.dumps(manifest, sort_keys=True)), "private value in manifest")
    require(manifest.get("schema") == "companion-p01-review04-v1", "manifest schema")
    require(manifest.get("timestamp_precision") == "date-only UTC", "honest timestamp")
    require(manifest.get("sanitized_host_class") == "Linux x86_64 local ext4/NVMe", "host class")
    require(manifest.get("fixture_sha256") == digest(FIXTURE), "fixture hash")
    evidence_commit = manifest.get("evidence_commit")
    pending = evidence_commit == "PENDING_NARROW_CORRECTION_COMMIT"
    require(pending or re.fullmatch(r"[0-9a-f]{40}", evidence_commit or "") is not None, "evidence commit")
    if not pending:
        require(subprocess.run(["git", "merge-base", "--is-ancestor", evidence_commit, "HEAD"], cwd=ROOT).returncode == 0, "Git ancestry")
    listed = manifest.get("result_file_sha256", {})
    require(set(listed) == set(RESULT_FILES), "result-file manifest scope")
    for name in RESULT_FILES:
        require(re.fullmatch(r"[0-9a-f]{64}", listed.get(name, "")) is not None, f"hash format {name}")
        require(digest(RESULTS / name) == listed[name], f"result hash {name}")

    closeout = load("phase01_closeout.json")
    require(closeout.get("status") == "PASS" and closeout.get("cycles", 0) >= 3000, "3,000 matrix status")
    require(set(closeout.get("seeds", [])) == {17, 23, 41}, "retained seeds")
    categories = closeout.get("categories", {})
    require(set(categories) == set(EXPECTED), "exhaustive category set")
    for name, (path, status, reason) in EXPECTED.items():
        item = categories[name]
        require(item.get("requested", 0) > 0 and item.get("applied") == item.get("requested"), f"category accounting {name}")
        require(item.get("transport_path") == path and item.get("expected_status") == status and item.get("expected_reason") == reason, f"category expectation {name}")
        require(item.get(status, 0) == item.get("requested"), f"category outcome {name}")
        require(item.get("reasons", {}).get(reason) == item.get("requested"), f"category reason {name}")
        require(item.get("care_attempt_delta", 0) == (0 if path == "ordinary" else item.get("requested")), f"care attempt delta {name}")
        require(item.get("care_outcome_delta", 0) == (item.get("requested") if name == "valid_safety_candidate" else 0), f"care outcome delta {name}")
        require(item.get("companion_event_delta", 0) == (item.get("requested") if path == "ordinary" else 0), f"companion delta {name}")
    equations = closeout.get("equations", {})
    require(equations.get("requested_total") == equations.get("observed_total") == closeout.get("cycles"), "total accounting")
    require(equations.get("invalid_accepted") == 0 and equations.get("accounting_exact") is True, "invalid accepted/equations")
    require(equations.get("care_attempt_rows") == sum(item.get("requested", 0) for name, item in categories.items() if EXPECTED[name][0] == "direct-care"), "attempt rows")
    require(equations.get("care_outcome_rows") == categories["valid_safety_candidate"].get("requested"), "outcome rows")
    require(equations.get("ordinary_care_attempt_rows") == equations.get("ordinary_care_outcome_rows") == 0, "ordinary care separation")
    for key in ("startup_ready", "unknown_kind_rejected_before_transport", "invalid_accepted_zero", "ordinary_separated", "care_alive_after_hostile", "persistent_idempotency", "producer_rotation", "care_store_fault_degraded", "care_store_recovered", "clean_shutdown"):
        require(closeout.get("lifecycle", {}).get(key) is True, f"lifecycle {key}")

    failure = load("failure_matrix.json")
    require(failure.get("status") == "PASS" and failure.get("group_count") == 12 and failure.get("exercised_pass_count") == 12, "12-group status")
    require(set(failure.get("groups", {})) == {"startup_readiness", "ordinary_role_restart", "direct_pair_replacement", "care_outage_recovery", "care_store_fault", "companion_independence", "invalid_input", "persistent_idempotency", "exact_persistence", "xdg_refusal", "godot_recovery", "shutdown_boundary"}, "12-group names")
    require(all(group.get("status") == "PASS" for group in failure["groups"].values()), "12-group pass assertions")
    require(failure["groups"]["invalid_input"].get("no_durable_acceptance") is True, "invalid durable acceptance")
    require(failure["groups"]["shutdown_boundary"].get("network_before_owned") == failure["groups"]["shutdown_boundary"].get("network_after_owned") == 0, "shutdown network census")
    require(failure["groups"]["shutdown_boundary"].get("children_dead") is True and failure["groups"]["shutdown_boundary"].get("checkout_status_unchanged") is True, "shutdown boundary")
    require(failure["groups"]["godot_recovery"].get("client_state") == ["connecting", "connected", "disconnected/degraded", "reconnecting", "connected"], "Godot state sequence")
    require(failure["groups"]["godot_recovery"].get("same_process_reconnect") is True, "Godot reconnect")

    contract = load("contract_closeout.json")
    require(contract.get("status") == "PASS" and len(contract.get("schemas", {})) == 9, "contract status")
    require("actual_wire_domains" not in contract, "unsupported wire claim")
    wire = {item.get("domain"): item for item in contract.get("wire_executions", [])}
    require(wire.get("ordinary_observation", {}).get("path") == "control->companion-core" and wire.get("ordinary_observation", {}).get("observed_messages", 0) > 0, "ordinary wire execution")
    require(wire.get("safety_candidate", {}).get("path") == "control->producer->care-core" and wire.get("safety_candidate", {}).get("observed_messages", 0) > 0, "care wire execution")
    for schema, cases in contract["schemas"].items():
        require(cases.get("valid") is True and cases.get("missing_required") is True and cases.get("unknown_field") is True and cases.get("wrong_type") is True, f"schema cases {schema}")

    godot = load("godot_bridge.json")
    require(godot.get("status") == "PASS" and godot.get("same_process_connected_before") is True and godot.get("bridge_disconnect_observed") is True and godot.get("same_process_reconnected") is True, "Godot bridge")
    regression = load("regression900.json")
    require(regression.get("status") == "PASS" and regression.get("duration_seconds", 0) >= 900 and not regression.get("failures"), "900-second regression")
    for key in ("invalid_rejected", "valid_accepted", "duplicate_after_care_restart", "producer_rotated", "stale_rejected", "store_fault_degraded", "store_fault_blocked", "store_recovered", "bridge_restarted", "clean_shutdown", "checkout_unchanged", "network_census_complete"):
        require(regression.get("observations", {}).get(key) is True, f"regression {key}")
    return {"status": "PASSED", "validator": "validate_phase01_review04.py", "checked_files": list(RESULT_FILES), "fixture_verified": True, "ancestry_verified": not pending, "circular_validation_input": False}

def main() -> int:
    try:
        result = validate()
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError, KeyError, TypeError, ValueError, AssertionError) as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        return 1
    (RESULTS / "validation_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("VALIDATION PASSED: Review 04 evidence is semantically bound")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
