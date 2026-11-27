f = open(OUT, "w")
try:
    import Globals
    uiMgr = Globals.uiMgr
    sw = uiMgr.get_ui_by_name("UISwallow")
    f.write("UISwallow: %r\n" % (sw,))
    if sw:
        f.write("isVisible: %r\n" % (getattr(sw, "isVisible", lambda: None)(),))
        f.write("dir: %r\n" % ([a for a in dir(sw) if not a.startswith("__")],))
    
    # Check camera / guide state
    p = getattr(Globals, "player", None)
    f.write("Globals.player: %r\n" % (p,))
    import BigWorld
    bp = BigWorld.player()
    f.write("BigWorld.player(): %r\n" % (bp,))
    if bp:
        f.write("inScenario: %r\n" % (getattr(bp, "inScenario", None),))
        f.write("isObserving: %r\n" % (getattr(bp, "isObserving", None),))
        f.write("guideID: %r\n" % (getattr(bp, "guideID", None),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
