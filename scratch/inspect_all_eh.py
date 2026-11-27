with open(OUT, 'w') as f:
    try:
        import Athlete
        for c in Athlete.PlayerAthlete.__mro__:
            if 'enterHall' in c.__dict__:
                fn = c.__dict__['enterHall']
                f.write('=== ' + c.__name__ + '.enterHall ===\n')
                f.write('repr: ' + repr(fn) + '\n')
                co = fn.im_func.func_code if hasattr(fn, 'im_func') else getattr(fn, 'func_code', None)
                if co:
                    f.write('  varnames: ' + repr(co.co_varnames) + '\n')
                    f.write('  names: ' + repr(co.co_names) + '\n')
                    f.write('  consts: ' + repr(co.co_consts) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
