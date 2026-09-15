#!/usr/bin/env python3
"""Deterministic tests for the fail-closed readiness poller."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from foundation_runtime_check import EXPECTED_ROLES, wait_for_stable_readiness  # noqa: E402


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


def health(*, ready, coverage="synthetic", state="healthy", roles=None):
    selected = EXPECTED_ROLES if roles is None else set(roles)
    return {
        "care_coverage": coverage,
        "children": [
            {"role": role, "ready": ready, "state": state}
            for role in sorted(selected)
        ],
    }


def delayed_ready_test():
    clock = FakeClock()
    samples = iter(
        [
            health(ready=False, coverage="degraded", roles={"care-core"}),
            health(ready=False),
            health(ready=True),
            health(ready=True),
        ]
    )
    result = wait_for_stable_readiness(
        Path("synthetic.sock"),
        process_alive=lambda: True,
        query_fn=lambda _path: next(samples),
        socket_exists_fn=lambda _path: True,
        monotonic_fn=clock.monotonic,
        sleep_fn=clock.sleep,
        timeout_ms=500,
        poll_interval_ms=10,
    )
    assert result["status"] == "PASS"
    assert result["reason"] == "stable_complete_readiness"
    assert result["sample_count"] == 4
    assert result["stable_ready_observed_ms"] == 30.0
    assert result["startup_trace"][0]["care_coverage"] == "degraded"
    assert result["startup_trace"][2]["ready_roles"] == sorted(EXPECTED_ROLES)
    return {"status": "PASS", "sample_count": result["sample_count"]}


def never_ready_test():
    clock = FakeClock()
    result = wait_for_stable_readiness(
        Path("synthetic.sock"),
        process_alive=lambda: True,
        query_fn=lambda _path: health(ready=False, coverage="degraded"),
        socket_exists_fn=lambda _path: True,
        monotonic_fn=clock.monotonic,
        sleep_fn=clock.sleep,
        timeout_ms=35,
        poll_interval_ms=10,
    )
    assert result["status"] == "FAIL"
    assert result["reason"] == "readiness_timeout"
    assert result["sample_count"] == 4
    assert result["startup_trace"][-1]["care_coverage"] == "degraded"
    return {"status": "EXPECTED_FAIL", "reason": result["reason"], "sample_count": result["sample_count"]}


def early_exit_test():
    clock = FakeClock()
    alive = iter([True, False])
    result = wait_for_stable_readiness(
        Path("synthetic.sock"),
        process_alive=lambda: next(alive),
        query_fn=lambda _path: health(ready=False),
        socket_exists_fn=lambda _path: True,
        monotonic_fn=clock.monotonic,
        sleep_fn=clock.sleep,
        timeout_ms=500,
        poll_interval_ms=10,
    )
    assert result["status"] == "FAIL"
    assert result["reason"] == "supervisor_exited_before_stable_readiness"
    assert result["startup_trace"][-1]["query_error_class"] == "supervisor_exited"
    return {"status": "EXPECTED_FAIL", "reason": result["reason"], "sample_count": result["sample_count"]}


if __name__ == "__main__":
    import json

    summary = {
        "delayed_ready": delayed_ready_test(),
        "never_ready": never_ready_test(),
        "supervisor_exit": early_exit_test(),
    }
    print(json.dumps(summary, sort_keys=True))
