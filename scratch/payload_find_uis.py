import sys
import traceback

with open(OUT, "w") as f:
    try:
        import Globals
        ui_mgr = getattr(Globals, "uiMgr", None)
        f.write("uiMgr: %r\n" % ui_mgr)
        if ui_mgr:
            for attr in dir(ui_mgr):
                if not attr.startswith("__"):
                    v = getattr(ui_mgr, attr)
                    if isinstance(v, (dict, list, tuple)):
                        f.write("  ui_mgr.%s = %r\n" % (attr, v if len(v) < 30 else len(v)))

        # Look in ui package
        import ui
        f.write("\nui dir: %r\n" % dir(ui))
        
        # Check all imported ui submodules
        ui_mods = [m for m in sys.modules.keys() if m.startswith("ui.") or "appearance" in m.lower() or "supply" in m.lower()]
        f.write("\nui_mods: %r\n" % ui_mods[:40])
    except Exception:
        f.write(traceback.format_exc())
