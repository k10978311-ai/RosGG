f = open(OUT, "w")
try:
    import Globals
    uiMgr = Globals.uiMgr
    skip_ui = uiMgr.get_ui_by_name("UISkipTutorial")
    f.write("UISkipTutorial: %r\n" % (skip_ui,))
    if skip_ui:
        for attr in ["btn_func_list", "onExit", "onExitBtnEvent", "tryLeaveMap", "widget_ui_path"]:
            f.write("%s: %r\n" % (attr, getattr(skip_ui, attr, None)))
        
        # Check panel children / nodes
        p = skip_ui.panel
        f.write("panel: %r\n" % (p,))
        if p and hasattr(p, "GetChildren"):
            f.write("children: %r\n" % ([c.name for c in p.GetChildren()],))
        
        # Check code of onExitBtnEvent or tryLeaveMap
        fn = getattr(skip_ui, "onExitBtnEvent", None) or getattr(skip_ui, "tryLeaveMap", None)
        if fn:
            co = fn.func_code
            f.write("fn: %r, names: %r, consts: %r\n" % (fn, co.co_names, [c for c in co.co_consts if not hasattr(c, "co_names")]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
