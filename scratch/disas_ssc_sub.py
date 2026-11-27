with open(OUT, 'w') as f:
    try:
        import Athlete
        raw = Athlete.PlayerAthlete.__dict__['showSelectCharacter']
        inner = raw.func_closure[0].cell_contents if getattr(raw, 'func_closure', None) else raw
        co = inner.func_code if hasattr(inner, 'func_code') else getattr(inner, '__code__', None)
        for c in co.co_consts:
            if hasattr(c, 'co_name'):
                f.write('=== Code ' + c.co_name + ' ===\n')
                f.write('names: ' + repr(c.co_names) + '\n')
                f.write('consts: ' + repr(c.co_consts) + '\n')
                f.write('varnames: ' + repr(c.co_varnames) + '\n')
                cb = bytearray(c.co_code)
                for i, b in enumerate(cb):
                    f.write('%d ' % b)
                f.write('\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
