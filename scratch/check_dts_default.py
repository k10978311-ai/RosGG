import sys
sys.path.insert(0, "extract")
import bwdefs
D = bwdefs.Defs()
print("dtsAppearancePackage default in D.defaults:")
print(D.defaults.get("dtsAppearancePackage"))
for p in D.base_client_props("Athlete"):
    if p[0] == "dtsAppearancePackage":
        print("Prop in Athlete:", p)
