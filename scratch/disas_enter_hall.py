OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete, dis
    fn = Athlete.PlayerAthlete.enterHall
    real_fn = fn.func_closure[0].cell_contents
    f.write("real_fn: %r\n" % real_fn)
    co = real_fn.func_code
    f.write("co_names: %r\n" % (co.co_names,))
    f.write("co_consts: %r\n" % (co.co_consts,))
    f.write("co_varnames: %r\n" % (co.co_varnames,))
    if hasattr(real_fn, 'func_closure') and real_fn.func_closure:
        for idx, cell in enumerate(real_fn.func_closure):
            f.write("  inner closure[%d]: %r\n" % (idx, cell.cell_contents))
    
    # Also disassemble instructions!
    import sys
    # Write dis to file
    old_stdout = sys.stdout
    sys.stdout = f
    dis.dis(co)
    sys.stdout = old_stdout
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
