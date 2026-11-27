f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import Account
    f.write('Account class: %r\n' % Account.Account)
    for name in dir(Account.Account):
        val = getattr(Account.Account, name)
        if callable(val) and hasattr(val, " im_func\):
 fn = val.im_func
 if fn.func_closure:
 for c in fn.func_closure:
 if hasattr(c.cell_contents, \func_code\):
 fn = c.cell_contents
 f.write('METHOD: %s\n' % name)
 f.write(' co_names: %r\n' % (fn.func_code.co_names,))
 f.write(' co_consts: %r\n' % ([x for x in fn.func_code.co_consts if not hasattr(x, \co_names\)],))
except Exception:
 import traceback
 f.write(traceback.format_exc())
f.close()
