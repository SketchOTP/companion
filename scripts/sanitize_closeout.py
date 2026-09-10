#!/usr/bin/env python3
"""Strip machine-specific identifiers from private closeout runner output."""
import argparse, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument("--kind", choices=("soak", "phase01", "failure"), required=True); p.add_argument("--input", type=Path, required=True); p.add_argument("--output", type=Path, required=True); a=p.parse_args()
    value=json.loads(a.input.read_text(encoding="utf-8"))
    if a.kind == "soak":
        samples=[]
        for row in value.get("samples", []):
            samples.append({k: row[k] for k in ("elapsed_seconds", "status", "care_coverage", "checkout_write_detected", "health_sha256") if k in row} | {"resources": {k: row.get("resources", {}).get(k) for k in ("rss_bytes", "cpu_ticks")}, "network": {"owned_count": row.get("network", {}).get("owned_count"), "error": row.get("network", {}).get("error")}})
        value={k:value.get(k) for k in ("status","started_utc","ended_utc","duration_seconds","samples","failures","injections","resident_supervisor_observed","godot_process_observed","checkout_write_detected","network_owned_counts","evidence_ceiling","claim_boundary")}; value["sample_observations"]=samples
    a.output.parent.mkdir(parents=True, exist_ok=True); a.output.write_text(json.dumps(value, indent=2, sort_keys=True)+"\n", encoding="utf-8")
if __name__ == "__main__": main()
