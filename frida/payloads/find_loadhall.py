# READ-ONLY: find code objects (in all loaded modules) referencing given names.
import sys, types
NEEDLES = ['loadHallScene']
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
seen = set()
def walk(co, path, depth=0):
    if depth > 6 or id(co) in seen: return
    seen.add(id(co))
    if any(n in co.co_names for n in NEEDLES):
        w('HIT %s names=%s consts=%r' % (path, list(co.co_names)[:50], [c for c in co.co_consts if isinstance(c, (str, int)) and not isinstance(c, bool)][:20]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): walk(c, path + '.' + c.co_name, depth + 1)
def scan(obj, path, depth=0):
    if depth > 3: return
    if isinstance(obj, types.FunctionType): walk(obj.func_code, path)
    elif isinstance(obj, (type, types.ClassType)):
        for k, v in list(obj.__dict__.items()):
            fn = getattr(v, 'func_code', None)
            if fn is not None: walk(fn, path + '.' + k)
            elif isinstance(v, (type, types.ClassType)): scan(v, path + '.' + k, depth + 1)
for mname, mod in sorted(sys.modules.items()):
    if mod is None: continue
    try:
        for k, v in list(vars(mod).items()):
            if getattr(v, '__module__', None) == mname: scan(v, mname + ':' + k)
    except Exception: pass
f.close()
