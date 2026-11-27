f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/ce_calls.txt', 'w')
try:
    import ClientEntity
    ce = ClientEntity.ClientEntity
    for k in dir(ce):
        fn = getattr(ce, k)
        if hasattr(fn, 'im_func'):
            co = fn.im_func.func_code
            if 'prerequisites' in co.co_names:
                f.write('%s calls prerequisites\n' % k)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
