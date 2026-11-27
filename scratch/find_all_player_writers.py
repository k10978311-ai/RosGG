import sys, types
f = open(OUT, "w")
try:
    NEEDLES = ('player',)
    seen = set()
    def scan_co(co, path):
        if id(co) in seen: return
        seen.add(id(co))
        names = co.co_names
        consts = co.co_consts
        if 'player' in names and 'Globals' in names:
            # Check if it writes to player
            f.write("Candidate: %s\n" % path)
        for c in consts:
            if hasattr(c, 'co_names'):
                scan_co(c, path + '.' + c.co_name)
    for mname, mod in sorted(sys.modules.items()):
        if mod is None: continue
        try:
            for k, v in list(vars(mod).items()):
                if hasattr(v, 'func_code'):
                    scan_co(v.func_code, mname + ':' + k)
                elif isinstance(v, (type, types.ClassType)):
                    for k2, v2 in list(v.__dict__.items()):
                        if hasattr(v2, 'func_code'):
                            scan_co(v2.func_code, mname + ':' + k + '.' + k2)
        except Exception:
            pass
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
