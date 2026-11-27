import Globals, sys, traceback

f = open(OUT, 'w')
try:
    f.write("=== ACTIVE UIs ===\n")
    uiMgr = Globals.uiMgr
    all_ui = getattr(uiMgr, '____all_ui__', {})
    for k, v in all_ui.items():
        f.write("%s: %s\n" % (k, type(v)))
        # list children/widgets
        if hasattr(v, 'panel'):
            f.write("  panel: %s\n" % (v.panel,))
        for attr in ['widget_ui_path', 'btn_func_list', 'ui_type']:
            if hasattr(v, attr):
                f.write("  %s: %s\n" % (attr, getattr(v, attr)))
    
    # Check UILogin specifically
    uilogin = all_ui.get('UILogin')
    if uilogin:
        f.write("\n=== UILogin details ===\n")
        for a in dir(uilogin):
            if not a.startswith('__'):
                try:
                    val = getattr(uilogin, a)
                    if not callable(val):
                        f.write("  %s = %r\n" % (a, str(val)[:120]))
                except:
                    pass

except Exception:
    f.write(traceback.format_exc())
f.close()
