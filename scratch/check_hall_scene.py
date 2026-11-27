f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/hall_scene.txt', 'w')
try:
    import const
    f.write('const.HALL_MAP_ID: %r\n' % getattr(const, 'HALL_MAP_ID', None))
    import maps_utils
    f.write('maps_utils.getMapInfo(20): %r\n' % getattr(maps_utils, 'getMapInfo', lambda x: None)(20))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
