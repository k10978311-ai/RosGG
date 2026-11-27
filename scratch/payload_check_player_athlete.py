import Athlete
import traceback

with open(OUT, "w") as f:
    try:
        cls = Athlete.PlayerAthlete
        f.write("PlayerAthlete mro: %r\n" % (cls.__mro__,))
        for m in ["enterHall", "_realEnterHall", "onLogin", "onBecomePlayer", "_onEnterWorld"]:
            if hasattr(cls, m):
                fn = getattr(cls, m)
                code = getattr(fn, "func_code", None)
                f.write("\n--- %s ---\n" % m)
                f.write("args: %r\nconsts: %r\nnames: %r\n" % (
                    code.co_varnames if code else None,
                    code.co_consts if code else None,
                    code.co_names if code else None
                ))
    except Exception:
        f.write(traceback.format_exc())
