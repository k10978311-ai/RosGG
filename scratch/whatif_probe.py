import sys, types, traceback, itertools
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    CE = sys.modules['entities.ClientEntity'] if 'entities.ClientEntity' in sys.modules else sys.modules['ClientEntity']
    cls = CE.ClientEntity
    fn = cls.__dict__['prerequisites']
    fn = getattr(fn, '__func__', fn)
    realG = CE.__dict__ if hasattr(CE,'__dict__') else fn.func_globals
    G0 = fn.func_globals
    w('globals Globals=%r Application=%r switches=%r' % (G0.get('Globals'), G0.get('Application'), G0.get('switches')))
    # find a live Athlete-like self
    import BigWorld
    class Fake(object):
        prerequisiteReady = False; useFlowControl = False; underFlowControl = False; allowToEnterWorld = False; mapID = 0
        def isEnterOnPlane(self): return True
        def isWaitingPreload(self): return False
    p = Fake()
    w('player=%r' % (p,))
    class Obj(object): pass
    def run(scene, gplayer, stage1, inloading, mapid):
        G = dict(G0)
        Gl = Obj(); Gl.inLoadingStage1 = stage1; Gl.inLoading = inloading; Gl.MAP_ID = mapid; Gl.player = gplayer
        Gl.entityFlowControl = None
        Ap = Obj(); Ap.scene = scene
        G['Globals'] = Gl; G['Application'] = Ap
        g2 = types.FunctionType(fn.func_code, G, fn.func_name, fn.func_defaults, fn.func_closure)
        try: return g2(p)
        except Exception as e: return 'EXC %r' % (e,)
    S = object()
    for scene in (None, S):
        for gp in (None, S):
            for st in (False,):
                for il in (False, True):
                    for mid in (-1, 0, 20, 701):
                        w('scene=%s gplayer=%s stage1=%s inLoading=%s MAP_ID=%s -> %r' % ('S' if scene else 'None', 'S' if gp else 'None', st, il, mid, run(scene, gp, st, il, mid)))
except Exception:
    w(traceback.format_exc())
f.close()
