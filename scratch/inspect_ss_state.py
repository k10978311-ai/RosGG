f = open(OUT, 'w')
try:
    import Globals, Athlete
    go = Athlete.GameObject
    scene = go.Find('Scene')
    ss = scene.GetComponent('SceneSystem') if scene else None
    f.write('ss._scene: %r\n' % getattr(ss, '_scene', None))
    f.write('ss._scene_stage: %r\n' % getattr(ss, '_scene_stage', None))
    f.write('ss.current_scene_name: %r\n' % getattr(ss, 'current_scene_name', None))
    f.write('ss.current_map_id: %r\n' % getattr(ss, 'current_map_id', None))
    f.write('ss.is_loading: %r\n' % getattr(ss, 'is_loading', None))
    import Application
    f.write('Application.scene: %r\n' % getattr(Application, 'scene', None))
    f.write('Application.isLoadingLevel: %r\n' % getattr(Application, 'isLoadingLevel', None))
    f.write('Application.loadedLevelName: %r\n' % getattr(Application, 'loadedLevelName', None))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
