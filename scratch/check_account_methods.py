import sys, os
sys.path.insert(0, 'extract')
import bwdefs
D = bwdefs.Defs()
methods = D.client_method_table('Account')
for idx, m in enumerate(methods):
    print(f'[{idx}] {m}')
