#!/usr/bin/env python3
"""Generate a minimal SPDX inventory from the locked foundation manifest."""
import argparse, json, pathlib, subprocess, time
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output", type=pathlib.Path, required=True); a=ap.parse_args()
    lock=pathlib.Path("Cargo.lock").read_text(encoding="utf-8")
    names=[]
    for line in lock.splitlines():
        if line.startswith("name = "): names.append(line.split("=",1)[1].strip().strip('"'))
    doc={"spdxVersion":"SPDX-2.3","dataLicense":"CC0-1.0","SPDXID":"SPDXRef-DOCUMENT","name":"companion-phase01-foundation","documentNamespace":"https://companion.local/sbom/phase01","creationInfo":{"created":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"creators":["Tool: companion-generate-sbom"]},"packages":[{"SPDXID":"SPDXRef-Package-"+name.replace("-","_"),"name":name,"versionInfo":"locked","downloadLocation":"NOASSERTION","licenseConcluded":"NOASSERTION"} for name in sorted(set(names))]}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(doc,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(f"sbom_ok packages={len(doc['packages'])}")
if __name__ == "__main__": main()
