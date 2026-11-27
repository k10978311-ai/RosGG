# READ-ONLY: Check Globals and PlayerAthlete hall flags
import sys, traceback

f = open(OUT, 'w')
def w(s): f.write(str(s) + '\n')

w("=== CHECK HALL VARS ===")
try:
    import BigWorld, Globals
    p = BigWorld.player()
    w("player: %r" % (p,))
    if p:
        w("  isInHall: %r" % getattr(p, 'isInHall', '<na>'))
        w("  hallSceneReady: %r" % getattr(p, 'hallSceneReady', '<na>'))
        w("  enterFirstFlag: %r" % getattr(p, 'enterFirstFlag', '<na>'))
        w("  availSupplement: %r" % (len(getattr(p, 'availSupplementDict', {})) if hasattr(p, 'availSupplementDict') else '<na>'))
        w("  luckyCarnivalData: %r" % getattr(p, 'luckyCarnivalData', '<na>'))
        
    for k in ('enterSelectModeFinished', 'isInHall', 'hallSceneReady', 'curScene'):
        w("Globals.%s = %r" % (k, getattr(Globals, k, '<na>')))

    um = getattr(Globals, 'uiMgr', None)
    if um:
        vis = getattr(um, '_UIMgr____all_ui__vis', {})
        w("Visible UIs: %r" % [k for k, v in vis.items() if v])
except Exception:
    w(traceback.format_exc())

w("=== END ===")
f.close()
