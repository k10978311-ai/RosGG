f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/dis_load_hall.txt', 'w')
try:
    import libclaudia, dis, sys
    fn = getattr(libclaudia.SceneSystem, 'loadHallScene', None)
    if hasattr(fn, 'im_func'): fn = fn.im_func
    if fn:
        f.write('co_names: %r\n' % (fn.func_code.co_names,))
        f.write('co_consts: %r\n' % (fn.func_code.co_consts,))
        orig = sys.stdout; sys.stdout = f; dis.dis(fn); sys.stdout = orig
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
