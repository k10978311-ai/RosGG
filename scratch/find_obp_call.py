import sys, os
sys.path.insert(0, 'extract')
from elf import ELF
PATH = 'extract/libclient.so'
e = ELF(PATH); d = e.d
s = b'onBecomePlayer'
idx = 0
hits = []
while True:
    idx = d.find(s, idx)
    if idx < 0: break
    hits.append(hex(e.off_to_vaddr(idx)))
    idx += len(s)
print('onBecomePlayer hits in libclient.so:', hits)
