f = open(OUT, "w")
try:
    import BigWorld, Globals
    p = BigWorld.player()
    f.write("player: %r\n" % (p,))
    if p:
        for a in dir(p):
            if not a.startswith('__'):
                try:
                    v = getattr(p, a)
                    if isinstance(v, (int, str, bool, float, list, dict, tuple)):
                        f.write("  p.%s = %r\n" % (a, v))
                    elif callable(v):
                        pass # method
                    else:
                        f.write("  p.%s: %s\n" % (a, type(v).__name__))
                except Exception as e:
                    f.write("  p.%s: <err %s>\n" % (a, e))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
