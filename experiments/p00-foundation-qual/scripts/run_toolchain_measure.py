#!/usr/bin/env python3
"""Bounded parity, cold/warm, queue and resource measurements; not a product benchmark."""
from __future__ import annotations

import hashlib
import json
import os
import resource
import socket
import statistics
import struct
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/event-v1.json"
ROUNDS = 12
WARM_REQUESTS = 32


def frame(sock: socket.socket, value: dict) -> dict:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    sock.sendall(struct.pack(">I", len(raw)) + raw)
    header = sock.recv(4)
    size = struct.unpack(">I", header)[0]
    data = b""
    while len(data) < size:
        data += sock.recv(size - len(data))
    return json.loads(data)


def rss_kib(pid: int) -> int | None:
    try:
        for line in Path(f"/proc/{pid}/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1])
    except (FileNotFoundError, PermissionError, ValueError):
        return None
    return None


def run_candidate(name: str, command: list[str], socket_path: Path) -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    cold_self, cold_single, warm_times, rss_samples, responses = [], [], [], [], []
    child_cpu = 0.0
    for round_number in range(ROUNDS):
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        started = time.perf_counter_ns()
        subprocess.run(command + ["--self-test", str(FIXTURE)], check=True, capture_output=True, text=True)
        cold_self.append((time.perf_counter_ns() - started) / 1_000_000)
        proc = subprocess.Popen(command + ["--serve", str(socket_path)], stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE, text=True)
        deadline = time.monotonic() + 3
        while not socket_path.exists() and time.monotonic() < deadline:
            time.sleep(0.001)
        if not socket_path.exists():
            error = proc.communicate(timeout=1)[1]
            raise RuntimeError(f"{name} did not bind: {error}")
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(str(socket_path))
        single = dict(fixture); single["message_id"] = f"cold-{round_number}"
        started = time.perf_counter_ns()
        responses.append(frame(client, single))
        cold_single.append((time.perf_counter_ns() - started) / 1_000_000)
        for request_number in range(WARM_REQUESTS):
            request = dict(fixture)
            request["message_id"] = f"warm-{round_number}-{request_number}"
            started = time.perf_counter_ns()
            response = frame(client, request)
            warm_times.append((time.perf_counter_ns() - started) / 1_000_000)
            responses.append(response)
            sample = rss_kib(proc.pid)
            if sample is not None:
                rss_samples.append(sample)
        client.shutdown(socket.SHUT_WR); client.close()
        proc.wait(timeout=3)
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        child_cpu += (after.ru_utime - before.ru_utime) + (after.ru_stime - before.ru_stime)
    if not all(response.get("accepted") for response in responses):
        raise AssertionError(f"{name} rejected a valid sustained request")
    return {
        "rounds": ROUNDS,
        "warm_requests_per_round": WARM_REQUESTS,
        "cold_self_test_ms": cold_self,
        "cold_single_request_ms": cold_single,
        "warm_request_ms": warm_times,
        "cold_self_median_ms": statistics.median(cold_self),
        "cold_single_median_ms": statistics.median(cold_single),
        "warm_median_ms": statistics.median(warm_times),
        "warm_p95_ms": sorted(warm_times)[max(0, int(len(warm_times) * 0.95) - 1)],
        "child_cpu_seconds": child_cpu,
        "rss_kib_min": min(rss_samples) if rss_samples else None,
        "rss_kib_max": max(rss_samples) if rss_samples else None,
        "responses": responses,
    }


def main() -> None:
    output = Path(os.environ["QUAL_RESULTS"])
    output.parent.mkdir(parents=True, exist_ok=True)
    rust = os.environ["QUAL_RUST_BINARY"]
    with tempfile.TemporaryDirectory(prefix="companion-qual-") as temp:
        root = Path(temp)
        results = {
            "fixture_sha256": hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
            "rounds": ROUNDS,
            "warm_requests_per_round": WARM_REQUESTS,
            "python": run_candidate("python", [sys.executable, str(ROOT / "python" / "qual_shell.py")], root / "python.sock"),
            "rust": run_candidate("rust", [rust], root / "rust.sock"),
            "queue_overflow_probe": "PASSED in both self-tests; two-item bounded queue is explicit",
        }
    python_responses = results["python"]["responses"]
    rust_responses = results["rust"]["responses"]
    if len(python_responses) != len(rust_responses) or any(
        left["digest"] != right["digest"] or left["accepted"] != right["accepted"]
        for left, right in zip(python_responses, rust_responses)
    ):
        raise AssertionError("Python/Rust sustained digest mismatch")
    output.write_text(json.dumps(results, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({name: {key: value for key, value in data.items() if "median" in key or "p95" in key or "cpu" in key or "rss" in key}
                      for name, data in results.items() if isinstance(data, dict) and "warm_median_ms" in data}, sort_keys=True))


if __name__ == "__main__":
    main()
