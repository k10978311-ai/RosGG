OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld, Globals
    p = BigWorld.player()
    f.write("player: %r\n" % (p,))
    if p:
        f.write("hallScene: %r\n" % getattr(p, 'hallScene', 'NO_ATTR'))
        f.write("enterFirstFlag: %r\n" % getattr(p, 'enterFirstFlag', 'NO_ATTR'))
        f.write("isEnterHallCalled: %r\n" % getattr(p, 'isEnterHallCalled', 'NO_ATTR'))
    
    # Check Globals.uiMgr
    um = getattr(Globals, 'uiMgr', None)
    if um:
        f.write("visible_uis: %r\n" % getattr(um, '_visible_uis', {}))
        for name in ('UILoading', 'UIMain', 'UIR2Main', 'UILogin'):
            ui = um.get_ui_by_name(name) if hasattr(um, 'get_ui_by_name') else None
            f.write("ui %s: %r (visible=%r)\n" % (name, ui, getattr(ui, 'isVisible', lambda: None)()))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
