f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/find_skip.txt", "w")
try:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    f.write("uiMgr: %r\n" % uiMgr)
    if uiMgr:
        uis = getattr(uiMgr, '_ui_dict', {})
        f.write("active uis: %r\n" % list(uis.keys()))
        for uiname, uiobj in uis.items():
            f.write("UI: %s -> %r\n" % (uiname, uiobj))
            for k in dir(uiobj):
                if 'skip' in k.lower():
                    f.write("  attr: %s = %r\n" % (k, getattr(uiobj, k)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
