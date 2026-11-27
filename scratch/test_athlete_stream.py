import sys
sys.path.insert(0, ".")
sys.path.insert(0, "extract")
import bwdefs
from ros_mock_server import _encode_appearance_pkg, _parse_seed_items, DEFAULT_SEEDED_ITEMS

D = bwdefs.Defs()
seed = _parse_seed_items("ATHLETE_SEED_ITEMS")
encoded = _encode_appearance_pkg(bwdefs, [it["itemID"] for it in seed], max(200, len(seed) + 50))
print(f"seed len: {len(seed)}, encoded len: {len(encoded)}")

# Check if dtsAppearancePackage is in Athlete props
props = D.base_client_props("Athlete")
pnames = [p[0] for p in props]
print(f"Total Athlete props: {len(props)}")
print(f"'dtsAppearancePackage' in Athlete props: {'dtsAppearancePackage' in pnames}")
for p in props:
    if p[0] == "dtsAppearancePackage":
        print(f"Prop definition: {p}")
        break

log = []
stream = bwdefs.stream_for(D, "Athlete", {"dtsAppearancePackage": encoded}, log)
for entry in log:
    if entry[0] == "dtsAppearancePackage":
        print(f"Stream log for dtsAppearancePackage: {entry}")
