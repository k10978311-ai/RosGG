f = open(OUT, 'w')
try:
    import Globals, BigWorld
    f.write('BigWorld.player(): %r\n' % BigWorld.player())
    f.write('Globals.player: %r\n' % getattr(Globals, 'player', None))
    uiMgr = Globals.uiMgr
    all_ui = getattr(uiMgr, '____all_ui__', getattr(uiMgr, '_UIMgr____all_ui__', {}))
    f.write('all_ui: %r\n' % list(all_ui.keys()))
    loading = all_ui.get('UILoading')
    if loading:
        for attr in ['_recordLoadingMapID', '_isLoading', '_lock', '_isDestroyed', 'is_active', 'is_visible']:
            f.write('loading.%s: %r\n' % (attr, getattr(loading, attr, 'N/A')))
    import sys
    f.write('sys.last_type: %r\n' % getattr(sys, 'last_type', None))
    f.write('sys.last_value: %r\n' % getattr(sys, 'last_value', None))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
