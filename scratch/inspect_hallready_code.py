import types
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall
    def get_inners(f_obj):
        res = []
        for c in (getattr(f_obj, "func_closure", None) or []):
            try: v = c.cell_contents
            except ValueError: continue
            if isinstance(v, types.FunctionType):
                res.append(v)
                res.extend(get_inners(v))
        return res
    
    inners = get_inners(fn)
    real_enter = inners[0]
    for c in real_enter.func_code.co_consts:
        if hasattr(c, "co_names") and c.co_name == "_realEnterHall":
            f.write("_realEnterHall subcodes:\n")
            for sub in c.co_consts:
                if hasattr(sub, "co_names"):
                    f.write("  sub: %s: names=%r consts=%r\n" % (sub.co_name, sub.co_names, [x for x in sub.co_consts if not hasattr(x, "co_names")]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
