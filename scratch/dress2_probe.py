import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    for mn in ('dts_appearance_utils','dts_appearance.const'):
        m = sys.modules.get(mn)
        names = [a for a in dir(m) if not a.startswith('__')]
        w('== %s (%d)' % (mn, len(names)))
        w(', '.join(n for n in names if any(s in n.lower() for s in ('default','init','gender','male','body','wear','born','new'))))
    for k in sys.modules:
        if k.startswith('data.') and any(s in k.lower() for s in ('appearance','dress','skin','cloth')):
            w('data mod ' + k)
except Exception:
    w(traceback.format_exc())
f.close()
