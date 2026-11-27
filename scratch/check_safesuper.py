with open(OUT, 'w') as f:
    try:
        import Athlete
        ss = Athlete.safesuper
        f.write('safesuper: ' + repr(ss) + '\n')
        co = ss.__code__ if hasattr(ss, '__code__') else getattr(ss, 'func_code', None)
        if co:
            f.write('co_names: ' + repr(co.co_names) + '\n')
            f.write('co_varnames: ' + repr(co.co_varnames) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
