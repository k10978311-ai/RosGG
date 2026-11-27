import sys, os
sys.path.insert(0, 'extract')
from elf import ELF
PATH = 'extract/libclient.so'
e = ELF(PATH); d = e.d
idx = d.find(b'iProxyNoCell')
print('iProxyNoCell:', idx)
