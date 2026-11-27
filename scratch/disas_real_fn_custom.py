with open(OUT, 'w') as f:
    try:
        import Athlete
        fn = Athlete.PlayerAthlete.enterHall
        real_fn = fn.func_closure[0].cell_contents
        co = real_fn.func_code
        code = bytearray(co.co_code)
        names = co.co_names
        consts = co.co_consts
        varnames = co.co_varnames
        
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
                    arg_str += ' (name: ' + str(names[arg]) + ')'
                if arg < len(consts):
                    c = consts[arg]
                    arg_str += ' (const: ' + (c.co_name if hasattr(c, 'co_name') else repr(c)) + ')'
                if arg < len(varnames):
                    arg_str += ' (var: ' + str(varnames[arg]) + ')'
            f.write('%4d: op=%3d %s\n' % (offset, op, arg_str))
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
