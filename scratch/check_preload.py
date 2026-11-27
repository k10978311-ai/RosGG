import sys
f = open(OUT, "w")
try:
    SS = sys.modules["libclaudia.Classes.SceneSystem"].SceneSystem
    for k, v in vars(SS).items():
        if "preload" in k.lower():
            f.write("Found %s: %r\n" % (k, v))
            if hasattr(v, "func_code"):
                f.write("names=%r\n" % (list(v.func_code.co_names),))
                f.write("consts=%r\n" % ([c for c in v.func_code.co_consts if not hasattr(c, "co_names")],))
                for c in v.func_code.co_consts:
                    if hasattr(c, "co_names"):
                        f.write("  inner %s: names=%r consts=%r\n" % (c.co_name, list(c.co_names), [x for x in c.co_consts if not hasattr(x, "co_names")]))
except Exception as e:
    import traceback
    f.write(traceback.format_exc())
f.close()
