# Discovery: import every ui.UI* screen module referenced by loaded code (class definitions only)
# and report code that references hall-scene loading. No game methods are called.
import sys, types, re
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
names = set(); seen = set()
def collect(co, depth=0):
    if depth > 6 or id(co) in seen: return
    seen.add(id(co))
    for c in co.co_consts:
        if isinstance(c, str) and re.match(r'^UI[A-Z]\w{2,40}$', c): names.add(c)
        elif isinstance(c, types.CodeType): collect(c, depth + 1)
for mname, mod in list(sys.modules.items()):
    if mod is None: continue
    try:
        for v in list(vars(mod).values()):
            if isinstance(v, types.FunctionType): collect(v.func_code)
            elif isinstance(v, (type, types.ClassType)):
                for mv in v.__dict__.values():
                    fc = getattr(mv, 'func_code', None)
                    if fc is not None: collect(fc)
    except Exception: pass
w('UI names referenced: %d' % len(names))
NEED = ('loadHallScene', 'HALL_MAP_ID')
ok = 0
def walk(co, path, depth=0):
    if depth > 5: return
    hit = [n for n in NEED if n in co.co_names]
    if hit: w('HIT %s %s' % (path, hit))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): walk(c, path + '.' + c.co_name, depth + 1)
for n in sorted(names):
    m = 'ui.' + n
    if m not in sys.modules:
        try: __import__(m); ok += 1
        except Exception: continue
    mod = sys.modules.get(m)
    if mod is None: continue
    for k, v in vars(mod).items():
        if isinstance(v, (type, types.ClassType)) and getattr(v, '__module__', None) == m:
            for mk, mv in v.__dict__.items():
                fc = getattr(mv, 'func_code', None)
                if fc is not None: walk(fc, '%s.%s.%s' % (m, k, mk))
        elif isinstance(v, types.FunctionType) and v.__module__ == m:
            walk(v.func_code, '%s.%s' % (m, k))
w('newly imported: %d' % ok)
f.close()
