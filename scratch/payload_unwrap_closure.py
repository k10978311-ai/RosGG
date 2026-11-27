import Athlete
import traceback

with open(OUT, "w") as f:
    try:
        fn = Athlete.PlayerAthlete.enterHall
        f.write("fn: %r\n" % fn)
        closure = getattr(fn, "func_closure", None)
        f.write("closure: %r\n" % (closure,))
        if closure:
            for i, c in enumerate(closure):
                f.write("  cell %d: %r\n" % (i, c.cell_contents))
                if hasattr(c.cell_contents, "func_code"):
                    cfn = c.cell_contents
                    f.write("    code: %r, consts: %r, names: %r\n" % (cfn.func_code.co_varnames, cfn.func_code.co_consts, cfn.func_code.co_names))
    except Exception:
        f.write(traceback.format_exc())
