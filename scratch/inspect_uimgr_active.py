f = open(OUT, "w")
try:
    import Globals
    uiMgr = Globals.uiMgr
    f.write("uiMgr attributes:\n")
    for a in dir(uiMgr):
        if not a.startswith('__'):
            try:
                v = getattr(uiMgr, a)
                if not callable(v):
                    f.write("  uiMgr.%s = %r\n" % (a, v))
            except Exception as e:
                pass
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
