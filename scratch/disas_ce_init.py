f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/dis_ce_init.txt', 'w')
try:
    import ClientEntity, dis, sys
    fn = ClientEntity.ClientEntity.__init__
    if hasattr(fn, 'im_func'): fn = fn.im_func
    f.write('co_names: %r\n' % (fn.func_code.co_names,))
    f.write('co_consts: %r\n' % (fn.func_code.co_consts,))
    f.write('co_varnames: %r\n' % (fn.func_code.co_varnames,))
    orig = sys.stdout; sys.stdout = f; dis.dis(fn); sys.stdout = orig
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
