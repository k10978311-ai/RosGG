f = open(OUT, "w")
try:
    import Globals
    f.write("Globals.loginScene: %r\n" % (getattr(Globals, "loginScene", None),))
    ls = getattr(Globals, "loginScene", None)
    if ls:
        f.write("dir(loginScene): %r\n" % ([a for a in dir(ls) if not a.startswith("__")],))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
