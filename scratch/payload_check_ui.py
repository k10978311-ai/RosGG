import sys
import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        f.write("Player: %r (class=%s, id=%s)\n" % (p, type(p).__name__, getattr(p, "id", None)))
        
        import Globals
        ui_mgr = getattr(Globals, "uiMgr", None)
        if ui_mgr:
            vis = {}
            for k, v in getattr(ui_mgr, "_ui_dict", {}).items():
                if v and getattr(v, "visible", False):
                    vis[k] = type(v).__name__
            f.write("Visible UIs: %r\n" % vis)
            f.write("current_focus: %r\n" % getattr(ui_mgr, "current_focus", None))
            
            # Check all UIs in _ui_dict
            f.write("all UIs: %r\n" % list(getattr(ui_mgr, "_ui_dict", {}).keys()))
    except Exception:
        f.write(traceback.format_exc())
