f = open(OUT, "w")
try:
    import Athlete, const, maps_utils
    import libclaudia.Classes.Application as app
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem")
    
    mapID = const.HALL_MAP_ID
    f.write("mapID: %r\n" % (mapID,))
    levelData = maps_utils.properties.getMapData(mapID)
    f.write("levelData: %r\n" % (levelData,))
    scenePath, navPath = maps_utils.getScenePath(levelData)
    f.write("scenePath: %r, navPath: %r\n" % (scenePath, navPath))
    
    # Check if app.PreloadLevel works
    f.write("Testing app.PreloadLevel...\n")
    pl_res = app.PreloadLevel(mapID, {"scnPath": scenePath, "navPath": navPath})
    f.write("PreloadLevel res: %r\n" % (pl_res,))
    if pl_res:
        f.write("dir(pl_res): %r\n" % ([a for a in dir(pl_res) if not a.startswith("__")],))
        f.write("is_done: %r\n" % (getattr(pl_res, "is_done", None),))
        f.write("progress: %r\n" % (getattr(pl_res, "progress", None),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
