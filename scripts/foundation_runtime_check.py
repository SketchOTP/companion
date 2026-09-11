#!/usr/bin/env python3
"""Fail-closed resident lifecycle and no-egress smoke check."""
import argparse, json, os, pathlib, signal, socket, subprocess, tempfile, time

def process_network_snapshot(pids):
    """Return observed AF_INET/AF_INET6 sockets owned by these PIDs."""
    try:
        result = subprocess.run(["ss", "-H", "-tunp"], capture_output=True, text=True, check=False)
    except OSError as exc:
        return {"count": None, "error": type(exc).__name__}
    if result.returncode != 0:
        return {"count": None, "error": f"ss_exit_{result.returncode}"}
    owned = 0
    for line in result.stdout.splitlines():
        owners = {int(value) for value in __import__("re").findall(r"pid=(\d+)", line)}
        if owners & set(pids):
            owned += 1
    return {"count": owned, "error": None}

def query(path):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(str(path))
    s.sendall(b'{"command":"health"}\n')
    s.shutdown(socket.SHUT_WR)
    response = json.loads(s.recv(65536))
    s.close()
    return json.loads(response["health"]) if "health" in response else response

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=pathlib.Path, required=True)
    args = ap.parse_args()
    binary = os.environ.get("FOUNDATION_SUPERVISOR", "target/release/ops-supervisor")
    with tempfile.TemporaryDirectory(prefix="companion-runtime-") as root:
        env = os.environ.copy()
        env["COMPANION_XDG_ROOT"] = root
        proc = subprocess.Popen([binary], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        control = pathlib.Path(root) / "companion" / "supervisor.sock"
        deadline = time.time() + 5
        while time.time() < deadline and not control.exists():
            time.sleep(.05)
        health, error = {}, None
        try:
            if not control.exists():
                raise FileNotFoundError("supervisor control socket did not become ready")
            health = query(control)
        except Exception as exc:
            error = type(exc).__name__
        rows = health.get("children", [])
        expected = {"companion-core", "identity-consent-vault", "godot-bridge", "sensor-gateway", "care-core"}
        roles = {x.get("role") for x in rows}
        resident = proc.poll() is None and expected.issubset(roles)
        observed_ready = all(x.get("ready") is True and x.get("state") == "healthy" for x in rows if x.get("role") in expected)
        network_observation = process_network_snapshot([proc.pid, *[int(x.get("pid")) for x in rows if x.get("pid")]])
        network = network_observation.get("count")
        inspection_errors = []
        # A dumpable=0 child intentionally denies same-user /proc/<pid>/fd
        # traversal. Retain that denial as a limitation while using the
        # process-attributed ss census below for AF_INET/AF_INET6 observation.
        proc_net = {}
        for name in ("tcp", "tcp6", "udp", "udp6"):
            path = pathlib.Path(f"/proc/net/{name}")
            try:
                lines = path.read_text(errors="replace").splitlines()
                proc_net[name] = max(0, len(lines) - 1)
            except OSError as exc:
                inspection_errors.append({"source": str(path), "error": type(exc).__name__})
        for child in rows:
            try:
                fd_dir = pathlib.Path(f"/proc/{int(child['pid'])}/fd")
                # Probe only to classify the hardening boundary.  Do not
                # treat permission denial as a missing capability.
                list(fd_dir.iterdir())
            except (OSError, KeyError, ValueError) as exc:
                inspection_errors.append({"source": f"/proc/{child.get('pid')}/fd", "error": type(exc).__name__})
        if proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=10)
        result = {
            "status": "PASS" if resident and observed_ready and health.get("care_coverage") == "synthetic" and network == 0 and network_observation.get("error") is None and proc.returncode == 0 else "FAIL",
            "resident": resident,
            "roles": sorted(roles),
            "observed_ready": observed_ready,
            "care_coverage": health.get("care_coverage"),
            "health_error": error,
            "network_socket_count": network,
            "network_observation": network_observation,
            "proc_net_socket_counts": proc_net,
            "proc_fd_inspection": "blocked_by_child_dumpable_hardening" if inspection_errors else "observed",
            "proc_inspection_errors": inspection_errors,
            "shutdown_returncode": proc.returncode,
            "claim_boundary": "engineering lifecycle observation only",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
