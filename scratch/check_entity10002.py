import BigWorld, Globals
f = open(OUT, 'w')
f.write('BigWorld.entities keys: %r\n' % list(BigWorld.entities.keys()))
for eid in (10001, 10002, 10003):
    e = BigWorld.entities.get(eid)
    f.write('  entity %d: %r (class=%s)\n' % (eid, e, e.__class__.__name__ if e else 'None'))
    if e:
        f.write('    dir: %r\n' % [a for a in dir(e) if not a.startswith('__')][:30])
f.close()
