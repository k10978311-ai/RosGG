f = open(OUT, "w")
try:
    import const, maps_utils
    from libclaudia.Classes.Application import Application as app
    mapID = const.HALL_MAP_ID
    f.write("HALL_MAP_ID: %r\n" % (mapID,))
    levelData = maps_utils.properties.getMapData(mapID)
    f.write("levelData: %r\n" % (levelData,))
    scenePath, navPath = maps_utils.getScenePath(levelData)
    f.write("scenePath: %r, navPath: %r\n" % (scenePath, navPath))
    
    # Check if files exist
    import os
    f.write("os.path.exists scenePath: %r\n" % (os.path.exists(scenePath) if scenePath else None,))
    
    # Check PreloadLevel
    task = app.PreloadLevel(mapID, {"scnPath": scenePath, "navPath": navPath})
    f.write("task: %r\n" % (task,))
    if task:
        for a in dir(task):
            if not a.startswith('__'):
                try:
                    f.write("  task.%s = %r\n" % (a, getattr(task, a)))
                except:
                    pass
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
