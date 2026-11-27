OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld, Athlete, types
    p = BigWorld.player()
    f.write("player: %r\n" % p)
    
    # check attributes on p
    f.write("p.hallScene: %r\n" % getattr(p, 'hallScene', 'NO_ATTR'))
    f.write("p.rookieEnterHall: %r\n" % getattr(p, 'rookieEnterHall', 'NO_ATTR'))
    f.write("p.enterFirstFlag: %r\n" % getattr(p, 'enterFirstFlag', 'NO_ATTR'))
    
    # check enterHall implementation
    fn = Athlete.PlayerAthlete.enterHall
    f.write("enterHall func: %r\n" % fn)
    if hasattr(fn, 'func_closure') and fn.func_closure:
        for idx, cell in enumerate(fn.func_closure):
            f.write("  closure[%d]: %r\n" % (idx, cell.cell_contents))
    
    # Check what UI is currently open!
    import Globals
    if hasattr(Globals, 'uiMgr'):
        f.write("uiMgr: %r\n" % Globals.uiMgr)
        if hasattr(Globals.uiMgr, '_all_ui'):
            f.write("all_ui: %r\n" % Globals.uiMgr._all_ui)
        if hasattr(Globals.uiMgr, '_cur_ui'):
            f.write("cur_ui: %r\n" % Globals.uiMgr._cur_ui)
    
    # Check scene
    import SceneSystem
    f.write("SceneSystem: %r\n" % SceneSystem)
    for k in dir(SceneSystem):
        if not k.startswith('_'):
            f.write("  SceneSystem.%s: %r\n" % (k, getattr(SceneSystem, k)))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
