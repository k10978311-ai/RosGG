OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall
    real_fn = fn.func_closure[0].cell_contents
    co = real_fn.func_code
    
    real_enter_hall_co = None
    for c in co.co_consts:
        if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
            real_enter_hall_co = c
            break
            
    f.write("_realEnterHall code len: %d\n" % len(real_enter_hall_co.co_code))
    f.write("_realEnterHall names: %r\n" % (real_enter_hall_co.co_names,))
    f.write("_realEnterHall consts: %r\n" % [c if not hasattr(c, 'co_name') else c.co_name for c in real_enter_hall_co.co_consts])
    f.write("_realEnterHall varnames: %r\n" % (real_enter_hall_co.co_varnames,))

    # Print bytecode bytes
    f.write("\nraw bytecode:\n")
    code = real_enter_hall_co.co_code
    i = 0
    while i < len(code):
        b = ord(code[i])
        f.write("%3d: byte=%02x (%d)\n" % (i, b, b))
        i += 1
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
