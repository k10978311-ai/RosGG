# READ-ONLY: names used by MapLoader + Avatar post-load functions
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def unwrap(fn):
    fn = getattr(fn, '__func__', fn)
    while isinstance(fn, types.FunctionType) and fn.func_closure:
        nxt = [c.cell_contents for c in fn.func_closure if isinstance(getattr(c, 'cell_contents', None), types.FunctionType)]
        if not nxt: break
        fn = nxt[0]
    return fn
for mn in ('helpers.MapLoader', 'entities.Avatar'):
    m = sys.modules[mn]
    for k, v in sorted(m.__dict__.items()):
        if isinstance(v, (type, types.ClassType)) and v.__module__ == mn:
            w('class %s.%s' % (mn, k))
            for a, x in sorted(v.__dict__.items()):
                fn = unwrap(x)
                if not isinstance(fn, types.FunctionType): continue
                if mn == 'helpers.MapLoader' or a in ('afterEnterSpace', '_createPlayer', 'onEnterWorld', 'onBecomePlayer', 'set_mapID', 'onSceneLoaded', 'onLoadFinish'):
                    co = fn.func_code
                    w('  %s L%d %s' % (a, co.co_firstlineno, list(co.co_names)[:30]))
f.close()
