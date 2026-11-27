import sys, os
sys.path.insert(0, 'extract')
import bwdefs
D = bwdefs.Defs()
print('Athlete files:', D.files.get('Athlete'))
txt = D.text('Athlete')
print('Athlete def head:\n', txt[:500])
