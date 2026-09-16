#!/usr/bin/env python3
"""Bounded sensor-gateway inventory using existing Linux device APIs only.

No semantic vision, speech, biometric, or raw-media persistence is performed.
"""
from __future__ import annotations
import argparse, glob, json, os, subprocess, time
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
    video_capture=[]
    for item in video:
        device=f"/dev/{item['device']}"
        started=time.monotonic_ns()
        try:
            probe=subprocess.run(["v4l2-ctl",f"--device={device}","--stream-mmap","--stream-count=2","--stream-to=/dev/null"],capture_output=True,text=True,timeout=8)
            returncode=probe.returncode; detail=probe.stderr.strip()[:240]
        except subprocess.TimeoutExpired:
            returncode=124; detail="bounded_capture_timeout"
        video_capture.append({"device":item["device"],"status":"PASS" if returncode==0 else "BLOCKED","returncode":returncode,"elapsed_ns":time.monotonic_ns()-started,"raw_persisted":False,"stderr_class":detail if returncode else None})
    audio_capture=[]
    for item in audio:
        card=item["device"]
        started=time.monotonic_ns()
        try:
            probe=subprocess.run(["arecord","-D",f"hw:{card},0","-d","1","-f","S16_LE","-r","16000","-t","raw","/dev/null"],capture_output=True,text=True,timeout=8)
            returncode=probe.returncode; detail=probe.stderr.strip()[:240]
        except subprocess.TimeoutExpired:
            returncode=124; detail="bounded_capture_timeout"
        audio_capture.append({"device":card,"status":"PASS" if returncode==0 else "BLOCKED","returncode":returncode,"elapsed_ns":time.monotonic_ns()-started,"raw_persisted":False,"stderr_class":detail if returncode else None})
    result={"profile":"COMPANION_ALPHA50_SENSOR_GATEWAY_V1","status":"PASS" if video_capture or audio_capture else "BLOCKED","monotonic_start_ns":time.monotonic_ns(),"video_devices":video,"audio_devices":audio,"video_capture":video_capture,"audio_capture":audio_capture,"webcam":{"status":"available" if any(x["status"]=="PASS" for x in video_capture) else "degraded_unavailable","raw_persistence":"ephemeral","semantic_recognition":False},"microphone":{"status":"available" if any(x["status"]=="PASS" for x in audio_capture) else "degraded_unavailable","raw_persistence":"ephemeral","speech_recognition":False},"routing":{"ordinary":"companion-core","safety_candidate":"direct-care-core","shared_companion_gate":False},"speaker":{"status":"not_attempted","non_speech_output":False},"evidence_ceiling":"E2_REPRODUCED"}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print(json.dumps(result,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
