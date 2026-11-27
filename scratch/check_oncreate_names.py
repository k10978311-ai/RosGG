f = open(OUT, "w")
try:
    import Athlete
    cls = Athlete.PlayerAthlete
    for mname in ('onCreate', 'onBecomePlayer'):
        fn = cls.__dict__[mname]
        co = fn.func_code
        f.write("=== %s ===\n" % mname)
        f.write("names: %r\n" % (co.co_names,))
        f.write("consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, 'co_names')],))
        for c in co.co_consts:
            if hasattr(c, 'co_names'):
                f.write("  sub %s names: %r\n" % (c.co_name, c.co_names))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
