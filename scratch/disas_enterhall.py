import sys, types, dis, StringIO
f = open(OUT, "w")
try:
    import Athlete
    p_cls = Athlete.PlayerAthlete
    for name in ["enterHall", "_realEnterHall", "enterHallUI", "onLogin"]:
        fn = p_cls.__dict__.get(name)
        f.write("=== %s: %r ===\n" % (name, fn))
        if fn:
            def inner(fn):
                for cell in (getattr(fn, "func_closure", None) or ()):
                    try: v = cell.cell_contents
                    except ValueError: continue
                    if isinstance(v, types.FunctionType): return inner(v)
                return fn
            real_fn = inner(fn)
            buf = StringIO.StringIO()
            old = sys.stdout; sys.stdout = buf
            dis.dis(real_fn)
            sys.stdout = old
            f.write(buf.getvalue() + "\n")
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
