from   os  import path
import sys

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from paths import *

# ___________________________________________________________________________ #
def F_exchanges():
     return 'Binance', 'yFinance'

# ___________________________________________________________________________ #
def F_LstTF(changeExchange):
   
    Binance   = ['1_Day', '3_Day', '1_Minute', '3_Minute', '5_Minute', '15_Minute', '30_Minute', '1_Hour', '2_Hour', '4_Hour', '6_Hour', '8_Hour', '12_Hour', '1_Week', '1_Month']
    yFinance  = ['1d', '5d', '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1wk', '1mo', '3mo']
    exchanges = {F_exchanges()[0]: Binance, F_exchanges()[1]: yFinance}

    for exchange, tfList in exchanges.items():
        if changeExchange == exchange:
            return tfList

# ___________________________________________________________________________ #
def F_lstPaths(exchange):

    listSymbol = [PATH_lstRightBnb, PATH_lstRightYfi]
    listBase   = [PATH_lstLeftBnb,  PATH_lstLeftYfi]

    for i in range(len(listSymbol)):
        if exchange == F_exchanges()[i]:
            return listBase[i], listSymbol[i]
        
# ___________________________________________________________________________ #
def F_lstFolders(exchange):

    listFolder = [PATH_FolderBnb, PATH_FolderYfi]

    for i in range(len(listFolder)):
        if exchange == F_exchanges()[i]:
            return listFolder[i]
        
# ___________________________________________________________________________ #


    