with open(OUT, 'w') as f:
    try:
        import sys, dis, StringIO
        mod = sys.modules.get('ui.UISkipTutorial')
        cls = getattr(mod, 'UISkipTutorial', None)
        meth = getattr(cls, 'tryLeaveMap', None)
        f.write('meth: ' + repr(meth) + '\n')
        co = meth.im_func.func_code
        f.write('consts: ' + repr(co.co_consts) + '\n')
        f.write('names: ' + repr(co.co_names) + '\n')
        # Check nested code objects
        for c in co.co_consts:
            if hasattr(c, 'co_code'):
                f.write('nested code: name=%s, consts=%r, names=%r\n' % (c.co_name, c.co_consts, c.co_names))
                buf = StringIO.StringIO()
                old = sys.stdout; sys.stdout = buf
                dis.dis(c)
                sys.stdout = old
                f.write('disassembly:\n' + buf.getvalue() + '\n')
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
