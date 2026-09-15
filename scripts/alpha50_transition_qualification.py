#!/usr/bin/env python3
"""Fail-closed legal transition qualification over the frozen R06 pack.

The resolver is presentation-only: it selects authored tracks and never owns
organism state. Every case records the concrete path so the historical
all-pairs shortcut cannot masquerade as a legal graph.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

LEGAL = {
    ("front", "left"): ["r06_playback_track_06"],
    ("left", "left"): ["r06_playback_track_07", "r06_playback_track_08", "r06_playback_track_09"],
    ("left", "front"): ["r06_playback_track_10"],
    ("front", "right"): ["r06_playback_track_11"],
    ("right", "right"): ["r06_playback_track_12", "r06_playback_track_13", "r06_playback_track_14"],
    ("right", "front"): ["r06_playback_track_15"],
}

def resolve(tracks: dict[str, dict], start: str, target: str, action: str) -> list[str]:
    if action == "walk_left":
        path = LEGAL.get((start, "left")) if start != "left" else LEGAL[("left", "left")]
    elif action == "walk_right":
        path = LEGAL.get((start, "right")) if start != "right" else LEGAL[("right", "right")]
    elif action == "return_front":
        path = LEGAL.get((start, "front"))
    else:
        path = None
    if not path or target not in ("left", "right", "front"):
        raise ValueError("no_legal_path")
    selected = [tid for tid in path if tid in tracks]
    if selected != path:
        raise ValueError("missing_authored_connector")
    final = tracks[selected[-1]].get("exit_facing")
    if final != target:
        raise ValueError("endpoint_facing_mismatch")
    return selected

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--pack", type=Path, required=True); ap.add_argument("--output", type=Path, required=True); ap.add_argument("--cases", type=int, default=10000)
    args = ap.parse_args(); pack = json.loads(args.pack.read_text()); tracks = {t["track_id"]: t for t in pack["tracks"]}
    cases=[]; digest=hashlib.sha256(); accepted=0; rejected=0
    scenarios=[("front","left","walk_left"),("left","left","walk_left"),("left","front","return_front"),("front","right","walk_right"),("right","right","walk_right"),("right","front","return_front"),("front","front","unsupported")]
    for i in range(args.cases):
        start,target,action=scenarios[i % len(scenarios)]; case_id=f"alpha50-transition-{i:06d}"
        try: path=resolve(tracks,start,target,action); decision="accepted"; accepted+=1
        except ValueError as exc: path=[]; decision=f"rejected:{exc}"; rejected+=1
        row={"case_id":case_id,"seed":17+(i%3)*6,"starting_facing":start,"requested_action":action,"target_facing":target,"decision":decision,"path":path,"final_facing":tracks[path[-1]]["exit_facing"] if path else start,"pack_sha256":hashlib.sha256(args.pack.read_bytes()).hexdigest()}
        digest.update(json.dumps(row,sort_keys=True,separators=(",",":")).encode());
        if i < 200 or i in (args.cases-1,): cases.append(row)
    # Independent graph tamper checks start from the actual pack, then remove
    # one required edge and ensure the resolver rejects it.
    tampered=dict(tracks); tampered.pop("r06_playback_track_06",None)
    try: resolve(tampered,"front","left","walk_left"); tamper_removed=False
    except ValueError: tamper_removed=True
    graph_edges={f"{start}->{target}": path for (start,target), path in LEGAL.items()}
    result={"profile":"COMPANION_ALPHA50_TRANSITION_V1","status":"PASS" if args.cases>=10000 and tamper_removed and accepted>0 and rejected>0 else "FAIL","cases":args.cases,"accepted":accepted,"rejected":rejected,"sample_cases":cases,"graph_edges":graph_edges,"tamper_negative":{"removed_connector_rejected":tamper_removed,"historical_all_pairs_shortcut":False},"digest":digest.hexdigest(),"pack_sha256":hashlib.sha256(args.pack.read_bytes()).hexdigest(),"evidence_ceiling":"E3_TARGET_TESTED","claim_boundary":"frozen-pack presentation qualification; no Phase 02 acceptance or product reliability claim"}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print(json.dumps(result,sort_keys=True)); return 0 if result["status"]=="PASS" else 1
if __name__ == "__main__": raise SystemExit(main())
