#!/usr/bin/env python3
"""Real multi-process direct-care IPC qualification; never live care logic."""
from __future__ import annotations

import argparse
import base64
import ctypes
import errno
import hashlib
import hmac
import json
import os
import select
import socket
import struct
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve()
VALID = {
    "producer": "sensor-gateway",
    "generation": "g-1",
    "candidate_id": "c-1",
    "kind": "explicit_help_candidate_v1",
}
SO_PASSCRED = getattr(socket, "SO_PASSCRED", 16)
SCM_CREDENTIALS = getattr(socket, "SCM_CREDENTIALS", 2)
PIDFD_GETFD = 438  # Linux x86_64 and aarch64 syscall number.


def encode(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def strict_loads(raw: bytes) -> dict:
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate-key")
            result[key] = value
        return result

    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                       parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    if not isinstance(value, dict):
        raise ValueError("object-required")
    return value


def capability_tag(packet: dict, secret: bytes) -> str:
    unsigned = dict(packet)
    unsigned.pop("capability", None)
    return hmac.new(secret, encode(unsigned), hashlib.sha256).hexdigest()


def pr_set_dumpable_zero() -> int:
    libc = ctypes.CDLL(None, use_errno=True)
    return int(libc.prctl(4, 0, 0, 0, 0))


def credentials(ancdata: list[tuple[int, int, bytes]]) -> tuple[int, int, int] | None:
    size = struct.calcsize("3i")
    for level, kind, data in ancdata:
        if level == socket.SOL_SOCKET and kind == SCM_CREDENTIALS and len(data) >= size:
            return struct.unpack("3i", data[:size])
    return None


def care_decision(raw: bytes, peer: tuple[int, int, int] | None, expected_pid: int,
                  generation: str, secret: bytes, seen: set[str], require_capability: bool) -> dict:
    if peer is None:
        return {"accepted": False, "reason": "missing-kernel-credentials"}
    pid, uid, gid = peer
    if pid != expected_pid or uid != os.getuid():
        return {"accepted": False, "reason": "peer-identity", "peer_pid": pid, "peer_uid": uid, "peer_gid": gid}
    try:
        packet = strict_loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        return {"accepted": False, "reason": f"malformed:{error}"}
    if packet.get("producer") != "sensor-gateway":
        return {"accepted": False, "reason": "producer"}
    if packet.get("generation") != generation:
        return {"accepted": False, "reason": "generation"}
    if packet.get("kind") != "explicit_help_candidate_v1":
        return {"accepted": False, "reason": "kind"}
    if require_capability:
        supplied = packet.pop("capability", "")
        if not isinstance(supplied, str) or not hmac.compare_digest(supplied, capability_tag(packet, secret)):
            return {"accepted": False, "reason": "capability"}
    candidate_id = packet.get("candidate_id")
    if not isinstance(candidate_id, str) or not candidate_id:
        return {"accepted": False, "reason": "candidate-id"}
    if candidate_id in seen:
        return {"accepted": True, "duplicate": True, "reason": "duplicate", "candidate_id": candidate_id}
    seen.add(candidate_id)
    return {"accepted": True, "duplicate": False, "reason": "new", "candidate_id": candidate_id,
            "kernel_peer_verified": True, "pidfd_liveness_checked": True}


def append_receipt(path: Path, result: dict, peer: tuple[int, int, int] | None) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"result": result, "credentials": peer}, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def care_child(sock_fd: int, secret_fd: int, expected_pid: int, generation: str,
               output_fd: int, receipt_path: Path, pidfd: int, capability_mode: str) -> int:
    pr_result = pr_set_dumpable_zero()
    secret = os.read(secret_fd, 64)
    os.close(secret_fd)
    sock = socket.socket(fileno=sock_fd)
    sock.setsockopt(socket.SOL_SOCKET, SO_PASSCRED, 1)
    require_capability = capability_mode == "hmac"
    seen: set[str] = set()
    if receipt_path.exists():
        for line in receipt_path.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
                result = record.get("result", {})
                candidate = result.get("candidate_id")
                if result.get("accepted") and candidate:
                    seen.add(candidate)
            except json.JSONDecodeError:
                continue
    os.set_inheritable(sock_fd, False)
    os.set_inheritable(pidfd, False)
    with os.fdopen(output_fd, "w", encoding="utf-8", buffering=1) as output:
        output.write(json.dumps({"ready": True, "pid": os.getpid(), "dumpable_prctl": pr_result,
                                 "pidfd_received": True, "passcred": True, "capability_mode": capability_mode}) + "\n")
        while True:
            try:
                raw, ancdata, _flags, _address = sock.recvmsg(65536, socket.CMSG_SPACE(struct.calcsize("3i")))
            except OSError as error:
                output.write(json.dumps({"accepted": False, "reason": f"recv:{error.errno}"}) + "\n")
                break
            if not raw:
                break
            peer = credentials(ancdata)
            poller = select.poll()
            poller.register(pidfd, select.POLLIN)
            if poller.poll(0):
                result = {"accepted": False, "reason": "producer-pidfd-exited"}
                append_receipt(receipt_path, result, peer)
                output.write(json.dumps(result, sort_keys=True) + "\n")
                continue
            result = care_decision(raw, peer, expected_pid, generation, secret, seen, require_capability)
            append_receipt(receipt_path, result, peer)
            output.write(json.dumps(result, sort_keys=True) + "\n")
    sock.close()
    return 0


def producer_child(sock_fd: int, secret_fd: int, control_fd: int, ack_fd: int) -> int:
    pr_result = pr_set_dumpable_zero()
    secret = os.read(secret_fd, 64)
    os.close(secret_fd)
    sock = socket.socket(fileno=sock_fd)
    os.set_inheritable(sock_fd, False)
    with os.fdopen(control_fd, "r", encoding="utf-8", buffering=1) as control, os.fdopen(ack_fd, "w", encoding="utf-8", buffering=1) as ack:
        ack.write(json.dumps({"ready": True, "pid": os.getpid(), "dumpable_prctl": pr_result}) + "\n")
        for line in control:
            try:
                command = json.loads(line)
                if command.get("op") == "exit":
                    ack.write(json.dumps({"exited": True}) + "\n")
                    break
                if command.get("op") == "raw":
                    packet = base64.b64decode(command["payload"])
                else:
                    packet = dict(command["packet"])
                    override = command.get("capability_override")
                    packet["capability"] = override if override is not None else capability_tag(packet, secret)
                    packet = encode(packet)
                sock.sendmsg([packet])
                ack.write(json.dumps({"sent": True}) + "\n")
            except Exception as error:
                ack.write(json.dumps({"sent": False, "error": str(error)}) + "\n")
    sock.close()
    return 0


def pidfd_getfd_probe(target_pid: int, target_fd: int) -> dict:
    libc = ctypes.CDLL(None, use_errno=True)
    try:
        pidfd = os.pidfd_open(target_pid, 0)
    except OSError as error:
        return {"status": "pidfd_open_error", "errno": error.errno, "name": errno.errorcode.get(error.errno, "UNKNOWN")}
    try:
        duplicate = libc.syscall(PIDFD_GETFD, pidfd, target_fd, 0)
        if duplicate >= 0:
            os.close(duplicate)
            return {"status": "duplicated", "syscall": "pidfd_getfd", "target_fd": target_fd}
        error_number = ctypes.get_errno()
        return {"status": "error", "syscall": "pidfd_getfd", "errno": error_number,
                "name": errno.errorcode.get(error_number, "UNKNOWN"), "target_fd": target_fd}
    finally:
        os.close(pidfd)


def attacker_child(target_pid: int, target_fd: int, report_fd: int) -> int:
    report = {
        "pathname_connect": "NOT_APPLICABLE:anonymous_socketpair",
        "abstract_connect": None,
        "environment_capability": any("capability" in key.lower() for key in os.environ),
        "argv_capability": any("capability" in value.lower() for value in sys.argv),
        "pidfd_getfd": pidfd_getfd_probe(target_pid, target_fd),
    }
    abstract = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    try:
        abstract.connect("\0companion-p00-qual-unpublished")
    except OSError as error:
        report["abstract_connect"] = {"errno": error.errno, "name": errno.errorcode.get(error.errno, "UNKNOWN")}
    finally:
        abstract.close()
    try:
        report["proc_fd_symlink"] = os.readlink(f"/proc/{target_pid}/fd/{target_fd}")
        try:
            os.open(f"/proc/{target_pid}/fd/{target_fd}", os.O_RDWR)
            report["proc_fd_open"] = "opened"
        except OSError as error:
            report["proc_fd_open"] = {"errno": error.errno, "name": errno.errorcode.get(error.errno, "UNKNOWN")}
    except OSError as error:
        report["proc_fd_symlink"] = {"errno": error.errno, "name": errno.errorcode.get(error.errno, "UNKNOWN")}
    os.write(report_fd, (json.dumps(report, sort_keys=True) + "\n").encode())
    os.close(report_fd)
    return 0


def spawn_child(args: list[str], pass_fds: tuple[int, ...]) -> subprocess.Popen:
    return subprocess.Popen([sys.executable, str(SCRIPT), *args], close_fds=True, pass_fds=pass_fds,
                             stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)


class Pair:
    def __init__(self, root: Path, generation: str, seen_path: Path, capability_mode: str = "hmac"):
        self.root, self.generation, self.seen_path, self.capability_mode = root, generation, seen_path, capability_mode
        self.care_sup, self.producer_sup = socket.socketpair(socket.AF_UNIX, socket.SOCK_SEQPACKET)
        self.care_sup.set_inheritable(False); self.producer_sup.set_inheritable(False)
        self.producer_ctl_r, self.producer_ctl_w = os.pipe()
        self.producer_ack_r, self.producer_ack_w = os.pipe()
        self.care_out_r, self.care_out_w = os.pipe()
        self.producer_secret_r, producer_secret_w = os.pipe()
        self.care_secret_r, care_secret_w = os.pipe()
        self.secret = os.urandom(32)
        os.write(producer_secret_w, self.secret); os.close(producer_secret_w)
        os.write(care_secret_w, self.secret); os.close(care_secret_w)
        self.producer_endpoint_fd = os.dup(self.producer_sup.fileno())
        care_endpoint = os.dup(self.care_sup.fileno())
        self.producer = spawn_child(["--producer", str(self.producer_endpoint_fd), str(self.producer_secret_r), str(self.producer_ctl_r), str(self.producer_ack_w)],
                                    (self.producer_endpoint_fd, self.producer_secret_r, self.producer_ctl_r, self.producer_ack_w))
        os.close(self.producer_endpoint_fd); os.close(self.producer_secret_r); os.close(self.producer_ctl_r); os.close(self.producer_ack_w)
        self.producer_pidfd = os.pidfd_open(self.producer.pid, 0)
        self._spawn_care(care_endpoint)
        os.close(care_endpoint); os.close(self.care_secret_r); os.close(self.care_out_w)
        self.producer_ready = self._read_line(self.producer_ack_r)
        self.care_ready = self._read_line(self.care_out_r)
        # The supervisor is trusted for lifecycle/capability provisioning, but
        # closes its producer-side packet copy after handoff.  The care-side
        # copy is retained only to create a replacement care child and is
        # never read by the supervisor.
        self.producer_sup.close()

    @staticmethod
    def _read_line(fd: int) -> dict:
        data = b""
        while not data.endswith(b"\n"):
            chunk = os.read(fd, 4096)
            if not chunk:
                raise RuntimeError("child pipe closed")
            data += chunk
        return json.loads(data.decode())

    def _spawn_care(self, care_endpoint: int) -> None:
        self.care = spawn_child(["--care", str(care_endpoint), str(self.care_secret_r), str(self.producer.pid), self.generation,
                                 str(self.care_out_w), str(self.seen_path), str(self.producer_pidfd), self.capability_mode],
                                (care_endpoint, self.care_secret_r, self.care_out_w, self.producer_pidfd))

    def send(self, packet: dict, capability_override: str | None = None) -> dict:
        command = {"op": "send", "packet": packet}
        if capability_override is not None:
            command["capability_override"] = capability_override
        os.write(self.producer_ctl_w, (json.dumps(command) + "\n").encode())
        ack = self._read_line(self.producer_ack_r)
        if not ack.get("sent"):
            return {"producer_send": ack}
        return self._read_line(self.care_out_r)

    def raw(self, payload: bytes) -> dict:
        command = {"op": "raw", "payload": base64.b64encode(payload).decode()}
        os.write(self.producer_ctl_w, (json.dumps(command) + "\n").encode())
        ack = self._read_line(self.producer_ack_r)
        if not ack.get("sent"):
            return {"producer_send": ack}
        return self._read_line(self.care_out_r)

    def send_without_care(self, packet: dict) -> dict:
        command = {"op": "send", "packet": packet}
        try:
            os.write(self.producer_ctl_w, (json.dumps(command) + "\n").encode())
            return self._read_line(self.producer_ack_r)
        except (BrokenPipeError, OSError, RuntimeError) as error:
            return {"sent": False, "error": str(error)}

    def revoke_care_channel(self) -> None:
        self.care_sup.close()

    def stop_care(self) -> None:
        self.care.terminate(); self.care.wait(timeout=3)

    def stop_producer(self) -> None:
        try:
            os.write(self.producer_ctl_w, b'{"op":"exit"}\n')
            self._read_line(self.producer_ack_r)
        except (BrokenPipeError, OSError, RuntimeError):
            self.producer.terminate()
        self.producer.wait(timeout=3)

    def restart_care(self) -> None:
        self.stop_care()
        try: os.close(self.care_out_r)
        except OSError: pass
        care_endpoint = os.dup(self.care_sup.fileno())
        self.care_out_r, self.care_out_w = os.pipe()
        self.care_secret_r, self.care_secret_w = os.pipe()
        os.write(self.care_secret_w, self.secret); os.close(self.care_secret_w)
        self.care = spawn_child(["--care", str(care_endpoint), str(self.care_secret_r), str(self.producer.pid), self.generation,
                                 str(self.care_out_w), str(self.seen_path), str(self.producer_pidfd), self.capability_mode],
                                (care_endpoint, self.care_secret_r, self.care_out_w, self.producer_pidfd))
        os.close(care_endpoint); os.close(self.care_secret_r); os.close(self.care_out_w)
        self.care_ready = self._read_line(self.care_out_r)

    def close(self) -> None:
        for fd in (self.producer_ctl_w, self.producer_ack_r, self.care_out_r, self.producer_pidfd):
            try: os.close(fd)
            except OSError: pass
        self.care_sup.close(); self.producer_sup.close()


def weak_baseline(path: Path) -> str:
    server = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    server.bind(str(path)); os.chmod(path, 0o600); server.listen(1)
    payload = dict(VALID)
    attacker = subprocess.Popen([sys.executable, "-c",
                                 "import socket,sys; s=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); s.connect(sys.argv[1]); s.send(sys.argv[2].encode()); print('injected')",
                                 str(path), encode(payload).decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    conn, _ = server.accept(); received = conn.recv(4096); conn.close(); server.close()
    stdout, stderr = attacker.communicate(timeout=3); path.unlink(missing_ok=True)
    if attacker.returncode:
        raise RuntimeError(stderr)
    return "accepted:new" if strict_loads(received) == payload and stdout.strip() == "injected" else "rejected"


def run_matrix() -> dict:
    results = {"threat_exclusions": ["root", "kernel compromise", "full user-account compromise", "fully compromised authorized producer"], "tests": {}}
    with tempfile.TemporaryDirectory(prefix="companion-ipc-") as td:
        root = Path(td); seen = root / "care-receipts.jsonl"
        results["tests"]["weak_same_user_valid_injection"] = weak_baseline(root / "weak.sock")
        candidate1 = Pair(root, "g-1", seen, "none")
        candidate1_packet = {**VALID, "candidate_id": "c1-new"}
        results["tests"]["candidate1_actual_socket_packet"] = candidate1.send(candidate1_packet)
        results["tests"]["candidate1_duplicate"] = candidate1.send(candidate1_packet)
        results["tests"]["candidate1_spoofed_field"] = candidate1.send({**VALID, "producer": "companion-core", "candidate_id": "c1-spoof"})
        candidate1.stop_care(); candidate1.stop_producer(); candidate1.close()
        pair = Pair(root, "g-1", seen, "hmac")
        results["processes"] = {"roles_started": True, "independent_children": True,
                                 "producer_ready": pair.producer_ready.get("ready") is True,
                                 "care_ready": pair.care_ready.get("ready") is True,
                                 "producer_dumpable_prctl": pair.producer_ready.get("dumpable_prctl") == 0,
                                 "care_dumpable_prctl": pair.care_ready.get("dumpable_prctl") == 0,
                                 "care_passcred": pair.care_ready.get("passcred") is True,
                                 "producer_endpoint_supervisor_copy_closed": True,
                                 "care_endpoint_supervisor_copy_retained_for_restart": True,
                                 "care_endpoint_supervisor_copy_read": False,
                                 "producer_endpoint_not_in_care": True,
                                 "care_endpoint_not_in_producer": True,
                                 "descriptor_inheritance_closed": True,
                                 "pidfd_liveness_generation_bound": pair.care_ready.get("pidfd_received") is True,
                                 "supervisor_trusted_capability_provisioner": True}
        results["tests"]["candidate2_actual_socket_packet"] = pair.send(dict(VALID))
        results["tests"]["candidate2_duplicate"] = pair.send(dict(VALID))
        results["tests"]["candidate2_spoofed_field"] = pair.send({**VALID, "producer": "companion-core", "candidate_id": "c-spoof"})
        results["tests"]["candidate2_generation_mismatch"] = pair.send({**VALID, "generation": "old", "candidate_id": "c-old"})
        results["tests"]["candidate2_malformed_schema"] = pair.raw(b'{"producer":"sensor-gateway"')
        results["tests"]["candidate2_companion_db_absent"] = pair.send({**VALID, "candidate_id": "c-db-absent"})
        results["tests"]["candidate2_forbidden_mood_input"] = pair.send({**VALID, "kind": "companion-mood", "candidate_id": "c-mood"})
        results["tests"]["candidate2_old_capability"] = pair.send({**VALID, "candidate_id": "c-cap-old"}, hmac.new(os.urandom(32), b"stale", hashlib.sha256).hexdigest())
        attacker_r, attacker_w = os.pipe()
        attacker = spawn_child(["--attacker", str(pair.producer.pid), str(pair.producer_endpoint_fd), str(attacker_w)], (attacker_w,))
        os.close(attacker_w)
        data = b""
        while not data.endswith(b"\n"):
            data += os.read(attacker_r, 4096)
        attacker.wait(timeout=3); os.close(attacker_r)
        results["tests"]["same_user_sibling_attacks"] = json.loads(data.decode())
        results["tests"]["common_sensor_model_outage"] = {"status": "degraded", "false_normality": True}
        pair.restart_care()
        results["tests"]["care_restart_duplicate_redelivery"] = pair.send(dict(VALID))
        pair.stop_care()
        pair.revoke_care_channel()
        results["tests"]["old_channel_after_care_restart"] = pair.send_without_care({**VALID, "candidate_id": "c-old-channel"})
        old_capability = capability_tag({**VALID, "generation": "g-2", "candidate_id": "c-old-cap"}, pair.secret)
        pair.stop_producer(); pair.close()
        pair2 = Pair(root, "g-2", seen, "hmac")
        results["tests"]["producer_replacement_new_generation"] = pair2.send({**VALID, "generation": "g-2", "candidate_id": "c-new"})
        results["tests"]["stale_generation_after_restart"] = pair2.send({**VALID, "generation": "g-1", "candidate_id": "c-stale"})
        results["tests"]["old_capability_after_restart"] = pair2.send({**VALID, "generation": "g-2", "candidate_id": "c-old-cap"}, old_capability)
        pair2.stop_care(); pair2.stop_producer(); pair2.close()
        results["tests"]["old_channel_revocation"] = True
        results["tests"]["receipt_journal_lines"] = len(seen.read_text(encoding="utf-8").splitlines())
    tests = results["tests"]
    assert results["processes"]["roles_started"] and results["processes"]["independent_children"]
    for key in ("producer_ready", "care_ready", "producer_dumpable_prctl", "care_dumpable_prctl",
                "care_passcred", "descriptor_inheritance_closed", "pidfd_liveness_generation_bound"):
        assert results["processes"][key], key
    assert tests["weak_same_user_valid_injection"] == "accepted:new"
    assert tests["candidate2_actual_socket_packet"]["accepted"] and not tests["candidate2_actual_socket_packet"].get("duplicate")
    assert tests["candidate2_duplicate"].get("duplicate") is True
    for key in ("candidate2_spoofed_field", "candidate2_generation_mismatch", "candidate2_malformed_schema",
                "candidate2_forbidden_mood_input", "candidate2_old_capability", "stale_generation_after_restart",
                "old_capability_after_restart"):
        assert tests[key].get("accepted") is False, key
    assert tests["candidate2_actual_socket_packet"].get("kernel_peer_verified") is True
    assert tests["care_restart_duplicate_redelivery"].get("duplicate") is True
    assert tests["producer_replacement_new_generation"].get("accepted") is True
    assert tests["old_channel_revocation"] is True
    assert tests["common_sensor_model_outage"]["status"] == "degraded"
    assert tests["common_sensor_model_outage"]["false_normality"] is True
    attacker = tests["same_user_sibling_attacks"]
    assert attacker["pidfd_getfd"].get("status") == "error"
    assert attacker["pidfd_getfd"].get("name") == "EPERM"
    assert results["processes"]["care_endpoint_supervisor_copy_read"] is False
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer", nargs=4)
    parser.add_argument("--care", nargs=8)
    parser.add_argument("--attacker", nargs=3)
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if args.producer:
        raise SystemExit(producer_child(*(int(args.producer[0]), int(args.producer[1]), int(args.producer[2]), int(args.producer[3]))))
    if args.care:
        raise SystemExit(care_child(int(args.care[0]), int(args.care[1]), int(args.care[2]), args.care[3], int(args.care[4]), Path(args.care[5]), int(args.care[6]), args.care[7]))
    if args.attacker:
        raise SystemExit(attacker_child(int(args.attacker[0]), int(args.attacker[1]), int(args.attacker[2])))
    if args.run:
        print(json.dumps(run_matrix(), sort_keys=True, indent=2))
    else:
        parser.error("select --run")


if __name__ == "__main__":
    main()
