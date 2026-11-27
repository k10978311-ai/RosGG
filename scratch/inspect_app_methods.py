f = open(OUT, "w")
try:
    import libclaudia.Classes.Application as app
    p_fn = getattr(app, "PreloadLevel", None)
    l_fn = getattr(app, "LoadLevelAtFinish", None)
    f.write("PreloadLevel: %r\n" % (p_fn,))
    f.write("LoadLevelAtFinish: %r\n" % (l_fn,))
    if hasattr(p_fn, "func_code"):
        co = p_fn.func_code
        f.write("PreloadLevel co_names: %r, consts: %r, varnames: %r\n" % (co.co_names, [c for c in co.co_consts if not hasattr(c, "co_names")], co.co_varnames))
    if hasattr(l_fn, "func_code"):
        co = l_fn.func_code
        f.write("LoadLevelAtFinish co_names: %r, consts: %r, varnames: %r\n" % (co.co_names, [c for c in co.co_consts if not hasattr(c, "co_names")], co.co_varnames))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
