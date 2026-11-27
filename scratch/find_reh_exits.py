OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall
    real_fn = fn.func_closure[0].cell_contents
    co = real_fn.func_code
    
    reh_code = None
    for c in co.co_consts:
        if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
            reh_code = c
            break
            
    code = bytearray(reh_code.co_code)
    i = 0
    n = len(code)
    while i < n:
        offset = i
        op = code[i]
        i += 1
        if op >= 90:
            arg = code[i] | (code[i+1] << 8)
            i += 2
            if op in (110, 111, 112, 113, 114, 120, 121, 122, 148, 132, 133):
                if arg > 749 or arg == 1007:
                    f.write("JUMP at offset %d (op %d) -> target %d\n" % (offset, op, arg))
        elif op == 94: # RETURN_VALUE
            f.write("RETURN at offset %d\n" % offset)

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
