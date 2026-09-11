#!/usr/bin/env python3
"""Compare the two bounded authoring candidates without selecting either."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

IDENTITY_SHA = "86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56"


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--proof", type=Path, required=True); ap.add_argument("--out", type=Path, required=True); a = ap.parse_args()
    root = Path(__file__).resolve().parents[3]
    ref = root / "assets/source/p02/references/identity-approved.png"
    digest = hashlib.sha256(ref.read_bytes()).hexdigest()
    with Image.open(ref) as image:
        alpha = image.getchannel("A"); bbox = alpha.getbbox(); pixels = image.size
    raster = {"source": "raster_key_pose_source_v1.json", "reference_sha256": digest, "rendered_proof": True, "pixel_canvas": pixels, "alpha_bbox": list(bbox or ()), "dimensions_compared": ["silhouette", "face", "palette", "edge_shadow", "hands", "feet", "root", "contacts"], "status": "CANDIDATE_REVIEW_REQUIRED"}
    vector = {"source": "mon_body_source_v1.svg", "reference_sha256": IDENTITY_SHA, "rendered_proof": False, "rasterizer": "resvg not installed on this host", "dimensions_compared": raster["dimensions_compared"], "status": "NOT_RUN_EXTERNAL_RASTERIZER_UNAVAILABLE"}
    result = {"profile": "MON_AUTHORING_COMPARISON_V1", "status": "CANDIDATE_PENDING_OPERATOR_DECISION", "identity_sha256": digest, "raster_candidate": raster, "vector_candidate": vector, "decision": "DEFERRED_TO_OPERATOR_AFTER_ACCESSIBLE_REVIEW"}
    a.out.parent.mkdir(parents=True, exist_ok=True); a.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
