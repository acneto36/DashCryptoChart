import sys
import traceback
from   os import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from DataFrames.mDataSeries         import *
from DataFrames.mFormatNumber       import *
from CreateIndicator.Plots.mPlots   import *
from SystemFiles.mWriteLog          import *
from CreateIndicator.Extra.mConsole import console
from paths                          import *

class IndLastPrice:
    def __init__(self, fig = None, df = None, symbol = ''):

        try:
            date = dates(df)
            cl   = closes(df)

            plotLines(fig, [date[1], date[-1]], [cl[-1], cl[-1]], '#31c404')
        
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
    indChannel = IndLastPrice()