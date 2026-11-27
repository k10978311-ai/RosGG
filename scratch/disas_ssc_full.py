with open(OUT, 'w') as f:
    try:
        import Athlete
        raw = Athlete.PlayerAthlete.__dict__['showSelectCharacter']
        inner = raw.func_closure[0].cell_contents if getattr(raw, 'func_closure', None) else raw
        co = inner.func_code if hasattr(inner, 'func_code') else getattr(inner, '__code__', None)
        f.write('showSelectCharacter co_names: ' + repr(co.co_names) + '\n')
        f.write('showSelectCharacter co_consts: ' + repr(co.co_consts) + '\n')
        f.write('showSelectCharacter co_varnames: ' + repr(co.co_varnames) + '\n')
        
        # Disassemble byte by byte
        cb = bytearray(co.co_code)
        i, n = 0, len(cb)
        while i < n:
            offset = i
            op = cb[i]
            i += 1
            arg_str = ''
            if op >= 90:
                arg = cb[i] | (cb[i+1] << 8)
                i += 2
                arg_str = str(arg)
                if arg < len(co.co_names): arg_str += ' (n: ' + str(co.co_names[arg]) + ')'
                if arg < len(co.co_consts): arg_str += ' (c: ' + repr(co.co_consts[arg]) + ')'
                if arg < len(co.co_varnames): arg_str += ' (v: ' + str(co.co_varnames[arg]) + ')'
            f.write('%4d: op=%3d %s\n' % (offset, op, arg_str))
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
