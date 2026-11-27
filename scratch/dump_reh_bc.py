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
        f.write("_realEnterHall code len: %d\n" % len(reh_code.co_code))
        # Let's inspect co_names and co_consts
        f.write("names: %r\n" % (reh_code.co_names,))
        f.write("consts: %r\n" % (reh_code.co_consts,))
        # Let's dump opcode offsets and names/consts referenced
        # In Python 2.7: op >= 90 has 2-byte argument
        i = 0
        bc = reh_code.co_code
        while i < len(bc):
            op = ord(bc[i])
            arg = None
            if op >= 90:
                arg = ord(bc[i+1]) | (ord(bc[i+2]) << 8)
                f.write("%4d: op=%3d arg=%5d" % (i, op, arg))
                # If arg matches name index
                if arg < len(reh_code.co_names):
                    f.write(" (name: %s)" % reh_code.co_names[arg])
                if arg < len(reh_code.co_consts):
                    f.write(" (const: %r)" % (reh_code.co_consts[arg],))
                f.write("\n")
                i += 3
            else:
                f.write("%4d: op=%3d\n" % (i, op))
                i += 1
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
