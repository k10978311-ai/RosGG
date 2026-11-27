f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/cur_state.txt', 'w')
try:
    import Globals, Application
    f.write('Globals.MAP_ID: %r\n' % getattr(Globals, 'MAP_ID', None))
    f.write('Globals.player: %r\n' % getattr(Globals, 'player', None))
    f.write('Application.scene: %r\n' % getattr(Application, 'scene', None))
    import BigWorld
    f.write('BigWorld.entities: %r\n' % list(BigWorld.entities.items()))
    f.write('BigWorld.player(): %r\n' % getattr(BigWorld, 'player', lambda: None)())
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
