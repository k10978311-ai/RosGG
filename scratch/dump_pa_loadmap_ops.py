f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/pa_loadmap_ops.txt', 'w')
try:
    import Avatar
    fn = Avatar.PlayerAvatar.loadMap.im_func
    f.write('raw: %r\n' % [ord(c) for c in fn.func_code.co_code])
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
