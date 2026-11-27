with open(OUT, 'w') as f:
    import types
    # find code object onHallSceneReady from scratch/disas_real_enterhall.py logic
    import Athlete
    fn = Athlete.PlayerAthlete.__dict__.get("_realEnterHall")
    def inner(fn):
        for cell in (getattr(fn, "func_closure", None) or ()):
            try: v = cell.cell_contents
            except ValueError: continue
            if isinstance(v, types.FunctionType): return inner(v)
        return fn
    real_fn = inner(fn)
    co = real_fn.func_code
    for c in co.co_consts:
        if hasattr(c, 'co_name') and c.co_name == 'onHallSceneReady':
            f.write("names: %r\n" % (c.co_names,))
            f.write("consts: %r\n" % ([x for x in c.co_consts if not hasattr(x, 'co_names')],))
            f.write("varnames: %r\n" % (c.co_varnames,))
            # disassemble
            code = bytearray(c.co_code)
            i = 0
            while i < len(code):
                offset = i
                op = code[i]
                i += 1
                arg_str = ''
                if op >= 90:
                    arg = code[i] | (code[i+1] << 8)
                    i += 2
                    arg_str = str(arg)
                    if arg < len(c.co_names): arg_str += ' (n: ' + str(c.co_names[arg]) + ')'
                    if arg < len(c.co_consts): arg_str += ' (c: ' + repr(c.co_consts[arg]) + ')'
                    if arg < len(c.co_varnames): arg_str += ' (v: ' + str(c.co_varnames[arg]) + ')'
                f.write('%4d: op=%3d %s\n' % (offset, op, arg_str))
