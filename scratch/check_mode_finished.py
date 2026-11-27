f = open(OUT, "w")
try:
    import Globals
    f.write("Globals.enterSelectModeFinished: %r\n" % (getattr(Globals, "enterSelectModeFinished", "<missing>"),))
    f.write("Globals.rookieEnterHall: %r\n" % (getattr(Globals, "rookieEnterHall", "<missing>"),))
    f.write("Globals.FIRST_LOAD: %r\n" % (getattr(Globals, "FIRST_LOAD", "<missing>"),))
    f.write("Globals.hasLogonServer: %r\n" % (getattr(Globals, "hasLogonServer", "<missing>"),))
    f.write("Globals.enterFirstFlag: %r\n" % (getattr(Globals, "enterFirstFlag", "<missing>"),))
    uiMgr = Globals.uiMgr
    for uiname in ["UISelectMode", "UISelectCharacter", "UILoading", "UIMain", "UIR2Main"]:
        ui = uiMgr.get_ui_by_name(uiname)
        f.write("%s: %r (visible=%r)\n" % (uiname, ui, getattr(ui, "isVisible", lambda: None)()))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
