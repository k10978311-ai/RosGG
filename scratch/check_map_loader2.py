f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/map_handshake2.txt", "w")
try:
    import Avatar
    ml_cls = getattr(Avatar, 'MapLoader', None)
    f.write("ml_cls: %r\n" % ml_cls)
    ml = ml_cls.getInstance()
    fn = getattr(ml, 'onHandshake', None)
    if hasattr(fn, 'im_func'): fn = fn.im_func
    f.write("onHandshake co_names: %r\n" % (fn.func_code.co_names,))
    f.write("onHandshake co_consts: %r\n" % ([x for x in fn.func_code.co_consts if not hasattr(x, 'co_names')],))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
