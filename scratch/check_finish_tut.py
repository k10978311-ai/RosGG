import sys, os
sys.path.insert(0, 'extract')
import bwdefs
D = bwdefs.Defs()
methods = D.methods('BattleGroundAvatar', 'BaseMethods')
for i, m in enumerate(methods):
    if 'tutorial' in m[0].lower():
        print(f'[{i}] {m[0]}: {m[1]}')
