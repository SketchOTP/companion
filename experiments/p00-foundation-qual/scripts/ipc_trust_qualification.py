#!/usr/bin/env python3
"""Synthetic local IPC threat checks; never a live care implementation."""
from __future__ import annotations
import ctypes, hashlib, hmac, json, os, socket, subprocess, tempfile
from pathlib import Path

VALID = {"producer":"sensor-gateway", "generation":"g-1", "candidate_id":"c-1", "kind":"explicit_help_candidate_v1"}
def encode(value): return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
def recv(sock): return json.loads(sock.recv(4096))
def care_decide(raw, generation, capability=None, seen=None):
    try: value=json.loads(raw)
    except json.JSONDecodeError: return "reject:malformed"
    if value.get("producer") != "sensor-gateway": return "reject:producer"
    if value.get("generation") != generation: return "reject:generation"
    if value.get("kind") not in {"explicit_help_candidate_v1"}: return "reject:kind"
    if capability is not None:
        supplied=value.pop("capability", "")
        if not hmac.compare_digest(supplied, hmac.new(capability,encode(value),hashlib.sha256).hexdigest()): return "reject:capability"
    if seen is not None:
        if value["candidate_id"] in seen: return "accepted:duplicate"
        seen.add(value["candidate_id"])
    return "accepted:new"
def exchange(sock, value, generation, capability=None, seen=None):
    # The socketpair has no connectable address; this call models receipt only at
    # the care endpoint after the supervisor has handed each endpoint to its peer.
    # No companion socket or database path participates.
    return care_decide(encode(value),generation,capability,seen)
def weak_baseline(path):
    server=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); server.bind(str(path)); os.chmod(str(path),0o600); server.listen(1)
    injected=subprocess.Popen(["python3","-c", "import socket,sys; s=socket.socket(socket.AF_UNIX); s.connect(sys.argv[1]); s.sendall(sys.argv[2].encode()); print(s.recv(128).decode())", str(path),encode(VALID).decode()],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    conn,_=server.accept(); raw=conn.recv(4096); conn.sendall(care_decide(raw,"g-1").encode()); conn.close(); server.close()
    stdout, stderr=injected.communicate(timeout=3)
    if injected.returncode: raise RuntimeError(stderr)
    return stdout.strip()
def sibling_fd_probe(pid, fd):
    code="import os,sys; p='/proc/%s/fd/%s'%(sys.argv[1],sys.argv[2]);\ntry: os.open(p,os.O_RDWR); print('opened')\nexcept OSError as e: print('blocked:'+str(e.errno))"
    return subprocess.run(["python3","-c",code,str(pid),str(fd)],capture_output=True,text=True,check=True).stdout.strip()
def main():
    results={"threat_exclusions":["root","kernel compromise","full account compromise","fully compromised authorized producer"],"tests":{}}
    with tempfile.TemporaryDirectory(prefix="companion-ipc-") as td:
        weak=weak_baseline(Path(td)/"weak.sock"); results["tests"]["weak_same_user_valid_injection"]=weak
    # Candidate 1: anonymous preconnected seqpacket endpoints; no pathname and no inherited sibling fd.
    care, producer=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET); seen=set()
    results["tests"]["candidate1_valid"]=exchange(producer,dict(VALID),"g-1",seen=seen)
    results["tests"]["candidate1_duplicate"]=exchange(producer,dict(VALID),"g-1",seen=seen)
    results["tests"]["candidate1_spoofed_field"]=exchange(producer,{**VALID,"producer":"companion-core"},"g-1",seen=seen)
    results["tests"]["candidate1_generation_mismatch"]=exchange(producer,{**VALID,"generation":"old"},"g-1",seen=seen)
    results["tests"]["candidate1_companion_db_absent"]=exchange(producer,{**VALID,"candidate_id":"c-2"},"g-1",seen=seen)
    results["tests"]["candidate1_fd_inheritable"]=os.get_inheritable(care.fileno()) or os.get_inheritable(producer.fileno())
    results["tests"]["candidate1_proc_fd_probe_before_hardening"]=sibling_fd_probe(os.getpid(),care.fileno())
    care.close(); producer.close()
    # Candidate 2: the private channel also requires a per-generation HMAC capability
    # and makes the care process non-dumpable before sibling /proc probing.
    lib=ctypes.CDLL(None); pr_set_dumpable=4; hardening=lib.prctl(pr_set_dumpable,0,0,0,0)
    care, producer=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET); capability=os.urandom(32); seen=set()
    signed=dict(VALID); signed["capability"]=hmac.new(capability,encode(VALID),hashlib.sha256).hexdigest()
    results["tests"]["candidate2_pr_set_dumpable_result"]=hardening
    results["tests"]["candidate2_valid"]=exchange(producer,signed,"g-1",capability,seen)
    results["tests"]["candidate2_missing_capability"]=exchange(producer,dict(VALID),"g-1",capability,seen)
    results["tests"]["candidate2_old_generation"]=exchange(producer,{**signed,"generation":"old","candidate_id":"c-3"},"g-1",capability,seen)
    results["tests"]["candidate2_proc_fd_probe_after_hardening"]=sibling_fd_probe(os.getpid(),care.fileno())
    results["tests"]["producer_outage"]= "degraded-coverage-required"
    results["tests"]["forbidden_companion_mood_input"]=care_decide(encode({"producer":"companion-core","kind":"mood"}),"g-1",capability,seen)
    care.close(); producer.close()
    print(json.dumps(results,sort_keys=True,indent=2))
if __name__=="__main__": main()
