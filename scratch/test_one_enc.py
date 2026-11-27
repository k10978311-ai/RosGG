import sys
sys.path.insert(0, ".")
sys.path.insert(0, "extract")
import bwdefs
from ros_mock_server import _encode_appearance_pkg

one_enc = _encode_appearance_pkg(bwdefs, [120901], 200)
print("one_enc hex:", one_enc.hex())
print("one_enc len:", len(one_enc))
