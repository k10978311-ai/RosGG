f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/pa_loadmap.txt', 'w')
try:
    import Avatar
    fn = getattr(Avatar.PlayerAvatar, 'loadMap', None)
    if hasattr(fn, 'im_func'): fn = fn.im_func
    if fn:
        f.write('co_names: %r\n' % (fn.func_code.co_names,))
        f.write('co_consts: %r\n' % (fn.func_code.co_consts,))
        f.write('co_varnames: %r\n' % (fn.func_code.co_varnames,))
    else:
        f.write('PlayerAvatar has no loadMap\n')
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
