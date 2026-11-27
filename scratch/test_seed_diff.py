import sys
sys.path.insert(0, ".")
sys.path.insert(0, "extract")
import bwdefs
from ros_mock_server import athlete_create_message, _encode_appearance_pkg
import os

D = bwdefs.Defs()

# Test 1: 0 items
os.environ["ATHLETE_SEED_ITEMS"] = ""
msg0 = athlete_create_message()
print("0 items msg len:", len(msg0))

# Test 2: 25 items
os.environ["ATHLETE_SEED_ITEMS"] = "120901:1,120902:1,120903:1,120904:1,120905:1,142080:1,142081:1,142082:1,140105:1,102568:1,102413:1,1102319:1,1111382:1,1111383:1,15:1,16:1,17:1,106500:1,106501:1,106502:1,104932:1,104935:1,250175:1,250153:1,250156:1"
msg25 = athlete_create_message()
print("25 items msg len:", len(msg25))
