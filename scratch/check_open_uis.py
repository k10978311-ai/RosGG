OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Globals
    uiMgr = Globals.uiMgr
    f.write("uiMgr: %r\n" % uiMgr)
    
    # Inspect all attributes on uiMgr
    for k in dir(uiMgr):
        if not k.startswith('__'):
            try:
                v = getattr(uiMgr, k)
                if not callable(v):
                    f.write("  uiMgr.%s = %r\n" % (k, v))
            except Exception as e:
                f.write("  uiMgr.%s ERROR: %s\n" % (k, e))
                
    # Also check UIManager stack or open UIs
    for attr in ('_ui_stack', '_stack', '_uis', '_all_ui', '_open_ui', '_active_ui', 'ui_dict', 'dict_ui'):
        if hasattr(uiMgr, attr):
            f.write("uiMgr.%s = %r\n" % (attr, getattr(uiMgr, attr)))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
