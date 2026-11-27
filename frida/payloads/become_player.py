# READ-ONLY: names used by onBecomePlayer/onEnterWorld/afterEnterWorld across all entity modules (unwrapping decorators).
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
TARGETS = ('onBecomePlayer', 'onEnterWorld', 'afterEnterWorld', 'onBecomeNonPlayer', 'enterWorld')
def inner(fn, depth=0):
    out = [fn]
    if depth < 3:
        for cell in (getattr(fn, 'func_closure', None) or ()):
            try: v = cell.cell_contents
            except ValueError: continue
            if isinstance(v, types.FunctionType): out += inner(v, depth + 1)
    return out
seen = set()
for mname, mod in sorted(sys.modules.items()):
    if mod is None: continue
    for cname, cls in list(vars(mod).items()):
        if not isinstance(cls, (type, types.ClassType)) or getattr(cls, '__module__', None) != mname: continue
        for t in TARGETS:
            fn = cls.__dict__.get(t)
            if not isinstance(fn, types.FunctionType) or id(fn) in seen: continue
            seen.add(id(fn))
            for g in inner(fn):
                n = g.func_code.co_names
                if 'Globals' in n and 'player' in n:
                    w('%s.%s.%s[%s] names=%s' % (mname, cname, t, g.__name__, list(n)[:40]))
f.close()
