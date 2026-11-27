f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/tlm_args.txt", "w")
try:
    import ui.UISkipTutorial
    fn = ui.UISkipTutorial.UISkipTutorial.tryLeaveMap.im_func
    f.write("co_varnames: %r\n" % (fn.func_code.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
