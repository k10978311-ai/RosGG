import sys, os
sys.path.insert(0, 'extract')
from elf import ELF
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
PATH = 'extract/libclient.so'
e = ELF(PATH); d = e.d
vaddr = int(sys.argv[1], 16)
n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
off = e.vaddr_to_off(vaddr)
chunk = d[off: off + n*4]
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
for ins in md.disasm(chunk, vaddr):
    print(f'  {hex(ins.address)}: {ins.mnemonic:8} {ins.op_str}')
