import Athlete
import traceback

with open(OUT, "w") as f:
    try:
        cls = Athlete.PlayerAthlete
        for name in dir(cls):
            if "hall" in name.lower() or "enter" in name.lower():
                fn = getattr(cls, name)
                if hasattr(fn, "func_code"):
                    f.write("Method: %s\n  varnames: %r\n  names: %r\n" % (name, fn.func_code.co_varnames, fn.func_code.co_names))
    except Exception:
        f.write(traceback.format_exc())
