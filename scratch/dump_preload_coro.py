f = open(OUT, "w")
try:
    import Athlete, dis
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem")
    pfn = ss.__class__.__dict__.get("_preloadLevelResCoro")
    co = pfn.func_code
    
    code = bytearray(co.co_code)
    i = 0
    n = len(code)
    while i < n:
        offset = i
        op = code[i]
        i += 1
        name = dis.opname[op] if op < len(dis.opname) else "OP_%d" % op
        arg_val = ""
        if op >= dis.HAVE_ARGUMENT:
            if i + 1 < n:
                arg = code[i] | (code[i+1] << 8)
                i += 2
                arg_val = str(arg)
                if op in dis.hasname and arg < len(co.co_names):
                    arg_val += " (" + co.co_names[arg] + ")"
                elif op in dis.haslocal and arg < len(co.co_varnames):
                    arg_val += " (" + co.co_varnames[arg] + ")"
                elif op in dis.hasconst and arg < len(co.co_consts):
                    c = co.co_consts[arg]
                    arg_val += " (" + (c.co_name if hasattr(c, "co_name") else repr(c)) + ")"
        f.write("%4d %-20s %s\n" % (offset, name, arg_val))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
