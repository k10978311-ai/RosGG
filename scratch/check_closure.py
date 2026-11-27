f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall.im_func
    f.write("fn: %r\n" % (fn,))
    f.write("closure: %r\n" % (fn.func_closure,))
    if fn.func_closure:
        for idx, c in enumerate(fn.func_closure):
            f.write("cell %d: %r\n" % (idx, c.cell_contents))
            if hasattr(c.cell_contents, 'func_code'):
                subco = c.cell_contents.func_code
                f.write("  sub func names: %r\n" % (subco.co_names,))
                f.write("  sub func consts: %r\n" % (subco.co_consts,))
                f.write("  sub func closure: %r\n" % (c.cell_contents.func_closure,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
