f = open(OUT, "w")
try:
    import sys
    for name in sys.modules:
        if "app" in name.lower():
            f.write("app mod: %s -> %r\n" % (name, sys.modules[name]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
