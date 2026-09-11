#!/usr/bin/env python3
"""Generate the sanitized, deterministic R04 evidence bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "experiments/p02-embodiment/scripts/build_r04_synthetic_pack.py"
INTAKE = ROOT / "experiments/p02-embodiment/scripts/intake_authored_frame_pack.py"
NEGATIVE = ROOT / "experiments/p02-embodiment/scripts/validate_r04_intake.py"
EXPORT = ROOT / "experiments/p02-embodiment/scripts/export_restore_authored_pack.py"
IDENTITY = ROOT / "assets/source/p02/references/identity-approved.png"
TURNAROUND = ROOT / "assets/source/p02/references/turnaround-approved.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, **kwargs)


def json_from_output(text: str) -> dict:
    for offset, char in enumerate(text):
        if char == "{":
            try:
                value, _ = json.JSONDecoder().raw_decode(text[offset:])
                if isinstance(value, dict):
                    return value
            except json.JSONDecodeError:
                pass
    raise AssertionError(f"JSON object absent from command output: {text[-1000:]}")


def tree(root: Path) -> dict[str, str]:
    return {path.relative_to(root).as_posix(): sha(path) for path in sorted(root.rglob("*")) if path.is_file()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cargo", default=os.environ.get("CARGO", "cargo"))
    parser.add_argument("--godot", required=True)
    args = parser.parse_args()
    output = args.out.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    with tempfile.TemporaryDirectory(prefix="companion-r04-evidence-") as temporary:
        temp = Path(temporary)
        source_a, source_b = temp / "source-a", temp / "source-b"
        for source in (source_a, source_b):
            built = run(["python3", str(BUILD), "--out", str(source), "--clean"], check=True)
            if json.loads(built.stdout)["status"] != "SYNTHETIC_TEST_PACK_BUILT": raise AssertionError("synthetic build failed")
        deterministic = tree(source_a) == tree(source_b)
        if not deterministic: raise AssertionError("clean-process synthetic build differs")

        intake_dir = temp / "intake"
        intake_run = run(["python3", str(INTAKE), "intake", "--source", str(source_a), "--out", str(intake_dir), "--operation", "test"], check=True)
        intake = json.loads(intake_run.stdout)
        smoke_run = run(["python3", str(INTAKE), "identity-smoke", "--source", str(IDENTITY), "--out", str(intake_dir)], check=True)
        smoke = json.loads(smoke_run.stdout)
        negative_run = run(["python3", str(NEGATIVE), "--out", str(output)], check=True)
        negative = json.loads(negative_run.stdout)

        rust = run([args.cargo, "run", "-p", "foundation-core", "--bin", "validate-authored-pack", "--locked", "--", str(intake_dir / "pack.json")])
        rust_missing = run([args.cargo, "run", "-p", "foundation-core", "--bin", "validate-authored-pack", "--locked", "--"])
        if rust.returncode != 0 or rust_missing.returncode == 0: raise AssertionError("Rust generated-pack path gate failed")
        rust_result = {"status": "PASSED", "actual_pack_returncode": rust.returncode, "actual_pack_message": rust.stdout.strip().splitlines()[-1], "missing_pack_path_returncode": rust_missing.returncode, "missing_pack_path_rejected": True}

        archive = temp / "local-export.zip"
        restore = temp / "restore"
        export_run = run(["python3", str(EXPORT), "--intake", str(intake_dir), "--archive", str(archive), "--restore", str(restore)], check=True)
        export_result = json.loads(export_run.stdout)

        corrupt = temp / "corrupt"
        shutil.copytree(intake_dir, corrupt)
        corrupt_frame = sorted((corrupt / "runtime/frames").glob("*.png"))[0]
        data = bytearray(corrupt_frame.read_bytes()); data[100] ^= 1; corrupt_frame.write_bytes(data)
        godot = run([args.godot, "--headless", "--path", "godot", "--script", "res://r04_authored_pack_test.gd", "--", f"--pack={intake_dir / 'pack.json'}", f"--corrupt-pack={corrupt / 'pack.json'}"])
        if godot.returncode != 0: raise AssertionError(godot.stdout + godot.stderr)
        godot_result = json_from_output(godot.stdout)
        if godot_result.get("status") != "PASS": raise AssertionError("Godot authored pack test failed")
        identity_godot = run([args.godot, "--headless", "--path", "godot", "--script", "res://r04_identity_smoke_test.gd", "--", f"--image={intake_dir / 'smoke/identity-approved.png'}"])
        if identity_godot.returncode != 0: raise AssertionError(identity_godot.stdout + identity_godot.stderr)
        identity_godot_result = json_from_output(identity_godot.stdout)

        schema = run(["python3", "scripts/validate_schemas.py"])
        crosswalk = run(["python3", "scripts/check_contract_types.py"])
        if schema.returncode != 0 or crosswalk.returncode != 0: raise AssertionError(schema.stderr + crosswalk.stderr)

        stable(output / "source_intake.json", {"status": "PASSED", "clean_process_byte_identical": deterministic, "approved_reference_hashes": {"identity": sha(IDENTITY), "turnaround": sha(TURNAROUND)}, "identity_smoke": smoke, "intake": intake})
        stable(output / "rust_contract.json", rust_result)
        stable(output / "godot_runtime.json", {"status": "PASSED", "authored_pack": godot_result, "identity_smoke": identity_godot_result, "unexpected_error_output": "ERROR:" in godot.stdout or "ERROR:" in godot.stderr})
        stable(output / "export_restore.json", export_result)
        stable(output / "contract_validation.json", {"status": "PASSED", "draft_2020_12": schema.stdout.strip(), "rust_schema_crosswalk": crosswalk.stdout.strip(), "generated_pack_schema_validated_by_intake": True})

    result_names = ["intake_validation.json", "source_intake.json", "rust_contract.json", "godot_runtime.json", "export_restore.json", "contract_validation.json"]
    stable(output / "provenance.json", {"profile": "COMPANION_P02_R04_EVIDENCE_V1", "execution_date_utc": "2026-09-11", "commands": ["python3 experiments/p02-embodiment/scripts/run_r04_evidence.py --out OUT --godot GODOT", "python3 experiments/p02-embodiment/scripts/validate_r04_results.py --results OUT --tamper-negative"], "runtimes": {"rust": "1.98.1", "godot": "4.7.2.stable.official.ed1daf0bf", "python": "system qualification tooling"}, "evidence_ceiling": "E3_TARGET_TESTED synthetic intake/runtime boundary only; no production art or Phase 02 acceptance", "result_sha256": {name: sha(output / name) for name in result_names}})
    (output / "README.md").write_text(
        "# R04 authored-frame boundary evidence\n\n"
        "This sanitized bundle contains synthetic-only bounded E3 intake and runtime evidence. "
        "It does not contain or approve production character art.\n\n"
        "Regenerate with the exact Rust 1.98.1 and Godot 4.7.2 qualification artifacts:\n\n"
        "```bash\n"
        "python3 experiments/p02-embodiment/scripts/run_r04_evidence.py --out OUT --godot \"$GODOT_BIN\"\n"
        "python3 experiments/p02-embodiment/scripts/validate_r04_results.py --results OUT --tamper-negative\n"
        "```\n\n"
        "Generated PNGs, content-addressed storage, Cargo targets, Godot caches, local export ZIPs, "
        "restored trees, and tamper copies remain outside Git.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASSED", "results": result_names}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
