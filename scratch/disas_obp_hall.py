with open(OUT, 'w') as f:
    try:
        import Athlete
        raw = Athlete.PlayerAthlete.__dict__['onBecomePlayer']
        inner = raw.func_closure[0].cell_contents if getattr(raw, 'func_closure', None) else raw
        co = inner.func_code if hasattr(inner, 'func_code') else inner.__code__
        
        code = bytearray(co.co_code)
        names = co.co_names
        consts = co.co_consts
        varnames = co.co_varnames
        
        # Look for index of hallScene in names
        hall_idx = names.index('hallScene') if 'hallScene' in names else -1
        f.write('hallScene index in names: ' + str(hall_idx) + '\n')
        
        # Disassemble around where hallScene is referenced
        i, n = 0, len(code)
        while i < n:
            offset = i
            op = code[i]
            i += 1
            arg = None
            if op >= 90:
                arg = code[i] | (code[i+1] << 8)
                i += 2
            # Check if this instruction references hallScene or LoadLevelAtFinish
            # op 96 is LOAD_ATTR, 155 is LOAD_GLOBAL, etc.
            f.write('%4d: op=%3d arg=%r\n' % (offset, op, arg))
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
