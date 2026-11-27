
with open(OUT, 'w') as f:
    try:
        import BigWorld, Globals
        p = BigWorld.player()
        f.write('p: ' + repr(p) + '\n')
        f.write('p dict: ' + repr({k: getattr(p, k) for k in dir(p) if 'hall' in k.lower() or 'scene' in k.lower() or 'enter' in k.lower()}) + '\n')
        import shared.switches as switches
        f.write('switches.URGENT_SWITCH_ENABLE_FORCE_UPGRADE: ' + repr(getattr(switches, 'URGENT_SWITCH_ENABLE_FORCE_UPGRADE', 'NOT_FOUND')) + '\n')
        import libclaudia
        app = libclaudia.Classes.Application.Application.instance()
        scene = app.scene
        f.write('app.scene: ' + repr(scene) + '\n')
        import libclaudia.Classes.GameObject as go
        scene_go = go.GameObject.Find('Scene')
        f.write('scene_go: ' + repr(scene_go) + '\n')
        if scene_go:
            ss = scene_go.GetComponent('SceneSystem')
            f.write('SceneSystem: ' + repr(ss) + '\n')
            f.write('ss dir: ' + repr([x for x in dir(ss) if 'hall' in x.lower() or 'scene' in x.lower() or 'load' in x.lower()]) + '\n')
            for attr in ['cur_scene_id', 'target_scene_id', 'is_loading', '_loading_scene']:
                if hasattr(ss, attr):
                    f.write('ss.' + attr + ': ' + repr(getattr(ss, attr)) + '\n')
        import ui.uiMgr as uiMgr
        f.write('current UIs: ' + repr(uiMgr.get_current_uis() if hasattr(uiMgr, 'get_current_uis') else 'no get_current_uis') + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
