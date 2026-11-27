import traceback
f = open(OUT, 'w')
try:
    import GameInit
    for name in dir(GameInit):
        if 'timeout' in name.lower() or 'inactive' in name.lower():
            val = getattr(GameInit, name)
            f.write('%s = %r\n' % (name, val))
            if callable(val) and hasattr(val, 'func_code'):
                f.write('  co_names: %r\n' % (val.func_code.co_names,))
                f.write('  co_consts: %r\n' % (val.func_code.co_consts,))
except Exception:
    f.write(traceback.format_exc())
f.close()
