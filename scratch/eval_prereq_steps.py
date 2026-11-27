with open(OUT, 'w') as f:
    try:
        import BigWorld, Globals, shared.switches as switches, ClientEntity
        p = BigWorld.player()
        App = vars(ClientEntity).get('Application')
        scene = getattr(App, 'scene', None)
        
        f.write('1. Globals.inLoadingStage1: ' + repr(getattr(Globals, 'inLoadingStage1', None)) + '\n')
        f.write('2. App.scene: ' + repr(scene) + '\n')
        f.write('3. Globals.inLoading: ' + repr(getattr(Globals, 'inLoading', None)) + '\n')
        f.write('4. Globals.MAP_ID: ' + repr(getattr(Globals, 'MAP_ID', None)) + '\n')
        f.write('5. getattr(p, mapID, 0): ' + repr(getattr(p, 'mapID', 0)) + '\n')
        f.write('6. Globals.player: ' + repr(getattr(Globals, 'player', None)) + '\n')
        f.write('7. switches.SysEnablePlaneNoEnterWorld: ' + repr(getattr(switches, 'SysEnablePlaneNoEnterWorld', None)) + '\n')
        f.write('8. getattr(p, entity, None): ' + repr(getattr(p, 'entity', None)) + '\n')
        f.write('9. getattr(p, isWaitingPreload, None): ' + repr(getattr(p, 'isWaitingPreload', None)) + '\n')
        f.write('10. switches.SysEnableEntityFlowControl: ' + repr(getattr(switches, 'SysEnableEntityFlowControl', None)) + '\n')
        f.write('11. Globals.entityFlowControl: ' + repr(getattr(Globals, 'entityFlowControl', None)) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
