'''
    Convertendo para o novo formato do tutorial.
    Erro ao calcular os resultados no layout direito!!!
'''


import sys
import traceback
from   os            import path
from   tkinter       import messagebox
import mttkinter         as mtk
import customtkinter     as ctk 
                

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from SystemFiles.mWriteLog              import *
from CreateIndicator.Extra.mConsole     import console
from CreateIndicator.Extra.mWidgets     import *
from Indicators.Functions.mCalculations import *
from DataFrames.mFormatNumber       import *
from DataFrames.mDataSeries             import *
from CreateIndicator.Extra.collection   import *
from paths                              import PATH_Icon

 
currentDir = path.dirname(path.realpath(__file__))
pathConfig = path.join(currentDir, 'configManageTrade.txt')
pathValues = path.join(currentDir, 'calculations.txt')
pathLog    = path.join(srcPath, 'Log', 'logs.txt')

# ___________________________________________________________________________ #
class InpManageTrade:
    def __init__(self, symbol = '', df = None):

        # mtTkinter version for multithreads
        self.root = mtk.mtTkinter.Tk()
        self.root.title("Manage Trader")
    
        self.root.configure(border = None)
        self.root.resizable(width = False, height = False)
        self.root.iconphoto(False, mtk.mtTkinter.PhotoImage(file = PATH_Icon))

        try:

            self.cl        = closes(df)
            self.corGl     = 'white'
            self.lstValues = readingInput(pathValues, symbol)

            # =========================================== #
            lstInputs      = readingInput(pathConfig, symbol)

            defaultValues  = [symbol, '0', '0', '0', '0', '0', '0', 'False']

            _, firstEntry, firstCoin, secondEntry, secondCoin, partial, partialCoin, confirm = valuesInList(lstInputs, defaultValues)
            # =========================================== #

            self.frameLeft = createFrame(
                self.root, 
                row        = 0, 
                column     = 0, 
                padx       = 5, 
                pady       = 5, 
                background = '#595959'
            )

            self.frameRight = createFrame(
                self.root, 
                row        = 0, 
                column     = 1, 
                padx       = 5, 
                pady       = 5, 
                background = '#755C35'
            )

            self.checkOverlay = inputCheckbox(self.frameLeft, 0, 0, 'Overlay')
            self.checkOverlay.configure(command = self.toggle_topmost)

            # Confirm if you have made the second entry to recalculate the average price and total coins
            self.checkConfirm = inputCheckbox(self.frameLeft, 0, 1, 'Confirm', defaultValue = confirm)
            
            self.F_createInputs(firstEntry, firstCoin, secondEntry, secondCoin, partial, partialCoin)

            inputLabel(self.frameLeft, 4, 0, text = '', background ='transparent')
            createHSeparator(self.frameLeft, 4, 0, 5)

            self.corGl = '#73D216' if float(firstCoin) > 0 else '#cc0000' # Color for gain or loss

            self.F_labelResult(symbol)


            # ================== BUTTON ================= #
            btnAplly = inputButton(self.frameLeft, 5, 1, text = 'Apply', position = 'full', background = '#047e00')
            btnAplly.configure(command = lambda: self.F_writeInputs(pathConfig, symbol))

            btnExit  = inputButton(self.frameLeft, 5, 0, text = 'Close', position = 'full')
            btnExit.configure(command = self.close_window)

            btnDelete = inputButton(self.frameLeft, 5, 4, text = 'Delete', position = 'right', background = '#CE5C00')
            btnDelete.configure(command = lambda: self.F_deleteValues(pathConfig, symbol))
            # =========================================== #
            
        except Exception as e:

            name      = f'{self.__class__.__name__[3:]}'
            errorMsg  = ''.join(traceback.format_exception_only(type(e), e)).strip()
            errorLine = traceback.extract_tb(e.__traceback__)[-1].lineno

            print(f"{errorMsg} -> Input '{name}' in Line {errorLine}")
            F_writeLog(pathLog, f"{errorMsg} -> Input '{name}' in Line {errorLine}")
            pass

    # ___________________________________________________________________________ #
    def F_writeInputs(self, path, symbol):

        lstInputs = [self.txtEntry1.value(), self.txtCoins1.value(), self.txtEntry2.value(), 
                     self.txtCoins2.value(), self.percent.value(), self.txtCoinsPart.value(), self.checkConfirm.value()]
        
        writeInput(path, symbol, lstInputs)

        self.F_labelResult(symbol)

    
    # ___________________________________________________________________________ #
    def F_labelResult(self, symbol):

        # Load the content of the config file and return a list with the results
        lstReceiveValues = F_loadValues( pathConfig, symbol, self.cl[-1])  #  

        print(f'lstReceiveValues {lstReceiveValues}')

        for i in range(len(lstReceiveValues)):

            # Keep total coins unchanged
            if i != 2:
                lstReceiveValues[i] = formatNumber(float(lstReceiveValues[i]))

        lstReceiveValues[1] = decimalFormat(float(lstReceiveValues[1]))

        if len(lstReceiveValues) > 0:

            lstInputs = [lstReceiveValues[0], lstReceiveValues[1], lstReceiveValues[2], 
                         lstReceiveValues[3], lstReceiveValues[4]]
        
            writeInput(pathValues, symbol, lstInputs)

        self.lstValues = readingInput(pathValues, symbol)
        self.inputs    = readingInput(pathConfig, symbol)
        formatPg       = F_partialGain(pathConfig, symbol, float(self.inputs[5]), float(self.inputs[6])) if len(self.inputs) > 0 else 0
        formatPg       = "{:.4f}".format(float(formatPg))  # Partial gain or exit position

        self.lstValues.append(formatPg)
        self.F_labelCreate(self.lstValues)

        print(f'lstvalues {self.lstValues}')
        

    # ___________________________________________________________________________ #
    def F_deleteValues(self, pathConfig, symbol):

        msg = messagebox.askyesno('', 'Delete values?')   
                
        if msg:
            lines = readFile(pathConfig)

            symbolFound = False

            for line in lines:
                partes = line.strip().split('; ')

                if len(partes) >= 1 and partes[0] == symbol:

                    lines.remove(line)
                    symbolFound = True

            # Rewrite the file with the updated lines (excluding the symbol line)
            if symbolFound:
                writeFile(lines, pathConfig)

            self.F_labelCreate(['0', '0', '0', '0', '0', '0', '0'])
            self.F_createInputs('0', '0', '0', '0', '0', '0')

    # ___________________________________________________________________________ #
    def F_createInputs(self, firstE, firstC, secE, secC, partial, partialCoin):

        self.txtEntry1 = inputEntry(self.frameLeft, 1, 0, '1st Entry', width = 140, defaultValue = firstE, textType = 'float')
        self.txtCoins1 = inputEntry(self.frameLeft, 1, 1, 'Coins',     width = 130, defaultValue = firstC, textType = 'float')

        self.txtEntry2 = inputEntry(self.frameLeft, 2, 0, '2nd Entry', width = 140, defaultValue = secE, textType = 'float')
        self.txtCoins2 = inputEntry(self.frameLeft, 2, 1, 'Coins',     width = 130, defaultValue = secC, textType = 'float')

        self.percent      = inputFloatSpinbox(self.frameLeft, 3, 0, '% Partial', maximum = 100, width = 4, defaultValue = float(partial))
        self.txtCoinsPart = inputEntry(self.frameLeft, 3, 1, 'Coins', width = 130, defaultValue = partialCoin, textType = 'float')

    # ___________________________________________________________________________ #
    def F_labelCreate(self, lstValues):

        inputLabel(self.frameRight, 0, 4, "Average price:", width = 150, textColor ="white", background = '#755C35')
        inputLabel(self.frameRight, 1, 4, "Total coins:",   width = 150, textColor ="white", background = '#755C35')
        inputLabel(self.frameRight, 2, 4, "Invested:",      width = 150, textColor ="white", background = '#755C35')
        inputLabel(self.frameRight, 3, 4, "Gain / Loss:",   width = 150, textColor ="white", background = '#755C35')
        inputLabel(self.frameRight, 4, 4, "Current value:", width = 150, textColor ="white", background = '#755C35')
        inputLabel(self.frameRight, 5, 4, "Partial gain:",  width = 150, textColor ="white", background = '#755C35')
                            
        inputLabel(self.frameRight, 0, 5, lstValues[1], width = 150, textColor = '#EDD400', background = '#414141')
        inputLabel(self.frameRight, 1, 5, lstValues[3], width = 150, textColor = '#EDD400', background = '#414141')
        inputLabel(self.frameRight, 2, 5, lstValues[4], width = 150, textColor = '#EDD400', background = '#414141')
        inputLabel(self.frameRight, 3, 5, lstValues[2], width = 150, textColor = self.corGl,  background = '#3465A4') 
        inputLabel(self.frameRight, 4, 5, lstValues[5], width = 150, textColor = self.corGl,  background = '#414141') 
        inputLabel(self.frameRight, 5, 5, lstValues[6], width = 150, textColor = self.corGl,  background = '#414141')    

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

    window = InpManageTrade()
    window.show()
# # =================================== #