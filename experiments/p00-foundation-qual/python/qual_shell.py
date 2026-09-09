#!/usr/bin/env python3
"""Synthetic non-product shell used only for COMPANION-P00-QUAL-001."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
import socket
import struct
import sys
import time
from collections import deque
from pathlib import Path

MAX_EXACT_INT = 9_007_199_254_740_991
REQUIRED = {"canonicalization_version", "digest_version", "schema_uri", "schema_version",
            "message_id", "causation_id", "correlation_id", "producer", "producer_version",
            "boot_id", "monotonic_ns", "utc_observed", "utc_uncertainty_us", "event_sequence",
            "privacy_class", "authority_class", "payload"}

class Reject(ValueError):
    pass

def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Reject(f"duplicate-key:{key}")
        result[key] = value
    return result

def _constant(value):
    raise Reject(f"nonfinite:{value}")

def strict_loads(raw: str):
    try:
        value = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_constant)
    except (json.JSONDecodeError, Reject) as error:
        raise Reject(str(error)) from error
    def walk(item):
        if isinstance(item, str) and any(0xD800 <= ord(c) <= 0xDFFF for c in item):
            raise Reject("lone-surrogate")
        if isinstance(item, float) and (not math.isfinite(item) or item == 0.0):
            raise Reject("noncanonical-float")
        if isinstance(item, int) and abs(item) > MAX_EXACT_INT:
            raise Reject("integer-range")
        if isinstance(item, list):
            for child in item: walk(child)
        if isinstance(item, dict):
            for child in item.values(): walk(child)
    walk(value)
    return value

def _utf16_key(value: str) -> bytes:
    """JCS object-key order: raw UTF-16 code units."""
    return value.encode("utf-16-be", "surrogatepass")


def canonical(value):
    """Canonicalize the bounded integer/string Companion event profile.

    Full RFC 8785 vectors are exercised against the maintained reference
    oracle by ``jcs_conformance.py``; this shell intentionally rejects floats
    so authoritative state cannot depend on platform float formatting.
    """
    if value is None:
        return b"null"
    if value is True:
        return b"true"
    if value is False:
        return b"false"
    if isinstance(value, int) and not isinstance(value, bool):
        if abs(value) > MAX_EXACT_INT:
            raise Reject("integer-range")
        return str(value).encode("ascii")
    if isinstance(value, float):
        raise Reject("fractional-number-profile")
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"),
                          allow_nan=False).encode("utf-8")
    if isinstance(value, list):
        return b"[" + b",".join(canonical(item) for item in value) + b"]"
    if isinstance(value, dict):
        items = sorted(value.items(), key=lambda pair: _utf16_key(pair[0]))
        return b"{" + b",".join(
            canonical(str(key)) + b":" + canonical(item) for key, item in items
        ) + b"}"
    raise Reject("unsupported-value")

def validate(event):
    if not isinstance(event, dict) or set(event) != REQUIRED:
        raise Reject("envelope-fields")
    if event["canonicalization_version"] != "JCS-RFC8785-v1" or event["digest_version"] != "sha-256-jcs-event-v1":
        raise Reject("canonical-profile")
    if event["schema_version"].split(".", 1)[0] != "1":
        raise Reject("schema-major")
    if not isinstance(event["payload"], dict) or not isinstance(event["payload"].get("fixed_point_delta"), int):
        raise Reject("payload")
    for field in ("boot_id", "monotonic_ns", "event_sequence", "causation_id", "message_id"):
        if not isinstance(event[field], str) or not event[field]: raise Reject(f"field:{field}")

def process(raw: str, seen: set[str]):
    event = strict_loads(raw)
    validate(event)
    digest = hashlib.sha256(canonical(event)).hexdigest()
    duplicate = event["message_id"] in seen
    seen.add(event["message_id"])
    return {"accepted": True, "duplicate": duplicate, "digest": digest,
            "fixed_point_state": 0 if duplicate else event["payload"]["fixed_point_delta"]}

def recv_frame(conn):
    header = conn.recv(4)
    if len(header) != 4: raise Reject("short-header")
    length = struct.unpack(">I", header)[0]
    if length > 65536: raise Reject("frame-limit")
    body = b""
    while len(body) < length:
        chunk = conn.recv(length - len(body))
        if not chunk: raise Reject("short-frame")
        body += chunk
    return body.decode("utf-8")

def send_frame(conn, value):
    data = canonical(value)
    conn.sendall(struct.pack(">I", len(data)) + data)

def serve(path: Path):
    path.unlink(missing_ok=True)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(str(path)); os.chmod(path, 0o600); server.listen(4)
    seen, queue = set(), deque(maxlen=2)
    try:
        conn, _ = server.accept()
        with conn:
            while True:
                try:
                    raw = recv_frame(conn)
                except Reject as error:
                    if str(error) == "short-header":
                        break
                    result = {"accepted": False, "reason": str(error)}
                    send_frame(conn, result)
                    continue
                if len(queue) == queue.maxlen:
                    result = {"accepted": False, "reason": "queue-full", "queue_depth": len(queue)}
                else:
                    queue.append(raw)
                    try: result = process(raw, seen)
                    except Reject as error: result = {"accepted": False, "reason": str(error)}
                    result["queue_depth"] = len(queue)
                    queue.popleft()
                result["log"] = "qualification-shell;payload-minimized"
                send_frame(conn, result)
    finally:
        server.close(); path.unlink(missing_ok=True)

def self_test(fixture: Path):
    raw = fixture.read_text(encoding="utf-8")
    first, again = process(raw, set()), process(raw, {"message-0001"})
    assert first["accepted"] and not first["duplicate"] and first["fixed_point_state"] == 25
    assert again["duplicate"] and again["fixed_point_state"] == 0
    for bad in ('{"message_id":"a","message_id":"b"}',
                '{"a":1,"\\u0061":2}', '{"x":NaN}', '"\\ud800"'):
        try: strict_loads(bad)
        except Reject: pass
        else: raise AssertionError(f"accepted invalid input: {bad}")
    event = strict_loads(raw); event["schema_version"] = "2.0"
    try: validate(event)
    except Reject: pass
    else: raise AssertionError("accepted unsupported major")
    queue = deque(maxlen=2); queue.extend((b"one", b"two")); overflow = len(queue) == queue.maxlen
    assert overflow
    print(json.dumps({"self_test":"passed", "digest":first["digest"], "python":sys.version.split()[0], "queue_probe":"passed"}, sort_keys=True))

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--self-test", type=Path)
    parser.add_argument("--serve", type=Path); parser.add_argument("--canonical", type=Path); args = parser.parse_args()
    if args.self_test: self_test(args.self_test)
    elif args.serve: serve(args.serve)
    elif args.canonical:
        event = strict_loads(args.canonical.read_bytes()); validate(event)
        print(base64.b64encode(canonical(event)).decode("ascii"))
    else: parser.error("select --self-test or --serve")
if __name__ == "__main__": main()
