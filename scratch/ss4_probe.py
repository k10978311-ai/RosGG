import sys, types, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
KEYS = set(['onHandshake','reconnectMapID','MapLoader','onLoadMap','onReconnect'])
seen = set(); hits = []
def walk(co, path, d=0):
    if d > 8 or id(co) in seen: return
    seen.add(id(co))
    k = KEYS & set(co.co_names)
    if k: hits.append('%s file=%s line=%d keys=%s' % (path, co.co_filename, co.co_firstlineno, sorted(k)))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): walk(c, path + '.' + c.co_name, d + 1)
def scan(obj, path, d=0, vis=None):
    if d > 4: return
    if vis is None: vis = set()
    if id(obj) in vis: return
    vis.add(id(obj))
    if isinstance(obj, (staticmethod, classmethod)): obj = obj.__func__
    if isinstance(obj, property):
        for g in (obj.fget, obj.fset):
            if g: scan(g, path, d+1, vis)
        return
    fn = getattr(obj, 'func_code', None)
    if fn is not None: walk(fn, path); return
    if isinstance(obj, types.CodeType): walk(obj, path); return
    if isinstance(obj, (type, types.ClassType)):
        for k, v in list(obj.__dict__.items()): scan(v, path + '.' + k, d + 1, vis)
try:
    for mname, mod in sorted(sys.modules.items()):
        if mod is None: continue
        try:
            for k, v in list(vars(mod).items()): scan(v, mname + ':' + k)
        except Exception: pass
    for h in sorted(set(hits)): w(h)
except Exception:
    w(traceback.format_exc())
w('done %d' % len(hits))
f.close()
