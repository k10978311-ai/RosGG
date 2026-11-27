f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/cocos_coord.txt", "w")
try:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    all_ui = getattr(uiMgr, '____all_ui__', {})
    skip_ui = all_ui.get('UISkipTutorial')
    if skip_ui:
        f.write("winSize: %r\n" % (getattr(skip_ui, 'winSize', None),))
        f.write("designRes: %r\n" % (skip_ui.getDesignResolutionSize(),))
        btn = skip_ui.get_widget_by_path('left_bottom/skip_btn')
        wp = btn.worldPosition
        f.write("worldPosition: %r\n" % (wp,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
