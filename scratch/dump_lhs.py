OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import libclaudia.Classes.SceneSystem as sc
    fn = sc.SceneSystem.loadHallScene
    f.write("loadHallScene: %r\n" % (fn,))
    co = fn.im_func.func_code if hasattr(fn, 'im_func') else fn.func_code
    f.write("co_names: %r\n" % (co.co_names,))
    f.write("co_consts: %r\n" % [c for c in co.co_consts if not hasattr(c, 'co_names')])
    f.write("co_varnames: %r\n" % (co.co_varnames,))
    
    # check instructions
    bc = bytearray(co.co_code)
    for i in range(0, len(bc), 3 if bc[0] >= 90 else 1):
        op = bc[i]
        arg = (bc[i+1] | (bc[i+2] << 8)) if (op >= 90 and i+2 < len(bc)) else 0
        arg_str = ""
        if op in (100, 101, 106, 108):
            arg_str = repr(co.co_names[arg]) if arg < len(co.co_names) else str(arg)
        elif op == 100:
            arg_str = repr(co.co_consts[arg]) if arg < len(co.co_consts) else str(arg)
        elif op in (124, 125):
            arg_str = repr(co.co_varnames[arg]) if arg < len(co.co_varnames) else str(arg)
        f.write("%4d: op=%3d (%d) %s\n" % (i, op, arg, arg_str))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
