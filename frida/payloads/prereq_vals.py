# READ-ONLY: values consulted by ClientEntity.prerequisites, via its module globals.
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import ClientEntity
g = vars(ClientEntity)
App = g.get('Application'); G = g.get('Globals'); sw = g.get('switches')
w('Application=%r scene=%r' % (App, getattr(App, 'scene', '<missing>')))
w('Globals.player=%r' % (getattr(G, 'player', '<missing>'),))
w('switches.SysEnablePlaneNoEnterWorld=%r SysEnableEntityFlowControl=%r' % (getattr(sw, 'SysEnablePlaneNoEnterWorld', '?'), getattr(sw, 'SysEnableEntityFlowControl', '?')))
f.close()
