f = open(OUT, "w")
try:
    import Athlete
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem") if scene else None
    
    lhs = ss.loadHallScene
    f.write("loadHallScene: %r\n" % (lhs,))
    code = lhs.im_func.func_code
    f.write("names: %r\n" % (code.co_names,))
    f.write("consts: %r\n" % (code.co_consts,))
    f.write("varnames: %r\n" % (code.co_varnames,))
    
    bc = code.co_code
    f.write("len(bc) = %d\n" % len(bc))
    i = 0
    while i < len(bc):
        op = ord(bc[i])
        arg = None
        if op >= 90:
            arg = ord(bc[i+1]) | (ord(bc[i+2]) << 8)
            n = code.co_names[arg] if arg < len(code.co_names) else ""
            c = repr(code.co_consts[arg]) if arg < len(code.co_consts) else ""
            v = code.co_varnames[arg] if arg < len(code.co_varnames) else ""
            f.write("%4d: op=%3d arg=%5d  n=%s  c=%s  v=%s\n" % (i, op, arg, n, c, v))
            i += 3
        else:
            f.write("%4d: op=%3d\n" % (i, op))
            i += 1
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
