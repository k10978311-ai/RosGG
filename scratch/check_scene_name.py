f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import ClientEntity, Globals
    App = vars(ClientEntity).get('Application')
    scene = getattr(App, 'scene', None)
    f.write('scene: %r\n' % scene)
    if scene:
        f.write('scene dir: %r\n' % dir(scene))
        for attr in ['name', 'path', 'id', 'mapID', 'scene_name', 'get_name']:
            if hasattr(scene, attr):
                f.write('scene.%s: %r\n' % (attr, getattr(scene, attr)))
    f.write('Globals.MAP_ID: %r\n' % getattr(Globals, 'MAP_ID', None))
    f.write('Globals.SCENE_PATH: %r\n' % getattr(Globals, 'SCENE_PATH', None))
    f.write('Globals.inLoading: %r\n' % getattr(Globals, 'inLoading', None))
    # check maps_utils
    try:
        import maps_utils
        f.write('maps_utils.get_map_id: %r\n' % getattr(maps_utils, 'get_map_id', None))
    except Exception as e:
        f.write('maps_utils err: %r\n' % e)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
