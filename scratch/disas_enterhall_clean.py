f = open(OUT, "w")
try:
    import Athlete, dis, StringIO, sys, types
    fn = Athlete.PlayerAthlete.enterHall
    if hasattr(fn, "im_func"): fn = fn.im_func
    # unwrap closure
    def unwrap(f):
        for c in (getattr(f, "func_closure", None) or []):
            try: v = c.cell_contents
            except ValueError: continue
            if isinstance(v, types.FunctionType): return unwrap(v)
        return f
    real = unwrap(fn)
    buf = StringIO.StringIO()
    old = sys.stdout; sys.stdout = buf
    dis.dis(real)
    sys.stdout = old
    f.write(buf.getvalue())
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
