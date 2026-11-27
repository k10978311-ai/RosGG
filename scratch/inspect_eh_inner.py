with open(OUT, 'w') as f:
    try:
        import Athlete
        raw = Athlete.PlayerAthlete.__dict__['enterHall']
        inner = raw.func_closure[0].cell_contents
        f.write('inner: ' + repr(inner) + '\n')
        co = inner.func_code
        f.write('co_varnames: ' + repr(co.co_varnames) + '\n')
        f.write('co_argcount: ' + str(co.co_argcount) + '\n')
        f.write('co_names: ' + repr(co.co_names) + '\n')
        f.write('co_consts: ' + repr(co.co_consts) + '\n')
        f.write('func_closure: ' + repr(getattr(inner, 'func_closure', None)) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
