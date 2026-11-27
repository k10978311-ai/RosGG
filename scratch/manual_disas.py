f = open(OUT, "w")
try:
    import Athlete
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem")
    pfn = ss.__class__.__dict__.get("_preloadLevelResCoro")
    co = pfn.func_code
    
    # Custom opcode decoder for Python 2.7
    import dis
    opname = list(dis.opname)
    
    code = bytearray(co.co_code)
    i = 0
    n = len(code)
    lines = []
    while i < n:
        offset = i
        op = code[i]
        i += 1
        name = opname[op] if op < len(opname) else "OP_%d" % op
        arg_val = ""
        if op >= dis.HAVE_ARGUMENT:
            if i + 1 < n:
                arg = code[i] | (code[i+1] << 8)
                i += 2
                arg_val = str(arg)
                if op in dis.hasname:
                    arg_val += " (" + co.co_names[arg] + ")"
                elif op in dis.haslocal:
                    arg_val += " (" + co.co_varnames[arg] + ")"
                elif op in dis.hasconst:
                    c = co.co_consts[arg]
                    arg_val += " (" + (c.co_name if hasattr(c, "co_name") else repr(c)) + ")"
        lines.append("%4d %-20s %s" % (offset, name, arg_val))
    f.write("\n".join(lines[:120]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
