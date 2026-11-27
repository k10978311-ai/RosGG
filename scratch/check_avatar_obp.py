f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/avatar_obp.txt", "w")
try:
    import Avatar
    pa = getattr(Avatar, 'PlayerAvatar', None)
    fn = getattr(pa, 'onBecomePlayer', None)
    if hasattr(fn, 'im_func'): fn = fn.im_func
    if fn.func_closure:
        for c in fn.func_closure:
            if hasattr(c.cell_contents, 'func_code'): fn = c.cell_contents
    f.write("onBecomePlayer co_names: %r\n" % (fn.func_code.co_names,))
    f.write("onBecomePlayer co_consts: %r\n" % ([x for x in fn.func_code.co_consts if not hasattr(x, 'co_names')],))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
