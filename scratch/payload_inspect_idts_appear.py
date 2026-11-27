import iDtsAppearancePackage
import traceback

with open(OUT, "w") as f:
    try:
        cls = iDtsAppearancePackage.iDtsAppearancePackage
        f.write("iDtsAppearancePackage dir:\n%r\n" % dir(cls))
        for m in dir(cls):
            if any(k in m.lower() for k in ["init", "clear", "login", "appear", "item"]):
                fn = getattr(cls, m)
                if hasattr(fn, "func_code"):
                    f.write("Method %s: args=%r, consts=%r, names=%r\n" % (
                        m, fn.func_code.co_varnames, fn.func_code.co_consts, fn.func_code.co_names
                    ))
    except Exception:
        f.write(traceback.format_exc())
