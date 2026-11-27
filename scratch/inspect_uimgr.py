f = open(OUT, "w")
try:
    import Globals
    uiMgr = Globals.uiMgr
    f.write("uiMgr class: %r\n" % (uiMgr.__class__,))
    f.write("dir(uiMgr): %r\n" % ([a for a in dir(uiMgr) if not a.startswith("__")],))
    # Look for ui instances or dicts
    for attr in dir(uiMgr):
        if not attr.startswith("__"):
            val = getattr(uiMgr, attr)
            if isinstance(val, dict):
                f.write("dict attr %s: %r\n" % (attr, val.keys()))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
