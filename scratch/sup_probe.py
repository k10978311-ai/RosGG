import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    lp = sys.modules['dts_appearance_utils'].legacyProperties
    w('lp supplement funcs: %r' % ([a for a in dir(lp) if 'upplement' in a],))
    su = sys.modules.get('supplement_utils')
    w('supplement_utils funcs: %r' % ([a for a in dir(su) if not a.startswith('_')][:80],))
except Exception:
    w(traceback.format_exc())
f.close()
