#!/usr/bin/env python3
"""Fail-closed resident lifecycle and no-egress smoke check."""
import argparse, json, os, pathlib, re, signal, socket, subprocess, tempfile, time

EXPECTED_ROLES = {
    "companion-core",
    "identity-consent-vault",
    "godot-bridge",
    "sensor-gateway",
    "care-core",
}
READINESS_TIMEOUT_MS = 5000
READINESS_POLL_INTERVAL_MS = 50
STABLE_READY_SAMPLES = 2

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


def _role_rows(health):
    rows = health.get("children", []) if isinstance(health, dict) else []
    return {row.get("role"): row for row in rows if isinstance(row, dict) and row.get("role")}


def _readiness_projection(health, supervisor_alive):
    by_role = _role_rows(health)
    roles_seen = sorted(by_role)
    ready_roles = sorted(
        role for role in EXPECTED_ROLES
        if by_role.get(role, {}).get("ready") is True
    )
    not_ready_roles = sorted(EXPECTED_ROLES - set(ready_roles))
    unhealthy_roles = sorted(
        role for role in EXPECTED_ROLES
        if role in by_role and by_role[role].get("state") != "healthy"
    )
    all_roles = EXPECTED_ROLES.issubset(set(roles_seen))
    all_ready = all_roles and len(ready_roles) == len(EXPECTED_ROLES)
    complete = (
        supervisor_alive
        and all_ready
        and not unhealthy_roles
        and health.get("care_coverage") == "synthetic"
    )
    return {
        "supervisor_alive": bool(supervisor_alive),
        "roles_seen": roles_seen,
        "ready_roles": ready_roles,
        "not_ready_roles": not_ready_roles,
        "unhealthy_roles": unhealthy_roles,
        "care_coverage": health.get("care_coverage") if isinstance(health, dict) else None,
        "all_roles": all_roles,
        "all_ready": all_ready,
        "complete_ready": complete,
    }


def wait_for_stable_readiness(
    control,
    *,
    process_alive,
    query_fn=query,
    socket_exists_fn=lambda path: path.exists(),
    monotonic_fn=time.monotonic,
    sleep_fn=time.sleep,
    timeout_ms=READINESS_TIMEOUT_MS,
    poll_interval_ms=READINESS_POLL_INTERVAL_MS,
):
    """Wait for two complete health samples, never equating socket existence with readiness."""
    if timeout_ms <= 0 or poll_interval_ms <= 0:
        raise ValueError("readiness timeout and poll interval must be positive")
    started = monotonic_fn()
    trace = []
    last_health = {}
    socket_observed_ms = None
    all_roles_observed_ms = None
    all_ready_observed_ms = None
    stable_ready_observed_ms = None
    consecutive_ready = 0
    reason = "readiness_timeout"
    status = "FAIL"

    while True:
        elapsed_ms = round((monotonic_fn() - started) * 1000, 3)
        if elapsed_ms >= timeout_ms:
            reason = "readiness_timeout"
            break
        alive = bool(process_alive())
        if not alive:
            projection = _readiness_projection(last_health, False)
            trace.append({
                "sample_index": len(trace),
                "elapsed_ms": elapsed_ms,
                **{key: projection[key] for key in (
                    "supervisor_alive", "roles_seen", "ready_roles", "not_ready_roles",
                    "unhealthy_roles", "care_coverage",
                )},
                "query_error_class": "supervisor_exited",
            })
            reason = "supervisor_exited_before_stable_readiness"
            break

        socket_observed = bool(socket_exists_fn(control))
        query_error_class = None
        health = last_health
        if socket_observed:
            if socket_observed_ms is None:
                socket_observed_ms = elapsed_ms
            try:
                health = query_fn(control)
                last_health = health if isinstance(health, dict) else {}
            except Exception as exc:  # sanitized class only; no endpoint/payload text
                query_error_class = type(exc).__name__
                health = last_health
        else:
            query_error_class = "socket_unavailable"

        projection = _readiness_projection(health, True)
        if projection["all_roles"] and all_roles_observed_ms is None:
            all_roles_observed_ms = elapsed_ms
        if projection["all_ready"] and not projection["unhealthy_roles"] and all_ready_observed_ms is None:
            all_ready_observed_ms = elapsed_ms
        trace.append({
            "sample_index": len(trace),
            "elapsed_ms": elapsed_ms,
            **{key: projection[key] for key in (
                "supervisor_alive", "roles_seen", "ready_roles", "not_ready_roles",
                "unhealthy_roles", "care_coverage", "complete_ready",
            )},
            "query_error_class": query_error_class,
        })

        if projection["complete_ready"]:
            consecutive_ready += 1
            if consecutive_ready >= STABLE_READY_SAMPLES:
                stable_ready_observed_ms = elapsed_ms
                status = "PASS"
                reason = "stable_complete_readiness"
                break
        else:
            consecutive_ready = 0

        remaining_ms = timeout_ms - round((monotonic_fn() - started) * 1000, 3)
        if remaining_ms <= 0:
            reason = "readiness_timeout"
            break
        sleep_fn(min(poll_interval_ms, remaining_ms) / 1000.0)

    return {
        "status": status,
        "reason": reason,
        "startup_trace": trace,
        "socket_observed_ms": socket_observed_ms,
        "all_roles_observed_ms": all_roles_observed_ms,
        "all_ready_observed_ms": all_ready_observed_ms,
        "stable_ready_observed_ms": stable_ready_observed_ms,
        "sample_count": len(trace),
        "poll_interval_ms": poll_interval_ms,
        "timeout_ms": timeout_ms,
        "final_health": last_health,
    }


def _sanitized_tail(text, limit=20):
    """Keep only a bounded, path-redacted stderr tail for diagnostics."""
    lines = text.splitlines()[-limit:]
    return [re.sub(r"/(?:[^\s:]+)", "<path>", line.strip()) for line in lines]

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
        readiness = wait_for_stable_readiness(
            control,
            process_alive=lambda: proc.poll() is None,
        )
        health = readiness.get("final_health", {})
        rows = health.get("children", []) if isinstance(health, dict) else []
        roles = {x.get("role") for x in rows if isinstance(x, dict) and x.get("role")}
        resident = proc.poll() is None and EXPECTED_ROLES.issubset(roles)
        observed_ready = readiness["status"] == "PASS"
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
        try:
            stdout_text, stderr_text = proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout_text, stderr_text = proc.communicate()
        result = {
            "status": "PASS" if readiness["status"] == "PASS" and resident and observed_ready and health.get("care_coverage") == "synthetic" and network == 0 and network_observation.get("error") is None and proc.returncode == 0 else "FAIL",
            "resident": resident,
            "roles": sorted(roles),
            "observed_ready": observed_ready,
            "care_coverage": health.get("care_coverage"),
            "health_error": None if readiness["status"] == "PASS" else next((entry["query_error_class"] for entry in reversed(readiness["startup_trace"]) if entry.get("query_error_class")), None),
            "readiness": {
                key: readiness[key]
                for key in (
                    "status", "reason", "startup_trace", "socket_observed_ms",
                    "all_roles_observed_ms", "all_ready_observed_ms",
                    "stable_ready_observed_ms", "sample_count", "poll_interval_ms",
                    "timeout_ms",
                )
            },
            "supervisor_stderr_tail": _sanitized_tail(stderr_text),
            "supervisor_stdout_present": bool(stdout_text),
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
