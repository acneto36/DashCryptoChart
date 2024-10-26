SEPARATE_WINDOW = False # If it's a histogram in a separate window, change to True

import sys
import traceback
from   os import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from DataFrames.mDataSeries           import *
from DataFrames.mFormatNumber         import *
from CreateIndicator.Extra.collection import *
from SystemFiles.mWriteLog            import *
from CreateIndicator.Extra.mConsole   import console
from CreateIndicator.Plots.mPlots     import *
from CreateIndicator.Extra.libs       import *
from paths                            import PATH_Log

currentDir = path.dirname(path.realpath(__file__))
pathConfig = path.join(currentDir, 'configMoveAverage.txt') # Automatically created file for sharing input with this indicator

class IndMoveAverage:
    def __init__(self, fig = None, df = None, symbol = ''):  # Do not remove parameters

        try:
            # =========================================== #
            lstInputs     = readingInput(pathConfig, symbol)
            defaultValues = [symbol, '100', 'sma', 'Single color', 'solid', '1', '#5cfffe', '#da2506', '30', '0.5']

            _, periods, avgType, multiColor, lineType, lineWidth, lineColor1, lineColor2, start, cloud = valuesInList(lstInputs, defaultValues)
            # =========================================== #

            cl         = closes(df)
            date       = dates(df)
            listColors = []
            
            startDay   = selectDay(df, int(start))
            ini        = startDay if startDay > int(periods) else int(periods) 
            mean       = MA(cl, int(periods), avgType)

            # Adjust list size
            lstMa      = [mean[i - int(periods)] for i in range(ini, len(cl))]

            # Multi color
            for i in range(1, len(lstMa)):
                listColors.append(lineColor1 if lstMa[i] > lstMa[i-1] else lineColor2)

            # Cloud
            listPricesUp = [price * 1.06 for price in lstMa]
            listPricesDn = [price * 0.94 for price in lstMa]

            plotFill(fig, date[ini:], lstMa, listPricesUp, f'rgba(15, 209, 64, {cloud})')
            plotFill(fig, date[ini:], lstMa, listPricesDn, f'rgba(209, 196, 15, {cloud})')

            # Lines option 'solid' 'dash', 'dot', and 'dashdot'
            if multiColor == 'Multi color':
                plotLineColor(fig, date[ini:], lstMa, listColors, widthLine = int(lineWidth))
            else:                                            # Optional, default typeLine 'solid' and widthLine 1
                plotLines(fig, date[ini:], lstMa,  lineColor1, typeLine = lineType, widthLine = int(lineWidth))

            
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

# ------------------------------------------------------------------------ #
if __name__ == "__main__":
    indChannel = IndMoveAverage() 