import sys, traceback, json
f = open(OUT, 'w')
def simple(v):
    if isinstance(v, (int, long, float, bool, type(None))): return v
    if isinstance(v, (str, unicode)):
        try: return v.decode('utf-8') if isinstance(v, str) else v
        except Exception: return repr(v)
    return None
def attrs(o):
    r = {}
    for a in dir(o):
        if a.startswith('_'): continue
        try: v = getattr(o, a)
        except Exception: continue
        if callable(v): continue
        if isinstance(v, (list, tuple)) and all(isinstance(x, (int, long, float)) for x in v): r[a] = list(v)
        elif isinstance(v, dict) and all(isinstance(k, (int, long)) and isinstance(x, (int, long, float)) for k, x in v.items()): r[a] = dict((str(k), x) for k, x in v.items())
        else:
            s = simple(v)
            if s is not None or v is None: r[a] = s
    return r
try:
    su = sys.modules['supplement_utils']
    d = su.getAvailableSupplementDictByTime()
    out = {}
    for sid, o in d.items():
        a = attrs(o)
        try:
            co = o.CURRENCY_OPTION
            a['_CO'] = attrs(co); a['_COT'] = type(co).__name__
        except Exception: pass
        a['_T'] = type(o).__name__
        out[str(sid)] = a
    f.write(json.dumps(out))
except Exception:
    f.write('ERR ' + traceback.format_exc())
f.close()
