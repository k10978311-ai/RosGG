with open(OUT, 'w') as f:
    try:
        import Athlete
        raw = Athlete.PlayerAthlete.__dict__['enterHall']
        f.write('raw: ' + repr(raw) + '\n')
        f.write('type: ' + str(type(raw)) + '\n')
        f.write('dict: ' + repr(getattr(raw, '__dict__', None)) + '\n')
        co = getattr(raw, 'func_code', None)
        if co:
            f.write('co_varnames: ' + repr(co.co_varnames) + '\n')
            f.write('co_argcount: ' + str(co.co_argcount) + '\n')
            f.write('co_flags: ' + hex(co.co_flags) + '\n')
            f.write('co_names: ' + repr(co.co_names) + '\n')
            f.write('co_consts: ' + repr(co.co_consts) + '\n')
            # Check closures
            f.write('func_closure: ' + repr(getattr(raw, 'func_closure', None)) + '\n')
            if getattr(raw, 'func_closure', None):
                for i, c in enumerate(raw.func_closure):
                    f.write('  cell ' + str(i) + ': ' + repr(c.cell_contents) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
