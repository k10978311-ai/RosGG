f = open(OUT, "w")
try:
    import Athlete, const
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem")
    p = Athlete.PlayerAthlete
    
    f.write("scene: %r\n" % (scene,))
    f.write("ss: %r\n" % (ss,))
    
    # Check what maps_utils.properties.getMapData(const.HALL_MAP_ID) returns
    import maps_utils
    md = maps_utils.properties.getMapData(const.HALL_MAP_ID)
    f.write("md: %r\n" % (md,))
    scnPath, navPath = maps_utils.getScenePath(md)
    f.write("scnPath: %r, navPath: %r\n" % (scnPath, navPath))
    
    # Check if scnPath exists in game resources / files
    import resource
    f.write("resource exists scnPath: %r\n" % (getattr(resource, "has_resource", lambda x: "<none>")(scnPath),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
