f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall.im_func
    inner_fn = fn.func_closure[0].cell_contents
    code = inner_fn.func_code
    reh_code = None
    for c in code.co_consts:
        if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
            reh_code = c
            break
            
    if reh_code:
        bc = reh_code.co_code
        i = 400
        while i < 750 and i < len(bc):
            op = ord(bc[i])
            arg = None
            if op >= 90:
                arg = ord(bc[i+1]) | (ord(bc[i+2]) << 8)
                n = reh_code.co_names[arg] if arg < len(reh_code.co_names) else ""
                c = repr(reh_code.co_consts[arg]) if arg < len(reh_code.co_consts) else ""
                v = reh_code.co_varnames[arg] if arg < len(reh_code.co_varnames) else ""
                f.write("%4d: op=%3d arg=%5d  n=%s  c=%s  v=%s\n" % (i, op, arg, n, c, v))
                i += 3
            else:
                f.write("%4d: op=%3d\n" % (i, op))
                i += 1
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
