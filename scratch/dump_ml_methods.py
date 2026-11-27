f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/ml_methods.txt', 'w')
try:
    import helpers.MapLoader as ML
    for m in ['doLoadMap', 'loadMap', '__init__']:
        fn = getattr(ML.MapLoader, m, None)
        if hasattr(fn, 'im_func'): fn = fn.im_func
        if fn:
            f.write('=== %s ===\n' % m)
            f.write('co_names: %r\n' % (fn.func_code.co_names,))
            f.write('co_consts: %r\n' % (fn.func_code.co_consts,))
            f.write('co_varnames: %r\n' % (fn.func_code.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
