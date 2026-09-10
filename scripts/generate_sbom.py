#!/usr/bin/env python3
"""Generate a deterministic SPDX 2.3 inventory from Cargo metadata/lock."""
import argparse, datetime, hashlib, json, pathlib, re, subprocess, os

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=pathlib.Path,required=True); args=ap.parse_args()
    metadata=json.loads(subprocess.check_output([os.environ.get("CARGO", "cargo"),"metadata","--format-version","1","--locked"],text=True))
    lock=pathlib.Path("Cargo.lock").read_text(encoding="utf-8")
    checksums={}
    for block in lock.split("[[package]]")[1:]:
        n=re.search(r'^name = "([^"]+)"',block,re.M); v=re.search(r'^version = "([^"]+)"',block,re.M); c=re.search(r'^checksum = "([^"]+)"',block,re.M)
        if n and v and c: checksums[(n.group(1),v.group(1))]=c.group(1)
    packages=[]; relationships=[]
    for package in sorted(metadata["packages"],key=lambda p:(p["name"],p["version"])):
        ident="SPDXRef-Package-"+re.sub(r"[^A-Za-z0-9.-]","_",f"{package['name']}-{package['version']}")
        source=package.get("source") or "NOASSERTION"
        license_id=package.get("license") or "NOASSERTION"
        item={"SPDXID":ident,"name":package["name"],"versionInfo":package["version"],"downloadLocation":source,"licenseConcluded":license_id,"licenseDeclared":license_id,"supplier":"NOASSERTION"}
        checksum=checksums.get((package["name"],package["version"]))
        if checksum: item["checksums"]=[{"algorithm":"SHA256","checksumValue":checksum}]
        else: item["checksums"]=[]
        packages.append(item)
        for dependency in package.get("dependencies",[]):
            target=next((p for p in metadata["packages"] if p["name"]==dependency["name"] and p["source"]==dependency.get("source")),None)
            if target:
                relationships.append({"spdxElementId":ident,"relationshipType":"DEPENDS_ON","relatedSpdxElement":"SPDXRef-Package-"+re.sub(r"[^A-Za-z0-9.-]","_",f"{target['name']}-{target['version']}")})
    epoch=os.environ.get("SOURCE_DATE_EPOCH")
    created=datetime.datetime.fromtimestamp(int(epoch),datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z") if epoch else "SOURCE_DATE_EPOCH_REQUIRED"
    doc={"spdxVersion":"SPDX-2.3","dataLicense":"CC0-1.0","SPDXID":"SPDXRef-DOCUMENT","name":"companion-phase01-foundation","documentNamespace":"https://companion.local/sbom/phase01","creationInfo":{"created":created,"creators":["Tool: companion-generate-sbom"]},"packages":packages,"relationships":[{"spdxElementId":"SPDXRef-DOCUMENT","relationshipType":"DESCRIBES","relatedSpdxElement":p["SPDXID"]} for p in packages]+sorted(relationships,key=lambda r:(r["spdxElementId"],r["relatedSpdxElement"]))}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(doc,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(f"sbom_ok packages={len(packages)} sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")
if __name__=="__main__": main()
