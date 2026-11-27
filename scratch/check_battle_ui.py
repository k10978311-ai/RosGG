f = open(OUT, "w")
try:
    import Globals
    uiMgr = Globals.uiMgr
    f.write("uiMgr: %r\n" % (uiMgr,))
    if uiMgr:
        for attr in ["_visible_ui", "_loaded_ui", "active_ui_list"]:
            f.write("%s: %r\n" % (attr, getattr(uiMgr, attr, "<none>")))
    
    # Check if there is a skip tutorial button/func
    import BigWorld
    p = BigWorld.player()
    f.write("p: %r\n" % (p,))
    if p:
        f.write("p.__class__: %r\n" % (p.__class__,))
        for attr in ["skipTutorial", "skipRookieGuide", "skipGuide", "leaveBattle", "exitBattle", "quitBattle"]:
            f.write("p.%s: %r\n" % (attr, getattr(p, attr, "<none>")))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
