with open(OUT, 'w') as f:
    try:
        import BigWorld, Globals, shared.switches as switches
        p = BigWorld.player()
        f.write('enterSelectModeFinished: ' + str(getattr(Globals, 'enterSelectModeFinished', 'None')) + '\n')
        f.write('FIRST_LOAD: ' + str(getattr(Globals, 'FIRST_LOAD', 'None')) + '\n')
        f.write('FIRST_LOAD_TIME: ' + str(getattr(Globals, 'FIRST_LOAD_TIME', 'None')) + '\n')
        f.write('URGENT_SWITCH_ENABLE_FORCE_UPGRADE: ' + str(getattr(switches, 'URGENT_SWITCH_ENABLE_FORCE_UPGRADE', 'None')) + '\n')
        
        # Check SceneSystem state
        import libclaudia.Classes.GameObject as go
        s = go.GameObject.Find('Scene')
        ss = s.GetComponent('SceneSystem')
        f.write('ss.is_loading: ' + str(getattr(ss, 'is_loading', 'None')) + '\n')
        f.write('ss._loading_scene: ' + str(getattr(ss, '_loading_scene', 'None')) + '\n')
        f.write('ss._preloadLevelResCoro: ' + str(getattr(ss, '_preloadLevelResCoro', 'None')) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
