f = open(OUT, "w")
try:
    import Athlete, types
    fn = Athlete.PlayerAthlete.enterHall
    if hasattr(fn, "im_func"): fn = fn.im_func
    def get_code(f):
        for c in (getattr(f, "func_closure", None) or []):
            try: v = c.cell_contents
            except ValueError: continue
            if isinstance(v, types.FunctionType): return get_code(v)
        return f
    real = get_code(fn)
    co = real.func_code
    for c in co.co_consts:
        if hasattr(c, "co_names") and c.co_name == "_realEnterHall":
            code = bytearray(c.co_code)
            f.write("_realEnterHall bytecode (%d bytes):\n" % len(code))
            f.write("names: %r\n" % (c.co_names,))
            f.write("consts: %r\n" % ([x if not hasattr(x, "co_names") else "<code %s>" % x.co_name for x in c.co_consts],))
            f.write("varnames: %r\n" % (c.co_varnames,))
            i = 0
            while i < len(code):
                off = i
                op = code[i]
                i += 1
                arg = ""
                if op >= 90:
                    arg_int = code[i] | (code[i+1] << 8)
                    i += 2
                    arg = str(arg_int)
                f.write("%4d: %3d %s\n" % (off, op, arg))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
