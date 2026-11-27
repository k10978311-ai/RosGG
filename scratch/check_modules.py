import sys
f = open(OUT, 'w')
keywords = ['item', 'prop', 'draw', 'lottery', 'lucky', 'skin', 'appear', 'suppl', 'mall', 'shop', 'package', 'repertory']
matched = []
for m in sorted(sys.modules.keys()):
    if any(k in m.lower() for k in keywords):
        matched.append(m)
f.write('Matched modules (%d):\n' % len(matched))
for m in matched:
    f.write('  %s\n' % m)
f.close()
