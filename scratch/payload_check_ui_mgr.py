import Globals
import traceback

with open(OUT, "w") as f:
    try:
        f.write("MAP_ID: %r\n" % getattr(Globals, "MAP_ID", None))
        f.write("isInHall: %r\n" % (Globals.isInHall() if callable(getattr(Globals, "isInHall", None)) else getattr(Globals, "isInHall", None)))
        f.write("isInGame: %r\n" % (Globals.isInGame() if callable(getattr(Globals, "isInGame", None)) else getattr(Globals, "isInGame", None)))
        f.write("hallSceneReady: %r\n" % getattr(Globals, "hallSceneReady", None))
        
        uiMgr = getattr(Globals, "uiMgr", None)
        f.write("uiMgr: %r\n" % uiMgr)
        if uiMgr:
            f.write("uiMgr dir: %r\n" % dir(uiMgr))
            if hasattr(uiMgr, "get_all_ui"):
                f.write("all_ui: %r\n" % uiMgr.get_all_ui())
            elif hasattr(uiMgr, "ui_dict"):
                f.write("ui_dict: %r\n" % uiMgr.ui_dict)
            elif hasattr(uiMgr, "active_ui"):
                f.write("active_ui: %r\n" % uiMgr.active_ui)

        uiPanels = getattr(Globals, "uiPanels", None)
        f.write("uiPanels: %r\n" % uiPanels)
        if uiPanels:
            f.write("uiPanels keys: %r\n" % (uiPanels.keys() if hasattr(uiPanels, "keys") else type(uiPanels)))

    except Exception:
        f.write(traceback.format_exc())
