"""User-authorized 20-second local movement-only webcam diagnostic."""
import json,os,sys,time
from collections import Counter
from pathlib import Path
os.environ['QT_QPA_PLATFORM']='windows'
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from core.gestures import GestureService
from core.gesture_preview import GesturePreview

def main():
    app=QApplication([sys.argv[0]]);service=GestureService();counts=Counter();moves=[]
    original=service._apply
    def move_only(event):
        if event['action']!='move':return
        import pyautogui
        before=tuple(pyautogui.position());original(event);after=tuple(pyautogui.position())
        moves.append(before!=after)
    service._apply=move_only
    window=GesturePreview(service);window.setWindowTitle('20-second local test — POINT to move; clicks disabled')
    # The test permission is fixed, not editable by the test window.
    window.control.hide();window.show()
    def sample():
        state=service.preview();counts[state['gesture'] if state['landmarks'] else 'no_hand']+=1
    timer=QTimer();timer.timeout.connect(sample);timer.start(100)
    try:
        service.arm('pc',True,0);QTimer.singleShot(20000,app.quit);app.exec()
    finally:
        status=service.status();service.stop();window.close();timer.stop()
        if service.thread:service.thread.join(timeout=5)
        report={'duration_limit_seconds':20,'gesture_poll_samples':dict(counts),'move_adapter_calls':len(moves),'observed_cursor_position_changes':sum(moves),'last_status':status['message'],'video_saved':False,'click_scroll_media_enabled':False}
        Path('physical-hand-diagnostics.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
if __name__=='__main__':main()
