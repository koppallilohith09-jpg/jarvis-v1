"""User-authorized <=90 second local calibration, movement only, no recording."""
import json,os,sys,time
from pathlib import Path
os.environ['QT_QPA_PLATFORM']='windows'
from PyQt6.QtWidgets import QApplication,QWidget,QVBoxLayout,QLabel,QPushButton
from PyQt6.QtCore import QTimer
from core.eye_control import service
from core.eye_panel import EyeCanvas,CalibrationView

def main():
    app=QApplication([sys.argv[0]]);window=QWidget();window.setWindowTitle('Local eye test — movement only; no recording')
    layout=QVBoxLayout(window);label=QLabel('Both eyes must be visible. Calibration opens when ready.');label.setWordWrap(True);layout.addWidget(label);layout.addWidget(EyeCanvas())
    stop=QPushButton('STOP AND CLOSE');stop.clicked.connect(app.quit);layout.addWidget(stop);window.resize(640,480);window.show()
    original_feed=service.feed;original_control=service.set_control;moves=[];detected=0;cal=None;enabled_at=None;opened=False
    def feed(points,now=None):
        import pyautogui
        before=tuple(pyautogui.position());original_feed(points,now)
        if service.control:moves.append(before!=tuple(pyautogui.position()))
    service.feed=feed;service.set_control=lambda enabled,clicks=False:original_control(enabled,False)
    service._act=lambda:None
    def tick():
        nonlocal cal,opened,detected,enabled_at
        state=service.snapshot()
        if state['feature'] is not None:detected+=1
        label.setText(state['message'])
        if not opened and state['feature'] is not None:
            opened=True;cal=CalibrationView()
        if state['control']:
            if enabled_at is None:enabled_at=time.monotonic()
            if time.monotonic()-enabled_at>10:app.quit()
    timer=QTimer();timer.timeout.connect(tick);timer.start(100)
    try:
        service.start(0);QTimer.singleShot(90000,app.quit);app.exec()
    finally:
        state=service.snapshot();service.stop();timer.stop()
        if cal:cal.close()
        window.close()
        if service.thread:service.thread.join(timeout=5)
        report={'duration_limit_seconds':90,'eyes_detected_poll_samples':detected,'calibrated':state['calibrated'],'pointer_enabled':state['control'],'move_adapter_calls':len(moves),'observed_cursor_position_changes':sum(moves),'last_status':state['message'],'calibration_result':cal.result if cal else 'No usable eye features detected.','video_saved':False,'dwell_clicks_enabled':False}
        Path('physical-eye-diagnostics.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
if __name__=='__main__':main()
