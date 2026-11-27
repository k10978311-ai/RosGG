with open(OUT, 'w') as f:
    try:
        import Athlete
        for c in Athlete.PlayerAthlete.__mro__:
            if 'enterHall' in c.__dict__:
                fn = c.__dict__['enterHall']
                co = fn.im_func.func_code if hasattr(fn, 'im_func') else getattr(fn, 'func_code', None)
                if co:
                    f.write(c.__name__ + '.enterHall args=' + repr(co.co_varnames[:co.co_argcount]) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
