import Globals, traceback

f = open(OUT, 'w')
try:
    all_ui = getattr(Globals.uiMgr, '____all_ui__', {})
    
    def dump_w(w, path=''):
        if not w: return
        name = getattr(w, 'name', '')
        cur_p = (path + "/" + name) if path else name
        visible = getattr(w, 'isVisible', lambda: True)()
        f.write("%s (visible=%s, type=%s)\n" % (cur_p, visible, type(w).__name__))
        if hasattr(w, 'getChildren'):
            for c in w.getChildren():
                dump_w(c, cur_p)

    for name in ['UILogin', 'UILanguageBtn', 'UIJumpTip']:
        ui = all_ui.get(name)
        if ui and hasattr(ui, 'panel'):
            f.write("\n=== " + name + " ===\n")
            dump_w(ui.panel)

except Exception:
    f.write(traceback.format_exc())
f.close()
