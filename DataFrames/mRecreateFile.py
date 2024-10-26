from   os  import path
import sys

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from paths                       import *
from DataFrames.mDataFrameBnb    import *
from DataFrames.mDataFrameYfi    import *
from DataFrames.mValuesDataFrame import F_valuesDataFrame


# # In a special case where the file exists but is empty, it needs to be deleted and recreated
def F_recreateDataFrame(exchange):

    SYMBOLS, _, _, _, timeframe = F_valuesDataFrame()

    pathFolder = PATH_FolderYfi if exchange == 'Yfinance' else PATH_FolderBnb

    for SYMBOL in SYMBOLS:

        fileName = f'{SYMBOL.lower()}_{timeframe}.csv'
        pathFile = os.path.join(pathFolder, fileName)

        if os.path.exists(pathFile):

            # Search for empty files
            if os.path.getsize(pathFile) == 0:
                
                print(f"The file {pathFile} is empty.\n")

                os.remove(os.path.join(pathFolder, pathFile))
                F_dtFrameYfi() if exchange == 'Yfinance' else F_dtFrameBnb()
                
