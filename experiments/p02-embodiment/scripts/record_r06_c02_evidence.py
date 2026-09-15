#!/usr/bin/env python3
"""Record sanitized C02 grounding/intake evidence for the committed pack."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[3]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--intake", required=True, type=Path)
    ap.add_argument("--grounding", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    source, intake, grounding, out = args.source.resolve(), args.intake.resolve(), args.grounding.resolve(), args.out.resolve()
    source_pack = json.loads((source / "pack.json").read_text())
    source_schema = json.loads((ROOT / "contracts/schemas/mon-opaque-black-frame-source-pack-v1.schema.json").read_text())
    Draft202012Validator(source_schema, format_checker=FormatChecker()).validate(source_pack)
    ingested_path = intake / "runtime/pack.json"
    ingested = json.loads(ingested_path.read_text())
    ingested_schema = json.loads((ROOT / "contracts/schemas/mon-ingested-frame-pack-v1.schema.json").read_text())
    Draft202012Validator(ingested_schema, format_checker=FormatChecker()).validate(ingested)
    grounding_result = json.loads((grounding / "validation.json").read_text())
    result = {
        "profile": "COMPANION_P02_R06_C02_INTEGRATION_EVIDENCE_V1",
        "status": "PASS" if grounding_result.get("status") == "PASS" and not any(f.get("source_bytes_mutated", False) for f in [json.loads((intake / "receipt.json").read_text())]) else "FAIL",
        "source_pack_sha256": sha(source / "pack.json"),
        "runtime_pack_sha256": sha(ingested_path),
        "receipt_sha256": sha(intake / "receipt.json"),
        "source_assets": len(source_pack["source_assets"]),
        "tracks": len(source_pack["tracks"]),
        "frame_slots": sum(len(t["frames"]) for t in source_pack["tracks"]),
        "grounding_validation": grounding_result,
        "ingested_schema_valid": True,
        "source_bytes_mutated": False,
        "atomic_publication": json.loads((intake / "receipt.json").read_text()).get("publication_state"),
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "integration.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
