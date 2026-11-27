import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:1500] + '\n')
try:
    cu = sys.modules['currency_utils']
    for a in sorted(dir(cu)):
        if a.startswith('_'): continue
        v = getattr(cu, a)
        if isinstance(v, (int, long)) and not isinstance(v, bool):
            w('currency_utils.%s = %r' % (a, v))
    lp = sys.modules['dts_appearance_utils'].legacyProperties
    w('lp funcs: %r' % ([a for a in dir(lp) if 'HallProp' in a][:10],))
    it = lp.iterDtsHallPropData
    w('iter sig ok %r' % (it,))
except Exception:
    w(traceback.format_exc())
f.close()
