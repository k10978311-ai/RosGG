f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/trace_prereq.txt', 'w')
try:
    import BigWorld, Globals, Application, switches
    p = BigWorld.player()
    f.write('p: %r\n' % p)
    f.write('1. p.prerequisiteReady: %r\n' % getattr(p, 'prerequisiteReady', None))
    f.write('2. Globals.inLoadingStage1: %r\n' % getattr(Globals, 'inLoadingStage1', None))
    f.write('3. Application.scene: %r\n' % getattr(Application, 'scene', None))
    f.write('4. Globals.inLoading: %r\n' % getattr(Globals, 'inLoading', None))
    f.write('5. Globals.MAP_ID: %r\n' % getattr(Globals, 'MAP_ID', None))
    f.write('6. getattr(p, mapID, 0): %r\n' % getattr(p, 'mapID', 0))
    f.write('   -> MAP_ID check: %r\n' % (getattr(Globals, 'MAP_ID', None) == getattr(p, 'mapID', 0)))
    f.write('7. Globals.player: %r\n' % getattr(Globals, 'player', None))
    f.write('8. isWaitingPreload: %r\n' % p.isWaitingPreload())
    f.write('9. switches.SysEnablePlaneNoEnterWorld: %r\n' % getattr(switches, 'SysEnablePlaneNoEnterWorld', None))
    f.write('10. switches.SysEnableEntityFlowControl: %r\n' % getattr(switches, 'SysEnableEntityFlowControl', None))
    f.write('11. getattr(p, allowToEnterWorld): %r\n' % getattr(p, 'allowToEnterWorld', None))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
