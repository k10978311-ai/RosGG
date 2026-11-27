with open(OUT, 'w') as f:
    try:
        import Athlete
        raw = Athlete.PlayerAthlete.__dict__['enterHall']
        inner = raw.func_closure[0].cell_contents
        co = inner.func_code
        reh_code = None
        for c in co.co_consts:
            if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
                reh_code = c
                break
        code = bytearray(reh_code.co_code)
        names = reh_code.co_names
        consts = reh_code.co_consts
        varnames = reh_code.co_varnames
        
        i, n = 0, len(code)
        while i < n:
            offset = i
            op = code[i]
            i += 1
            arg_str = ''
            if op >= 90:
                arg = code[i] | (code[i+1] << 8)
                i += 2
                arg_str = str(arg)
                if arg < len(names): arg_str += ' (n: ' + str(names[arg]) + ')'
                if arg < len(consts): arg_str += ' (c: ' + repr(consts[arg]) + ')'
                if arg < len(varnames): arg_str += ' (v: ' + str(varnames[arg]) + ')'
            f.write('%4d: op=%3d %s\n' % (offset, op, arg_str))
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
