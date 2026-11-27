f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/btn_pos.txt", "w")
try:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    all_ui = getattr(uiMgr, '____all_ui__', {})
    skip_ui = all_ui.get('UISkipTutorial')
    if skip_ui:
        btn = skip_ui.get_widget_by_path('left_bottom/skip_btn')
        f.write("btn: %r\n" % btn)
        if btn:
            f.write("btn dir: %r\n" % dir(btn))
            for k in ['getWorldPosition', 'getPosition', 'getContentSize', 'getBoundingBox']:
                if hasattr(btn, k):
                    f.write("btn.%s() = %r\n" % (k, getattr(btn, k)()))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
