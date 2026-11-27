# READ-ONLY: disassemble ClientEntity.prerequisites and read the globals it consults.
import sys, dis, StringIO
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import ClientEntity, BigWorld
fn = ClientEntity.ClientEntity.__dict__['prerequisites']
buf = StringIO.StringIO()
old = sys.stdout; sys.stdout = buf
try:
    dis.dis(fn)
finally:
    sys.stdout = old
w(buf.getvalue())
p = BigWorld.player()
w('player.prerequisiteReady=%r' % (getattr(p, 'prerequisiteReady', '<missing>'),))
import Globals
for k in ('inLoadingStage1', 'inLoading', 'MAP_ID'):
    w('Globals.%s=%r' % (k, getattr(Globals, k, '<missing>')))
try:
    import Application
    w('Application.scene=%r' % (getattr(Application, 'scene', '<missing>'),))
except Exception as e:
    w('Application import err %r' % (e,))
w('player.mapID=%r isWaitingPreload=%r' % (getattr(p, 'mapID', '<missing>'), getattr(p, 'isWaitingPreload', '<missing>')))
f.close()
