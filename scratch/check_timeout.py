import BigWorld, Globals
f = open(OUT, 'w')
for a in dir(BigWorld):
    if any(k in a.lower() for k in ('inactivity', 'timeout', 'network', 'resend')):
        f.write('BW %s: %r\n' % (a, getattr(BigWorld, a)))
gi = getattr(Globals, 'gameInit', None)
f.write('Globals.gameInit: %r\n' % gi)
if gi:
    f.write('  gi attrs: %r\n' % [x for x in dir(gi) if 'timeout' in x.lower() or 'inactivity' in x.lower()])
f.close()
