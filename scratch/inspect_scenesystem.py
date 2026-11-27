OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    real_fn = Athlete.PlayerAthlete.enterHall.func_closure[0].cell_contents
    GameObject = real_fn.func_globals.get('GameObject')
    scene_go = GameObject.Find('Scene')
    ss = scene_go.GetComponent('SceneSystem')
    f.write("SceneSystem: %r, type=%r\n" % (ss, type(ss)))
    f.write("SceneSystem dir: %r\n" % dir(ss))
    
    # check attributes on ss
    for attr in ('is_loading', 'isLoading', 'cur_scene', 'scene_name', 'loading_scene', 'hallScene', 'scene_id', 'map_id'):
        if hasattr(ss, attr):
            f.write("  ss.%s: %r\n" % (attr, getattr(ss, attr)))
            
    # Also inspect onHallSceneReady!
    co = real_fn.func_code
    for c in co.co_consts:
        if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
            for c2 in c.co_consts:
                if hasattr(c2, 'co_name') and c2.co_name == 'onHallSceneReady':
                    f.write("\nonHallSceneReady names: %r\n" % (c2.co_names,))
                    f.write("onHallSceneReady consts: %r\n" % [x if not hasattr(x, 'co_name') else x.co_name for x in c2.co_consts])
                    f.write("onHallSceneReady varnames: %r\n" % (c2.co_varnames,))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
