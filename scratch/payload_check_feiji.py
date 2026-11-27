import Globals
import traceback

with open(OUT, "w") as f:
    try:
        uiMgr = Globals.uiMgr
        main_ui = getattr(uiMgr, "____focus_main_ui__", None)
        fw = getattr(main_ui, "dlgFeijiAnimWidget", None)
        f.write("dlgFeijiAnimWidget: %r\n" % fw)
        if fw:
            f.write("dir: %r\n" % dir(fw))
            for attr in ["visible", "isVisible", "enabled", "close", "on_close", "onClose"]:
                if hasattr(fw, attr):
                    f.write("  %s: %r\n" % (attr, getattr(fw, attr)))
    except Exception:
        f.write(traceback.format_exc())
