# READ-ONLY: query BigWorld getter state (no setters, no game logic).
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import BigWorld
for name in ('player', 'online', 'server', 'prereqEntities', 'unknownEntities', 'cachedEntities', 'controlledEntities', 'getEntityDefsMd5', 'serverTime', 'getInactivityTimeout'):
    try:
        v = getattr(BigWorld, name)
        r = v() if callable(v) else v
        try:
            r = dict(r.items()) if hasattr(r, 'items') else r
        except Exception:
            pass
        w('%s -> %r' % (name, r))
    except Exception as e:
        w('%s -> EXC %r' % (name, e))
f.close()
