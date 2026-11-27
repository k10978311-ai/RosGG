f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/active_uis.txt", "w")
try:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    all_ui = getattr(uiMgr, '____all_ui__', None)
    f.write("all_ui: %r\n" % all_ui)
    if all_ui:
        for k in dir(all_ui):
            f.write("all_ui.%s = %r\n" % (k, getattr(all_ui, k)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
