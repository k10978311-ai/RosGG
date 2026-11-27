f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import const
    f.write('const.HALL_MAP_ID: %r\n' % getattr(const, 'HALL_MAP_ID', None))
    for k in dir(const):
        if 'MAP' in k or 'HALL' in k:
            f.write('const.%s = %r\n' % (k, getattr(const, k)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
