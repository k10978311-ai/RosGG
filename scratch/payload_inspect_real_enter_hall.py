import Athlete
import traceback

with open(OUT, "w") as f:
    try:
        fn = Athlete.PlayerAthlete.enterHall
        closure = getattr(fn, "func_closure", None)
        orig_fn = closure[0].cell_contents
        for c in orig_fn.func_code.co_consts:
            if hasattr(c, "co_name") and c.co_name == "_realEnterHall":
                f.write("_realEnterHall code:\n")
                f.write("  varnames: %r\n" % (c.co_varnames,))
                f.write("  consts: %r\n" % (c.co_consts,))
                f.write("  names: %r\n" % (c.co_names,))
    except Exception:
        f.write(traceback.format_exc())
