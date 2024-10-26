
import sys
import traceback
from   os             import path
from   CTkColorPicker import *
import mttkinter      as mtk
import customtkinter  as ctk 

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from SystemFiles.mWriteLog            import *
from CreateIndicator.Extra.mWidgets   import *
from CreateIndicator.Extra.collection import *
from CreateIndicator.Extra.mConsole   import console
from paths                            import PATH_Icon, PATH_Log

currentDir = path.dirname(path.realpath(__file__))
pathConfig = path.join(currentDir, 'configMoveAverage.txt')  # Automatically created file for this input

# ___________________________________________________________________________ #
class InpMoveAverage:
    def __init__(self, symbol = '', df = None): # Do not remove parameters
 
        # mtTkinter version for multithreads
        self.root = mtk.mtTkinter.Tk()
        self.root.title("Move average")

        self.root.configure(border = None)
        self.root.resizable(width = False, height = False)
        self.root.iconphoto(False, mtk.mtTkinter.PhotoImage(file = PATH_Icon))

        try:
            # =========================================== #
            lstInputs     = readingInput(pathConfig, symbol)
            defaultValues = [symbol, '100', 'sma', 'Single color', 'solid', '1', '#5cfffe', '#da2506', '30', '0.5']

            _, period, avgType, colorType, lineType, lineWidth, colorUp, colorDn, start, cloud = valuesInList(lstInputs, defaultValues)
            # =========================================== #

            self.frame = createFrame(
                self.root, 
                row        = 0, 
                column     = 0, 
                padx       = 5, 
                pady       = 5, 
                background = '#444444'
            )

            self.checkOverlay = inputCheckbox(self.frame, 0, 0, 'Overlay')
            self.checkOverlay.configure(command = self.toggle_topmost)

            listMa = ['sma', 'ema', 'wma', 'smma', 'zlema']

            self.spinStart   = inputIntSpinbox(self.frame, 1, 0, 'Start',     maximum = 2000, width = 4, defaultValue = int(start))
            self.spinPeriods = inputIntSpinbox(self.frame, 2, 0, 'Periods',   maximum = 2000, width = 4, defaultValue = int(period))
            self.optTypeAvg  = inputOptions(self.frame,    3, 0, 'Type AVG',   values = listMa , defaultValue = avgType)
            self.optColor    = inputOptions(self.frame,    4, 0, 'Type color', values = ['Single color', 'Multi color'], defaultValue = colorType)
            self.optTypeLine = inputOptions(self.frame,    5, 0, 'Type line',  values = ['solid', 'dash', 'dot', 'dashdot'], defaultValue = lineType)
            self.spinLine    = inputIntSpinbox(self.frame, 6, 0, 'Line width',  width = 4, defaultValue = int(lineWidth))
            self.color1      = inputColor(self.frame,      7, 0, 'Color1',      color = colorUp, defaultColor = 'white')
            self.color2      = inputColor(self.frame,      8, 0, 'Color2',      color = colorDn, defaultColor = 'orange')
            self.slider      = inputSlider(self.frame,     9, 0, 0, 1, float(cloud), text = 'cloud')

            btnAplly = inputButton(self.frame, 10, 1, 'Apply', position = 'full', background = '#047e00')
            btnAplly.configure(command = lambda: self.F_writeInputs(pathConfig, symbol))

            btnExit  = inputButton(self.frame, 10, 0, 'Close', position = 'full')
            btnExit.configure(command = self.close_window)

        except Exception as e:

            name      = f'{self.__class__.__name__[3:]}'
            errorMsg  = ''.join(traceback.format_exception_only(type(e), e)).strip()
            errorLine = traceback.extract_tb(e.__traceback__)[-1].lineno

            print(f"{errorMsg} -> Input '{name}' in Line {errorLine}")
            F_writeLog(PATH_Log, f"{errorMsg} -> Input '{name}' in Line {errorLine}")
            pass
        
    # ___________________________________________________________________________ #
    def F_writeInputs(self, path, symbol):

        lstInputs = [self.spinPeriods.value(), self.optTypeAvg.value(), self.optColor.value(), 
                     self.optTypeLine.value(), self.spinLine.value(), self.color1.value(), 
                     self.color2.value(), self.spinStart.value(), self.slider.value()]
        
        writeInput(path, symbol, lstInputs)

    # ___________________________________________________________________________ #
    def toggle_topmost(self):

        if self.checkOverlay.value():
            self.root.attributes('-topmost', 1)
        else:
            self.root.attributes('-topmost', 0)

    # ___________________________________________________________________________ #
    def show(self):
        self.root.mainloop()

    # ___________________________________________________________________________ #
    def close_window(self):
        self.root.destroy()

# ___________________________________________________________________________ #
if __name__ == '__main__':

    window = InpMoveAverage()
    window.show()
