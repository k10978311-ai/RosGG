import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    A = sys.modules['libclaudia.Classes.Application'].Application
    cl = A.____current_level__
    objs = cl.GetAllSubObjects()
    w('subobjs=%r' % (objs,))
    for o in objs:
        w('obj %r name=%r attrs=%r' % (o, getattr(o,'name',None), [a for a in dir(o) if not a.startswith('__')][:40]))
        try: w('  comps=%r' % (o.GetComponents() if hasattr(o,'GetComponents') else 'nofn'))
        except Exception as e: w('  comps err %r' % e)
        try: w('  SceneSystem=%r' % (o.GetComponent('SceneSystem'),))
        except Exception as e: w('  ss err %r' % e)
    m = sys.modules['libclaudia.Classes.SceneSystem']
    w('SceneSystem module attrs: %r' % [a for a in dir(m) if not a.startswith('__')])
    S = getattr(m, 'Scene', None)
    if S: w('Scene.__dict__: %r' % sorted(S.__dict__.keys()))
    SS = m.SceneSystem
    w('SceneSystem funcs: %r' % sorted(k for k in SS.__dict__.keys() if not k.startswith('__'))[:80])
except Exception:
    w(traceback.format_exc())
f.close()
