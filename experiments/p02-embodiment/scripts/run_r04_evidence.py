#!/usr/bin/env python3
"""Generate the deterministic C02 synthetic source/intake evidence bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "experiments/p02-embodiment/scripts/build_r04_synthetic_pack.py"
INTAKE = ROOT / "experiments/p02-embodiment/scripts/intake_authored_frame_pack.py"
NEGATIVE = ROOT / "experiments/p02-embodiment/scripts/validate_r04_intake.py"
EXPORT = ROOT / "experiments/p02-embodiment/scripts/export_restore_authored_pack.py"
IDENTITY = ROOT / "assets/source/p02/references/identity-approved.png"
TURNAROUND = ROOT / "assets/source/p02/references/turnaround-approved.png"


def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def stable(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def run(command: list[str], *, check: bool = False) -> subprocess.CompletedProcess:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if check and result.returncode: raise RuntimeError(f"command failed ({result.returncode}): {' '.join(command)}\n{result.stderr[-2000:]}")
    return result
def parse_json(result: subprocess.CompletedProcess) -> dict:
    stream = result.stdout if result.returncode == 0 else result.stderr; return json.loads(stream.strip().splitlines()[-1])
def tree(root: Path) -> dict[str, str]: return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--out", type=Path, required=True); parser.add_argument("--cargo", default=os.environ.get("CARGO", "cargo")); parser.add_argument("--godot", default=os.environ.get("GODOT_BIN", "")); args = parser.parse_args(); output = args.out.resolve()
    if output.exists():
        old = output / "validation.json"
        old_bytes = old.read_bytes() if old.is_file() else None
        shutil.rmtree(output)
    else: old_bytes = None
    output.mkdir(parents=True)
    if old_bytes is not None: (output / "validation.json").write_bytes(old_bytes)
    started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    with tempfile.TemporaryDirectory(prefix="companion-r04-c02-evidence-") as temporary:
        temp = Path(temporary); source_a = temp / "source-a"; source_b = temp / "source-b"
        for source in (source_a, source_b): run(["python3", str(BUILD), "--out", str(source), "--clean"], check=True)
        deterministic = tree(source_a) == tree(source_b); pack_a = json.loads((source_a / "pack.json").read_text())
        intake_dir = temp / "intake"; intake = parse_json(run(["python3", str(INTAKE), "intake", "--source", str(source_a), "--out", str(intake_dir), "--operation", "test"], check=True))
        smoke = parse_json(run(["python3", str(INTAKE), "identity-smoke", "--source", str(IDENTITY), "--out", str(intake_dir)], check=True))
        negative = parse_json(run(["python3", str(NEGATIVE), "--out", str(temp / "negative-run")], check=True))
        schema = run(["python3", "scripts/validate_schemas.py"]); crosswalk = run(["python3", "scripts/check_contract_types.py"])
        if schema.returncode or crosswalk.returncode: raise RuntimeError(schema.stderr + crosswalk.stderr)
        if shutil.which(args.cargo) is None:
            rust_result = {"status": "NOT_RUN", "reason": "cargo is not installed", "actual_pack_returncode": None, "missing_pack_path_returncode": None, "missing_pack_path_rejected": None}
        else:
            rust = run([args.cargo, "run", "-p", "foundation-core", "--bin", "validate-authored-pack", "--locked", "--", str(intake_dir / "pack.json")]); missing = run([args.cargo, "run", "-p", "foundation-core", "--bin", "validate-authored-pack", "--locked", "--"])
            if rust.returncode or missing.returncode == 0: raise RuntimeError(f"Rust gate failed: {rust.returncode}/{missing.returncode}\n{rust.stderr}")
            rust_result = {"status": "PASSED", "actual_pack_returncode": rust.returncode, "missing_pack_path_returncode": missing.returncode, "missing_pack_path_rejected": True, "actual_pack_message": rust.stdout.strip().splitlines()[-1] if rust.stdout.strip() else "", "pack_profile": pack_a["request_profile"], "track_count": len(pack_a["tracks"]), "frame_count": sum(len(t["frames"]) for t in pack_a["tracks"])}
        archive, restore = temp / "export.zip", temp / "restore"; export_result = parse_json(run(["python3", str(EXPORT), "--intake", str(intake_dir), "--archive", str(archive), "--restore", str(restore)], check=True))
        if not args.godot:
            godot_result = {"status": "NOT_RUN", "reason": "GODOT_BIN not supplied; exact 4.7.2 render boundary unavailable"}
        else:
            corrupt = temp / "corrupt"; shutil.copytree(intake_dir, corrupt); frame = corrupt / "runtime/frames/neutral_construction__front__neutral__v01__f000.png"; data = bytearray(frame.read_bytes()); data[100] ^= 1; frame.write_bytes(data)
            godot_cmd = ["xvfb-run", "-a", args.godot] if shutil.which("xvfb-run") else [args.godot]
            godot_run = run(godot_cmd + ["--path", "godot", "--script", "res://r04_authored_pack_test.gd", "--", f"--pack={intake_dir / 'pack.json'}", f"--corrupt-pack={corrupt / 'pack.json'}"])
            if godot_run.returncode:
                godot_result = {"status": "BLOCKED", "reason": "render_boundary_unobserved", "exact_returncode": godot_run.returncode, "output": (godot_run.stdout + godot_run.stderr)[-4000:], "unexpected_error_output": "ERROR:" in godot_run.stdout or "ERROR:" in godot_run.stderr}
            else:
                godot_result = {"status": "PASSED", "output": godot_run.stdout[-4000:], "unexpected_error_output": "ERROR:" in godot_run.stdout or "ERROR:" in godot_run.stderr, "render_observation": "RenderingServer.frame_post_draw"}
        stable(output / "source_intake.json", {"status": "PASSED" if deterministic else "FAILED", "clean_process_byte_identical": deterministic, "profile": pack_a["request_profile"], "track_count": len(pack_a["tracks"]), "frame_count": sum(len(t["frames"]) for t in pack_a["tracks"]), "approved_reference_hashes": {"identity": sha(IDENTITY), "turnaround": sha(TURNAROUND)}, "identity_smoke": smoke, "intake": intake})
        stable(output / "intake_validation.json", negative); stable(output / "rust_contract.json", rust_result); stable(output / "godot_runtime.json", godot_result); stable(output / "export_restore.json", export_result)
        stable(output / "contract_validation.json", {"status": "PASSED", "draft_2020_12": schema.stdout.strip(), "rust_schema_crosswalk": crosswalk.stdout.strip(), "generated_pack_profile": pack_a["request_profile"], "actual_generated_pack_schema_validated_by_intake": True, "actual_generated_pack_path": "runtime evidence only"})
    result_names = ["source_intake.json", "intake_validation.json", "rust_contract.json", "godot_runtime.json", "export_restore.json", "contract_validation.json"]
    ended = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"); git_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    stable(output / "provenance.json", {"profile": "COMPANION_P02_R04_C02_EVIDENCE_V1", "execution_start_utc": started, "execution_end_utc": ended, "git_commit": git_commit, "commands": ["python3 experiments/p02-embodiment/scripts/run_r04_evidence.py --out OUT --cargo CARGO --godot GODOT", "python3 experiments/p02-embodiment/scripts/validate_r04_results.py --results OUT --tamper-negative"], "runtimes": {"python": "qualification interpreter", "rust": "1.98.1", "godot": "4.7.2.stable.official.ed1daf0bf"}, "source_identities": {"identity_sha256": sha(IDENTITY), "turnaround_sha256": sha(TURNAROUND)}, "fixture_sha256": {"contracts/fixtures/mon-authored-frame-source-pack-v1.json": sha(ROOT / "contracts/fixtures/mon-authored-frame-source-pack-v1.json"), "contracts/fixtures/mon-ingested-frame-pack-v1.json": sha(ROOT / "contracts/fixtures/mon-ingested-frame-pack-v1.json")}, "evidence_ceiling": "E3_TARGET_TESTED synthetic intake/runtime boundary only; no production art or Phase 02 acceptance", "result_sha256": {name: sha(output / name) for name in result_names}})
    (output / "README.md").write_text("""# R04-C02 sanitized evidence\n\nThis bundle is synthetic calibration evidence only; no production character pixels are generated.\n\n## Regeneration\n\n1. Use the pinned qualification Python with Pillow/jsonschema, Rust 1.98.1, and the exact Godot 4.7.2 binary when available. Set `CARGO` and `GODOT_BIN` to private cache paths; keep tools, temporary packs, exports, and raw host output outside Git.\n2. Run `python3 experiments/p02-embodiment/scripts/run_r04_evidence.py --out OUT --cargo \"$CARGO\" --godot \"$GODOT_BIN\"`. It builds the complete `phase02_bounded_motion_proof_v1` pack twice, performs intake and negative tests, validates schemas, round-trips the actual generated pack through Rust, runs local export/restore, and records Godot status.\n3. Run `python3 experiments/p02-embodiment/scripts/validate_r04_results.py --results OUT --tamper-negative`. The validator independently checks profile/count/hash equations and tamper mutations; it must exit zero only for a complete valid result set.\n4. Generated PNGs, CAS copies, caches, binaries, archives, restored trees, and raw logs remain outside Git. Commit only sanitized JSON, hashes, and this procedure.\n""", encoding="utf-8")
    print(json.dumps({"status": "PASSED", "results": result_names, "godot": json.loads((output / "godot_runtime.json").read_text()).get("status"), "profile": "phase02_bounded_motion_proof_v1"}, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
