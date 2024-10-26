SEPARATE_WINDOW = False

import os
import sys
import traceback

srcPath = os.path.realpath(os.path.join(os.path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from DataFrames.mDataSeries           import *
from DataFrames.mFormatNumber         import *
from CreateIndicator.Extra.collection import *
from SystemFiles.mWriteLog            import *
from CreateIndicator.Extra.mConsole   import console
from CreateIndicator.Plots.mPlots     import *
from paths                            import PATH_Log

currentDir = os.path.dirname(os.path.realpath(__file__))
pathConfig = os.path.join(currentDir, 'configHoursChannel.txt')

# ___________________________________________________________________________ #
class IndHoursChannel:
    def __init__(self, fig = None, df = None, symbol = ''):
        
        try:

            date  = dates(df)
            idx   = indexes(df)
            hg    = highs(df)

            # =========================================== #
            lstInputs     = readingInput(pathConfig, symbol)
            defaultValues = [symbol, '2024-01-01 00:00', '2024-02-01 00:00', 'False', 'Normal']

            _, startDate, endDate, candleColor, lineSize = valuesInList(lstInputs, defaultValues)
            # =========================================== #
            
            candleColor = bool(candleColor)

            lstColors       = []
            self.startIndex = 0
            self.endIndex   = 0
            self.startPrice = 0
            self.endPrice   = 0

            startDate   = pdDatetime(startDate)
            endDate     = pdDatetime(endDate)
            firstDate   = date[0]

            # Get the initial and final points of the channel
            for i in range(len(date)-1, 0, -1):

                lstColors.append('gray')
                date[i] = date[i]

                if date[i] == endDate:

                    self.endIndex = idx[i]
                    self.endPrice = hg[i]

                if date[i] == startDate:

                    self.startIndex = idx[i]
                    self.startPrice = hg[i]
                    break

            
            # To avoid bugs, the chosen start date must be later than the first existing date
            if startDate > firstDate and endDate > startDate:

                # Maximum and minimum of the chosen range
                maxPrices = maxPrice(df, self.startIndex, self.endIndex)
                minPrices = minPrice(df, self.startIndex, self.endIndex)

                # ___________________ CHANNEL __________________________ #
                lstDates  = [startDate, endDate]

                # Central line
                lstAnchor = [self.startPrice, self.endPrice]

                newPrice  = ( F_extendLine(lstAnchor[0], lstAnchor[1], self.startIndex, self.endIndex, len(date))
                                if lineSize == 'Size' else lstAnchor[1] )
                
                stretchLine = date[-1] if lineSize == 'Size' else lstDates[1]

                plotLines(fig, [lstDates[0], stretchLine], [lstAnchor[0], newPrice], '#FFE305' )
                
                # Percentage of channel expansion
                colors  = ['#888A85', '#888A85', '#888A85', '#0AB5B5', '#888A85', '#888A85', '#888A85', '#0AB5B5']
                lstPerc = [0.15, 0.28, 0.45, 0.65, -0.15, -0.28, -0.45, -0.65] 
                lstExp  = []

                for x in range(len(lstPerc)):
                    lstExp.append(lstPerc[x] * (maxPrices - minPrices))

                # Expansion calculation
                for x in range(len(lstExp)):

                    priceIni = self.startPrice + lstExp[x]
                    priceEnd = newPrice + lstExp[x]
                    prices   = [float(formatNumber(priceIni)), float(formatNumber(priceEnd))]

                    plotLines(fig, [lstDates[0], stretchLine], prices, colors[x])

                if candleColor:

                    plotCandle(fig, df, idx, 'gray')
                    plotCandle(fig, df, [self.startIndex, self.endIndex], 'red')
                

        except Exception as e:

            name      = f'{self.__class__.__name__[3:]}'
            errorMsg  = ''.join(traceback.format_exception_only(type(e), e)).strip()
            errorLine = traceback.extract_tb(e.__traceback__)[-1].lineno
            
            if 'add_trace' in errorMsg:
                pass

            else:
                print(f"{errorMsg} -> Indicator '{name}' in Line {errorLine}")
                F_writeLog(PATH_Log, f"{errorMsg} -> Indicator '{name}' in Line {errorLine}")
                pass


# --------------------------------------------------------------------------- #
def F_extendLine(iniPrice, endPrice, iniIndex, endIndex, size):
    # Coordinates of points A and B on the y-axis
    idx1, price1 = iniIndex, iniPrice

    # Coordinates of points A and B on the x-axis
    idx2, price2 = endIndex, endPrice

    # Calculate the slope of the line
    slope = (price2 - price1) / (idx2 - idx1)

    for x in range(idx1, size + 1):
        # Calculate the corresponding y coordinates using the slope
        newPrice = price1 + slope * (x - idx1)

    return newPrice

# ------------------------------------------------------------------------ #
if __name__ == "__main__":
    indChannel = IndHoursChannel() 



