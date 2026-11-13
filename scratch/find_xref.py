import struct

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

target_va = 0x2a2766f

# In ARM64:
# ADRP Xd, #imm
# imm is relative to PC page (PC & ~0xFFF).
# opcode: [31: 0] [30:29 immlo] [28:24 10000] [23:5 immhi] [4:0 Rd]
# ADD Xd, Xn, #imm12
# LDR Xd, [Xn, #imm12]

# Let's search all 4-byte aligned instructions in .text
# First let's check literal pools (8-byte pointer = target_va)
ptr_matches = []
for i in range(0, len(data) - 8, 8):
    val = struct.unpack_from("<Q", data, i)[0]
    if val == target_va:
        ptr_matches.append(i)
print("Literal pool matches for target_va:", [hex(x) for x in ptr_matches])

# Now search ADRP instructions
# target_page = target_va & ~0xFFF = 0x2a27000
target_page = target_va & ~0xFFF
target_lo = target_va & 0xFFF

adrp_matches = []
# Scan executable section (0 to 0x2a00000 roughly)
for pc in range(0, 0x2a00000, 4):
    insn = struct.unpack_from("<I", data, pc)[0]
    # Check if ADRP: (insn & 0x9F000000) == 0x90000000
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
            # check next few instructions for ADD/LDR with target_lo
            for j in range(1, 4):
                next_insn = struct.unpack_from("<I", data, pc + j*4)[0]
                # ADD (immediate, 64-bit): 0x91000000
                if (next_insn & 0xFF800000) == 0x91000000:
                    rn = (next_insn >> 5) & 0x1F
                    add_imm = (next_insn >> 10) & 0xFFF
                    if rn == rd and add_imm == target_lo:
                        adrp_matches.append((pc, pc + j*4))
                # LDR (literal/unsigned offset) could also happen
print("ADRP+ADD matches:", [(hex(p1), hex(p2)) for p1, p2 in adrp_matches])
