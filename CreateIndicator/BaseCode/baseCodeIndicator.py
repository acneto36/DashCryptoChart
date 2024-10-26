SEPARATE_WINDOW = False # If it's a histogram in a separate window, change to True

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
pathConfig = os.path.join(currentDir, 'config.txt')    # Automatically created file for sharing input with this indicator

# ------------------------------------------------------------------------ #
class IndNewName: # The name must start with 'Ind'
    def __init__(self, fig = None, df = None, symbol = ''):  # Do not remove parameters

        try:
            # Available data series
            op     = opens(df)
            hg     = highs(df)
            lw     = lows(df)
            cl     = closes(df)
            vl     = volumes(df)
            idx    = indexes(df)
            date   = dates(df)
            lenght = size(df)

            # ============== values from input=========== #
            lstInputs     = readingInput( pathConfig, symbol )
            # Examble default values, only string!
            defaultValues = [symbol, 'entry', '5', '1.5', 'None', '0.5', '#ffffff', '2024-01-01 00:00' ] 
            _, value1, value2, value3, value4, value5, value6, value7 = valuesInList(lstInputs, defaultValues)
            # =========================================== #


            

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
    showInd = IndNewName()