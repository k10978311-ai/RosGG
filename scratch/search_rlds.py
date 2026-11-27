f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/rlds_info.txt', 'w')
try:
    import Avatar
    pa = Avatar.PlayerAvatar
    for k in dir(pa):
        fn = getattr(pa, k)
        if hasattr(fn, 'im_func'):
            co = fn.im_func.func_code
            if 'requestLeaveDynamicSpace' in co.co_names or 'leave' in k.lower():
                f.write('PlayerAvatar.%s: %r\n' % (k, co.co_names))
    # Also check client methods on Avatar.def
    import sys
    sys.path.insert(0, '/sdcard')
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
