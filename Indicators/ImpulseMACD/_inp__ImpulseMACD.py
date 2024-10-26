import os
import sys
import traceback
import mttkinter as mtk

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

currentDir  = os.path.dirname(os.path.realpath(__file__))
pathConfig  = os.path.join(currentDir, 'configImpulsemacd.txt')  # Automatically created file for this input
histoHeight = int(readFile(PATH_HWaves)[0]) if len(readFile(PATH_HWaves)) > 0 else 3 # For histogram

# ___________________________________________________________________________ #
class InpImpulsemacd:  # The name must start with 'Inp'
    def __init__(self, symbol = '', df = None): # Do not remove parameters

        # mtTkinter version for multithreads
        self.root = mtk.mtTkinter.Tk()

        self.root.configure(bg = '#595959')
        self.root.minsize(150, 150)
        self.root.title("Impulse MACD")

        self.root.configure(border = None)
        self.root.resizable(width  = False, height = False)
        self.root.iconphoto(False, mtk.mtTkinter.PhotoImage(file = PATH_Icon))
 
        try:
            # =========================================== #
            lstInputs     = readingInput( pathConfig, symbol )
            defaultValues = [symbol, '30', '34', '9', '#65c907', '#278a00', '#c70606', 
                             '#aa5c03', '#026dac', '#f0e000', '0.5', '2']
            
            _, days, periodH, periodS, cor1, cor2, cor3, cor4, cor5, cor6, fill, width = valuesInList(lstInputs, defaultValues)
            # =========================================== #

            self.frame  = createFrame(self.root, row = 0, column = 0, padx = 5, pady = 5)

            #  Default checkbox to keep the window above others.
            self.checkOverlay = inputCheckbox(self.frame, 0, 0, 'Overlay')
            self.checkOverlay.configure(command = self.toggle_topmost)
            
            self.days    = inputIntSpinbox(self.frame, 1, 0, 'Total days', minimum = 1, maximum = 300, width = 4, defaultValue = int(days))
            self.periodH = inputIntSpinbox(self.frame, 2, 0, 'Period ImpulseMACD', minimum = 1, maximum = 500, width = 4, defaultValue = int(periodH))
            self.periodS = inputIntSpinbox(self.frame, 3, 0, 'Period ImpulseHisto', minimum = 1, maximum = 500, width = 4, defaultValue = int(periodS))
            self.height  = inputIntSpinbox(self.frame, 4, 0, 'Height MACD', 0, 5, width = 4, defaultValue = histoHeight)
            self.fill    = inputSlider(self.frame,     5, 0, 0, 1, defaultValue = fill, text = 'Fill:')
            self.width   = inputIntSpinbox(self.frame, 6, 0, 'Width line', minimum = 1, maximum = 6, width = 4, defaultValue = int(width))
            createVSeparator(self.frame, row = 1, column = 0, rowspan = 6)

            self.color1 = inputColor(self.frame, 1, 1, 'Macd 1', color = cor1, defaultColor = '#65c907')
            self.color2 = inputColor(self.frame, 2, 1, 'Macd 2', color = cor2, defaultColor = '#278a00')
            self.color3 = inputColor(self.frame, 3, 1, 'Macd 3', color = cor3, defaultColor = '#c70606')
            self.color4 = inputColor(self.frame, 4, 1, 'Macd 4', color = cor4, defaultColor = '#aa5c03')
            self.color5 = inputColor(self.frame, 5, 1, 'Histo',  color = cor5, defaultColor = '#026dac')
            self.color6 = inputColor(self.frame, 6, 1, 'Signal', color = cor6, defaultColor = '#f0e000')
            createHSeparator(self.frame, row = 7, column = 0, colspan = 5)

            button  = inputButton(self.frame, 8, 0, 'Apply', position = 'full', background = '#047e00')
            button.configure(command = lambda: self.writeInputs(pathConfig, symbol))

            btnExit = inputButton(self.frame, 8, 4, 'Close', position = 'full')
            btnExit.configure(command = self.close_window)


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

        lstInputs = [self.days.value(), self.periodH.value(), self.periodS.value(), self.color1.value(), 
                     self.color2.value(), self.color3.value(), self.color4.value(), self.color5.value(), 
                     self.color6.value(), self.fill.value(), self.width.value()]
        
        writeInput(path, symbol, lstInputs, isHistogram = True, heightHistogram = self.height.value())

        
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

    window = InpImpulsemacd()
    window.show()
# =================================== #