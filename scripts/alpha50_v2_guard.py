#!/usr/bin/env python3
"""Fail closed if the Alpha acceptance binary regresses to historical V1."""
from pathlib import Path
import re
import argparse

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--source", type=Path, required=True); args = ap.parse_args()
    text = args.source.read_text(encoding="utf-8")
    forbidden = (r"\bOrganismState\b", r"organism::", r"record_interaction", r"record_action_outcome", r"correct_memory")
    hits = [token for token in forbidden if re.search(token, text)]
    if hits:
        print("V1_ACCEPTANCE_GUARD_FAIL", ",".join(hits)); return 1
    print("V2_ACCEPTANCE_GUARD_PASS"); return 0

if __name__ == "__main__": raise SystemExit(main())
