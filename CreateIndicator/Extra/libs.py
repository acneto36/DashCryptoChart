import math
import sys
from   os     import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from DataFrames.mDataSeries import *

# ___________________________________________________________________________ #
def MA(lstPrice: list, period: int, avgType: str = 'sma') -> list:

    ''' 
        Returns a list with 'Moving Average' values\n
        AvgType = 'sma', 'ema', 'wma', 'smma', 'zlema' 
    '''

    lstMa = []

    if len(lstPrice) < period:
        return []

    # ___________________________________________________________________________ #
    # ___________________________________________________________________________ #
    def F_ema(listPrice: list) -> list:

        lstEma = []

        alpha   = 2 / (period + 1)
        firstMa = sum(listPrice[:period]) / period
        oldEma  = firstMa

        for i in range(period, len(listPrice)):

            ema    = (listPrice[i] - oldEma) * alpha + oldEma
            oldEma = ema

            lstEma.append( ema )

        return lstEma

    # ___________________________________________________________________________ #
    # ___________________________________________________________________________ #
    if avgType == 'sma':

        for i in range(period, len(lstPrice)):

            sums = 0

            for j in range(i-period, i):
                sums += lstPrice[j]

            sma = sums / period
            lstMa.append( sma )

    # ___________________________________________________________________________ #
    elif avgType == 'ema':

        return F_ema(lstPrice)

    # ___________________________________________________________________________ #
    elif avgType == 'wma':
        
        weights    = list(range(1, period+1))
        sumWeights = sum(weights)

        for i in range(period, len(lstPrice) + 1):

            subList = lstPrice[i - period : i]
            wma     = sum(subList[j] * weights[j] for j in range(period)) / sumWeights
            lstMa.append( wma )

    # ___________________________________________________________________________ #
    elif avgType == 'smma':

        sma     = sum(lstPrice[:period]) / period
        oldSmma = sma

        for i in range(period, len(lstPrice)):

            smma    = (oldSmma * (period - 1) + lstPrice[i]) / period
            oldSmma = smma
            lstMa.append( smma )

    # ___________________________________________________________________________ #
    elif avgType == 'zlema':
    
        ema1     = F_ema(lstPrice)
        ema2     = F_ema(ema1)

        diffEma1 = len(lstPrice) - len(ema1)
        diffEma2 = len(lstPrice) - len(ema2)

        for i in range(period, len(lstPrice)):

            emaDiff = ema1[i - diffEma1] - ema2[i - diffEma2]
            zlema   = ema1[i - diffEma1] + emaDiff

            lstMa.append( zlema )

    return lstMa

# ___________________________________________________________________________ #
def VWAP(lstPrice: list, lstVolume: list, startIndex: int) -> list:

    '''
        From the parameter startIndex, the VWAP calculation will begin.\n  
        Returns: 
            List with prices from the VWAP calculation.
    '''

    num     = 0
    den     = 0
    vwap    = 0
    lstVwap = []

    for i in range(startIndex, len(lstPrice)):

        num += lstPrice[i] * lstVolume[i]
        den += lstVolume[i]
        vwap = num / den

        lstVwap.append(vwap)

    return lstVwap

# ___________________________________________________________________________ #
def STDDEV(lstPrice: list, period: int) -> list:

    '''
        Returns a list with 'Standard deviation (STDDEV)' values
    '''

    if len(lstPrice) < period:
        return []

    lstStddev = []

    for i in range(period, len(lstPrice) + 1):
        subList    = lstPrice[i - period : i]

        mean       = sum(subList) / len(subList)
        variance   = sum((x - mean) ** 2 for x in subList) / (len(subList) - 1)
        squareRoot = math.sqrt(variance)

        lstStddev.append(squareRoot)

    return lstStddev

# ___________________________________________________________________________ #
def ATR(highList: list, lowList: list, closeList: list, period: int) -> list:

    '''
        Returns a list with 'Average True Range (ATR)' values.
        Takes three separate lists: high prices, low prices, and closing prices.
    '''

    if len(highList) < period or len(lowList) < period or len(closeList) < period:
        return []

    atrValues = []
    atr       = 0

    for i in range(period, len(highList)):

        high      = highList[i]
        low       = lowList[i]
        closePrev = closeList[i - 1]

        # True Range (TR) calculation using high, low, and previous close
        tr = max(high - low, abs(high - closePrev), abs(low - closePrev))

        if i == period:
            # Initialize ATR using the first True Range
            atr = tr
        else:
            # Calculate the weighted average ATR
            atr = (atr * (period - 1) + tr) / period

        atrValues.append(atr)

    return atrValues