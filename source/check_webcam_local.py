"""Run only with the user's permission. No image recording or OS input."""
import json
import time
from core.local_privacy import install_network_guard
install_network_guard()
from core.gestures import GestureService

def main():
    service=GestureService();seen=set();poses=set();hand_frames=0
    service.arm('pc',False)
    start=time.monotonic()
    try:
        while time.monotonic()-start<15:
            state=service.preview()
            if state['mode']=='off':break
            with service.lock:seq=service.seq
            if seq not in seen and seq>=0:
                seen.add(seq)
                if state['landmarks']:
                    hand_frames+=1
                    if state['gesture']:poses.add(state['gesture'])
            time.sleep(.05)
        state=service.status()
        report={'frames':len(seen),'frames_with_hand':hand_frames,'poses':sorted(poses),'input_control':service.control,'images_saved':False,'error':state['message'] if state['mode']=='off' else None}
        print(json.dumps(report))
    finally:
        service.stop()
        if service.thread:service.thread.join(timeout=3)

if __name__=='__main__':main()
