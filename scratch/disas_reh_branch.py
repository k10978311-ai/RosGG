with open(OUT, 'w') as f:
    try:
        import Athlete
        fn = Athlete.PlayerAthlete.enterHall
        real_fn = fn.func_closure[0].cell_contents
        reh = None
        for c in real_fn.func_code.co_consts:
            if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
                reh = c
                break
        code = bytearray(reh.co_code)
        names = reh.co_names
        consts = reh.co_consts
        varnames = reh.co_varnames
        
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
                if arg < len(names):
                    arg_str += ' (n: ' + str(names[arg]) + ')'
                if arg < len(consts):
                    c = consts[arg]
                    arg_str += ' (c: ' + (c.co_name if hasattr(c, 'co_name') else repr(c)) + ')'
                if arg < len(varnames):
                    arg_str += ' (v: ' + str(varnames[arg]) + ')'
            if 130 <= offset <= 260:
                f.write('%4d: op=%3d %s\n' % (offset, op, arg_str))
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
