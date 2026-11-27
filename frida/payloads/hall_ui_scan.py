# Discovery: import hall UI modules (class definitions only, as the game does on first use) and
# scan their code for hall-scene loading. No game methods are called.
import sys, types, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
NEED = ('loadHallScene', 'HALL_MAP_ID', 'LoadLevelAtFinish', 'hallScene', 'setHallSceneReady', 'enterHall')
for m in ('ui.UISelectMode', 'ui.UIMain', 'ui.UILoading'):
    try:
        __import__(m)
        w('imported %s' % m)
    except Exception:
        w('import %s failed: %s' % (m, traceback.format_exc().splitlines()[-1]))
def walk(co, path, depth=0):
    if depth > 5: return
    hit = [n for n in NEED if n in co.co_names]
    if hit: w('HIT %s %s' % (path, hit))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): walk(c, path + '.' + c.co_name, depth + 1)
for m in ('ui.UISelectMode', 'ui.UIMain', 'ui.UILoading'):
    mod = sys.modules.get(m)
    if mod is None: continue
    for k, v in vars(mod).items():
        if isinstance(v, (type, types.ClassType)) and getattr(v, '__module__', None) == m:
            for mk, mv in v.__dict__.items():
                fn = getattr(mv, 'func_code', None)
                if fn is not None: walk(fn, '%s.%s.%s' % (m, k, mk))
        elif isinstance(v, types.FunctionType) and v.__module__ == m:
            walk(v.func_code, '%s.%s' % (m, k))
f.close()
