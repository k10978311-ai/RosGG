"""Search the whole binary for an 8-byte little-endian literal equal to a string's vaddr
(literal-pool reference), then disassemble around each literal-pool site."""
import struct, sys
from elf import ELF
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN

PATH = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
e = ELF(PATH); d = e.d

marker = sys.argv[1] if len(sys.argv) > 1 else "Got corrupted message header"
si = d.find(marker.encode())
st = d.rfind(b"\x00", 0, si) + 1
sva = e.off_to_vaddr(st)
print(f"string va {hex(sva)}: {d[st:st+50]!r}")

needle = struct.pack("<Q", sva)
text = e.sec(".text"); tlo, thi = text["offset"], text["offset"]+text["size"]
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)

i = 0; found = 0
while True:
    i = d.find(needle, i)
    if i < 0: break
    va = e.off_to_vaddr(i)
    insec = next((s["sname"] for s in e.secs if s["addr"] and s["type"]!=8 and s["addr"]<=va<s["addr"]+s["size"]), "?")
    print(f"\nliteral@ off {hex(i)} va {hex(va)} (section {insec})")
    found += 1
    # if the literal is inside .text, disassemble an LDR that loads it (PC-relative within +-1MB)
    if tlo <= i < thi:
        # find a preceding/following LDR literal referencing this address
        for probe in range(max(tlo, i-0x100000), min(thi, i+0x100000), 4):
            w = struct.unpack_from("<I", d, probe)[0]
            if (w & 0x3B000000) == 0x18000000 and (w & 0xFF000000) in (0x58000000,):  # LDR (literal) 64-bit
                imm19 = (w >> 5) & 0x7FFFF
                if imm19 & 0x40000: imm19 -= 0x80000
                pva = e.off_to_vaddr(probe)
                if pva + imm19*4 == va:
                    print(f"  LDR literal at {hex(pva)} loads it; disasm:")
                    start = probe - 20*4
                    for ins in md.disasm(d[start:probe+8*4], e.off_to_vaddr(start)):
                        mk = " <<<" if ins.address == pva else ""
                        print(f"    {hex(ins.address)}: {ins.mnemonic:8} {ins.op_str}{mk}")
                    break
    i += 8
print(f"\ntotal literals: {found}")
