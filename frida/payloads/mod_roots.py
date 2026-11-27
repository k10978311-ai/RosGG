# READ-ONLY: top-level module roots + names containing 'oading'
import sys
f = open(OUT, 'w')
roots = {}
for n, m in sys.modules.items():
    if m is None: continue
    r = n.split('.')[0]; roots[r] = roots.get(r, 0) + 1
f.write('%r\n' % sorted(roots.items(), key=lambda x: -x[1])[:60])
f.write('%r\n' % sorted(n for n, m in sys.modules.items() if m and 'oading' in n))
f.close()
