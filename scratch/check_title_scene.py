f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import ClientEntity
    App = vars(ClientEntity).get('Application')
    f.write('App: %r\n' % App)
    f.write('App.scene: %r\n' % getattr(App, 'scene', None))
    import Globals
    f.write('Globals.inLoadingStage1: %r\n' % getattr(Globals, 'inLoadingStage1', None))
    f.write('Globals.inLoading: %r\n' % getattr(Globals, 'inLoading', None))
    f.write('Globals.MAP_ID: %r\n' % getattr(Globals, 'MAP_ID', None))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
