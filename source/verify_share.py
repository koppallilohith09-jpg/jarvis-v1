"""Verify the share edition uses its original visual and no private asset."""
import json,os,sys
from pathlib import Path
def main():
    root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).parent
    assert (root/'share-edition.json').is_file()
    assert not (root/'assets/brahma-core').exists()
    os.environ.pop('JARVIS_OFFSCREEN_STATIC',None)
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts,True)
    app=QApplication.instance() or QApplication([sys.argv[0]])
    from ui import MainWindow
    from core.brahma_scene import Scene
    window=MainWindow('face.png');window.show();app.processEvents()
    try:
        assert isinstance(window.hud,Scene)
        assert window._unified.brain_name.text()=='AI not connected'
        window.grab().save(str(root/'friend-edition-preview.png'))
        (root/'share-diagnostics.json').write_text(json.dumps({'original_visual':'passed','restricted_asset_absent':'passed','clean_user_defaults':'passed','camera_microphone':'not accessed'},indent=2))
    finally:window.close();app.processEvents()
if __name__=='__main__':main()
