import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        import Globals
        f.write("Globals.inLoadingStage1: %r\n" % getattr(Globals, "inLoadingStage1", "NOT_FOUND"))
        
        import Application
        scene = getattr(Application, "scene", None)
        f.write("Application.scene: %r\n" % scene)
        if scene:
            f.write("scene.inLoading: %r\n" % getattr(scene, "inLoading", "NOT_FOUND"))
            f.write("scene.MAP_ID: %r\n" % getattr(scene, "MAP_ID", "NOT_FOUND"))
        
        if hasattr(p, "isWaitingPreload"):
            f.write("p.isWaitingPreload: %r\n" % getattr(p, "isWaitingPreload"))
        if hasattr(p, "isEnterOnPlane"):
            f.write("p.isEnterOnPlane: %r\n" % getattr(p, "isEnterOnPlane"))
        if hasattr(p, "switches"):
            f.write("p.switches: %r\n" % getattr(p, "switches", None))

        # Test prerequisites() return value
        res = p.prerequisites()
        f.write("p.prerequisites() returned: %r\n" % (res,))
        f.write("p.prerequisiteReady now: %r\n" % getattr(p, "prerequisiteReady", "NOT_FOUND"))
    except Exception:
        f.write(traceback.format_exc())
