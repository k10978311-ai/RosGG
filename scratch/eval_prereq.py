f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/prereq_out.txt", "w")
try:
    import ClientEntity, Globals, BigWorld
    p = BigWorld.player()
    f.write("player: %r\n" % (p,))
    if p:
        f.write("1. p.prerequisiteReady: %r\n" % getattr(p, 'prerequisiteReady', None))
        f.write("2. Globals.inLoadingStage1: %r\n" % getattr(Globals, 'inLoadingStage1', None))
        App = vars(ClientEntity).get('Application')
        f.write("3. App.scene: %r\n" % getattr(App, 'scene', None))
        f.write("4. Globals.inLoading: %r\n" % getattr(Globals, 'inLoading', None))
        f.write("5. getattr(p, 'mapID', 0): %r\n" % getattr(p, 'mapID', 0))
        f.write("6. Globals.MAP_ID: %r\n" % getattr(Globals, 'MAP_ID', None))
        f.write("7. Globals.player: %r\n" % getattr(Globals, 'player', None))
        sw = vars(ClientEntity).get('switches')
        f.write("8. sw.SysEnablePlaneNoEnterWorld: %r\n" % getattr(sw, 'SysEnablePlaneNoEnterWorld', None))
        f.write("9. p.entity: %r\n" % getattr(p, 'entity', None))
        try:
            f.write("10. p.isWaitingPreload(): %r\n" % p.isWaitingPreload())
        except Exception as e:
            f.write("10. p.isWaitingPreload() err: %r\n" % (e,))
        efc = getattr(Globals, 'entityFlowControl', None)
        f.write("12. Globals.entityFlowControl: %r\n" % (efc,))
        f.write("13. getattr(p, 'useFlowControl', True): %r\n" % getattr(p, 'useFlowControl', '<missing>'))
        f.write("14. getattr(p, 'underFlowControl', False): %r\n" % getattr(p, 'underFlowControl', '<missing>'))
        f.write("15. getattr(p, 'allowToEnterWorld', False): %r\n" % getattr(p, 'allowToEnterWorld', '<missing>'))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
