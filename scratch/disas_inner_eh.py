with open(OUT, 'w') as f:
    try:
        import Athlete
        raw = Athlete.PlayerAthlete.__dict__['enterHall']
        inner = raw.func_closure[0].cell_contents
        co = inner.func_code
        
        # Simple opcode walker for Python 2.7
        # Python 2.7 opcodes:
        # HAVE_ARGUMENT = 90
        code_bytes = bytearray(co.co_code)
        i = 0
        n = len(code_bytes)
        names = co.co_names
        consts = co.co_consts
        varnames = co.co_varnames
        
        while i < n:
            offset = i
            op = code_bytes[i]
            i += 1
            arg_str = ''
            if op >= 90:
                arg = code_bytes[i] | (code_bytes[i+1] << 8)
                i += 2
                arg_str = str(arg)
                # op 100 is LOAD_CONST, 101 STORE_NAME, 106 LOAD_ATTR, 116 LOAD_GLOBAL, 124 LOAD_FAST, etc.
                if op == 100 and arg < len(consts): arg_str += ' (c: ' + repr(consts[arg]) + ')'
                elif op in (106, 108, 116) and arg < len(names): arg_str += ' (n: ' + str(names[arg]) + ')'
                elif op in (124, 125) and arg < len(varnames): arg_str += ' (v: ' + str(varnames[arg]) + ')'
            f.write('%4d: op=%3d %s\n' % (offset, op, arg_str))
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
