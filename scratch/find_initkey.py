import struct, capstone

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

target_va = 0x2a46eea
target_page = target_va & ~0xFFF
target_lo = target_va & 0xFFF

adrp_matches = []
for pc in range(0, 0x2a00000, 4):
    insn = struct.unpack_from("<I", data, pc)[0]
    if (insn & 0x9F000000) == 0x90000000:
        immlo = (insn >> 29) & 0x3
        immhi = (insn >> 5) & 0x7FFFF
        imm = (immhi << 2) | immlo
        if imm & (1 << 20):
            imm -= (1 << 21)
        pc_page = pc & ~0xFFF
        dest_page = pc_page + (imm << 12)
        if dest_page == target_page:
            rd = insn & 0x1F
            for j in range(1, 4):
                next_insn = struct.unpack_from("<I", data, pc + j*4)[0]
                if (next_insn & 0xFF800000) == 0x91000000:
                    rn = (next_insn >> 5) & 0x1F
                    add_imm = (next_insn >> 10) & 0xFFF
                    if rn == rd and add_imm == target_lo:
                        adrp_matches.append((pc, pc + j*4))

print("ADRP+ADD matches for initKey string:", [(hex(p1), hex(p2)) for p1, p2 in adrp_matches])

if adrp_matches:
    func_addr = adrp_matches[0][0] & ~0x3F # approximate function start
    # Let's disassemble around it
    cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    start = max(0, adrp_matches[0][0] - 0x80)
    for insn in cs.disasm(data[start : start + 0x120], start):
        print(f"0x{insn.address:x}: {insn.mnemonic:10s} {insn.op_str}")
