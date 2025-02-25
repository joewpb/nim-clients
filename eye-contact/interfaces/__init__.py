import os
import sys
from . import eyecontact_pb2
pwd = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, pwd)
from . import eyecontact_pb2_grpc
sys.path.remove(pwd)
