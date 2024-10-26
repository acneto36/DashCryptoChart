import sys
from   os import path
import pandas as pd


srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from DataFrames.mValuesDataFrame           import *
from CreateIndicator.Extra.mWriteReadInput import *
from CreateIndicator.consoleLog            import ConsoleLog  
from SystemFiles.mWriteLog                 import *
from paths                                 import PATH_Log

# ___________________________________________________________________________ #
def readDataFrame(symbol: str):

    symbolCsv = F_valuesDataFrame()[3]
    
    csv_file = symbolCsv[symbol]
    df       = pd.read_csv(csv_file)

    return df

# ___________________________________________________________________________ #
def console(logValue): # Used in indicators and inputs.
     F_writeConsole(PATH_Log, logValue)

# ___________________________________________________________________________ #
def openConsole(parent):

    if not hasattr(parent, 'guiLog') or not parent.guiLog.isVisible():
        parent.guiLog = ConsoleLog(PATH_Log)
        # parent.guiLog.show()
