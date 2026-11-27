# READ-ONLY introspection payload: report the current player entity and its properties.
import sys
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import BigWorld
p = BigWorld.player()
w('player=%r' % (p,))
if p is not None:
    w('class=%s module=%s id=%r' % (p.__class__.__name__, p.__class__.__module__, getattr(p, 'id', None)))
    w('MRO=%s' % [c.__name__ for c in p.__class__.__mro__][:20])
    for k in ('playerUUID', 'playerName', 'bindedPlayerName', 'identifierName', 'baseNickname', 'gid', 'isMobileAccount'):
        try:
            w('  %s=%r' % (k, getattr(p, k)))
        except Exception as e:
            w('  %s: ERR %r' % (k, e))
w('entities=%r' % (dict(BigWorld.entities.items()),))
w('modules Account*/Login*: %s' % sorted(m for m in sys.modules if m.split('.')[-1].startswith(('Account', 'PlayerAccount', 'LoginProxy'))))
f.close()
