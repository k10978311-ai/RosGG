import sys
sys.path.insert(0, ".")
sys.path.insert(0, "extract")
import bwdefs
from ros_mock_server import _encode_appearance_pkg

D = bwdefs.Defs()
t = D.resolve("DTS_APPEARANCE_PACKAGE3")
empty_enc = _encode_appearance_pkg(bwdefs, [], 200)
print("empty_enc hex:   ", empty_enc.hex())
print("default_value hex:", bwdefs.default_value(t).hex())
