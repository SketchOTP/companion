#!/usr/bin/env python3
"""Bounded sensor-gateway inventory using existing Linux device APIs only.

No semantic vision, speech, biometric, or raw-media persistence is performed.
"""
from __future__ import annotations
import argparse, glob, json, os, time
from pathlib import Path

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=Path,required=True); a=ap.parse_args()
    video=[]
    for path in sorted(glob.glob("/dev/video*")):
        try:
            st=os.stat(path); video.append({"device":Path(path).name,"mode":oct(st.st_mode & 0o777),"available":True})
        except OSError as exc: video.append({"device":Path(path).name,"available":False,"error_class":type(exc).__name__})
    audio=[]
    alsa=Path("/proc/asound/cards")
    if alsa.exists():
        for line in alsa.read_text(errors="replace").splitlines():
            if line.strip(): audio.append({"device":line.strip().split()[0],"available":True,"source":"/proc/asound/cards"})
    result={"profile":"COMPANION_ALPHA50_SENSOR_GATEWAY_V1","status":"PASS","monotonic_start_ns":time.monotonic_ns(),"video_devices":video,"audio_devices":audio,"webcam":{"status":"available" if video else "degraded_unavailable","raw_persistence":"ephemeral","semantic_recognition":False},"microphone":{"status":"available" if audio else "degraded_unavailable","raw_persistence":"ephemeral","speech_recognition":False},"routing":{"ordinary":"companion-core","safety_candidate":"direct-care-core","shared_companion_gate":False},"speaker":{"status":"not_attempted","non_speech_output":False},"evidence_ceiling":"E1_OBSERVED"}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print(json.dumps(result,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
