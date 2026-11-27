import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    import BigWorld, Globals
    App = sys.modules['libclaudia.Classes.Application'].Application
    p = BigWorld.player()
    w('player=%s id=%s' % (p.__class__.__name__ if p else None, getattr(p, 'id', None)))
    w('inLoadingStage1=%r scene=%r inLoading=%r MAP_ID=%r Globals.player=%r' % (getattr(Globals,'inLoadingStage1','?'), App.scene, getattr(Globals,'inLoading','?'), getattr(Globals,'MAP_ID','?'), getattr(Globals,'player','?')))
    if p is not None:
        w('p.mapID=%r allowToEnterWorld=%r inWorld=%r hallScene=%r loadCompFinished=%r' % (getattr(p,'mapID','?'), getattr(p,'allowToEnterWorld','?'), getattr(p,'inWorld','?'), getattr(p,'hallScene','?'), getattr(p,'loadCompFinished','?')))
        try: w('isWaitingPreload=%r' % p.isWaitingPreload())
        except Exception as e: w('iwp err %r' % e)
        try: w('prerequisites()=%r' % p.prerequisites())
        except Exception as e: w('pre err %r' % e)
    um = Globals.uiMgr
    w('stack=%r' % getattr(um, '____ui_stack_main__', '?'))
    vis = getattr(um, '_UIMgr____all_ui__vis', {})
    w('visible=%r' % [k for k, v in vis.items() if v][:30])
except Exception:
    w(traceback.format_exc())
f.close()
