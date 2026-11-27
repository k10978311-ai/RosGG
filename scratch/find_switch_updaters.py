OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import sys, types
    needle = 'URGENT_SWITCH_ENABLE_FORCE_UPGRADE'
    f.write("Searching for %s...\n" % needle)
    
    def check_fn(fn, name):
        co = getattr(fn, 'func_code', None)
        if not isinstance(co, types.CodeType): return
        if needle in co.co_names or needle in [str(c) for c in co.co_consts]:
            f.write("Found in %s (file %s)\n" % (name, co.co_filename))
        for c in co.co_consts:
            if isinstance(c, types.CodeType):
                if needle in c.co_names or needle in [str(x) for x in c.co_consts]:
                    f.write("Found in sub %s.%s (file %s)\n" % (name, c.co_name, c.co_filename))

    for mname, mod in sorted(sys.modules.items()):
        if not mod: continue
        for k, v in list(vars(mod).items()):
            if hasattr(v, 'func_code') or hasattr(v, 'im_func'):
                check_fn(getattr(v, 'im_func', v), "%s.%s" % (mname, k))
            elif isinstance(v, (type, types.ClassType)):
                for ck, cv in list(v.__dict__.items()):
                    if hasattr(cv, 'func_code') or hasattr(cv, 'im_func'):
                        check_fn(getattr(cv, 'im_func', cv), "%s.%s.%s" % (mname, k, ck))
                            
    # Also check how switches are updated from server RPCs
    # Look for any method containing 'switch' or 'config' on PlayerAthlete
    import Athlete
    for k in sorted(dir(Athlete.PlayerAthlete)):
        kl = k.lower()
        if 'switch' in kl or 'gm' in kl or 'config' in kl or 'table' in kl:
            f.write("PlayerAthlete candidate method: %s\n" % k)

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
