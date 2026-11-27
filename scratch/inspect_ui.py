f = open(OUT, "w")
try:
    import Globals
    ui = getattr(Globals, "uiMgr", None)
    f.write("uiMgr: %r\n" % (ui,))
    if ui:
        for a in dir(ui):
            if not a.startswith('__'):
                try:
                    val = getattr(ui, a)
                    if isinstance(val, (int, str, bool, list, dict, set, tuple)):
                        f.write("  ui.%s = %r\n" % (a, val))
                    else:
                        f.write("  ui.%s: %s\n" % (a, type(val).__name__))
                except Exception as e:
                    f.write("  ui.%s: <err %s>\n" % (a, e))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
