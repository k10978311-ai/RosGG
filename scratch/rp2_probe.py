import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:900] + '\n')
try:
    import dis
    um = sys.modules.get('ui.UIMain')
    cls = um.UIMain
    fn = cls.showRedPoint
    fn = getattr(fn, 'im_func', fn)
    c = fn.func_code
    w('names %r' % (c.co_names,))
    w('consts %r' % (c.co_consts,))
    w('varnames %r argcount %r' % (c.co_varnames, c.co_argcount))
    w('firstline %r' % c.co_firstlineno)
except Exception:
    w(traceback.format_exc())
f.close()
