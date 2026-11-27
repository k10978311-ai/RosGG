import sys, types
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.__dict__.get("enterHall")
    def inner(fn):
        for cell in (getattr(fn, "func_closure", None) or ()):
            try: v = cell.cell_contents
            except ValueError: continue
            if isinstance(v, types.FunctionType): return inner(v)
        return fn
    real_fn = inner(fn)
    co = real_fn.func_code
    f.write("co_varnames: %r\n" % (co.co_varnames,))
    f.write("co_consts: %r\n" % ([c if not hasattr(c, "co_names") else "<code>" for c in co.co_consts],))
    for c in co.co_consts:
        if hasattr(c, "co_names"):
            f.write("nested code %s: names=%r consts=%r varnames=%r\n" % (c.co_name, c.co_names, [x for x in c.co_consts if not hasattr(x, "co_names")], c.co_varnames))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
