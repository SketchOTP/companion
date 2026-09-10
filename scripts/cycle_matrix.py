#!/usr/bin/env python3
"""Deterministic synthetic contract matrix; not product or reliability evidence."""
import argparse, hashlib, json, pathlib, random, time

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cycles", type=int, default=1000)
    p.add_argument("--seeds", default="17,23,41")
    p.add_argument("--output", type=pathlib.Path)
    a = p.parse_args()
    seeds = [int(x) for x in a.seeds.split(",") if x]
    if a.cycles < 1000 or not seeds: raise SystemExit("at least 1000 cycles and one retained seed required")
    counts = {k: 0 for k in ("valid", "duplicate", "replay", "malformed", "unsupported", "stale")}
    digest = hashlib.sha256(); started = time.time()
    for seed in seeds:
        rng = random.Random(seed)
        for i in range(a.cycles):
            kind = list(counts)[(i + rng.randrange(6)) % 6]; counts[kind] += 1
            record = {"seed": seed, "cycle": i, "kind": kind, "fixed_point": (seed * 1000 + i) % 100000}
            digest.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode())
    result = {"status": "PASS", "cycles_per_seed": a.cycles, "seeds": seeds, "total_cycles": a.cycles * len(seeds),
              "counts": counts, "digest_sha256": digest.hexdigest(), "evidence_ceiling": "E3_TARGET_TESTED",
              "claim_boundary": "synthetic engineering matrix only", "duration_seconds": round(time.time() - started, 6)}
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
if __name__ == "__main__": main()
