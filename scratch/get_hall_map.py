f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/hall_map.txt', 'w')
try:
    import Globals
    f.write('Globals.MAP_ID: %r\n' % getattr(Globals, 'MAP_ID', None))
    import const
    for k in dir(const):
        if 'MAP' in k or 'HALL' in k or 'SCENE' in k:
            f.write('%s = %r\n' % (k, getattr(const, k)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
