#!/usr/bin/env python3
"""Explicit, operator-authorized offline-authoring cutout call; never runtime.

References iHero's provider boundary; no iHero jobs, orders, or notifications run.
Credentials are read only from the explicitly supplied env file and never logged.
Canonical intake must happen after this source-authoring operation.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
import uuid

from PIL import Image

PROVIDERS = {
    "removebg": ("https://api.remove.bg/v1.0/removebg", "REMOVEBG_API_KEY", "X-Api-Key"),
    "photoroom": ("https://sdk.photoroom.com/v1/segment", "PHOTOROOM_API_KEY", "x-api-key"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--credentials-file", type=Path, required=True)
    ap.add_argument("--provider", choices=PROVIDERS, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise SystemExit("output_exists")
    endpoint, key_name, header = PROVIDERS[args.provider]
    values = {}
    for line in args.credentials_file.read_text().splitlines():
        key, sep, value = line.partition("=")
        if sep and key.strip() == key_name:
            values[key_name] = value.strip().strip("\"'")
    secret = values.get(key_name) or os.environ.get(key_name)
    if not secret:
        raise SystemExit("provider_credential_missing")
    source = args.source.read_bytes()
    boundary = "companion-" + uuid.uuid4().hex
    fields = {"format": "png"}
    if args.provider == "removebg":
        fields.update(size="full", crop="false", type="graphic")
    else:
        # Review 11: explicit cutout-subject RGBA, no provider crop/resize.
        fields.update(channels="rgba", size="full", crop="false")
    body = bytearray()
    for key, value in fields.items():
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode())
    body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="image_file"; filename="candidate.png"\r\nContent-Type: image/png\r\n\r\n'.encode())
    body.extend(source)
    body.extend(f'\r\n--{boundary}--\r\n'.encode())
    req = urllib.request.Request(endpoint, bytes(body), {header: secret, "Content-Type": "multipart/form-data; boundary=" + boundary}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            output = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        # Do not expose remote response bodies or credentials in logs.
        print(json.dumps({"status": "FAILED", "provider": args.provider, "http_status": error.code}))
        return 1
    image = Image.open(io.BytesIO(output))
    original = Image.open(io.BytesIO(source))
    if image.size != original.size or image.mode != "RGBA" or image.getchannel("A").getextrema() != (0, 255):
        raise SystemExit("provider_output_contract_failed")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("xb") as stream:
        stream.write(output)
    evidence = {"status": "PASSED", "provider": args.provider, "http_status": status,
                "input_sha256": hashlib.sha256(source).hexdigest(), "output_sha256": hashlib.sha256(output).hexdigest(),
                "dimensions": list(image.size), "mode": image.mode, "alpha_range": [0, 255],
                "dimensions_preserved": True, "request_fields": fields,
                "role": "source_authoring_cutout_not_immutable_intake"}
    args.out.with_suffix(".provenance.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps(evidence))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
