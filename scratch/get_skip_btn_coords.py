f = open(OUT, "w")
try:
    import Globals
    skip_ui = Globals.uiMgr.get_ui_by_name("UISkipTutorial")
    f.write("UISkipTutorial: %r\n" % (skip_ui,))
    p = skip_ui.panel
    f.write("panel: %r\n" % (p,))
    
    # Try get_widget_by_path
    btn = skip_ui.get_widget_by_path("left_bottom/skip_btn")
    f.write("btn: %r\n" % (btn,))
    if btn:
        f.write("btn dir: %r\n" % ([a for a in dir(btn) if not a.startswith("__")],))
        for meth in ["GetPosition", "getPosition", "GetWorldPosition", "getWorldPosition", "GetBoundingBox", "getBoundingBox", "GetContentSize", "getContentSize", "getWorldPosition2D"]:
            if hasattr(btn, meth):
                try:
                    f.write("%s: %r\n" % (meth, getattr(btn, meth)()))
                except Exception as e:
                    f.write("%s: <err %s>\n" % (meth, e))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
