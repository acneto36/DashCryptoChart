import sys
import traceback
from   os import path


srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from CreateIndicator.Extra.collection import *
from CreateIndicator.Extra.mConsole   import console
from CreateIndicator.Plots.mPlots     import *
from DataFrames.mFormatNumber         import *
from DataFrames.mDataSeries           import *
from SystemFiles.mWriteLog            import *

currentDir = path.abspath(path.join(path.dirname(__file__)))
pathConfig = path.join(currentDir, 'configManageTrade.txt')
pathLog    = path.join(srcPath, 'Log', 'logs.txt')

# ___________________________________________________________________________ #
class IndManage:
    def __init__(self, fig = None, df = None, symbol = ''):

        try:

            date = dates(df)

            # =========================================== #
            lstInputs     = readingInput(pathConfig, symbol)
            defaultValues = [symbol, '0', '0', '0', '0', '0', '0', 'False']

            _, firstPrice, firstCoin, secPrice, secCoin, partialPrice, partialCoin, confirm = valuesInList(lstInputs, defaultValues)
            # =========================================== #

            firstPrice   = float(firstPrice)
            firstCoin    = float(firstCoin)
            secPrice     = float(secPrice)
            secCoin      = float(secCoin)
            partialPrice = float(partialPrice)
            partialCoin  = float(partialCoin)

            # First entry
            firstEntry   = firstCoin * firstPrice                                                           
            # Second entry or simulate entry
            secondEntry  = secCoin * secPrice                                          
            # Total invested
            sumOfAmount  = firstEntry + secondEntry

            sumOfCoins   = firstCoin + secCoin
            # New AVG price
            averagePrice = self.F_averagePrice( sumOfAmount, sumOfCoins )
            # Simulate partial
            partial      = averagePrice + ((partialPrice * averagePrice) / 100) if partialPrice > 0 else 0.0   

            # Update values after confirming the simulation
            avgPrice     = averagePrice if confirm == 'True' else firstPrice
            legendEntry1 = 'AVG Price'  if confirm == 'True' else '1st Entry'
            dateX        = shiftDateHours(date[-1], 20)

            if firstCoin > 0:

                avgPrice = formatNumber(avgPrice)

                plotLabel(fig, dateX, float(avgPrice), f'{avgPrice} - {legendEntry1}', 'center', '#f1f1f1', 13,
                        True, 'left', 30, 2, 0, "rgba(145, 142, 142, 0.308)", "rgba(95, 243, 9, 0.637)")

            if partialCoin > 0 and partialCoin <= sumOfCoins:

                partial = formatNumber(partial)

                plotLabel(fig, dateX, float(partial), f'{partial} - Partial', 'center', '#ebebeb', 13,
                        True, 'left', 30, 2, 0, "rgba(145, 142, 142, 0.308)", "rgba(245, 123, 0, 0.733)")

            if secCoin > 0 and confirm == 'False':

                averagePrice = formatNumber(averagePrice)

                plotLabel(fig, dateX, float(averagePrice), f'{averagePrice} - AVG Price', 'center', '#ebebeb', 13,
                        True, 'left', 30, 2, 0, "rgba(145, 142, 142, 0.308)", "rgba(10, 252, 240, 0.507)")

                secPrice = formatNumber(secPrice)

                plotLabel(fig, dateX, float(secPrice), f'{secPrice} - 2nd Entry', 'center', '#ebebeb', 13,
                        True, 'left', 30, 2, 0, "rgba(145, 142, 142, 0.308)", "rgba(237, 213, 0, 0.678)")

        except Exception as e:

            name      = f'{self.__class__.__name__[3:]}'
            errorMsg  = ''.join(traceback.format_exception_only(type(e), e)).strip()
            errorLine = traceback.extract_tb(e.__traceback__)[-1].lineno

            print(f"{errorMsg} -> Indicator '{name}' in Line {errorLine}")
            F_writeLog(pathLog, f"{errorMsg} -> Indicator '{name}' in Line {errorLine}")
            pass

    # ___________________________________________________________________________ #
    def F_averagePrice(self, amount, coins):

        if coins == 0:
            return 0

        value = amount / coins
        avg   = "{:.9f}".format(value)

        return float(avg)

# ------------------------------------------------------------------------ #
if __name__ == "__main__":
    indChannel = IndManage()

