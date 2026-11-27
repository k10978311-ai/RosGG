import dis
print("151 in dis.opname:", dis.opname[151] if 151 < len(dis.opname) else "unknown")
# Let's inspect dis.opmap in standard Python 2.7
