import sys
import csv
import os
import traceback
import yfinance as yf
import pandas   as pd

srcPath = os.path.realpath(os.path.join(os.path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)



import DataFrames.mRecreateFile         as newFile
import DataFrames.mUpdateCsvFile        as updt
from   paths                        import *
from   SystemFiles.mWriteRead       import *
from   SystemFiles.mListSymbols     import *
from   DataFrames.mReturnLists      import *
from   DataFrames.mFormatNumber import *
from   DataFrames.mValuesDataFrame  import F_valuesDataFrame

# ___________________________________________________________________________ #
def F_createFiles(pathFile, ohlc):
    # "Create the file and save the DataFrame's data."
    with open(pathFile, 'w', newline = '') as file:

        writer = csv.writer(file, delimiter = ',')
        header = ['index', 'date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'stock splits']
        writer.writerow(header)

        # Reorganize the columns
        ohlc = ohlc[header]

        for _, row in ohlc.iterrows():

            row['date'] = pd.to_datetime(row['date']).tz_localize(None)
            candlestick = [formatNumber(value) for value in row.tolist()]
            
            writer.writerow(candlestick)

# ___________________________________________________________________________ #
def F_dtFrameYfi(writeCompleteFile = False):

    try:
        exchange   = readingFile(PATH_Exchanges)
        returnList = F_lstPaths(exchange[0])
        SYMBOLS    = F_listSymbols(returnList[1])
        tf         = F_readTimeframe(exchange[0], PATH_TimeFrame)
        start      = readingFile(PATH_DateIni)[0]

        if not os.path.exists(PATH_FolderYfi):
            os.makedirs(PATH_FolderYfi)

        for symbol in SYMBOLS:
            
            OHLC       = yf.Ticker(symbol).history(start = start, interval = tf)

            # Remove time zone information, if necessary
            OHLC.index = pd.to_datetime(OHLC.index).tz_localize(None)

            OHLC.insert(0, 'Index', range(0, len(OHLC)), True)
            OHLC.insert(1, 'Date', OHLC.index)

            # Converts column names to lowercase
            OHLC.columns = map(str.lower, OHLC.columns)

            fileName     = f'{symbol.lower()}_{tf}.csv'
            pathFile     = os.path.join(PATH_FolderYfi, fileName)

            if writeCompleteFile:
                try:
                    # "Upon clicking Save/Update, create a new file, or if the file exists, recreate it."
                    F_createFiles(pathFile, OHLC)

                except Exception as e:

                    tb = traceback.format_exc()
                    print(f"Error writing complete file in DataFrameYfi: {pathFile}: {tb}\n")
                    
            else:
                if os.path.exists(pathFile):

                    try:
                        # Retrieve the values stored in the CSV file.
                        dfFileCsv    = pd.read_csv(pathFile)

                        # "Retrieve the last index of the DataFrame and the last index from the CSV file for comparison."
                        lastIndexYfi = OHLC['index'].iloc[-1]
                        lastIndexCsv = dfFileCsv.iloc[-1]['index']

                        lastRow      = OHLC.iloc[-1]
                        missingRows  = OHLC[OHLC['index'] >= lastIndexCsv]

                        updt.F_updateCsv(pathFile, dfFileCsv, lastIndexYfi, lastIndexCsv, lastRow, missingRows)

                    except Exception as e:
                        
                        newFile.F_recreateDataFrame('Yfinance')
                        
                        tb = traceback.format_exc()
                        print(f"Error DataFrameYfi: {pathFile}: {tb}\n")
                        raise
                        
                else:
                    # "If accidentally deleted, recreate the file."
                    try:
                        F_createFiles(pathFile, OHLC)

                    except Exception as e:

                        tb = traceback.format_exc()
                        print(f"Error writing file in DataFrameYfi: {pathFile}: {tb}\n")
                        raise 
                       

    except Exception as e:

        # Capture the complete traceback.
        tb = traceback.format_exc()
        print(f"Error occurred in F_dtFrameYfi:\n{tb}\n")
        raise  # Propagate the exception so that previous methods can also catch it.


# F_dtFrameYfi()

     