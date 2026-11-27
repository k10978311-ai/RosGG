f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/btn_check.txt", "w")
try:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    all_ui = getattr(uiMgr, '____all_ui__', {})
    skip_ui = all_ui.get('UISkipTutorial')
    if skip_ui:
        btn = skip_ui.get_widget_by_path('left_bottom/skip_btn')
        f.write("btn visible: %r\n" % btn.isVisible())
        ccw = btn.underlyingCCWidget
        f.write("ccw: %r\n" % ccw)
        f.write("ccw isTouchEnabled: %r\n" % ccw.isTouchEnabled())
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
