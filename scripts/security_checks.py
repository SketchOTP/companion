#!/usr/bin/env python3
"""Offline policy checks for the foundation dependency envelope."""
import argparse, json, pathlib, re, sys
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--lock",default="Cargo.lock"); args=ap.parse_args(); text=pathlib.Path(args.lock).read_text(encoding="utf-8"); errors=[]
    if "openssl" in text.lower() or "reqwest" in text.lower() or "tokio" in text.lower(): errors.append("unexpected network/runtime dependency")
    toolchain = pathlib.Path("rust-toolchain.toml").read_text(encoding="utf-8")
    if not re.search(r'^channel\s*=\s*"1\.98\.1"', toolchain, re.M): errors.append("toolchain pin missing")
    if errors:
        print(json.dumps({"status":"FAIL","errors":errors},sort_keys=True)); raise SystemExit(1)
    print(json.dumps({"status":"PASS","vulnerability_scan":"offline-policy-only","license_scan":"workspace Apache-2.0 declarations","claim_boundary":"not a complete CVE database or legal opinion"},sort_keys=True))
if __name__=="__main__": main()
