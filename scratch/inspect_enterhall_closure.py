import types
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall
    f.write("fn: %r\n" % (fn,))
    f.write("closure: %r\n" % ([getattr(c, "cell_contents", None) for c in (fn.func_closure or [])],))
    
    # Unwrap closure to find all inner functions
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
    f.write("all inners: %r\n" % (inners,))
    for i, infn in enumerate(inners):
        f.write("\n--- inner %d: %s ---\n" % (i, infn.func_name))
        co = infn.func_code
        f.write("names: %r\n" % (co.co_names,))
        f.write("varnames: %r\n" % (co.co_varnames,))
        f.write("consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, "co_names")],))
        for c in co.co_consts:
            if hasattr(c, "co_names"):
                f.write("  subcode %s: names=%r varnames=%r\n" % (c.co_name, c.co_names, c.co_varnames))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
