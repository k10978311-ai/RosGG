import Athlete
import traceback

with open(OUT, "w") as f:
    try:
        fn = Athlete.PlayerAthlete.enterHall
        closure = getattr(fn, "func_closure", None)
        orig_fn = closure[0].cell_contents
        code = orig_fn.func_code
        f.write("orig_fn code:\n")
        f.write("  name: %r\n" % code.co_name)
        f.write("  varnames: %r\n" % (code.co_varnames,))
        f.write("  consts: %r\n" % (code.co_consts,))
        f.write("  names: %r\n" % (code.co_names,))
    except Exception:
        f.write(traceback.format_exc())
