# READ-ONLY: where does PlayerAthlete.prerequisites resolve, and what does the gate see now?
import types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import BigWorld, Globals, ClientEntity
p = BigWorld.player()
w('player=%r' % (p,))
for cls in type(p).__mro__:
    if 'prerequisites' in cls.__dict__:
        w('prerequisites defined in %s (%s)' % (cls.__name__, cls.__module__)); break
App = vars(ClientEntity).get('Application')
w('scene=%r Globals.player=%r inLoadingStage1=%r inLoading=%r MAP_ID=%r' % (getattr(App, 'scene', '?'), Globals.player, Globals.inLoadingStage1, Globals.inLoading, Globals.MAP_ID))
w('prerequisiteReady=%r mapID=%r' % (getattr(p, 'prerequisiteReady', '?'), getattr(p, 'mapID', '<none>')))
try:
    w('isWaitingPreload()=%r' % (p.isWaitingPreload(),))
except Exception as e:
    w('isWaitingPreload err %r' % (e,))
f.close()
