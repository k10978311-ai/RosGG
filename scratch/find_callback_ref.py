f = open(OUT, "w")
try:
    import Athlete
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem")
    pfn = ss.__class__.__dict__.get("_preloadLevelResCoro")
    co = pfn.func_code
    
    # Check if 'callback' is in co_varnames
    f.write("co_varnames: %r\n" % (co.co_varnames,))
    cb_idx = co.co_varnames.index("callback")
    f.write("callback index: %d\n" % cb_idx)
    
    # Find all references to callback in bytecode
    code = bytearray(co.co_code)
    for i in range(len(code)):
        if code[i] in (124, 125): # LOAD_FAST, STORE_FAST
            arg = code[i+1] | (code[i+2] << 8)
            if arg == cb_idx:
                f.write("offset %d: op=%d (callback)\n" % (i, code[i]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
