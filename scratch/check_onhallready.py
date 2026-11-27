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
    for c in co.co_consts:
        if hasattr(c, "co_names") and c.co_name == "_realEnterHall":
            f.write("_realEnterHall found!\n")
            for c2 in c.co_consts:
                if hasattr(c2, "co_names"):
                    f.write("nested in _realEnterHall: %s names=%r consts=%r\n" % (c2.co_name, c2.co_names, [x for x in c2.co_consts if not hasattr(x, "co_names")]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
