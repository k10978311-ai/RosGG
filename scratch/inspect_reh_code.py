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
        f.write('reh_code: ' + repr(reh_code) + '\n')
        if reh_code:
            f.write('  varnames: ' + repr(reh_code.co_varnames) + '\n')
            f.write('  names: ' + repr(reh_code.co_names) + '\n')
            f.write('  consts: ' + repr(reh_code.co_consts) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
