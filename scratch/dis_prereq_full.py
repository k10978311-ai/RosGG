f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/dis_prereq_full.txt', 'w')
try:
    import ClientEntity, dis
    fn = ClientEntity.ClientEntity.prerequisites
    if hasattr(fn, 'im_func'): fn = fn.im_func
    f.write('co_names: %r\n' % (fn.func_code.co_names,))
    f.write('co_consts: %r\n' % (fn.func_code.co_consts,))
    f.write('co_varnames: %r\n' % (fn.func_code.co_varnames,))
    import sys
    orig_stdout = sys.stdout
    sys.stdout = f
    dis.dis(fn)
    sys.stdout = orig_stdout
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
