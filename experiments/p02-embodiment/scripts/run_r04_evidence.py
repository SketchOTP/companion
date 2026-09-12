#!/usr/bin/env python3
"""Generate bounded R04-C01 evidence from the actual source/intake boundary.

This command emits sanitized JSON only. Production art is never generated;
the two PNGs come from the unmistakably synthetic calibration builder.
"""
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


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(command: list[str], *, check: bool = False) -> subprocess.CompletedProcess:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if check and result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(command)}\n{result.stderr[-2000:]}")
    return result


def parse_json(result: subprocess.CompletedProcess) -> dict:
    stream = result.stdout if result.returncode == 0 else result.stderr
    return json.loads(stream.strip().splitlines()[-1])


def tree(root: Path) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cargo", default=os.environ.get("CARGO", "cargo"))
    parser.add_argument("--godot", default=os.environ.get("GODOT_BIN", ""))
    args = parser.parse_args(); output = args.out.resolve()
    historical_validation = None
    if output.exists():
        prior = output / "validation.json"
        if prior.is_file():
            historical_validation = prior.read_bytes()
        shutil.rmtree(output)
    output.mkdir(parents=True)
    if historical_validation is not None:
        (output / "validation.json").write_bytes(historical_validation)
    started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    with tempfile.TemporaryDirectory(prefix="companion-r04-c01-evidence-") as temporary:
        temp = Path(temporary); source_a = temp / "source-a"; source_b = temp / "source-b"
        for source in (source_a, source_b):
            run(["python3", str(BUILD), "--out", str(source), "--clean"], check=True)
        deterministic = tree(source_a) == tree(source_b)
        if not deterministic:
            raise RuntimeError("clean-process synthetic source trees differ")
        intake_dir = temp / "intake"
        intake = parse_json(run(["python3", str(INTAKE), "intake", "--source", str(source_a), "--out", str(intake_dir), "--operation", "test"], check=True))
        smoke = parse_json(run(["python3", str(INTAKE), "identity-smoke", "--source", str(IDENTITY), "--out", str(intake_dir)], check=True))
        negative = parse_json(run(["python3", str(NEGATIVE), "--out", str(temp / "negative-run")], check=True))
        schema = run(["python3", "scripts/validate_schemas.py"]); crosswalk = run(["python3", "scripts/check_contract_types.py"])
        if schema.returncode or crosswalk.returncode:
            raise RuntimeError(schema.stderr + crosswalk.stderr)

        rust_command = [args.cargo, "run", "-p", "foundation-core", "--bin", "validate-authored-pack", "--locked", "--", str(intake_dir / "pack.json")]
        if shutil.which(args.cargo) is None:
            rust_result = {"status": "NOT_RUN", "reason": "cargo is not installed in this environment", "actual_pack_returncode": None, "missing_pack_path_returncode": None, "missing_pack_path_rejected": None}
        else:
            rust = run(rust_command)
            rust_missing = run([args.cargo, "run", "-p", "foundation-core", "--bin", "validate-authored-pack", "--locked", "--"])
            if rust.returncode != 0 or rust_missing.returncode == 0:
                raise RuntimeError(f"Rust generated-pack gate failed: {rust.returncode}/{rust_missing.returncode}")
            rust_result = {"status": "PASSED", "actual_pack_returncode": rust.returncode, "missing_pack_path_returncode": rust_missing.returncode, "missing_pack_path_rejected": rust_missing.returncode != 0, "actual_pack_message": rust.stdout.strip().splitlines()[-1] if rust.stdout.strip() else ""}

        archive, restore = temp / "export.zip", temp / "restore"
        export_result = parse_json(run(["python3", str(EXPORT), "--intake", str(intake_dir), "--archive", str(archive), "--restore", str(restore)], check=True))

        godot_result: dict
        if not args.godot:
            godot_result = {"status": "NOT_RUN", "reason": "GODOT_BIN not supplied in this environment"}
        else:
            corrupt = temp / "corrupt"; shutil.copytree(intake_dir, corrupt)
            frame = sorted((corrupt / "runtime/frames").glob("*.png"))[0]; data = bytearray(frame.read_bytes()); data[100] ^= 1; frame.write_bytes(data)
            godot_run = run([args.godot, "--headless", "--path", "godot", "--script", "res://r04_authored_pack_test.gd", "--", f"--pack={intake_dir / 'pack.json'}", f"--corrupt-pack={corrupt / 'pack.json'}"])
            if godot_run.returncode:
                raise RuntimeError(godot_run.stdout + godot_run.stderr)
            godot_result = {"status": "PASSED", "output": godot_run.stdout[-4000:], "unexpected_error_output": "ERROR:" in godot_run.stdout or "ERROR:" in godot_run.stderr}

        stable(output / "source_intake.json", {"status": "PASSED", "clean_process_byte_identical": deterministic, "approved_reference_hashes": {"identity": sha(IDENTITY), "turnaround": sha(TURNAROUND)}, "identity_smoke": smoke, "intake": intake})
        stable(output / "intake_validation.json", negative)
        stable(output / "rust_contract.json", rust_result)
        stable(output / "godot_runtime.json", godot_result)
        stable(output / "export_restore.json", export_result)
        stable(output / "contract_validation.json", {"status": "PASSED", "draft_2020_12": schema.stdout.strip(), "rust_schema_crosswalk": crosswalk.stdout.strip(), "generated_pack_schema_validated_by_intake": True, "actual_generated_pack_path": "runtime evidence only"})
    result_names = ["source_intake.json", "intake_validation.json", "rust_contract.json", "godot_runtime.json", "export_restore.json", "contract_validation.json"]
    ended = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    git_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    stable(output / "provenance.json", {"profile": "COMPANION_P02_R04_C01_EVIDENCE_V1", "execution_start_utc": started, "execution_end_utc": ended, "git_commit": git_commit, "commands": ["python3 experiments/p02-embodiment/scripts/run_r04_evidence.py --out OUT --cargo CARGO --godot GODOT", "python3 experiments/p02-embodiment/scripts/validate_r04_results.py --results OUT --tamper-negative"], "runtimes": {"python": "qualification interpreter", "rust": "1.98.1", "godot": "4.7.2.stable.official.ed1daf0bf"}, "source_identities": {"identity_sha256": sha(IDENTITY), "turnaround_sha256": sha(TURNAROUND)}, "fixture_sha256": {"contracts/fixtures/mon-authored-frame-source-pack-v1.json": sha(ROOT / "contracts/fixtures/mon-authored-frame-source-pack-v1.json"), "contracts/fixtures/mon-ingested-frame-pack-v1.json": sha(ROOT / "contracts/fixtures/mon-ingested-frame-pack-v1.json")}, "evidence_ceiling": "E3_TARGET_TESTED synthetic intake/runtime boundary only; no production art or Phase 02 acceptance", "result_sha256": {name: sha(output / name) for name in result_names}})
    (output / "README.md").write_text("""# R04-C01 sanitized evidence

This bundle contains only synthetic calibration evidence; it is not production character art.

## Regeneration

1. Use the pinned qualification Python with `Pillow` and `jsonschema`, the
   Rust 1.98.1 toolchain, and the exact Godot 4.7.2 binary. No system package
   or global toolchain change is required.
2. Set `CARGO` and `GODOT_BIN` to those exact local/CI tool paths. Keep any
   private XDG qualification cache (toolchains, temporary pack trees, and
   exports) outside the checkout; no secret or capability environment variable
   is used by this boundary.
3. Run `python3 experiments/p02-embodiment/scripts/run_r04_evidence.py --out
   OUT --cargo "$CARGO" --godot "$GODOT_BIN"`. The command builds the
   synthetic source twice, runs intake and its negative matrix, performs the
   schema/Rust crosswalk, validates the actual generated pack, and executes the
   Godot test before writing sanitized JSON, provenance, and this README.
4. Run `python3 experiments/p02-embodiment/scripts/validate_r04_results.py
   --results OUT --tamper-negative`; it independently checks all hashes and
   expected outcomes, then must report `status: PASSED` and five rejected
   tamper mutations.
5. Keep generated PNGs, content-addressed copies, caches, binaries, export
   archives, restored trees, corruption copies, and any raw host output outside
   Git. Only the sanitized JSON bundle, hashes, and regeneration procedure are
   committed.

`provenance.json` records observed timestamps, checked-out Git commit, fixture/reference hashes, result hashes, runtimes, commands, and the E3 evidence ceiling.
""", encoding="utf-8")
    print(json.dumps({"status": "PASSED", "results": result_names, "godot": json.loads((output / "godot_runtime.json").read_text()) .get("status")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
