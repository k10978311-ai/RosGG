OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall
    real_fn = fn.func_closure[0].cell_contents
    co = real_fn.func_code
    
    # Find _realEnterHall code object in co_consts
    real_enter_hall_co = None
    for c in co.co_consts:
        if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
            real_enter_hall_co = c
            break
            
    f.write("enterHall code len: %d\n" % len(co.co_code))
    f.write("enterHall names: %r\n" % (co.co_names,))
    f.write("enterHall consts: %r\n" % [c if not hasattr(c, 'co_name') else c.co_name for c in co.co_consts])
    
    if real_enter_hall_co:
        f.write("\n_realEnterHall names: %r\n" % (real_enter_hall_co.co_names,))
        f.write("_realEnterHall consts: %r\n" % [c if not hasattr(c, 'co_name') else c.co_name for c in real_enter_hall_co.co_consts])
        f.write("_realEnterHall varnames: %r\n" % (real_enter_hall_co.co_varnames,))

    # Print bytecode bytes
    f.write("\nraw bytecode:\n")
    code = co.co_code
    i = 0
    while i < len(code):
        b = ord(code[i])
        f.write("%3d: byte=%02x (%d)\n" % (i, b, b))
        i += 1
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
