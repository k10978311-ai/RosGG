import Globals
import traceback

with open(OUT, "w") as f:
    try:
        uiMgr = Globals.uiMgr
        main_ui = getattr(uiMgr, "____focus_main_ui__", None)
        f.write("main_ui: %r\n" % main_ui)
        if hasattr(main_ui, "panel"):
            p = main_ui.panel
            f.write("panel: %r, dir: %r\n" % (p, dir(p)))
        # Check btn_func_list
        if hasattr(main_ui, "btn_func_list"):
            f.write("btn_func_list: %r\n" % getattr(main_ui, "btn_func_list"))
        # Check all attributes containing 'exit', 'leave', 'feiji', 'plane', 'bag'
        for attr in dir(main_ui):
            if any(k in attr.lower() for k in ["exit", "leave", "feiji", "plane", "bag", "btn", "touch"]):
                try:
                    f.write("  %s = %r\n" % (attr, getattr(main_ui, attr)))
                except Exception as e:
                    f.write("  %s error: %s\n" % (attr, e))
    except Exception:
        f.write(traceback.format_exc())
