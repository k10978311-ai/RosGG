import sys
f = open(OUT, "w")
try:
    import ClientEntity, Globals, BigWorld
    p = BigWorld.player()
    f.write("inLoadingStage1: %r\n" % getattr(Globals, "inLoadingStage1", None))
    App = vars(ClientEntity).get("Application")
    f.write("App.scene: %r\n" % getattr(App, "scene", None))
    f.write("p.prerequisiteReady: %r\n" % getattr(p, "prerequisiteReady", None))
    f.write("Globals.inLoading: %r\n" % getattr(Globals, "inLoading", None))
    f.write("Globals.MAP_ID: %r\n" % getattr(Globals, "MAP_ID", None))
    f.write("Globals.player: %r\n" % getattr(Globals, "player", None))
    sw = vars(ClientEntity).get("switches")
    f.write("switches: %r\n" % sw)
    if sw:
        f.write("  SysEnablePlaneNoEnterWorld: %r\n" % getattr(sw, "SysEnablePlaneNoEnterWorld", None))
        f.write("  SysEnableEntityFlowControl: %r\n" % getattr(sw, "SysEnableEntityFlowControl", None))
    f.write("p.entity: %r\n" % getattr(p, "entity", None))
    f.write("p.isWaitingPreload: %r\n" % getattr(p, "isWaitingPreload", None))
    if hasattr(p, "isWaitingPreload"):
        f.write("p.isWaitingPreload(): %r\n" % p.isWaitingPreload())
    
    # What does ClientEntity.prerequisites(p) check?
    # Let's inspect the code object's constants and names:
    co = ClientEntity.ClientEntity.prerequisites.im_func.func_code
    f.write("co_names: %r\n" % (co.co_names,))
    f.write("co_consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, "co_names")],))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
