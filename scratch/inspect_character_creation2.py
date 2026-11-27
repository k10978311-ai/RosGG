f = open(OUT, "w")
try:
    import Athlete, dis, StringIO, sys, types
    pa = Athlete.PlayerAthlete
    
    def unwrap(fn):
        for cell in (getattr(fn, "func_closure", None) or ()):
            try: v = cell.cell_contents
            except ValueError: continue
            if isinstance(v, types.FunctionType):
                return unwrap(v)
        return fn

    for name in ["onBecomePlayer", "showSelectCharacter", "onCreateCharacter", "onRoleCreateSuc"]:
        fn = pa.__dict__.get(name)
        real = unwrap(fn)
        co = real.func_code
        f.write("=== %s (names=%r, consts=%r) ===\n" % (
            name, co.co_names, [c for c in co.co_consts if not hasattr(c, "co_names")]))
        for c in co.co_consts:
            if hasattr(c, "co_names"):
                f.write("  nested %s: names=%r, consts=%r\n" % (
                    c.co_name, c.co_names, [x for x in c.co_consts if not hasattr(x, "co_names")]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
