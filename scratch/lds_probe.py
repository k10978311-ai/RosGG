import sys, types, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def info(fn, tag):
    co = fn.func_code
    w('== %s args=%r\n names=%r\n consts=%r' % (tag, co.co_varnames[:co.co_argcount], list(co.co_names), [repr(c)[:50] for c in co.co_consts]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): w('  inner %s names=%r consts=%r' % (c.co_name, list(c.co_names), [repr(x)[:40] for x in c.co_consts]))
try:
    import Globals
    info(Globals.loadDefaultScene, 'Globals.loadDefaultScene')
    for n in ('loadScene','loadLoginScene','getLoginScene','enterLoginScene'):
        if hasattr(Globals, n): info(getattr(Globals, n), 'Globals.'+n)
    ss = sys.modules['libclaudia.Classes.SceneSystem'].SceneSystem
    for n in ('LoadNeoxScene','Awake','_SceneSystem__loadGame','loadMap','loadHallScene'):
        fn = ss.__dict__.get(n)
        if fn: info(fn, 'SceneSystem.'+n)
except Exception:
    w(traceback.format_exc())
f.close()
