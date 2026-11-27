f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/skip_tut.txt", "w")
try:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    all_ui = getattr(uiMgr, '____all_ui__', {})
    skip_ui = all_ui.get('UISkipTutorial')
    f.write("skip_ui: %r\n" % skip_ui)
    if skip_ui:
        f.write("dir: %r\n" % dir(skip_ui))
        cls = skip_ui.__class__
        f.write("cls: %r\n" % cls)
        for m in dir(cls):
            val = getattr(cls, m)
            if callable(val) and hasattr(val, 'im_func'):
                f.write("method: %s, co_names=%r\n" % (m, val.im_func.func_code.co_names))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
