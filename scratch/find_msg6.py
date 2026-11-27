import sys, os
sys.path.insert(0, 'extract')
from elf import ELF
PATH = 'extract/libclient.so'
e = ELF(PATH); d = e.d
# Search for strings relating to createCellPlayer
for s in [b'createCellPlayer', b'createBasePlayer', b'onCellPlayerCreate', b'onBasePlayerCreate']:
    idx = d.find(s)
    if idx >= 0:
        va = e.off_to_vaddr(idx)
        print(f'{s.decode()} found at {hex(va)}')
