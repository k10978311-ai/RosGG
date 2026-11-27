# READ-ONLY: Application / SceneSystem state.
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import ClientEntity, sys
App = vars(ClientEntity).get('Application')
w('Application type=%r' % (type(App),))
for a in sorted(dir(App)):
    if a.startswith('__'): continue
    try:
        v = getattr(App, a)
        if not callable(v): w('  App.%s=%r' % (a, v if len(repr(v)) < 160 else repr(v)[:160]))
    except Exception as e:
        w('  App.%s ERR %r' % (a, e))
SS = sys.modules.get('libclaudia.Classes.SceneSystem')
w('SceneSystem module=%r' % (SS,))
try:
    import GameObject as GO
except Exception:
    GO = None
try:
    from libclaudia.Classes.GameObject import GameObject
    s = GameObject.Find('Scene')
    w('GameObject.Find(Scene)=%r' % (s,))
    if s is not None:
        comp = s.GetComponent('SceneSystem')
        w('SceneSystem comp=%r' % (comp,))
        for a in sorted(dir(comp)):
            if a.startswith('_') and not a.startswith('_scene'): continue
            try:
                v = getattr(comp, a)
                if not callable(v): w('  SS.%s=%r' % (a, v if len(repr(v)) < 160 else repr(v)[:160]))
            except Exception: pass
except Exception as e:
    w('GameObject err %r' % (e,))
f.close()
