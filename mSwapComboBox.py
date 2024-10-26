import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paths                    import *
from SystemFiles.mWriteRead   import *
from SystemFiles.mManageLists import *
from DataFrames.mReturnLists  import *


chosenExchange = None
flagSwapList   = False
flagSwapTf     = False

# ___________________________________________________________________________ #
def F_updateCheckBox(cbboxExchange, cbboxTF, listLeft, listRight):
    
    F_swapExchange(cbboxExchange, listLeft, listRight)
    F_swapListTf(cbboxTF)

    defaultValue = F_readTimeframe(chosenExchange, PATH_TimeFrame)
    cbboxTF.setCurrentText(defaultValue)
# ___________________________________________________________________________ #
def F_swapExchange(cbbox, listLeft, listRight):

    global chosenExchange 
    global flagSwapTf 

    selectedValue  = cbbox.currentText()
    chosenExchange = selectedValue
    flagSwapTf     = True

    F_writeFile(selectedValue, PATH_Exchanges)
    F_updateLists(listLeft, listRight, chosenExchange)

# ___________________________________________________________________________ #
def F_swapListTf(cbbox):

    global flagSwapList

    # Set the flag to indicate that the F_swapListTf method 
    # is being called and block any unauthorized calls to the F_swapTimeFrame method
    flagSwapList = True

    cbbox.clear()
    lstTF = F_LstTF(chosenExchange)
    cbbox.addItems(lstTF)

    # Reset the flag after adjustments
    flagSwapList = False

 # ___________________________________________________________________________ #
def F_swapTimeFrame(cbbox, exchange):
    
    global flagSwapList
    global chosenExchange
    global flagSwapTf
     
    if flagSwapList:
        return 

    # chosenExchange receives the default value from the main file only once
    if not flagSwapTf:
        chosenExchange = exchange

    selectedValue = cbbox.currentText()

    F_writeTimeframe(selectedValue, PATH_TimeFrame, chosenExchange)

    cbbox.setStyleSheet("color: white;")

# ___________________________________________________________________________ #
