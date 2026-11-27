f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import Globals, BigWorld
    f.write('Globals.MAP_ID: %r\n' % getattr(Globals, 'MAP_ID', None))
    f.write('Globals.player: %r\n' % getattr(Globals, 'player', None))
    f.write('BigWorld.player(): %r\n' % (BigWorld.player(),))
    f.write('BigWorld.entities: %r\n' % (list(BigWorld.entities.keys()) if hasattr(BigWorld, 'entities') else None,))
    import sys
    f.write('sys.modules count: %d\n' % len(sys.modules))
    # Check scene
    try:
        import SceneSystem
        f.write('SceneSystem dir: %r\n' % dir(SceneSystem))
    except Exception as e:
        f.write('SceneSystem err: %r\n' % (e,))
    # Look for map or hall scene
    for mod in ['SceneSystem', 'ClientEntity', 'Globals', 'World', 'GameApp']:
        m = sys.modules.get(mod)
        if m:
            for k in dir(m):
                if 'MAP' in k or 'SCENE' in k or 'HALL' in k or 'LOBBY' in k or 'map' in k:
                    f.write('%s.%s = %r\n' % (mod, k, getattr(m, k)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
