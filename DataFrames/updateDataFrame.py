
import sys
import threading
import traceback
from   os  import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from DataFrames.mSwapDataFrame import *

# ___________________________________________________________________________ #
class UpdateDataFrame(threading.Thread):

    def __init__(self):
            super().__init__()

    def run(self):
        try:
            F_chooseDataFrame(True)

        except Exception as e:

            tb = traceback.format_exc()
            print(f"Error occurred:\n{tb}")

# ___________________________________________________________________________ #