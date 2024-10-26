import os
import sys
import traceback
from   tkinter      import messagebox
import mttkinter        as mtk

srcPath = os.path.realpath(os.path.join(os.path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from CreateIndicator.Extra.mWriteReadInput import *
from CreateIndicator.Extra.collection      import *
from CreateIndicator.Extra.mWidgets        import *
from CreateIndicator.Extra.mConsole        import console
from DataFrames.mFormatNumber              import *
from DataFrames.mDataSeries                import *
from SystemFiles.mWriteLog                 import *
from paths                                 import PATH_Icon, PATH_Log, PATH_HWaves

currentDir = os.path.dirname(os.path.realpath(__file__))
pathConfig = os.path.join(currentDir, 'configVwap.txt')  # Automatically created file for this input
pathWave   = int(readFile(PATH_HWaves)[0]) if len(readFile(PATH_HWaves)) > 0 else 0 # For histogram

# ___________________________________________________________________________ #
class InpVwap:  # The name must start with 'Inp'
    def __init__(self, symbol = '', df = None): # Do not remove parameters

        # mtTkinter version for multithreads
        self.root = mtk.mtTkinter.Tk()

        self.root.configure(bg = '#595959')
        self.root.minsize(150, 150)
        self.root.title("VWAP")

        self.root.configure(border = None)
        self.root.resizable(width  = False, height = False)
        self.root.iconphoto(False, mtk.mtTkinter.PhotoImage(file = PATH_Icon))
 
        try:
            # ============== values from input=========== #
            lstInputs      = readingInput( pathConfig, symbol )
            # Examble default values, only string!
            defaultValues  = [symbol, '5', '#ffffff' ] 
            _, days, color = valuesInList(lstInputs, defaultValues)
            # =========================================== #

            self.frame = createFrame(self.root, row = 0, column = 0, padx = 5, pady = 5)

            #  Checkbox padrão para manter a janela acima das outras 'Opcional'
            self.checkOverlay = inputCheckbox(self.frame, 0, 0, 'Overlay')
            self.checkOverlay.configure(command = self.toggle_topmost)

            self.intSpinBox = inputIntSpinbox(self.frame, 1, 0, 'Total days', minimum = 1, maximum = 2000, width = 3, defaultValue = int(days), position = 'right')
            self.color      = inputColor(self.frame, 2, 0, 'Line', color, defaultColor = '#ffffff')

            button = inputButton(self.frame, 3, 0, 'Apply', position = 'full', background = '#047e00')
            button.configure(command = lambda: self.writeInputs(pathConfig, symbol))


        # Use 'except pass' to avoid crashing the Dash server if an error occurs in the input
        except Exception as e:

            name      = f'{self.__class__.__name__[3:]}'
            errorMsg  = ''.join(traceback.format_exception_only(type(e), e)).strip()
            errorLine = traceback.extract_tb(e.__traceback__)[-1].lineno

            print(f"{errorMsg} -> Input '{name}' in Line {errorLine}")
            F_writeLog(PATH_Log, f"{errorMsg} -> Input '{name}' in Line {errorLine}")
            pass
    
    # ___________________________________________________________________________ #
    def writeInputs(self, path, symbol):

        lstInputs = [self.intSpinBox.value(), self.color.value()]
        
        writeInput(path, symbol, lstInputs)
        
    # ___________________________________________________________________________ #
    def toggle_topmost(self):

        self.root.attributes('-topmost', 0)

        if self.checkOverlay.value():
            self.root.attributes('-topmost', 1)

    # ___________________________________________________________________________ #
    def show(self):
        self.root.mainloop()

    # ___________________________________________________________________________ #
    def close_window(self):
        self.root.destroy()

# ___________________________________________________________________________ #
if __name__ == '__main__':

    window = InpVwap()
    window.show()
# =================================== #