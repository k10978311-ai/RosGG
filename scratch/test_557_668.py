OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld, Globals, Athlete
    p = BigWorld.player()
    
    f.write("Testing 557-668...\n")
    # check doRealnameAuthenAgain
    val = getattr(p, 'doRealnameAuthenAgain', False)
    f.write("getattr doRealnameAuthenAgain: %r\n" % val)
    
    # check GameInit
    real_fn = Athlete.PlayerAthlete.enterHall.func_closure[0].cell_contents
    co = real_fn.func_code
    for c in co.co_consts:
        if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
            reh_co = c
            break
            
    f.write("reh_co names 40-50: %r\n" % (reh_co.co_names[40:50],))
    
    # Test GameInit.updateInactivityTimeout()
    try:
        from common import GameInit
        f.write("import GameInit: %r\n" % GameInit)
        if hasattr(GameInit, 'updateInactivityTimeout'):
            GameInit.updateInactivityTimeout()
            f.write("GameInit.updateInactivityTimeout: OK\n")
    except Exception as e:
        f.write("GameInit test: %r\n" % e)
        
    # Test GameObject.Find('Scene').GetComponent('SceneSystem').loadHallScene
    import GameObject
    scene = GameObject.Find('Scene')
    ss = scene.GetComponent('SceneSystem')
    f.write("ss.loadHallScene: %r\n" % ss.loadHallScene)

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
