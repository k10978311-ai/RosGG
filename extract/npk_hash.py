"""NeoX NXPK file-name hash, executed straight from libclient.so under Unicorn.

The NPK index (28-byte entries, sorted by sign) is looked up with the u32 returned by
libclient+0x1d173d4 (C-string variant; 0x1d179f8 tail-calls it). The function is a
self-contained leaf (registers only), so we map its code and run it on a string.

    python npk_hash.py "entities/defs/Athlete.def" ...
"""
import os, struct, sys
from unicorn import Uc, UC_ARCH_ARM64, UC_MODE_ARM
from unicorn.arm64_const import UC_ARM64_REG_X0, UC_ARM64_REG_LR, UC_ARM64_REG_SP

HERE = os.path.dirname(os.path.abspath(__file__))
FN, FN_END = 0x1d173d4, 0x1d175f0

_code = None


def _load():
    global _code
    if _code is None:
        sys.path.insert(0, HERE)
        from elf import ELF
        e = ELF(os.path.join(HERE, "libclient.so"))
        off = e.vaddr_to_off(FN)
        _code = e.d[off:off + (FN_END - FN)]
    return _code


def npk_hash(name):
    code = _load()
    if isinstance(name, str):
        name = name.encode()
    mu = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
    base, data, stack, ret = 0x100000, 0x200000, 0x300000, 0x400000
    mu.mem_map(base, 0x1000 * ((len(code) // 0x1000) + 2))
    mu.mem_write(base, code)
    mu.mem_map(data, 0x10000)
    mu.mem_write(data, name + b"\x00" * 8)
    mu.mem_map(stack, 0x10000)
    mu.mem_map(ret, 0x1000)
    mu.mem_write(ret, b"\x1f\x20\x03\xd5")  # nop
    mu.reg_write(UC_ARM64_REG_X0, data)
    mu.reg_write(UC_ARM64_REG_SP, stack + 0x8000)
    mu.reg_write(UC_ARM64_REG_LR, ret)
    mu.emu_start(base, ret, count=200000)
    return mu.reg_read(UC_ARM64_REG_X0) & 0xFFFFFFFF


if __name__ == "__main__":
    for n in sys.argv[1:]:
        print(f"{npk_hash(n):08x}  {n}")
