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
    consts = reh_co.co_consts
    
    i = 370
    while i < 440:
        offset = i
        op = code[i]
        i += 1
        arg_val = ""
        if op >= 90:
            arg = code[i] | (code[i+1] << 8)
            i += 2
            arg_val = str(arg)
            if op in (101, 116, 96, 155, 156):
                if arg < len(names): arg_val += " (name: %s)" % names[arg]
            elif op == 100 or op in (124, 125):
                if arg < len(consts):
                    c = consts[arg]
                    arg_val += " (const: %r)" % (c.co_name if hasattr(c, 'co_name') else c)
            elif op in (110, 111, 112, 113, 114, 120, 121, 122, 148):
                arg_val += " -> %d" % arg
        f.write("%4d: op=%d %s\n" % (offset, op, arg_val))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
