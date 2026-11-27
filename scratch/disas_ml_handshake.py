f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/ml_handshake.txt', 'w')
try:
    import helpers.MapLoader as ML, dis, sys
    fn = ML.MapLoader.onHandshake
    if hasattr(fn, 'im_func'): fn = fn.im_func
    f.write('co_names: %r\n' % (fn.func_code.co_names,))
    f.write('co_consts: %r\n' % (fn.func_code.co_consts,))
    orig = sys.stdout; sys.stdout = f; dis.dis(fn); sys.stdout = orig
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
