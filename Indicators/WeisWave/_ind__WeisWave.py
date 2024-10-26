SEPARATE_WINDOW = True

import sys
import traceback
from   os import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from CreateIndicator.Extra.mWriteReadInput import *
from CreateIndicator.Extra.collection      import *
from CreateIndicator.Extra.mConsole        import console
from CreateIndicator.Extra.libs            import *
from CreateIndicator.Plots.mPlots          import *
from DataFrames.mDataSeries                import *
from DataFrames.mFormatNumber              import *
from SystemFiles.mWriteLog                 import *
from paths                                 import PATH_Log

currentDir = path.dirname(path.realpath(__file__))
pathConfig = path.join(currentDir, 'configWeisWave.txt')

# ___________________________________________________________________________ #
class IndWeisWave:
    def __init__(self, fig = None, df = None, symbol = ''):
        
        try:

            self.date = dates(df)
            self.size = size(df)
            self.cl   = closes(df)
            self.vl   = volumes(df)

            # =========================================== #
            lstInputs     = readingInput(pathConfig, symbol)
            defaultValues = [symbol, '2', '0', 'Normal', '#5cfffe', '#da2506']

            _, self.startWave, self.percent, self.dirWave, self.colorUp, self.colorDn = valuesInList(lstInputs, defaultValues)
            # =========================================== #

            # Pre-allocation of values in the lists
            lstWave   = [0] * self.size
            lstColors = ['white'] * self.size
            lstDir    = [0] * self.size

            startWave = selectDay(df, int(self.startWave))

            # First, collect the direction
            self.F_waveDir(int(self.startWave), lstDir)

            # Second, configure dir wave, volume wave and color wave
            self.F_createWave(lstWave, lstDir, lstColors, startWave)

            # Lastly, plot the histogram
            plotHistogram(fig, self.date, lstWave, lstColors)

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

    # ___________________________________________________________________________ #
    def F_waveDir(self, start, lstDir):

        diff     = 0
        newDir   = 0
        oldValue = 0

        for index in range(start, self.size):

            diff = ((self.cl[index] - oldValue) * 100) / self.cl[index]

            if oldValue < self.cl[index] and diff >= float(self.percent):

                newDir        = 1
                lstDir[index] = 1

            elif oldValue > self.cl[index] and diff <= -float(self.percent):

                newDir        = -1
                lstDir[index] = -1
            
            # Continuation of movement
            if ( newDir ==  1 and self.cl[index] >= oldValue or 
                 newDir == -1 and self.cl[index] <= oldValue ):

                oldValue      = self.cl[index]
                lstDir[index] = newDir

        # Corrects the direction of movement
        for i in range(self.size-2, start, -1):
                       
            if lstDir[i] == 0:
                lstDir[i] = lstDir[i+1]

    # ___________________________________________________________________________ #
    def F_createWave(self, lstWave, lstDir, lstColor, start):

        for i in range(start-1, self.size):

            continuation = True if lstDir[i] == lstDir[i-1] else False
            dirVol       = -self.vl[i] if self.dirWave == 'Invert' and lstDir[i] == -1 else self.vl[i]

            lstWave[i]   = dirVol if not continuation else lstWave[i-1] + dirVol
            lstColor[i]  = self.colorUp if lstDir[i] == 1 else self.colorDn if lstDir[i] == -1 else '#ffffff'

# ------------------------------------------------------------------------ #
if __name__ == "__main__":
    indChannel = IndWeisWave() 