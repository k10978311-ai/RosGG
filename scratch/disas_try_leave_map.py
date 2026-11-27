f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/dis_tlm.txt", "w")
try:
    import ui.UISkipTutorial, dis, sys, StringIO
    fn = ui.UISkipTutorial.UISkipTutorial.tryLeaveMap.im_func
    f.write("co_names: %r\n" % (fn.func_code.co_names,))
    f.write("co_consts: %r\n" % ([x for x in fn.func_code.co_consts if not hasattr(x, 'co_names')],))
    old_stdout = sys.stdout
    sys.stdout = s = StringIO.StringIO()
    dis.dis(fn)
    sys.stdout = old_stdout
    f.write("dis:\n" + s.getvalue())
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
