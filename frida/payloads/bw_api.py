# READ-ONLY: list BigWorld module API and docstrings of player/entity related functions.
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import BigWorld
names = [a for a in dir(BigWorld) if not a.startswith('_')]
w('ALL: ' + ' '.join(names))
for a in names:
    if any(k in a.lower() for k in ('player', 'entit', 'type', 'proxy', 'connect', 'server', 'log')):
        doc = (getattr(getattr(BigWorld, a), '__doc__', '') or '').strip().replace('\n', ' ')
        w('%s: %s' % (a, doc[:200]))
f.close()
