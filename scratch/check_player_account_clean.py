f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/p_acc.txt", "w")
try:
    import Account
    f.write("Account attrs: %r\n" % dir(Account))
    pa = getattr(Account, 'PlayerAccount', None)
    if pa:
        f.write("PlayerAccount: %r\n" % (pa,))
        for m in ['onLogin', 'onChannelLogin', 'loadSceneAfterReconnect']:
            if hasattr(pa, m):
                fn = getattr(pa, m)
                if hasattr(fn, 'im_func'): fn = fn.im_func
                if fn.func_closure:
                    for c in fn.func_closure:
                        if hasattr(c.cell_contents, 'func_code'): fn = c.cell_contents
                f.write("pa.%s: co_names=%r, co_consts=%r\n" % (m, fn.func_code.co_names, [x for x in fn.func_code.co_consts if not hasattr(x, 'co_names')]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
