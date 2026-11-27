f = open(OUT, "w")
try:
    import BigWorld, Athlete
    p = BigWorld.player()
    f.write("p: %r\n" % (p,))
    cls = p.__class__
    f.write("cls: %r\n" % (cls,))
    for m in sorted(dir(cls)):
        if not m.startswith('__') and ('hall' in m.lower() or 'scene' in m.lower() or 'load' in m.lower() or 'char' in m.lower() or 'ui' in m.lower()):
            f.write("  %s\n" % (m,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
