OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall
    real_fn = fn.func_closure[0].cell_contents
    co = real_fn.func_code
    for c in co.co_consts:
        if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
            reh_co = c
            break
            
    code = bytearray(reh_co.co_code)
    names = reh_co.co_names
    varnames = reh_co.co_varnames
    f.write("varnames: %r\n" % (varnames,))
    
    i = 0
    while i < len(code):
        offset = i
        op = code[i]
        i += 1
        if op >= 90:
            arg = code[i] | (code[i+1] << 8)
            i += 2
            # Check if arg references varname 6 (GameInit)
            if arg == 6 or (arg < len(names) and 'GameInit' in names[arg]):
                f.write("offset %4d: op=%d arg=%d\n" % (offset, op, arg))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
