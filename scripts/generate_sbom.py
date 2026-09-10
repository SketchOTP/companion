#!/usr/bin/env python3
"""Generate a deterministic SPDX inventory from Cargo.lock."""
import argparse, hashlib, json, pathlib, re

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=pathlib.Path,required=True); a=ap.parse_args(); text=pathlib.Path("Cargo.lock").read_text(encoding="utf-8"); blocks=text.split("[[package]]")[1:]; packages=[]
    for block in blocks:
        name=re.search(r'^name = "([^"]+)"',block,re.M); version=re.search(r'^version = "([^"]+)"',block,re.M); source=re.search(r'^source = "([^"]+)"',block,re.M)
        if not name or not version: continue
        n=name.group(1); packages.append({"SPDXID":"SPDXRef-Package-"+re.sub(r"[^A-Za-z0-9.-]","_",n),"name":n,"versionInfo":version.group(1),"downloadLocation":source.group(1) if source else "NOASSERTION","licenseConcluded":"NOASSERTION","licenseDeclared":"NOASSERTION","checksums":[{"algorithm":"SHA256","checksumValue":"LOCKFILE-DERIVED"}]})
    packages.sort(key=lambda p:(p["name"],p["versionInfo"]))
    doc={"spdxVersion":"SPDX-2.3","dataLicense":"CC0-1.0","SPDXID":"SPDXRef-DOCUMENT","name":"companion-phase01-foundation","documentNamespace":"https://companion.local/sbom/phase01","creationInfo":{"created":"SOURCE_DATE_EPOCH_REQUIRED","creators":["Tool: companion-generate-sbom"]},"packages":packages,"relationships":[{"spdxElementId":"SPDXRef-DOCUMENT","relationshipType":"DESCRIBES","relatedSpdxElement":p["SPDXID"]} for p in packages]}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(doc,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(f"sbom_ok packages={len(packages)} sha256={hashlib.sha256(a.output.read_bytes()).hexdigest()}")
if __name__=="__main__": main()
