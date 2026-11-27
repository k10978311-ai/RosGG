# READ-ONLY: names/consts of ui.UILoginLoop and MapLoader-related functions.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def cs(co, path, depth=0):
    if depth > 3: return
    w('%s%s names=%s consts=%r' % ('  ' * depth, path, list(co.co_names)[:60], [c for c in co.co_consts if isinstance(c, (str, int, float)) and not isinstance(c, bool)][:20]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): cs(c, c.co_name, depth + 1)
def dump(mname, filt=None):
    mod = sys.modules.get(mname)
    if mod is None: w('## %s NOT LOADED' % mname); return
    w('## %s' % mname)
    for k, v in sorted(vars(mod).items()):
        if isinstance(v, (type, types.ClassType)) and getattr(v, '__module__', None) == mname:
            for mk, mv in sorted(v.__dict__.items()):
                fn = getattr(mv, 'func_code', None)
                if fn is not None and (filt is None or any(x in mk.lower() for x in filt)): cs(fn, k + '.' + mk)
        elif isinstance(v, types.FunctionType) and v.__module__ == mname and (filt is None or any(x in k.lower() for x in filt)):
            cs(v.func_code, k)
dump('ui.UILoginLoop')
w('MapLoader-ish modules: %s' % sorted(m for m in sys.modules if 'maploader' in m.lower() or 'map_loader' in m.lower()))
for m in sorted(sys.modules):
    if 'maploader' in m.lower(): dump(m, ('load', 'scene', 'enter', 'hall', 'login'))
f.close()
