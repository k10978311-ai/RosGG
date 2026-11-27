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
            # 120 = SETUP_LOOP, 121 = SETUP_EXCEPT, 122 = SETUP_FINALLY, 123 = SETUP_WITH
            if op in (120, 121, 122, 123):
                f.write("SETUP op=%d at offset %d -> delta %d (target %d)\n" % (op, offset, arg, offset + 3 + arg))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
