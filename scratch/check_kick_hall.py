f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/kick_hall.txt", "w")
try:
    import Avatar
    pa = getattr(Avatar, 'PlayerAvatar', None)
    f.write("PlayerAvatar: %r\n" % pa)
    if pa and hasattr(pa, 'kickOutToHall'):
        fn = getattr(pa, 'kickOutToHall')
        if hasattr(fn, 'im_func'): fn = fn.im_func
        if fn.func_closure:
            for c in fn.func_closure:
                if hasattr(c.cell_contents, 'func_code'): fn = c.cell_contents
        f.write("kickOutToHall co_names: %r\n" % (fn.func_code.co_names,))
        f.write("kickOutToHall co_consts: %r\n" % ([x for x in fn.func_code.co_consts if not hasattr(x, 'co_names')],))
        f.write("kickOutToHall co_varnames: %r\n" % (fn.func_code.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
