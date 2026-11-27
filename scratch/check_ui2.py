import Globals
f = open(OUT, 'w')
um = Globals.uiMgr
f.write('uiMgr attrs: %r\n' % [a for a in dir(um) if not a.startswith('__')])
for a in dir(um):
    if 'ui' in a.lower():
        v = getattr(um, a, None)
        if isinstance(v, dict):
            f.write('  dict %s: %r\n' % (a, v.keys()))
f.close()
