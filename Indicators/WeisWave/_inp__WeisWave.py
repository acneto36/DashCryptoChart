import sys
import traceback
from   os             import path
import mttkinter          as mtk
import customtkinter      as ctk 
from   CTkColorPicker import *

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from CreateIndicator.Extra.collection import *
from SystemFiles.mWriteLog            import *
from CreateIndicator.Extra.mWidgets   import *
from CreateIndicator.Extra.mConsole   import console
from paths                            import *

currentDir = path.dirname(path.realpath(__file__))
pathConfig = path.join(currentDir, 'configWeisWave.txt')
pathLog    = path.join(srcPath, 'Log', 'logs.txt')

histoHeight = int(readFile(PATH_HWaves)[0]) if len(readFile(PATH_HWaves)) > 0 else 3 # For histogram

# ___________________________________________________________________________ #
class InpWeisWave:

    def __init__(self, symbol = '', df = None):

        self.root = mtk.mtTkinter.Tk()
        self.root.title( "Weis Wave" )

        self.root.configure(border = None)
        self.root.resizable(width = False, height = False)
        self.root.iconphoto(False, mtk.mtTkinter.PhotoImage(file = PATH_Icon))

        try:

            lstInputs     = readingInput(pathConfig, symbol)
            defaultValues = [symbol, '2', '0', 'Normal', '#5cfffe', '#da2506']

            _, startDay, percent, invert, colorUp, colorDn = valuesInList(lstInputs, defaultValues)

            self.frame = createFrame(
                self.root, 
                row        = 0, 
                column     = 0, 
                padx       = 5, 
                pady       = 5, 
                background = '#444444'
            )

            # =================== CHECKBOX ================= #
            self.checkOverlay = inputCheckbox(self.frame, 0, 0, 'Overlay')
            self.checkOverlay.configure(command = self.toggle_topmost)

            self.spinDays    = inputIntSpinbox(self.frame,   1, 0, 'Total days', minimum = -10, maximum = 2000, width = 4, defaultValue = int(startDay))
            self.spinPercent = inputFloatSpinbox(self.frame, 2, 0, 'Percent', width = 4, defaultValue = float(percent))
           
            self.optionMenu  = inputOptions(self.frame, 3, 0, text = 'Wave', values = ['Normal', 'Invert'], defaultValue = invert)
            self.spinHeight  = inputIntSpinbox(self.frame, 4, 0, 'Height', width = 4, defaultValue = histoHeight)
           
            self.colorUp     = inputColor(self.frame, row = 5, column = 0, text = 'Up',   color = colorUp, defaultColor = 'green')
            self.colorDn     = inputColor(self.frame, row = 6, column = 0, text = 'Down', color = colorDn, defaultColor = 'orange')

            btnAplly = inputButton(self.frame, 7, 1, text = 'Apply', position = 'full', background = '#047e00')
            btnAplly.configure(command = lambda: self.F_writeInputs(pathConfig, symbol))

            btnExit  = inputButton(self.frame, 7, 0, text = 'Close', position = 'full')
            btnExit.configure(command = self.close_window)


        except Exception as e:

            name      = f'{self.__class__.__name__[3:]}'
            errorMsg  = ''.join(traceback.format_exception_only(type(e), e)).strip()
            errorLine = traceback.extract_tb(e.__traceback__)[-1].lineno

            print(f"{errorMsg} -> Input '{name}' in Line {errorLine}")
            F_writeLog(pathLog, f"{errorMsg} -> Input '{name}' in Line {errorLine}")
            pass

    # ___________________________________________________________________________ #
    def F_writeInputs(self, path, symbol):

        lstInputs = [self.spinDays.value(), self.spinPercent.value(), self.optionMenu.value(), 
                     self.colorUp.value(), self.colorDn.value()]
        
        writeInput(path, symbol, lstInputs, True, self.spinHeight.value())

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

    window = InpWeisWave()
    window.show()
