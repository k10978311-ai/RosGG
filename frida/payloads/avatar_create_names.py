# READ-ONLY: Avatar post-enter functions (names + line ranges)
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
cands = [n for n, m in sys.modules.items() if m and (n == 'Avatar' or n.endswith('.Avatar'))]
w('modules %s' % cands)
for mn in cands:
    m = sys.modules[mn]
    for k, v in sorted(m.__dict__.items()):
        if isinstance(v, (type, types.ClassType)) and getattr(v, '__module__', '') == mn:
            for a in ('afterEnterSpace', '_createPlayer', '_createPlayerGO', 'onEnterSpace', 'onEnterWorld', '_onPlayerGOCreated', 'onPlayerGOLoaded'):
                if a in v.__dict__:
                    fn = unwrap(v.__dict__[a]); co = fn.func_code
                    w('%s.%s.%s L%d vars=%s\n   names=%s' % (mn, k, a, co.co_firstlineno, list(co.co_varnames), list(co.co_names)))
f.close()
