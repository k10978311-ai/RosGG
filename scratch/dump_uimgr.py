f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/ui_dump.txt", "w")
try:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    f.write("uiMgr dir: %r\n" % dir(uiMgr))
    for k in ['_ui_stack', '_all_ui', '_cached_ui', '_active_ui', '_uis', 'ui_dict', '_visible_ui']:
        if hasattr(uiMgr, k):
            f.write("uiMgr.%s = %r\n" % (k, getattr(uiMgr, k)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
