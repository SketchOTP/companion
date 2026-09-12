#!/usr/bin/env python3
"""Canonical, fail-closed Godot qualification runner for R04-C03.

The runner is intentionally small and is shared by local reproduction, the
hosted workflow, and ``run_r04_evidence.py``.  Godot application channels and
the Xvfb wrapper channel are retained separately so a diagnostic can be
classified without losing its provenance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
RUNNER_VERSION = "r04-c03-godot-runner-v1"
ERROR_RE = re.compile(r"\bERROR:\s*.*")
WARNING_RE = re.compile(r"\bWARNING:\s*.*")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    if not path.is_file():
        return digest.hexdigest()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_digest(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(item.relative_to(path).as_posix().encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(item.read_bytes()).digest())
    return digest.hexdigest()


def _lines(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def channel_matches(path: Path, pattern: re.Pattern[str]) -> list[str]:
    return [line.strip() for line in _lines(path) if pattern.search(line)]


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def classify_logs(stdout: list[str], stderr: list[str], engine: list[str]) -> dict[str, Any]:
    """Classify only Godot channels; wrapper diagnostics are never mixed in."""
    errors_by_channel = {
        "stdout": [line.strip() for line in stdout if ERROR_RE.search(line)],
        "stderr": [line.strip() for line in stderr if ERROR_RE.search(line)],
        "engine": [line.strip() for line in engine if ERROR_RE.search(line)],
    }
    warnings_by_channel = {
        "stdout": [line.strip() for line in stdout if WARNING_RE.search(line)],
        "stderr": [line.strip() for line in stderr if WARNING_RE.search(line)],
        "engine": [line.strip() for line in engine if WARNING_RE.search(line)],
    }
    errors = _unique([line for lines in errors_by_channel.values() for line in lines])
    warnings = _unique([line for lines in warnings_by_channel.values() for line in lines])
    return {
        "godot_error_lines": errors,
        "godot_error_lines_by_channel": errors_by_channel,
        "godot_warning_lines": warnings,
        "godot_warning_lines_by_channel": warnings_by_channel,
        "godot_error_count": len(errors),
        "godot_warning_count": len(warnings),
        "godot_gate": "PASSED" if not errors else "FAILED",
    }


def _extract_json(text: str) -> dict[str, Any] | None:
    decoder = json.JSONDecoder()
    found: dict[str, Any] | None = None
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            value, end = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if end and isinstance(value, dict):
            found = value
    return found


def _sanitized(value: str, *, temp_root: Path | None = None) -> str:
    # Arguments are frequently encoded as ``--key=/private/path``.  Redact
    # the path portion without changing the option spelling.
    if temp_root is not None:
        temp_text = str(temp_root)
        if temp_text in value:
            return value.replace(temp_text, "<qualification-temp>")
    path = Path(value)
    if temp_root is not None:
        try:
            return f"<qualification-temp>/{path.relative_to(temp_root).as_posix()}"
        except ValueError:
            pass
    if path.is_absolute():
        return f"<absolute>/{path.name}"
    return value


def _sanitized_command(command: list[str], temp_root: Path) -> list[str]:
    return [_sanitized(item, temp_root=temp_root) for item in command]


def _version(godot: Path) -> str:
    result = subprocess.run([str(godot), "--version"], cwd=ROOT, text=True, capture_output=True, check=False)
    text = (result.stdout + "\n" + result.stderr).strip()
    return text.splitlines()[-1] if text else "unknown"


def _renderer_summary(lines: list[str]) -> dict[str, str]:
    summary: dict[str, str] = {}
    for line in lines:
        stripped = line.strip()
        if "OpenGL API" in stripped or "Vulkan" in stripped or "Using Device:" in stripped:
            summary.setdefault("renderer", stripped)
        if "DisplayServer" in stripped or "display server" in stripped.lower():
            summary.setdefault("display_server", stripped)
    summary.setdefault("display_server", os.environ.get("DISPLAY", "unavailable"))
    summary.setdefault("rendering_method", "observed in Godot output or unavailable")
    return summary


def run_qualification(
    *,
    godot: Path,
    out: Path,
    mode: str,
    pack: Path | None = None,
    corrupt_pack: Path | None = None,
    project: Path = ROOT / "godot",
    label: str = "qualification",
    script: str | None = None,
    script_args: list[str] | None = None,
    use_xvfb: bool = True,
) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    stdout_path = out / "godot.stdout.log"
    stderr_path = out / "godot.stderr.log"
    engine_path = out / "godot.engine.log"
    xvfb_path = out / "xvfb-wrapper.log"
    cache = project / ".godot"
    cache_before = tree_digest(cache)

    # Explicitly select Godot's documented Dummy audio driver for every
    # qualification mode.  Import already implies Dummy under --headless,
    # while semantic runs use Xvfb for rendering and would otherwise probe
    # host ALSA devices and emit a genuine ERR_CANT_OPEN diagnostic before
    # falling back.  This keeps the audio boundary deterministic without
    # changing the host or suppressing an engine error.
    audio_args = ["--audio-driver", "Dummy"]
    if mode == "import":
        godot_args = [*audio_args, "--headless", "--path", str(project), "--editor", "--quit"]
    else:
        selected_script = script or "r04_authored_pack_test.gd"
        if pack is None:
            raise ValueError("--pack is required for semantic mode")
        godot_args = [*audio_args, "--path", str(project), "--script", f"res://{selected_script}"]
        args = list(script_args or [])
        if not args:
            args = [f"--pack={pack}"]
            if corrupt_pack is not None:
                args.append(f"--corrupt-pack={corrupt_pack}")
        godot_args += ["--", *args]
    command = [str(godot), "--log-file", str(engine_path), *godot_args]
    wrapped = ["xvfb-run", "-a", "-e", str(xvfb_path), *command] if use_xvfb and shutil.which("xvfb-run") else command
    started = time.monotonic_ns()
    process = subprocess.run(wrapped, cwd=ROOT, text=True, capture_output=True, check=False)
    elapsed_ns = time.monotonic_ns() - started
    stdout_path.write_text(process.stdout, encoding="utf-8")
    stderr_path.write_text(process.stderr, encoding="utf-8")
    if not xvfb_path.exists():
        xvfb_path.write_text("", encoding="utf-8")
    engine_lines = _lines(engine_path)
    stdout_lines = _lines(stdout_path)
    stderr_lines = _lines(stderr_path)
    classification = classify_logs(stdout_lines, stderr_lines, engine_lines)
    semantic = _extract_json(process.stdout + "\n" + process.stderr)
    cache_after = tree_digest(cache)
    all_lines = stdout_lines + stderr_lines + engine_lines
    result: dict[str, Any] = {
        "runner_version": RUNNER_VERSION,
        "label": label,
        "mode": mode,
        "godot_version": _version(godot),
        "process_exit_code": process.returncode,
        "display_server": os.environ.get("DISPLAY", "unavailable"),
        "renderer_driver": _renderer_summary(all_lines),
        "command": _sanitized_command(wrapped, out.parent),
        "pack_sha256": sha256(pack) if pack else None,
        "stdout_sha256": sha256(stdout_path),
        "stderr_sha256": sha256(stderr_path),
        "engine_log_sha256": sha256(engine_path),
        "xvfb_log_sha256": sha256(xvfb_path),
        "stdout_log": stdout_path.name,
        "stderr_log": stderr_path.name,
        "engine_log": engine_path.name,
        "xvfb_log": xvfb_path.name,
        "cache_before_exists": cache.exists() if cache_before is not None else False,
        "cache_before_digest": cache_before,
        "cache_after_exists": cache.exists() if cache_after is not None else False,
        "cache_after_digest": cache_after,
        "elapsed_ms": round(elapsed_ns / 1_000_000, 3),
        "semantic_test_result": semantic,
        "wrapper_diagnostics": _lines(xvfb_path),
        **classification,
    }
    result["status"] = "PASSED" if process.returncode == 0 and classification["godot_gate"] == "PASSED" else "FAILED"
    (out / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--mode", choices=("import", "semantic"), required=True)
    parser.add_argument("--pack", type=Path)
    parser.add_argument("--corrupt-pack", type=Path)
    parser.add_argument("--project", type=Path, default=ROOT / "godot")
    parser.add_argument("--label", default="qualification")
    parser.add_argument("--script", default=None)
    parser.add_argument("--script-arg", action="append", default=[])
    parser.add_argument("--no-xvfb", action="store_true")
    args = parser.parse_args()
    result = run_qualification(
        godot=args.godot.resolve(), out=args.out.resolve(), mode=args.mode,
        pack=args.pack.resolve() if args.pack else None,
        corrupt_pack=args.corrupt_pack.resolve() if args.corrupt_pack else None,
        project=args.project.resolve(), label=args.label, script=args.script,
        script_args=args.script_arg or None, use_xvfb=not args.no_xvfb,
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
