import os
import sys
import traceback
import mttkinter  as mtk

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
pathConfig  = os.path.join(currentDir, 'config.txt')  # Automatically created file for this input

# histoHeight = int(readFile(PATH_HWaves)[0]) if len(readFile(PATH_HWaves)) > 0 else 3 # For histogram

# ___________________________________________________________________________ #
class InpNewName:  # The name must start with 'Inp'
    def __init__(self, symbol = '', df = None): # Do not remove parameters

        # mtTkinter version for multithreads
        self.root = mtk.mtTkinter.Tk()

        self.root.configure(bg = '#595959')
        self.root.minsize(150, 150)
        self.root.title("My input")

        self.root.configure(border = None)
        self.root.resizable(width  = False, height = False)
        self.root.iconphoto(False, mtk.mtTkinter.PhotoImage(file = PATH_Icon))
 
        try:
            # ============== values from input=========== #
            '''
                This code block must be inserted into the indicator file and the input file.  
                Always keep it identical in both files to avoid errors when reading the saved settings.
            '''
            lstInputs     = readingInput( pathConfig, symbol )
            # Examble default values, only string!
            defaultValues = [symbol, 'entry', '5', '1.5', 'None', '0.5', '#ffffff', '2024-01-01 00:00' ] 
            _, value1, value2, value3, value4, value5, value6, value7 = valuesInList(lstInputs, defaultValues)
            # =========================================== #

            self.frame = createFrame(self.root, row = 0, column = 0, padx = 5, pady = 5)

            #  Default checkbox to keep the window above others 'Optional'.
            self.checkOverlay = inputCheckbox(self.frame, 0, 0, 'Overlay')
            self.checkOverlay.configure(command = self.toggle_topmost)


            lstValues = ['valueA', 'valueB', 'valueC']

            inputLabel(self.frame, 1, 0, text = 'My label', textColor = 'white', background ='#575757')

            self.entry        = inputEntry(self.frame, row = 2, column = 0, text = 'Entry', width = 140, defaultValue = value1, textType = 'text')
            
            self.intSpinBox   = inputIntSpinbox(self.frame,   3, 0, 'Spin int', minimum = -10, maximum = 2000, width = 4, defaultValue = int(value2))
            self.floatSpinBox = inputFloatSpinbox(self.frame, 4, 0, 'Spin Float', width = 4, defaultValue = float(value3))
            
            self.optionMenu = inputOptions(self.frame, 5, 0, text = 'Options', values = lstValues, defaultValue = value4)
            self.slider     = inputSlider(self.frame,  6, 0, 0, 1, defaultValue = value5)
            self.color      = inputColor(self.frame,   7, 0, 'Up', color = value6, defaultColor = 'white')
            
            self.dateTime   = inputDatetime(self.frame, 8, 0, 'Date time', dateTime = value7)

            button = inputButton(self.frame, 9, 0, 'Apply', position = 'full', background = '#047e00')
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
    # Example of how to record values for input
        
    def writeInputs(self, path, symbol):

        lstInputs = [self.entry.value(), self.intSpinBox.value(), self.floatSpinBox.value(), self.optionMenu.value(), 
                     self.slider.value(), self.color.value(), self.dateTime.value()]
        
        writeInput(path, symbol, lstInputs)

        # if is Histogram #
        # writeInput(path, symbol, lstInputs, True, self.spinHeight.value())

        # Check values in log #
        # console(f'list {lstInputs}')

        
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

    window = InpNewName()
    window.show()
# =================================== #