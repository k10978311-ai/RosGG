f = open(OUT, "w")
try:
    import Globals
    f.write("Globals functions:\n")
    for k in sorted(dir(Globals)):
        v = getattr(Globals, k)
        if callable(v):
            f.write("  %s: %r\n" % (k, v))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
