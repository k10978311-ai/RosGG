f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/dis_clean.txt', 'w')
try:
    import ClientEntity, dis
    fn = ClientEntity.ClientEntity.prerequisites
    if hasattr(fn, 'im_func'):
        fn = fn.im_func
    code = fn.func_code
    f.write('co_varnames: %r\n' % (code.co_varnames,))
    f.write('co_names: %r\n' % (code.co_names,))
    f.write('co_consts: %r\n' % ([c for c in code.co_consts if not hasattr(c, 'co_names')],))
    raw = [ord(c) for c in code.co_code]
    i = 0
    while i < len(raw):
        op = raw[i]
        opname = dis.opname[op]
        if op >= dis.HAVE_ARGUMENT:
            arg = raw[i+1] + (raw[i+2] << 8)
            f.write('%4d %-20s %d\n' % (i, opname, arg))
            i += 3
        else:
            f.write('%4d %-20s\n' % (i, opname))
            i += 1
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
