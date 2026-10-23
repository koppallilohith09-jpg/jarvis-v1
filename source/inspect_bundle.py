from pathlib import Path
import pefile
root=Path(__file__).resolve().parent/'dist/JARVIS-Local-Gestures/_internal'
files={}
for path in root.rglob('*'):
    if path.suffix.lower() in ('.dll','.pyd'):files.setdefault(path.name.lower(),[]).append(path)
for name in ('qtwidgets.pyd','qtgui.pyd','qtcore.pyd','qt6widgets.dll','qt6gui.dll','qt6core.dll'):
    for path in files.get(name,[]):
        pe=pefile.PE(str(path))
        for imported in getattr(pe,'DIRECTORY_ENTRY_IMPORT',[]):
            dependency=imported.dll.decode().lower()
            if dependency not in files:continue
            for lib in files[dependency]:
                target=pefile.PE(str(lib));exports={s.name for s in getattr(getattr(target,'DIRECTORY_ENTRY_EXPORT',None),'symbols',[]) if s.name}
                missing=[s.name.decode(errors='replace') for s in imported.imports if s.name and s.name not in exports]
                if missing:print(name, '->',lib.relative_to(root),'MISSING',missing[:15])
