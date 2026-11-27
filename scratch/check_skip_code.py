f = open(OUT, 'w')
try:
    import Globals, dis, StringIO, sys
    ui = Globals.uiMgr.get_ui_by_name('UISkipTutorial')
    f.write('ui: %r
' % (ui,))
    if ui:
        fn = getattr(ui, 'tryLeaveMap', None) or getattr(ui, 'onExitBtnEvent', None)
        f.write('fn: %r
' % (fn,))
        if fn:
            buf = StringIO.StringIO()
            old = sys.stdout; sys.stdout = buf
            dis.dis(fn)
            sys.stdout = old
            f.write(buf.getvalue() + '
')
            for c in fn.func_code.co_consts:
                if hasattr(c, 'co_names'):
                    buf = StringIO.StringIO()
                    old = sys.stdout; sys.stdout = buf
                    dis.dis(c)
                    sys.stdout = old
                    f.write('sub %s:
%s
' % (c.co_name, buf.getvalue()))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
