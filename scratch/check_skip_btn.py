f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/skip_btn_info.txt", "w")
try:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    all_ui = getattr(uiMgr, '____all_ui__', {})
    skip_ui = all_ui.get('UISkipTutorial')
    if skip_ui:
        panel = getattr(skip_ui, 'panel', None)
        f.write("panel: %r\n" % panel)
        widget = getattr(skip_ui, 'widget', None)
        f.write("widget: %r\n" % widget)
        f.write("binder: %r\n" % getattr(skip_ui, 'binder', None))
        f.write("btn_func_list: %r\n" % getattr(skip_ui, 'btn_func_list', None))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
