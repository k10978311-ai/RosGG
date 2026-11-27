f = open(OUT, "w")
try:
    import BigWorld, Globals
    p = BigWorld.player()
    f.write("BigWorld.player(): %r\n" % (p,))
    if p:
        f.write("class: %s\n" % (p.__class__.__name__,))
        f.write("id: %d\n" % (p.id,))
        f.write("nickname: %r\n" % (getattr(p, "baseNickname", None),))
        f.write("isInHall: %r\n" % (getattr(Globals, "isInHall", None),))
        f.write("isHallSceneReady: %r\n" % (getattr(Globals, "isHallSceneReady", lambda: None)(),))
    ui = Globals.uiMgr
    f.write("loaded_ui: %r\n" % (getattr(ui, "_loaded_ui", None),))
    f.write("visible_ui: %r\n" % (getattr(ui, "_visible_ui", None),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
