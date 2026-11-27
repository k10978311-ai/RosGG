import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    c = sys.modules['const'] if 'const' in sys.modules else __import__('const')
    for k in dir(c):
        if 'INACTIVE' in k.upper(): w('%s = %r' % (k, getattr(c, k)))
    sw = sys.modules['shared.switches']
    for k in dir(sw):
        if 'INACTIV' in k.upper(): w('switch %s = %r' % (k, getattr(sw, k)))
except Exception:
    w(traceback.format_exc())
f.close()
