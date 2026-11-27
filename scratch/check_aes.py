f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/aes_info.txt", "w")
try:
    import Avatar
    pa = getattr(Avatar, 'PlayerAvatar', None)
    fn = getattr(pa, 'afterEnterSpace', None)
    if hasattr(fn, 'im_func'): fn = fn.im_func
    f.write("afterEnterSpace: %r\n" % fn)
    if fn:
        f.write("co_names: %r\n" % (fn.func_code.co_names,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
