import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:700] + '\n')
try:
    u = sys.modules['dts_appearance_utils']
    for fn in ('getBodyAppearanceData','getWearableAppearanceData','getDtsBodyAppearanceGender'):
        g = getattr(u, fn).func_globals if hasattr(getattr(u, fn),'func_globals') else {}
        w('%s co_names=%r' % (fn, getattr(getattr(u, fn),'func_code',None) and getattr(u, fn).func_code.co_names))
    # scan modules for large dicts keyed by int with dict values having 'gender'
    import types
    for mn, m in list(sys.modules.items()):
        if m is None or not any(s in mn.lower() for s in ('appearance','dress','body','wear')): continue
        for a in dir(m):
            try: v = getattr(m, a)
            except Exception: continue
            if isinstance(v, dict) and len(v) > 40:
                k = next(iter(v)); w('%s.%s dict len=%d k=%r v=%r' % (mn, a, len(v), k, v[k]))
except Exception:
    w(traceback.format_exc())
f.close()
