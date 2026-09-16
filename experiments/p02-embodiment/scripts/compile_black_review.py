#!/usr/bin/env python3
"""Compile existing black-backed art into an offline review, never new art."""
import argparse
import hashlib
import json
import shutil
import struct
from pathlib import Path

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_bundle(directory, prefix, out):
    request = json.loads((directory / "requests.json").read_text())
    assets = {}
    for row in request["drawings"]:
        name = row["id"]
        if Path(row["file"]).name != row["file"]:
            raise ValueError("unsafe_source_path")
        source = directory / "raw" / row["file"]
        if sha(source) != row["sha256"]:
            raise ValueError("source_hash_mismatch")
        key = prefix + "_" + name
        dest = out / "raw" / (key + ".png")
        shutil.copyfile(source, dest)
        if dest.read_bytes() != source.read_bytes():
            raise ValueError("copy_mismatch")
        assets[key] = {"path": "raw/" + dest.name, "sha256": sha(dest),
                       "source_id": name, "source_bundle": prefix}
    tracks = []
    for item in request["tracks"]:
        frames = []
        for f in item["frames"]:
            if type(f["duration_ticks"]) is not int or f["duration_ticks"] <= 0:
                raise ValueError("invalid_ticks")
            key = prefix + "_" + f["drawing_id"]
            if key not in assets:
                raise ValueError("missing_drawing")
            frames.append({"asset": key, "ticks": f["duration_ticks"], "label": f["label"]})
        tracks.append({"id": prefix + "_" + item["id"], "title": item["id"].replace("_", " "),
                       "frames": frames, "completion": item["completion"],
                       "group": "Diagnostics" if prefix == "retry" else "Individual studies",
                       "note": "Existing drawings only. Known continuity defects; no interpolation or new frames."})
    return assets, tracks

def compose(track_id, title, parts):
    frames = []
    for part in parts:
        frames.extend({**f, "stage": f.get("stage", part["title"])} for f in part["frames"])
    return {"id": track_id, "title": title, "frames": frames, "completion": "once",
            "group": "Full review", "note": "Full action ordering using available key drawings. Missing in-betweens remain visible."}

def validate(data, root):
    assert data["status"] == "ASSEMBLED_EXISTING_FRAMES_NOT_FINISHED_ANIMATION"
    assert len({t["id"] for t in data["tracks"]}) == len(data["tracks"])
    for key, asset in data["assets"].items():
        assert sha(root / asset["path"]) == asset["sha256"], key
    for track in data["tracks"]:
        assert track["completion"] in ("once", "loop")
        assert track["frames"]
        for frame in track["frames"]:
            assert frame["asset"] in data["assets"]
            assert type(frame["ticks"]) is int and frame["ticks"] > 0
    assert len(data["coverage"]) == 12
    for row in data["coverage"]:
        item = next(t for t in data["tracks"] if t["id"] == row["track_id"])
        assert row["available_unique_drawings"] == len({f["asset"] for f in item["frames"]})
        assert row["status"] in ("INCOMPLETE", "CANDIDATE_DRAWINGS_REVIEW_REQUIRED")
    return True

def build(args):
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / "raw").mkdir()
    assets, base = load_bundle(args.studies, "base", out)
    extra, retry = load_bundle(args.retry, "retry", out)
    assets.update(extra)
    by = {t["id"].removeprefix("base_"): t for t in base}
    listen_history = []
    if getattr(args, "listen", None):
        added, connected = load_bundle(args.listen, "listen", out)
        shutil.copytree(args.listen, out / "authoring")
        if len(connected) != 1 or connected[0]["id"] != "listen_listen_acknowledge_connected":
            raise ValueError("unexpected_listen_track")
        assets.update(added)
        old = dict(by["front_listen_acknowledge_key_study"])
        old["title"] = "Historical Listen → Ack — three-pose blocking"
        listen_history.append(old)
        track = connected[0]
        track["note"] = "New reference-edited candidate drawings: attention → listen hold → one acknowledgment → follow-through → rest. No source warping or runtime interpolation. Visual approval and measured contacts remain open."
        by["front_listen_acknowledge_key_study"] = track
    coverage = []
    individual = []
    mappings = [("idle_breathe_front", "front_breathe_key_study", 16),
                ("listen_acknowledge_front", "front_listen_acknowledge_key_study", 16)]
    for side in ("left", "right"):
        mappings += [(f"turn_front_to_{side}", side + "_outward_turn_key_study", 8),
                     (f"walk_start_{side}", side + "_start_key_study", 6),
                     (f"walk_loop_{side}", side + "_gait_key_study", 16),
                     (f"walk_stop_{side}", side + "_stop_key_study", 6),
                     (f"turn_{side}_to_front", side + "_return_turn_key_study", 8)]
    for name, old, floor in mappings:
        item = by[old]
        item["title"] = name.replace("_", " ")
        item["group"] = "12 required actions"
        unique = len({f["asset"] for f in item["frames"]})
        coverage.append({"action": name, "available_slots": len(item["frames"]),
                         "available_unique_drawings": unique, "required_min": floor,
                         "status": "CANDIDATE_DRAWINGS_REVIEW_REQUIRED" if unique >= floor else "INCOMPLETE", "track_id": item["id"]})
        individual.append(item)
    full = []
    for side in ("left", "right"):
        parts = [by[side + "_outward_turn_key_study"], by[side + "_start_key_study"],
                 by[side + "_gait_key_study"], by[side + "_gait_key_study"],
                 by[side + "_stop_key_study"], by[side + "_return_turn_key_study"],
                 by["front_breathe_key_study"]]
        full.append(compose("full_" + side, side.title() + " — turn, start, two cycles, stop, return, breathe", parts))
    full.append(compose("full_presence", "Front — breathe, listen, acknowledge, settle, breathe",
                        [by["front_breathe_key_study"], by["front_listen_acknowledge_key_study"],
                         by["front_breathe_key_study"]]))
    reel = compose("full_reel", "All actions — complete review reel", full)
    for item in base:
        if item["id"].startswith("base_construction"):
            item["group"] = "Eight facings"
    diagnostics = [t for t in base if "inbetween_diagnostic" in t["id"]] + retry + listen_history
    for diagnostic in diagnostics:
        diagnostic["group"] = "Diagnostics"
    sheet_prov = json.loads((args.sheets / "provenance.json").read_text())
    for index, row in enumerate(sheet_prov["attempts"]):
        source = args.sheets / row["file"]
        if sha(source) != row["sha256"]:
            raise ValueError("sheet_hash_mismatch")
        key = "sheet_" + str(index)
        target = out / "raw" / row["file"]
        shutil.copyfile(source, target)
        if source.read_bytes() != target.read_bytes():
            raise ValueError("copy_mismatch")
        data = source.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("not_png")
        w, h = struct.unpack(">II", data[16:24])
        assets[key] = {"path": "raw/" + row["file"], "sha256": sha(target), "source_id": row["file"]}
        frames = []
        for i in range(16):
            x0, y0 = (i % 4) * w // 4, (i // 4) * h // 4
            x1, y1 = (i % 4 + 1) * w // 4, (i // 4 + 1) * h // 4
            frames.append({"asset": key, "ticks": 2, "label": "sheet cell " + str(i),
                           "crop": [x0, y0, x1 - x0, y1 - y0]})
        diagnostics.append({"id": key, "title": "Rejected joint-sheet walk" + (" — repair" if index else ""),
                            "frames": frames, "completion": "loop", "group": "Diagnostics",
                            "note": row["observation"] + " Equal-grid playback only; registration is not corrected."})
    data = {"profile": "COMPILED_BLACK_REVIEW_V1", "status": "ASSEMBLED_EXISTING_FRAMES_NOT_FINISHED_ANIMATION",
            "fps": 24, "assets": assets, "coverage": coverage,
            "tracks": [reel] + full + individual +
                      [t for t in base if t["group"] == "Eight facings"] + diagnostics,
            "source_pixels_modified": False, "new_drawings_created": 0,
            "additional_authored_bundle": bool(getattr(args, "listen", None)),
            "world_contacts": "NOT_RUN", "operator_motion_approval": "NOT_RUN"}
    if getattr(args, "listen", None):
        authored = json.loads((args.listen / "prompts.json").read_text())["new_outputs"]
        authored_ids = {row["id"] for row in authored}
        data["authoring_campaign_outputs"] = len(authored_ids)
        data["included_newly_authored_drawings"] = sum(
            key.removeprefix("listen_") in authored_ids for key in assets if key.startswith("listen_"))
    validate(data, out)
    text = json.dumps(data, indent=2, sort_keys=True)
    (out / "manifest.json").write_text(text + "\n")
    template = Path(__file__).with_name("compiled_black_review.html").read_text()
    (out / "index.html").write_text(template.replace("/*__MANIFEST__*/", text.replace("</", "<\\/")))
    (out / "README.txt").write_text("Open index.html in a browser. No install/server required.\n"
        "This compiles candidate drawings, NOT production-approved animation. Use 1x/0.25x, frame stepping and timeline.\n"
        "Full reel and complete action orderings are provided. Diagnostics remain separate.\n"
        "Source PNGs are byte-identical copies; sheet crops occur only while drawing the review canvas.\n")
    result = {"status": "PASSED_REVIEW_ASSEMBLY", "assets": len(assets), "tracks": len(data["tracks"]),
              "required_actions": 12, "new_drawings": 0, "completed_production_tracks": 0,
              "included_newly_authored_drawings": data.get("included_newly_authored_drawings", 0),
              "manifest_sha256": sha(out / "manifest.json"), "html_sha256": sha(out / "index.html"),
              "files": {p.relative_to(out).as_posix(): sha(p) for p in sorted(out.rglob("*")) if p.is_file()}}
    (out / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "files"}))
    return data

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ("studies", "retry", "sheets", "out"):
        ap.add_argument("--" + name, type=Path, required=True)
    ap.add_argument("--listen", type=Path, help="Optional separately authored Listen/Ack review bundle")
    build(ap.parse_args())
