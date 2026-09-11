#!/usr/bin/env python3
"""Validate the deterministic SPDX inventory shape and exact external inputs."""
import argparse, json, re
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",type=Path,required=True); a=p.parse_args()
    doc=json.loads(a.input.read_text(encoding="utf-8"))
    assert doc.get("spdxVersion") == "SPDX-2.3"
    assert doc.get("documentNamespace") == "https://companion.local/sbom/phase01"
    names={(x.get("name"),x.get("versionInfo")):x for x in doc.get("packages",[])}
    assert ("rustc","1.98.1") in names
    assert ("godot","4.7.2.stable.official.ed1daf0bf") in names
    assert ("sqlite","3.53.4") in names
    for pkg in doc["packages"]:
        assert pkg.get("SPDXID") and pkg.get("licenseDeclared")
        assert re.fullmatch(r"[A-Za-z0-9._-]+", pkg["SPDXID"].replace("SPDXRef-", ""))
    print(f"sbom_validation_ok packages={len(doc['packages'])}")

if __name__ == "__main__": main()
