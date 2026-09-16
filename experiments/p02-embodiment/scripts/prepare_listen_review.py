#!/usr/bin/env python3
"""Bind selected imagegen outputs to review timing; never edit image pixels."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare(root, selection_path):
    selection = json.loads(selection_path.read_text())
    sequence = selection["sequence"]
    if sequence[0]["drawing_id"] != "front" or sequence[-1]["drawing_id"] != "front":
        raise ValueError("rest_endpoints_required")
    rejected = selection["rejected"]
    ids = list(dict.fromkeys(f["drawing_id"] for f in sequence))
    if set(ids) & set(rejected):
        raise ValueError("rejected_drawing_selected")
    for f in sequence:
        if type(f["duration_ticks"]) is not int or f["duration_ticks"] <= 0:
            raise ValueError("invalid_duration")
        if Path(f["drawing_id"]).name != f["drawing_id"]:
            raise ValueError("unsafe_drawing_id")
    drawings = []
    inventory = []
    for p in sorted((root / "raw").glob("*.png")):
        with Image.open(p) as im:
            im.load()
            size, mode = list(im.size), im.mode
        inventory.append({"id": p.stem, "sha256": sha(p), "size": size, "mode": mode,
                          "selected": p.stem in ids, "rejection": rejected.get(p.stem)})
    lookup = {r["id"]: r for r in inventory}
    for name in ids:
        row = lookup[name]
        if row["size"] != [1254, 1254] or row["mode"] != "RGB":
            raise ValueError("unexpected_raw_review_format")
        drawings.append({"id": name, "file": name + ".png", "sha256": row["sha256"]})
    if len({r["sha256"] for r in drawings}) != len(drawings):
        raise ValueError("duplicate_source_bytes")
    result = {"profile": "BLACK_LISTEN_ACK_REVIEW_V1", "approval_state": "candidate",
              "production_intake": "NOT_RUN", "completion_status": "CONNECTED_CANDIDATE_REVIEW",
              "drawings": drawings, "tracks": [{"id": "listen_acknowledge_connected",
              "completion": "once", "frames": sequence}]}
    (root / "requests.json").write_text(json.dumps(result, indent=2) + "\n")
    evidence = {"status": "PASSED_SOURCE_BINDING_ONLY", "raw_files": inventory,
                "selected_drawings": len(ids), "slots": len(sequence),
                "ticks": sum(f["duration_ticks"] for f in sequence), "fps": 24,
                "requests_sha256": sha(root / "requests.json"),
                "selection_sha256": sha(selection_path), "prompts_sha256": sha(root / "prompts.json"),
                "root_contacts": "NOT_QUALIFIED", "production_approval": "NOT_RUN"}
    (root / "source_evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
    return evidence

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--selection", type=Path, required=True)
    a = ap.parse_args()
    print(json.dumps(prepare(a.root, a.selection)))
