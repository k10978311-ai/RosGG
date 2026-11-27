f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/cb_tlm.txt", "w")
try:
    import ui.UISkipTutorial
    fn = ui.UISkipTutorial.UISkipTutorial.tryLeaveMap.im_func
    for c in fn.func_code.co_consts:
        if hasattr(c, 'co_names'):
            f.write("code: %s, co_names=%r, co_consts=%r\n" % (
                c.co_name, c.co_names, [x for x in c.co_consts if not hasattr(x, 'co_names')]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
