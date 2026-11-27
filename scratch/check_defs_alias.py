import sys
sys.path.insert(0, "extract")
import bwdefs
D = bwdefs.Defs()
matches = [k for k in D._alias.keys() if "APPEARANCE" in k.upper()]
print("Matching aliases:", matches)
for m in matches:
    print(f"\n--- {m} ---")
    print(D._alias[m])
