f = open(OUT, "w")
try:
    import BigWorld
    p = BigWorld.player()
    f.write("Class: %s\n" % (p.__class__.__name__,))
    f.write("Bases: %r\n" % ([b.__name__ for b in p.__class__.__mro__],))
    matches = []
    for m in dir(p):
        ml = m.lower()
        if any(k in ml for k in ['hall', 'login', 'scene', 'enter', 'lobby', 'create', 'ready']):
            matches.append((m, str(type(getattr(p, m)))))
    for m, t in sorted(matches):
        f.write("  %s (%s)\n" % (m, t))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
