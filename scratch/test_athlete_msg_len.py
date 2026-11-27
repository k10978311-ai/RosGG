import sys
sys.path.insert(0, ".")
sys.path.insert(0, "extract")
import bwdefs
from ros_mock_server import athlete_create_message

msg = athlete_create_message()
print("athlete_create_message len:", len(msg))
