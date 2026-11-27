with open(OUT, 'w') as f:
    try:
        from libclaudia.Classes.GameObject import GameObject
        scene_go = GameObject.Find('Scene')
        f.write('scene_go: ' + repr(scene_go) + '\n')
        if scene_go:
            ss = scene_go.GetComponent('SceneSystem')
            f.write('ss: ' + repr(ss) + '\n')
            f.write('ss dict: ' + repr({k: repr(getattr(ss, k)) for k in dir(ss) if not k.startswith('__')}) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
