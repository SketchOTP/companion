#!/usr/bin/env python3
"""Independent fail-closed validator for the committed Phase 01 evidence."""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(os.environ.get("QUAL_CLOSEOUT_ROOT", Path(__file__).resolve().parents[1] / "evidence" / "phase01-closeout"))
REPO = Path(__file__).resolve().parents[1]
FIXTURE = REPO / "experiments/p00-foundation-qual/fixtures/event-v1.json"

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
    return h.hexdigest()

def load(name):
    value = json.loads((ROOT / name).read_text(encoding="utf-8"))
    text = json.dumps(value, sort_keys=True)
    if re.search(r"/(?:home|srv|tmp|run)/|(?:hostname|username|serial(?:[-_ ]?number)?)|(?:secret|capability)[-_ ]?(?:bytes?|material|token|value)", text, re.I):
        raise ValueError(f"private value in {name}")
    return value

def require(ok, message):
    if not ok: raise AssertionError(message)

def main() -> int:
    try:
        manifest = load("manifest.json")
        require(manifest.get("schema") == "companion-p01-closeout-v1", "schema")
        require(manifest.get("timestamp_precision") in {"observed UTC", "date-only UTC"}, "timestamp precision")
        require(manifest.get("fixture_sha256") == sha(FIXTURE), "fixture hash")
        files = manifest.get("result_files", {})
        require(files, "result files")
        for name, expected in files.items():
            require(re.fullmatch(r"[0-9a-f]{64}", expected or "") is not None, f"hash format {name}")
            require(sha(ROOT / name) == expected, f"hash mismatch {name}")
        commit = manifest.get("evidence_commit")
        require(re.fullmatch(r"[0-9a-f]{40}", commit or "") is not None, "evidence commit")
        require(subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=REPO).returncode == 0, "ancestry")
        closeout = load("phase01_closeout.json")
        require(closeout.get("status") == "PASS" and closeout.get("cycles", 0) >= 3000, "resident closeout")
        require(len(closeout.get("seeds", [])) >= 3 and len(closeout.get("counts", {})) >= 10, "matrix diversity")
        require(all(v > 0 for k, v in closeout.get("counts", {}).items() if k not in {"valid"}), "invalid category coverage")
        failure = load("failure_matrix.json")
        require(failure.get("status") == "PASS" and failure.get("scenario_count") == 37 and all(failure.get("scenarios", {}).values()), "failure matrix")
        contract = load("contract_closeout.json")
        require(contract.get("status") == "PASS", "contract closeout")
        soak = load("soak.json")
        require(soak.get("status") == "PASS" and soak.get("duration_seconds", 0) >= 3600 and not soak.get("failures"), "resident soak")
        result = {"status":"PASSED","hashes_verified":True,"fixture_verified":True,"ancestry_verified":True,"circular_input":False,"checked_files":sorted(files)}
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, AssertionError, subprocess.SubprocessError) as exc:
        print(f"CLOSEOUT VALIDATION FAILED: {exc}", file=sys.stderr); return 1
    (ROOT / "validation.json").write_text(json.dumps(result, sort_keys=True, indent=2)+"\n", encoding="utf-8")
    print("CLOSEOUT VALIDATION PASSED")
    return 0

if __name__ == "__main__": raise SystemExit(main())
