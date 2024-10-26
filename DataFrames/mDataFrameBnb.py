import sys
import csv
import traceback
from   os             import path 
from   binance.client import Client
import pandas             as pd
import numpy              as np

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

import DataFrames.mRecreateFile         as newFile
import DataFrames.mUpdateCsvFile        as updt
from   paths                        import *
from   SystemFiles.mWriteRead       import *
from   SystemFiles.mListSymbols     import *
from   DataFrames.mApiKeyBnb        import *
from   DataFrames.mReturnLists      import *
from   DataFrames.mFormatNumber import *
from   DataFrames.mValuesDataFrame  import F_valuesDataFrame

# ___________________________________________________________________________ #
def F_intervalBnb():

    interval  = F_readTimeframe('Binance', PATH_TimeFrame)

    choice = (
        Client.KLINE_INTERVAL_1DAY     if interval == '1_Day'     else
        Client.KLINE_INTERVAL_3DAY     if interval == '3_Day'     else
        Client.KLINE_INTERVAL_1MINUTE  if interval == '1_Minute'  else
        Client.KLINE_INTERVAL_3MINUTE  if interval == '3_Minute'  else
        Client.KLINE_INTERVAL_5MINUTE  if interval == '5_Minute'  else
        Client.KLINE_INTERVAL_15MINUTE if interval == '15_Minute' else
        Client.KLINE_INTERVAL_30MINUTE if interval == '30_Minute' else
        Client.KLINE_INTERVAL_1HOUR    if interval == '1_Hour'    else
        Client.KLINE_INTERVAL_2HOUR    if interval == '2_Hour'    else
        Client.KLINE_INTERVAL_4HOUR    if interval == '4_Hour'    else
        Client.KLINE_INTERVAL_6HOUR    if interval == '6_Hour'    else
        Client.KLINE_INTERVAL_8HOUR    if interval == '8_Hour'    else
        Client.KLINE_INTERVAL_12HOUR   if interval == '12_Hour'   else
        Client.KLINE_INTERVAL_1WEEK    if interval == '1_Week'    else
        Client.KLINE_INTERVAL_1MONTH 
    )
    
    return choice

# ___________________________________________________________________________ #
def F_dtFrameBnb(writeCompleteFile = False):

    def binanceDataFrame(klines):
        df = pd.DataFrame(klines.reshape(-1, 12), dtype = float, columns = ['date',
                                                                            'open',
                                                                            'high',
                                                                            'low',
                                                                            'close',
                                                                            'volume',
                                                                            'CT',
                                                                            'QV',
                                                                            'N',
                                                                            'TB',
                                                                            'TQ',
                                                                            'I']
        )
        
        df['date'] = pd.to_datetime(df['date'], unit = 'ms')
        df.insert(0, 'index', range(0, len(df)), True)

        return df
    
    # ___________________________________________________________________________ #
    def F_createFiles(pathFile, klines_np, klines_df, historicalCandle):
        # "Create the file and save the DataFrame's data."
        with open(pathFile, 'w', newline = '') as file:

            writer       = csv.writer(file, delimiter = ',')
            klines_np[0] = np.array(historicalCandle)
            klines_df[0] = binanceDataFrame(klines_np[0])
            df_formatted = klines_df[0]
            
            header = ['index', 'date', 'open', 'high', 'low', 'close', 'volume', 'CT', 'QV', 'N', 'TB', 'TQ', 'I']
            writer.writerow(header)
            
            for _, row in df_formatted.iterrows():

                candlestick = [formatNumber(value) for value in row.tolist()]
                writer.writerow(candlestick)

    # ___________________________________________________________________________ #
    if not os.path.exists(PATH_FolderBnb):
        os.makedirs(PATH_FolderBnb)
    
    try:
        klines_np  = dict()
        klines_df  = dict()
        client     = Client(str(F_apiKey()[0]), str(F_apiKey()[1]))
        start      = readingFile(PATH_DateIni)[0]

        exchange   = readingFile(PATH_Exchanges)
        returnList = F_lstPaths(exchange[0])
        SYMBOLS    = F_listSymbols(returnList[1])

        for SYMBOL in SYMBOLS:

            tf                = F_readTimeframe(exchange[0], PATH_TimeFrame)
            interval          = F_intervalBnb()
            fileName          = f'{SYMBOL.lower()}_{tf}.csv'
            pathFile          = os.path.join(PATH_FolderBnb, fileName)
            historicalCandles = client.get_historical_klines(SYMBOL, interval, start)

            if writeCompleteFile:
                try:
                    # "Upon clicking Save/Update, create a new file, or if the file exists, recreate it."
                    F_createFiles(pathFile, klines_np, klines_df, historicalCandles )

                except Exception as e:

                    tb = traceback.format_exc()
                    print(f"Error writing complete file in DataFrameBnb: {pathFile}: {tb}\n")
                    
            else:
                if os.path.exists(pathFile):

                    try:
                        # Retrieve the values stored in the CSV file.
                        dfFileCsv    = pd.read_csv(pathFile)

                        # Retrieve the new historical data.
                        klines_np[0] = np.array(historicalCandles)
                        klines_df[0] = binanceDataFrame(klines_np[0])

                        # "Retrieve the last index of the DataFrame and the last index from the CSV file for comparison."
                        lastIndexBnb = klines_df[0].iloc[-1]['index']
                        lastIndexCsv = dfFileCsv.iloc[-1]['index']
                        
                        lastRow      = klines_df[0].iloc[-1]
                        missingRows  = klines_df[0][klines_df[0]['index'] >= lastIndexCsv]

                        updt.F_updateCsv(pathFile, dfFileCsv, lastIndexBnb, lastIndexCsv, lastRow, missingRows)

                    except Exception as e:

                        newFile.F_recreateDataFrame('Binance')
                        
                        tb = traceback.format_exc()
                        print(f"Error DataFrameBnb: {pathFile}: {tb}\n")

                else:
                    # "If accidentally deleted, recreate the file."
                    try:
                        F_createFiles(pathFile, klines_np, klines_df, historicalCandles)
                    except Exception as e:
                        
                        tb = traceback.format_exc()
                        print(f"Error writing file in DataFrameBnb: {pathFile}: {tb}\n")
                        raise 

    except Exception as e:

        # Capture the complete traceback.
        tb = traceback.format_exc()
        print(f"Error occurred in F_dtFrameYfi: {tb}\n")
        raise  # Propagate the exception so that previous methods can also catch it.


# F_dtFrameBnb(True)