import traceback, sys
f = open(OUT, 'w')
try:
    import Globals
    fn = getattr(Globals, 'loadDefaultScene', None)
    f.write('loadDefaultScene: %r\n' % fn)
    if fn:
        if hasattr(fn, 'im_func'): fn = fn.im_func
        f.write('fn module: %r\n' % getattr(fn, '__module__', None))
        f.write('fn code: %r\n' % getattr(fn, 'func_code', None))
        f.write('fn globals: %r\n' % [k for k in fn.func_globals.keys() if 'scene' in k.lower()])
except Exception:
    f.write(traceback.format_exc())
f.close()
