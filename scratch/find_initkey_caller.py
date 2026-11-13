import struct

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

# Let's find callers of 0x98cd90 or surrounding function start
# Let's find function start of 0x98ce00
# Look backward from 0x98cd90 for STP x29, x30
pos = 0x98cd90
while pos > 0x98cb00:
    insn = struct.unpack_from("<I", data, pos)[0]
    if insn == 0xa9bf7bfd: # stp x29, x30, [sp, #-0x10]!
        break
    # Or sub sp, sp
    if (insn & 0xFF800000) == 0xd1000000:
        # check if stp x29, x30 nearby
        pass
    pos -= 4
print(f"Function entry candidate around: {hex(pos)}")

# Search for BL instructions targeting the function
# BL: opcode [31:26] = 0b100101 (0x94000000)
# imm26 sign-extended * 4 = target - pc
for pc in range(0, 0x2a00000, 4):
    insn = struct.unpack_from("<I", data, pc)[0]
    if (insn & 0xFC000000) == 0x94000000:
        imm = insn & 0x03FFFFFF
        if imm & (1 << 25):
            imm -= (1 << 26)
        target = pc + imm * 4
        if 0x98cc00 <= target <= 0x98ce00:
            print(f"Call from {hex(pc)} to {hex(target)}")
