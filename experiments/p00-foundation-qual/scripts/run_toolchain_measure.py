#!/usr/bin/env python3
"""Repeatable synthetic parity/startup samples; not a product benchmark."""
from __future__ import annotations
import json, os, socket, statistics, struct, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/event-v1.json"

def frame(sock, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    sock.sendall(struct.pack(">I", len(raw)) + raw)
    size = struct.unpack(">I", sock.recv(4))[0]
    data = b""
    while len(data) < size: data += sock.recv(size-len(data))
    return json.loads(data)

def run_candidate(name, command, socket_path, rounds=12):
    fixture_raw = FIXTURE.read_text()
    self_times=[]; startup=[]; responses=[]
    for _ in range(rounds):
        start=time.monotonic_ns()
        done=subprocess.run(command+["--self-test", str(FIXTURE)], check=True, capture_output=True, text=True)
        self_times.append((time.monotonic_ns()-start)/1_000_000)
        proc=subprocess.Popen(command+["--serve", str(socket_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        deadline=time.monotonic()+3
        while not socket_path.exists() and time.monotonic()<deadline: time.sleep(.002)
        if not socket_path.exists():
            stderr=proc.communicate(timeout=1)[1]; raise RuntimeError(f"{name} did not bind: {stderr}")
        start=time.monotonic_ns()
        client=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); client.connect(str(socket_path))
        response=frame(client, json.loads(fixture_raw)); client.close()
        proc.wait(timeout=3)
        startup.append((time.monotonic_ns()-start)/1_000_000); responses.append(response)
    return {"self_test_ms":self_times,"request_roundtrip_ms":startup,"self_test_median_ms":statistics.median(self_times),"request_median_ms":statistics.median(startup),"responses":responses}

def main():
    out=Path(os.environ["QUAL_RESULTS"]); out.parent.mkdir(parents=True, exist_ok=True)
    rust=os.environ["QUAL_RUST_BINARY"]
    with tempfile.TemporaryDirectory(prefix="companion-qual-") as td:
        base=Path(td)
        results={"fixture_sha256":__import__("hashlib").sha256(FIXTURE.read_bytes()).hexdigest(),"rounds":12,
          "python":run_candidate("python",[sys.executable,str(ROOT/"python/qual_shell.py")],base/"python.sock"),
          "rust":run_candidate("rust",[rust],base/"rust.sock")}
    assert all(r["accepted"] and r["digest"]==results["python"]["responses"][0]["digest"] for r in results["python"]["responses"]+results["rust"]["responses"])
    out.write_text(json.dumps(results,sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:{"self_test_median_ms":v["self_test_median_ms"],"request_median_ms":v["request_median_ms"]} for k,v in results.items() if isinstance(v,dict) and "self_test_median_ms" in v},sort_keys=True))
if __name__=="__main__": main()
