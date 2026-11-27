# READ-ONLY introspection payload: dump the Account client module (names/consts only).
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def cs(co, path, depth=0):
    if depth > 4: return
    strs = [c for c in co.co_consts if isinstance(c, str) and len(c) < 100]
    w('%s%s(%s) names=%s strs=%s' % ('  ' * depth, path, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names)[:70], strs[:25]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): cs(c, c.co_name, depth + 1)
w('Account-ish modules: %s' % sorted(m for m in sys.modules if m.split('.')[-1] in ('Account', 'PlayerAccount', 'LoginProxy') or m.startswith('Account')))
mod = sys.modules.get('Account')
if mod is None:
    w('Account NOT LOADED')
else:
    w('file=%s' % getattr(mod, '__file__', '?'))
    for k, v in sorted(vars(mod).items()):
        if isinstance(v, (type, types.ClassType)) and getattr(v, '__module__', None) == 'Account':
            w('class %s bases=%s' % (k, [b.__name__ + '@' + getattr(b, '__module__', '?') for b in v.__bases__]))
            for mk, mv in sorted(v.__dict__.items()):
                fn = getattr(mv, 'func_code', None)
                if fn is not None: cs(fn, k + '.' + mk, 1)
        elif isinstance(v, types.FunctionType) and v.__module__ == 'Account':
            cs(v.func_code, k)
f.close()
