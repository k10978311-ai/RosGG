import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:500] + '\n')
try:
    import Globals
    u = sys.modules['dts_appearance_utils']
    w('utils.legacyProperties = %r' % (getattr(u, 'legacyProperties', 'MISSING'),))
    w('Globals.legacyProperties = %r' % (getattr(Globals, 'legacyProperties', 'MISSING'),))
    holders = []
    for k, m in list(sys.modules.items()):
        if m is not None and hasattr(m, 'legacyProperties'):
            v = getattr(m, 'legacyProperties')
            holders.append((k, v is None))
    w('modules with legacyProperties attr: %d, None in %d' % (len(holders), sum(1 for k, n in holders if n)))
    nn = [k for k, n in holders if not n]
    w('non-None holders: %r' % (nn[:15],))
    if nn:
        v = getattr(sys.modules[nn[0]], 'legacyProperties')
        w('example value %r attrs %r' % (v, [a for a in dir(v) if not a.startswith('__')][:25]))
    w('lp module in sys.modules: %r' % [k for k in sys.modules if 'legacy' in k.lower()])
except Exception:
    w(traceback.format_exc())
f.close()
