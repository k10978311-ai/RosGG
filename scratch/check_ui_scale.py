f = open(OUT, "w")
try:
    import Globals
    skip_ui = Globals.uiMgr.get_ui_by_name("UISkipTutorial")
    f.write("winSize: %r\n" % (getattr(skip_ui, "winSize", None),))
    f.write("defaultResolutionSize: %r\n" % (getattr(skip_ui, "defaultResolutionSize", None),))
    f.write("getDesignResolutionSize(): %r\n" % (getattr(skip_ui, "getDesignResolutionSize", lambda: None)(),))
    
    # Also check underlyingCCWidget
    btn = skip_ui.get_widget_by_path("left_bottom/skip_btn")
    cc = btn.underlyingCCWidget
    f.write("cc: %r\n" % (cc,))
    if cc:
        for m in ["getPosition", "getWorldPosition", "getBoundingBox", "getContentSize"]:
            if hasattr(cc, m):
                f.write("cc.%s: %r\n" % (m, getattr(cc, m)()))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
