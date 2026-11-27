f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import ClientEntity
    App = vars(ClientEntity).get('Application')
    scene = getattr(App, 'scene', None)
    fn = getattr(scene, 'loadHallScene', None)
    f.write('loadHallScene: %r\n' % fn)
    if fn:
        if hasattr(fn, 'im_func'): fn = fn.im_func
        code = getattr(fn, 'func_code', None)
        if code:
            f.write('co_names: %r\n' % (code.co_names,))
            f.write('co_consts: %r\n' % ([c for c in code.co_consts if not hasattr(c, 'co_names')],))
            f.write('co_varnames: %r\n' % (code.co_varnames,))
        else:
            f.write('fn has no func_code (native?)\n')
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
