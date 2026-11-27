f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/globals_fn.txt', 'w')
try:
    import Globals, dis, sys
    for fn_name in ['setInHall', 'setPlayerAvatar']:
        fn = getattr(Globals, fn_name, None)
        if fn:
            f.write('=== Globals.%s ===\n' % fn_name)
            f.write('co_names: %r\n' % (fn.func_code.co_names,))
            f.write('co_consts: %r\n' % (fn.func_code.co_consts,))
            orig = sys.stdout; sys.stdout = f; dis.dis(fn); sys.stdout = orig
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
