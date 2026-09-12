#!/usr/bin/env python3
"""Build and qualify the actual R05 operator-authorized candidate sprite pack."""
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

from PIL import Image

from run_godot_qualification import run_qualification

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "experiments/p02-embodiment/scripts/build_r05_candidate_pack.py"
INTAKE = ROOT / "experiments/p02-embodiment/scripts/intake_authored_frame_pack.py"
EXPORT = ROOT / "experiments/p02-embodiment/scripts/export_restore_authored_pack.py"
SHEETS = ROOT / "assets/source/p02/r05/imagegen"
COMMITTED_MANIFEST = ROOT / "assets/source/p02/r05/candidate-source-pack-manifest.json"
EXPECTED_ROLES = {
    ("neutral_construction", "front"): 1,
    ("neutral_construction", "right"): 1,
    ("neutral_construction", "front_left"): 1,
    ("idle_breathe", "front_left"): 8,
    ("walk", "front_left"): 8,
    ("orient_front_to_front_left", "front"): 4,
    ("orient_front_left_to_front", "front_left"): 4,
    ("listen_acknowledge", "front_left"): 6,
}
RESULT_NAMES = [
    "candidate_pack.json",
    "intake.json",
    "rust_contract.json",
    "godot_runtime.json",
    "frame_qa.json",
    "export_restore.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(item.read_bytes()).digest())
    return digest.hexdigest()


def stable(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def command(argv: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv[0]} {argv[1]}\n{result.stderr[-2000:]}")
    return result


def parse_stdout(result: subprocess.CompletedProcess[str]) -> dict:
    for line in reversed(result.stdout.splitlines()):
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise RuntimeError("command did not emit a JSON result")


def mutate_frame(pack_root: Path) -> None:
    frame = pack_root / "runtime/frames/neutral_construction__front__neutral__v01__f000.png"
    with Image.open(frame) as source:
        image = source.convert("RGBA")
    pixel = image.getpixel((512, 512))
    image.putpixel((512, 512), (pixel[0] ^ 1, pixel[1], pixel[2], pixel[3]))
    image.save(frame, "PNG", optimize=False)


def frame_qa(source: Path, pack: dict) -> dict:
    roots_ok = True
    safety_violations: list[str] = []
    perimeter_violations: list[str] = []
    planted: list[dict] = []
    for track in pack["tracks"]:
        starts: list[int] = []
        tick = 0
        for frame in track["frames"]:
            starts.append(tick)
            tick += frame["duration_ticks"]
            roots_ok &= frame["landmarks"]["root"] == {"state": "visible", "point": {"x": 512, "y": 896}}
            path = source / "frames" / frame["filename"]
            with Image.open(path) as opened:
                image = opened.convert("RGBA")
            box = image.getchannel("A").getbbox()
            if box is None or box[0] < 64 or box[1] < 32 or box[2] > 961 or box[3] > 961:
                safety_violations.append(frame["frame_id"])
            alpha = image.getchannel("A")
            if any(alpha.getpixel(point) for point in [(x, 0) for x in range(1024)] + [(x, 1023) for x in range(1024)] + [(0, y) for y in range(1024)] + [(1023, y) for y in range(1024)]):
                perimeter_violations.append(frame["frame_id"])
        for span in track["contacts"]:
            if span["state"] != "planted":
                continue
            points = []
            for start, frame in zip(starts, track["frames"], strict=True):
                if span["start_tick"] <= start < span["end_tick"]:
                    value = frame["landmarks"][span["landmark"]]
                    if value["state"] == "visible":
                        points.append((value["point"]["x"], value["point"]["y"]))
            drift = max((max(p[i] for p in points) - min(p[i] for p in points) for i in (0, 1)), default=0)
            planted.append({"track_id": track["track_id"], "landmark": span["landmark"], "sample_count": len(points), "max_rendered_drift_px": drift, "status": "PASSED" if points and drift <= 2 else "FAILED"})
    unique = {frame["source_sha256"] for track in pack["tracks"] for frame in track["frames"]}
    return {
        "status": "PASSED" if roots_ok and not safety_violations and not perimeter_violations and all(row["status"] == "PASSED" for row in planted) else "FAILED",
        "profile": "COMPANION_P02_R05_FRAME_QA_V1",
        "root_metadata_exact": roots_ok,
        "safety_region_violations": safety_violations,
        "transparent_perimeter_violations": perimeter_violations,
        "planted_contact_observations": planted,
        "frame_occurrences": sum(len(track["frames"]) for track in pack["tracks"]),
        "unique_source_hashes": len(unique),
        "identity_quality": "OPERATOR_VISUAL_REVIEW_PENDING",
        "evidence_ceiling": "Rendered bounds/contact observations; automated checks do not approve identity or motion quality.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cargo", default=os.environ.get("CARGO", "cargo"))
    parser.add_argument("--godot", type=Path, required=True)
    args = parser.parse_args()
    output = args.out.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    artifact = output / "artifact"
    source = artifact / "source-pack"
    ingested = artifact / "ingested-pack"
    started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    build_result = parse_stdout(command(["python3", str(BUILD), "--sheets", str(SHEETS), "--out", str(source), "--clean"], check=True))
    with tempfile.TemporaryDirectory(prefix="companion-p02-r05-") as temporary:
        temp = Path(temporary)
        second = temp / "source-pack-second"
        command(["python3", str(BUILD), "--sheets", str(SHEETS), "--out", str(second), "--clean"], check=True)
        deterministic = tree_sha(source) == tree_sha(second)
        pack = json.loads((source / "pack.json").read_text(encoding="utf-8"))
        roles = {(track["family"], track["selection_facing"]): len(track["frames"]) for track in pack["tracks"]}
        committed_equal = (source / "pack.json").read_bytes() == COMMITTED_MANIFEST.read_bytes()
        intake_result = parse_stdout(command(["python3", str(INTAKE), "intake", "--source", str(source), "--out", str(ingested), "--operation", "review"], check=True))

        for argv in (["python3", "scripts/validate_schemas.py"], ["python3", "scripts/check_contract_types.py"]):
            command(argv, check=True)

        rust = command([args.cargo, "run", "-p", "foundation-core", "--bin", "validate-authored-pack", "--locked", "--", str(ingested / "pack.json")])
        missing = command([args.cargo, "run", "-p", "foundation-core", "--bin", "validate-authored-pack", "--locked", "--"])
        if rust.returncode != 0 or missing.returncode == 0:
            raise RuntimeError(f"Rust actual-pack gate failed: actual={rust.returncode} missing={missing.returncode}\n{rust.stderr[-2000:]}")

        corrupt = temp / "corrupt-pack"
        shutil.copytree(ingested, corrupt)
        mutate_frame(corrupt)
        import_result = run_qualification(godot=args.godot.resolve(), out=output / "diagnostics/import", mode="import", label="r05-import")
        godot_runs = []
        script_args = [f"--pack={ingested / 'pack.json'}", f"--corrupt-pack={corrupt / 'pack.json'}", "--operation=review"]
        for label in ("r05-cold", "r05-warm"):
            godot_runs.append(run_qualification(godot=args.godot.resolve(), out=output / f"diagnostics/{label}", mode="semantic", pack=ingested / "pack.json", corrupt_pack=corrupt / "pack.json", label=label, script_args=script_args))

        archive = temp / "candidate-export.zip"
        restore = temp / "restored"
        export_result = parse_stdout(command(["python3", str(EXPORT), "--intake", str(ingested), "--archive", str(archive), "--restore", str(restore)], check=True))

    frame_result = frame_qa(source, pack)
    candidate = {
        "status": "PASSED" if deterministic and committed_equal and roles == EXPECTED_ROLES else "FAILED",
        "profile": "COMPANION_P02_R05_CANDIDATE_PACK_V1",
        "pack_id": pack["pack_id"],
        "pack_revision": pack["pack_revision"],
        "approval_state": pack["approval_state"],
        "request_profile": pack["request_profile"],
        "track_count": len(pack["tracks"]),
        "frame_occurrences": sum(len(track["frames"]) for track in pack["tracks"]),
        "unique_source_hashes": len({frame["source_sha256"] for track in pack["tracks"] for frame in track["frames"]}),
        "expected_roles": [{"family": key[0], "selection_facing": key[1], "frame_count": value} for key, value in EXPECTED_ROLES.items()],
        "observed_roles": [{"family": key[0], "selection_facing": key[1], "frame_count": value} for key, value in roles.items()],
        "clean_process_byte_identical": deterministic,
        "committed_manifest_byte_identical": committed_equal,
        "source_pack_sha256": sha(source / "pack.json"),
        "source_tree_sha256": tree_sha(source),
        "source_sheet_sha256": build_result["source_sheet_sha256"],
        "operator_visual_approval": "PENDING",
    }
    godot = {
        "status": "PASSED" if import_result["status"] == "PASSED" and all(run["status"] == "PASSED" for run in godot_runs) else "FAILED",
        "import": import_result,
        "runs": godot_runs,
        "godot_error_count": import_result["godot_error_count"] + sum(run["godot_error_count"] for run in godot_runs),
        "render_observation": "RenderingServer.frame_post_draw",
    }
    stable(output / "candidate_pack.json", candidate)
    stable(output / "intake.json", intake_result)
    stable(output / "rust_contract.json", {
        "status": "PASSED", "actual_pack_returncode": rust.returncode,
        "missing_pack_path_returncode": missing.returncode, "missing_pack_path_rejected": True,
        "message": rust.stdout.strip().splitlines()[-1], "track_count": len(pack["tracks"]),
    })
    stable(output / "godot_runtime.json", godot)
    stable(output / "frame_qa.json", frame_result)
    stable(output / "export_restore.json", export_result)
    ended = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    commit = command(["git", "rev-parse", "HEAD"], check=True).stdout.strip()
    stable(output / "provenance.json", {
        "profile": "COMPANION_P02_R05_EVIDENCE_PROVENANCE_V1",
        "execution_start_utc": started,
        "execution_end_utc": ended,
        "git_commit": commit,
        "command": "python3 experiments/p02-embodiment/scripts/run_r05_candidate_evidence.py --out OUT --cargo CARGO --godot GODOT",
        "runtimes": {"python": "qualification interpreter", "rust": "1.98.1", "godot": "4.7.2.stable.official.ed1daf0bf"},
        "source_identities": {"identity_sha256": "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56", "turnaround_sha256": "3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4"},
        "source_sheet_sha256": build_result["source_sheet_sha256"],
        "artifact_tree_sha256": tree_sha(artifact),
        "result_sha256": {name: sha(output / name) for name in RESULT_NAMES},
        "evidence_ceiling": "E3_TARGET_TESTED candidate art intake/playback plus visual review material; operator approval and Phase 02 acceptance remain pending.",
    })
    (output / "README.md").write_text(
        "# R05 candidate pack evidence\n\nGenerated normalized frames, typed sidecars, review media, and the immutable ingested pack are under `artifact/`. The art remains `candidate`; automated validation does not approve identity or motion quality. Regenerate with the command in `provenance.json`, then run `python3 experiments/p02-embodiment/scripts/validate_r05_results.py --results OUT --tamper-negative`.\n",
        encoding="utf-8",
    )
    overall = all(item["status"] == "PASSED" for item in (candidate, godot, frame_result))
    print(json.dumps({"status": "PASSED" if overall else "FAILED", "tracks": candidate["track_count"], "frame_occurrences": candidate["frame_occurrences"], "unique_source_hashes": candidate["unique_source_hashes"], "operator_visual_approval": "PENDING"}, sort_keys=True))
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
