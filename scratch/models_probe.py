import sys, traceback, gc
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    found = 0
    for o in gc.get_objects():
        try:
            if type(o).__name__ == 'UIMain' and hasattr(o, 'models'):
                found += 1
                w('UIMain obj %r' % (o,))
                m = o.models
                w('models type %r len %r' % (type(m), len(m)))
                for k, v in m.items():
                    w('  key %r -> %r' % (k, v if not isinstance(v, dict) else dict((a, repr(b)[:80]) for a, b in v.items())))
                for a in ('gid','myGid','selfGid'):
                    if hasattr(o, a): w('  %s=%r' % (a, getattr(o, a)))
        except Exception:
            pass
    w('found=%d' % found)
except Exception:
    w(traceback.format_exc())
f.close()
