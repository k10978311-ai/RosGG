import sys, os
sys.path.insert(0, 'extract')
import bwdefs
D = bwdefs.Defs()
methods = D.methods('Athlete', 'BaseMethods')
print('Athlete base methods count:', len(methods))
for i, m in enumerate(methods):
    if m[0] in ('handshake', 'getGMTable', 'createCharacter', 'enterHall', 'login'):
        print(f'[{i}] {m[0]}: {m[1]}')
