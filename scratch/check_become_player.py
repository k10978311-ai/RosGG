import sys, dis, StringIO, types
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.__dict__.get("onBecomePlayer")
    f.write("onBecomePlayer: %r\n" % fn)
    def inner(fn):
        for cell in (getattr(fn, "func_closure", None) or ()):
            try: v = cell.cell_contents
            except ValueError: continue
            if isinstance(v, types.FunctionType): return inner(v)
        return fn
    real_fn = inner(fn)
    f.write("real_fn: %r\n" % real_fn)
    co = real_fn.func_code
    f.write("co_names: %r\n" % (co.co_names,))
    f.write("co_consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, "co_names")],))
    buf = StringIO.StringIO()
    old = sys.stdout; sys.stdout = buf
    dis.dis(real_fn)
    sys.stdout = old
    f.write(buf.getvalue()[:2000])
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
