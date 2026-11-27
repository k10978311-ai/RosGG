f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/load_map20.txt', 'w')
try:
    import GameObject
    ss = GameObject.Find('Scene').GetComponent('SceneSystem')
    f.write('ss: %r\n' % ss)
    # Check if loadMap(20) or loadHallScene() is what loads map 20
    f.write('has loadHallScene: %s\n' % hasattr(ss, 'loadHallScene'))
    f.write('has loadMap: %s\n' % hasattr(ss, 'loadMap'))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
