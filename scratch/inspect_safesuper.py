with open(OUT, 'w') as f:
    try:
        import utils
        ss = utils.safesuper
        f.write('utils.safesuper attrs: ' + repr(dir(ss)) + '\n')
        for k in dir(ss):
            v = getattr(ss, k)
            f.write(k + ': ' + repr(v) + '\n')
            co = getattr(v, '__code__', getattr(v, 'func_code', None))
            if co:
                f.write('  names: ' + repr(co.co_names) + '\n')
                f.write('  varnames: ' + repr(co.co_varnames) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
