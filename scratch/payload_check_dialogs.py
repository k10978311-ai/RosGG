import Globals
import traceback

with open(OUT, "w") as f:
    try:
        uiMgr = Globals.uiMgr
        # Check active panels / widgets
        for attr in ["____focus_popup_ui__", "____ui_queue_popup__", "____active_ui_general__", "____active_const_ui__", "____active_main_add_ui__"]:
            f.write("%s: %r\n" % (attr, getattr(uiMgr, attr, None)))
        
        main_ui = getattr(uiMgr, "____focus_main_ui__", None)
        if main_ui:
            f.write("main_ui: %r\n" % main_ui)
            f.write("main_ui dir: %r\n" % dir(main_ui))
    except Exception:
        f.write(traceback.format_exc())
