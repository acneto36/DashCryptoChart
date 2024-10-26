SEPARATE_WINDOW = True # If it's a histogram in a separate window, change to True

'''
    Original indicator: @LazyBear "Tradingview"
'''

import os 
import sys
import traceback

srcPath = os.path.realpath(os.path.join(os.path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from CreateIndicator.Extra.mWriteReadInput import *
from CreateIndicator.Extra.collection      import *
from CreateIndicator.Extra.mConsole        import console
from CreateIndicator.Plots.mPlots          import *
from CreateIndicator.Extra.libs            import *
from DataFrames.mFormatNumber              import *
from DataFrames.mDataSeries                import *
from SystemFiles.mWriteLog                 import *
from paths                                 import PATH_Log


currentDir = os.path.dirname(os.path.realpath(__file__))
pathConfig = os.path.join(currentDir, 'configImpulsemacd.txt') # Automatically created file for sharing input with this indicator

# ------------------------------------------------------------------------ #
class IndImpulsemacd: # The name must start with 'Ind'
    def __init__(self, fig = None, df = None, symbol = ''):  # Do not remove parameters

        try:
            cl     = closes(df)
            hg     = highs(df)
            lw     = lows(df)
            date   = dates(df)
            lenght = size(df)

            # =========================================== #
            lstInputs     = readingInput( pathConfig, symbol )
            defaultValues = [symbol, '30', '34', '9', '#65c907', '#278a00', '#c70606', 
                             '#aa5c03', '#026dac', '#f0e000', '0.5', '2']
            
            _, days, periodH, periodS, cor1, cor2, cor3, cor4, cor5, cor6, fill, width = valuesInList(lstInputs, defaultValues)
            # =========================================== #

            periodH   = int(periodH)
            periodS   = int(periodS)
            period    = max(int(periodH), int(periodS))
            lstColors = []

            color     = hexcolorToRgba(cor5, fill)

            startDay = selectDay(df, int(days))
            ini      = startDay if startDay > period else period

            hlc3 = [((cl[i] + hg[i] + lw[i]) / 3) for i in range(lenght)] 

            hi  = MA(hg,   periodH, 'smma')
            lo  = MA(lw,   periodH, 'smma')
            mi  = MA(hlc3, periodH, 'zlema')

            md  = [(mi[i - periodH] - hi[i - periodH]) if mi[i - periodH] > hi[i - periodH] else 
                   (mi[i - periodH] - lo[i - periodH]) if mi[i - periodH] < lo[i - periodH] else 0 for i in range(ini, lenght)]

            sb  = MA(md, periodS, 'sma')
            sh  = [md[i] - sb[i - periodS] for i in range(len(md))]
       
            for i in range(ini, lenght):

                if hlc3[i] > mi[i - periodH]: 
                    lstColors.append( cor1 if hlc3[i] > hi[i - periodH] else cor2 )
                    
                else:
                    lstColors.append( cor3 if hlc3[i] < lo[i - periodH] else cor4 )

            plotHistogram(fig, date[ini:], md, lstColors)

            plotFill(fig, date[ini:], sh, ([0] * len(sh)), color, isHistogram = True)

            # When passing the date, adjust correctly with the 'sb' value list
            plotLines(fig, date[ini + periodS:], sb, colorRGB = cor6, widthLine = int(width), isHistogram = True) 

            

        # Use 'except pass' to avoid crashing the Dash server if an error occurs in the indicator
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
    showInd = IndImpulsemacd()