f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/acc_ls.txt', 'w')
try:
    import Account, dis, sys
    fn = getattr(Account.Account, 'loadSceneAfterReconnect', None)
    if hasattr(fn, 'im_func'): fn = fn.im_func
    f.write('loadSceneAfterReconnect: %r\n' % fn)
    if fn:
        f.write('co_names: %r\n' % (fn.func_code.co_names,))
        f.write('co_consts: %r\n' % (fn.func_code.co_consts,))
        orig = sys.stdout; sys.stdout = f; dis.dis(fn); sys.stdout = orig
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
