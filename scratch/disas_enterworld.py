f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import ClientEntity
    fn = ClientEntity.ClientEntity.enterWorld
    if hasattr(fn, 'im_func'):
        fn = fn.im_func
    f.write('enterWorld co_names: %r\n' % (fn.func_code.co_names,))
    f.write('enterWorld co_consts: %r\n' % ([x for x in fn.func_code.co_consts if not hasattr(x, 'co_names')],))
    f.write('enterWorld co_varnames: %r\n' % (fn.func_code.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
