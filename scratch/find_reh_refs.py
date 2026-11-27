OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import sys, types
    needle = 'rookieEnterHall'
    f.write("Searching for %s...\n" % needle)
    
    for mname, mod in sorted(sys.modules.items()):
        if not mod: continue
        for k, v in list(vars(mod).items()):
            co = getattr(getattr(v, 'im_func', v), 'func_code', None)
            if isinstance(co, types.CodeType):
                if needle in co.co_names:
                    f.write("Found in %s.%s (file %s)\n" % (mname, k, co.co_filename))
            elif isinstance(v, (type, types.ClassType)):
                for ck, cv in list(v.__dict__.items()):
                    co = getattr(getattr(cv, 'im_func', cv), 'func_code', None)
                    if isinstance(co, types.CodeType):
                        if needle in co.co_names:
                            f.write("Found in class %s.%s.%s (file %s)\n" % (mname, k, ck, co.co_filename))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
