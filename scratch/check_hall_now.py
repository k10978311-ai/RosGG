OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld, Globals, world
    f.write("BigWorld.player: %r\n" % (BigWorld.player(),))
    f.write("active_scene: %r\n" % (world.get_active_scene(),))
    
    # Check UIs
    uiMgr = getattr(Globals, "uiMgr", None)
    if uiMgr:
        f.write("uiMgr: %r\n" % (uiMgr,))
        f.write("visible_uis: %r\n" % getattr(uiMgr, '_visible_uis', {}))
        f.write("ui_stack: %r\n" % getattr(uiMgr, '_ui_stack', []))
        f.write("entered_uis: %r\n" % getattr(uiMgr, '_entered_uis', []))
    
    # Check SceneSystem
    import Athlete
    real_fn = Athlete.PlayerAthlete.enterHall.func_closure[0].cell_contents
    GameObject = real_fn.func_globals.get('GameObject')
    scene_go = GameObject.Find('Scene')
    if scene_go:
        ss = scene_go.GetComponent('SceneSystem')
        f.write("SceneSystem: %r\n" % (ss,))
        f.write("  cur_scene: %r\n" % getattr(ss, '_scene', None))
        f.write("  scene_stage: %r\n" % getattr(ss, '_scene_stage', None))
    
    # Check player attributes
    p = BigWorld.player()
    if p:
        f.write("p.hallScene: %r\n" % getattr(p, 'hallScene', None))
        f.write("p.is_in_hall: %r\n" % getattr(p, 'is_in_hall', None))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
