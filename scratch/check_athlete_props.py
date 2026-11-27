import sys, os
sys.path.insert(0, 'extract')
import bwdefs
D = bwdefs.Defs()
base_props = D.base_client_props('Athlete')
print('Athlete base props with map:', [p for p in base_props if 'map' in p[0].lower()])
cell_props = D.cell_own_client_props('Athlete')
print('Athlete cell props:', cell_props)
cell_avatar = D.cell_own_client_props('BattleGroundAvatar')
print('BattleGroundAvatar cell props with map:', [p for p in cell_avatar if 'map' in p[0].lower()])
