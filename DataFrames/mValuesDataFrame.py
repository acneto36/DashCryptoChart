import sys
from   os import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from paths                    import *
from SystemFiles.mWriteRead   import *
from SystemFiles.mListSymbols import *
from SystemFiles.mPathModule  import *
from DataFrames.mReturnLists  import *

def F_valuesDataFrame():

    exchange   = readingFile(PATH_Exchanges)[0]        # List of exchanges.
    timeframe  = F_readTimeframe(exchange, PATH_TimeFrame)
    returnList = F_lstPaths(exchange)                  # Lists with right and left symbols.
    SYMBOLS    = F_listSymbols(returnList[1])          # Right list of symbols.
    LSTINDS    = F_moduleIndicators('_ind__')[0]       # Indicator name
    LSTINPS    = F_moduleIndicators('_inp__')[0]       # input name
    pathFolder = F_lstFolders(exchange)                # Exchange folder with CSV files.

    symbolCsv  = ( {symbol: os.path.join( pathFolder, 
                   f'{symbol.lower()}_{timeframe}.csv') for symbol in SYMBOLS} ) # List with the paths of the CSV files.

    return SYMBOLS, LSTINDS, LSTINPS, symbolCsv, timeframe