import sys
import traceback
from   os        import path
import mttkinter     as mtk

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from CreateIndicator.Extra.collection import *
from SystemFiles.mWriteLog            import *
from CreateIndicator.Extra.mWidgets   import *
from CreateIndicator.Extra.mConsole   import console
from paths                            import PATH_Icon, PATH_Log

currentDir = path.dirname(path.realpath(__file__))
pathConfig = path.join(currentDir, 'configHoursChannel.txt')

# ___________________________________________________________________________ #
class InpHoursChannel:
    def __init__(self, symbol = '', df = None):

        self.root = mtk.mtTkinter.Tk()
        self.root.title( "Hours channel" )

        self.root.configure(border = None)
        self.root.resizable(width = False, height = False)
        self.root.iconphoto(False, mtk.mtTkinter.PhotoImage(file = PATH_Icon))

        try:
            # =========================================== #
            lstInputs     = readingInput(pathConfig, symbol)
            defaultValues = [symbol, '2024-01-01 00:00', '2024-02-01 00:00', 'False', 'Normal']

            _, startDate, endDate, colorCandle, extendLine = valuesInList(lstInputs, defaultValues)
            # =========================================== #

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

            self.candleColor  = inputCheckbox(self.frame, 0, 1, 'Color candle', defaultValue = colorCandle)

            # =================== DATE TIME ================ #
            self.startDate  = inputDatetime(self.frame, 2, 0, text = 'Start date', dateTime = startDate)
            self.endDate    = inputDatetime(self.frame, 3, 0, text = 'End date',   dateTime = endDate)

            # =================== OPTION MENU ================= #
            self.optionMenu = inputOptions(self.frame, 4, 0, text = 'Extend Line', values = ['Normal', 'Size'], defaultValue = extendLine)
            
            # ================== BUTTON ================= #
            btnAplly = inputButton(self.frame, 5, 1, text = 'Apply', position = 'full', background = '#047e00')
            btnAplly.configure(command = lambda: self.writeInputs(pathConfig, symbol))

            btnExit  = inputButton(self.frame, 5, 0, text = 'Close', position = 'full')
            btnExit.configure(command = self.close_window)

        except Exception as e:

            name      = f'{self.__class__.__name__[3:]}'
            errorMsg  = ''.join(traceback.format_exception_only(type(e), e)).strip()
            errorLine = traceback.extract_tb(e.__traceback__)[-1].lineno

            print(f"{errorMsg} -> Input '{name}' in Line {errorLine}")
            F_writeLog(PATH_Log, f"{errorMsg} -> Input '{name}' in Line {errorLine}")
            pass
    
    # ___________________________________________________________________________ #
    def writeInputs(self, path, symbol):

        lstInputs = [self.startDate.value(), self.endDate.value(), 
                     self.candleColor.value(), self.optionMenu.value()]

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

    window = InpHoursChannel()
    window.show()
# =================================== #



