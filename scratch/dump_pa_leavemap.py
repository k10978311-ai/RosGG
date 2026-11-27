f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/pa_leavemap.txt', 'w')
try:
    import Avatar
    for name in ['leaveMap', 'onRequestLeaveDynamicSpace']:
        fn = getattr(Avatar.PlayerAvatar, name, None)
        if hasattr(fn, 'im_func'): fn = fn.im_func
        if fn:
            f.write('=== %s ===\n' % name)
            f.write('co_names: %r\n' % (fn.func_code.co_names,))
            f.write('co_consts: %r\n' % (fn.func_code.co_consts,))
            f.write('co_varnames: %r\n' % (fn.func_code.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
