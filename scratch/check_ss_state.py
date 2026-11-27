OUT = '/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log'
f = open(OUT, 'w')
try:
    import Athlete
    real_fn = Athlete.PlayerAthlete.enterHall.func_closure[0].cell_contents
    GameObject = real_fn.func_globals.get('GameObject')
    scene_go = GameObject.Find('Scene')
    ss = scene_go.GetComponent('SceneSystem')
    f.write('ss._scene: %r\n' % (getattr(ss, '_scene', None),))
    f.write('ss._scene_stage: %r\n' % (getattr(ss, '_scene_stage', None),))
    f.write('ss._preloadLevelResCoro: %r\n' % (getattr(ss, '_preloadLevelResCoro', None),))
    f.write('ss.camera: %r\n' % (getattr(ss, 'camera', None),))
    
    # Check coroutines
    import world
    f.write('world active scene: %r\n' % (world.get_active_scene(),))
    
    # Check BigWorld.player()
    import BigWorld
    p = BigWorld.player()
    f.write('player: %r\n' % (p,))
    f.write('player.isEnterHallCalled: %r\n' % getattr(p, 'isEnterHallCalled', None))
    f.write('player.m_enterHallTimer: %r\n' % getattr(p, 'm_enterHallTimer', None))
    f.write('player.hallScene: %r\n' % getattr(p, 'hallScene', None))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
