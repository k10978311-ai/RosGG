import sys
sys.path.insert(0, "extract")
import bwdefs
D = bwdefs.Defs()
t = D.resolve("DTS_APPEARANCE_PACKAGE3")
val = bwdefs.default_value(t)
print("Default value hex:", val.hex())
print("Default value len:", len(val))
