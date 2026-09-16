#!/usr/bin/env python3
"""Metadata-only Openbox/display probe; never captures desktop pixels."""
import json, os, subprocess
def run(cmd):
    try: return subprocess.run(cmd,capture_output=True,text=True,timeout=5).stdout.strip()
    except Exception as e: return f"unavailable:{e}"
def main():
    print(json.dumps({"display":os.environ.get("DISPLAY"),"session":os.environ.get("XDG_SESSION_TYPE"),"xrandr":run(["xrandr","--query"]),"window_manager":run(["wmctrl","-m"]),"screen_tree":run(["xwininfo","-root","-tree"]),"media_capture":"not performed"},sort_keys=True))
if __name__=="__main__": main()
