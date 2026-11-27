OUT = '/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log'
f = open(OUT, 'w')
try:
    import Globals, BigWorld
    f.write('Globals.MAP_ID: %r\n' % getattr(Globals, 'MAP_ID', None))
    f.write('Globals.inLoading: %r\n' % getattr(Globals, 'inLoading', None))
    f.write('Globals.inLoadingStage1: %r\n' % getattr(Globals, 'inLoadingStage1', None))
    f.write('Globals.player: %r\n' % getattr(Globals, 'player', None))
    f.write('BigWorld.player(): %r\n' % BigWorld.player())
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
