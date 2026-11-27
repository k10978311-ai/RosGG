import sys, types, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
KEYS = set(['SetScene','____scene_object__'])
seen = set()
def walk(co, path, d=0):
    if d > 6 or id(co) in seen: return
    seen.add(id(co))
    if KEYS & set(co.co_names) or co.co_name in KEYS:
        w('%s file=%s line=%d names=%r' % (path, co.co_filename, co.co_firstlineno, list(co.co_names)[:40]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): walk(c, path + '.' + c.co_name, d + 1)
def scan(obj, path, d=0):
    if d > 3: return
    fn = getattr(obj, 'func_code', None)
    if fn is not None: walk(fn, path); return
    if isinstance(obj, (type, types.ClassType)):
        for k, v in list(obj.__dict__.items()):
            if isinstance(v, (staticmethod, classmethod)): v = v.__func__
            if isinstance(v, property): 
                for g in (v.fget, v.fset):
                    if g: scan(g, path+'.'+k, d+1)
                continue
            scan(v, path + '.' + k, d + 1)
try:
    for mname, mod in sorted(sys.modules.items()):
        if mod is None: continue
        try:
            for k, v in list(vars(mod).items()):
                if getattr(v, '__module__', None) == mname: scan(v, mname + ':' + k)
        except Exception: pass
    for mn in ():
        m = sys.modules.get(mn)
        if m:
            for cn in ('Player'+mn, mn):
                c = getattr(m, cn, None)
                if c: w('MRO %s: %s' % (cn, [x.__name__ for x in c.__mro__]))
except Exception:
    w(traceback.format_exc())
w('done')
f.close()
