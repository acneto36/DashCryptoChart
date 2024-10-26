import os, sys
import time
from   PyQt5.QtCore import QThread

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paths                     import PATH_UpdateSec
from DataFrames.mSwapDataFrame import *
from SystemFiles.mWriteRead    import *

# ================================================================================= #   
class DashThread(QThread):

    def __init__(self, app):
        super().__init__()
        self._stopEvent = False
        self.app        = app

    def run(self):

        while not self._stopEvent:
            try:
                self.app.run()

            except Exception as e:
                print("Error DashThread main:", e)
                continue

    def stop(self):
        self._stopEvent = True


# ================================================================================= #
class DataFrameThread(QThread):

    def __init__(self):
        super().__init__()
        self._stopEvent = False
        

    def run(self):
        while not self._stopEvent:
            try:
                spinDefault = F_readUpdateSec(PATH_UpdateSec)
                F_chooseDataFrame(False)
                time.sleep(int(spinDefault)) 

            except Exception as e:
                print("Error DataFrameThread:", e)
                continue

    def stop(self):
        self._stopEvent = True
