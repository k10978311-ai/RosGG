f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/call_tlm2.txt", "w")
try:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    all_ui = getattr(uiMgr, '____all_ui__', {})
    skip_ui = all_ui.get('UISkipTutorial')
    if skip_ui:
        res = skip_ui.tryLeaveMap('Do you want to skip the tutorial?')
        f.write("tryLeaveMap res: %r\n" % res)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
