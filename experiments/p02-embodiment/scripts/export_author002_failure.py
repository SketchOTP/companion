#!/usr/bin/env python3
"""Package rejected study evidence; never produces an intake or animation pack."""
import argparse
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_exact(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    original = source.read_bytes()
    destination.write_bytes(original)
    if destination.read_bytes() != original or source.read_bytes() != original:
        raise AssertionError("evidence bytes changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=Path, required=True)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--cutouts", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    request = json.loads(args.requests.read_text())
    results = []
    for study in request["studies"]:
        source = args.raw / study["file"]
        destination = args.out / study["group"] / (study["id"] + ".png")
        copy_exact(source, destination)
        with Image.open(source) as im:
            row = {**study, "artifact_path": destination.relative_to(args.out).as_posix(),
                   "sha256": digest(source), "size": list(im.size), "mode": im.mode,
                   "byte_preservation": "PASSED"}
        results.append(row)
    for path in sorted(args.cutouts.iterdir()):
        if path.suffix in (".png", ".json"):
            copy_exact(path, args.out / "cutouts" / path.name)
    for path in sorted(args.review.iterdir()):
        if path.suffix in (".png", ".json"):
            copy_exact(path, args.out / "review" / path.name)
    compare = ["left_passing_near", "left_passing_repair", "left_passing_repair2",
               "left_passing_far", "right_contact_near", "right_passing_near"]
    board = Image.new("RGB", (1800, 1320), "#ececf0")
    draw = ImageDraw.Draw(board)
    draw.text((12, 10), "AUTHOR-002: REJECTED KEY STUDIES - NO INTAKE / NO ANIMATION QUALITY CLAIM", fill="black")
    for index, name in enumerate(compare):
        path = args.out / "gait" / (name + ".png")
        with Image.open(path) as im:
            view = im.convert("RGBA")
            view.thumbnail((580, 580), Image.Resampling.LANCZOS)
            x, y = (index % 3) * 600 + 10, (index // 3) * 630 + 42
            board.paste(view, (x, y), view)
        draw.text((x, y + 590), name, fill="black")
    board.save(args.out / "review" / "key-gate-failure.png")
    receipt = {"directive": request["directive"], "status": request["status"],
               "evidence_level": "E1_OBSERVED", "visual_assessment": "MODEL_NOT_OPERATOR",
               "observed_at_utc": datetime.now(timezone.utc).isoformat(),
               "construction_output_count": sum(r["group"] == "construction" for r in results),
               "gait_output_count": sum(r["group"] == "gait" for r in results),
               "promoted_frame_count": 0, "studies": results,
               "downstream": {k: "NOT_RUN" for k in ("normalization", "v2_intake", "rust_v2", "godot_v2", "world_contact_qa", "complete_action_playback")}}
    (args.out / "study-results.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    files = sorted(p for p in args.out.rglob("*") if p.is_file())
    manifest = {p.relative_to(args.out).as_posix(): digest(p) for p in files}
    (args.out / "SHA256.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    # Two independently usable archives keep uploads bounded; no archive is a runtime pack.
    for group in ("construction", "gait", "review"):
        archive = args.out.parent / (args.out.name + "-" + group + ".zip")
        if archive.exists():
            raise FileExistsError("refuse archive overwrite")
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as z:
            for path in sorted((args.out / group).rglob("*")):
                if path.is_file():
                    z.write(path, path.relative_to(args.out))
            for name in ("study-results.json", "SHA256.json"):
                z.write(args.out / name, name)
        print(json.dumps({"archive": archive.name, "bytes": archive.stat().st_size, "sha256": digest(archive)}))
    print(json.dumps({"studies": len(results), "all_exact_copies": True, "promoted_frames": 0}))


if __name__ == "__main__":
    main()
