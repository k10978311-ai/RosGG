import sys
f = open(OUT, "w")
try:
    import ClientEntity, Globals
    App = vars(ClientEntity).get("Application")
    scene = getattr(App, "scene", None)
    f.write("isCoroutineRunning(_preloadLevelResCoro): %r\n" % scene.isCoroutineRunning("_preloadLevelResCoro"))
    f.write("scene._scene: %r\n" % getattr(scene, "_scene", None))
    f.write("scene._mapID: %r\n" % getattr(scene, "_mapID", None))
    f.write("Globals.MAP_ID: %r\n" % getattr(Globals, "MAP_ID", None))
    f.write("Globals.PREV_MAP_ID: %r\n" % getattr(Globals, "PREV_MAP_ID", None))
    f.write("Globals.inLoading: %r\n" % getattr(Globals, "inLoading", None))
    f.write("Globals.hallSceneReady: %r\n" % getattr(Globals, "hallSceneReady", None))
    f.write("Globals.player: %r\n" % getattr(Globals, "player", None))
    import BigWorld
    p = BigWorld.player()
    f.write("BigWorld.player(): %r\n" % p)
    f.write("BigWorld.entities: %r\n" % dict(BigWorld.entities.items()))
    f.write("BigWorld.prereqEntities: %r\n" % BigWorld.prereqEntities())
    f.write("BigWorld.cachedEntities: %r\n" % BigWorld.cachedEntities())
    # Let's check why player is in prereqEntities:
    f.write("p.prerequisiteReady: %r\n" % getattr(p, "prerequisiteReady", None))
    # What are the prerequisites of p?
    if hasattr(p, "prerequisites"):
        try:
            f.write("p.prerequisites() -> %r\n" % (p.prerequisites(),))
        except Exception as e:
            f.write("p.prerequisites() err -> %r\n" % (e,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
