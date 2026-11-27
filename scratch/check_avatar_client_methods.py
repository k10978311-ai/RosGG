import sys, os
sys.path.insert(0, 'extract')
import bwdefs
D = bwdefs.Defs()
methods = D.client_method_table('BattleGroundAvatar')
for i, m in enumerate(methods):
    if any(k in m[0].lower() for k in ('leave', 'hall', 'lobby', 'scene', 'quit', 'exit', 'kick', 'return', 'gameover', 'settle', 'result')):
        print(f'[{i}] {m[0]}: {m[1]}')
