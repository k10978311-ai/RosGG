f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/ce_prereq_full.txt', 'w')
try:
    import ClientEntity
    fn = ClientEntity.ClientEntity.prerequisites.im_func
    co = fn.func_code
    f.write('co_names: %r\n' % (co.co_names,))
    f.write('co_consts: %r\n' % (co.co_consts,))
    f.write('co_varnames: %r\n' % (co.co_varnames,))
    raw = [ord(c) for c in co.co_code]
    f.write('raw: %r\n' % raw)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
