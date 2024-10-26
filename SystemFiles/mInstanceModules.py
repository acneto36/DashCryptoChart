import sys
import threading
import inspect
from   os import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from SystemFiles.mWriteRead  import *
from SystemFiles.mPathModule import *
from                   paths import *

thread = threading.Thread()

# --------------------------------------------------------------------------- #
def F_filterClass(method):

    module      =  F_reloadModule([method])
    classes     = [cls for cls in module.__dict__.values() if inspect.isclass(cls)]
    filterClass = [cls for cls in classes if 'Indicators' in cls.__module__]

    return classes, filterClass

# --------------------------------------------------------------------------- #
def F_selectInput(selectedInput, selectedSymbol, click, cont, df):  # Use in callBack

    global thread

    lstInput, lstModules = F_moduleIndicators('_inp__')

    if click > cont:
        if not thread.is_alive():
            for i in range(len(lstInput)):
                if selectedInput == lstInput[i]:

                    cont   = click
                    method = lstModules[i]
                    thread = threading.Thread(target = lambda: F_instanceInput(method, selectedSymbol, df))
                    thread.start()                 
                    break
        else:
            # If the thread is active, keep the variable 'cont' at the same value as 'click' to avoid opening an unwanted window
            cont += 1

    return cont

# --------------------------------------------------------------------------- #
def F_instanceInput(method, symbol, df):

    classes, filterClass = F_filterClass(method)
    
    if classes:
        for cls in filterClass:
            
            gui = cls(symbol, df)
            gui.show()
            break

# --------------------------------------------------------------------------- #
def F_loadModules(df, indicatorFolder, selectedSymbol, prefix: str):  # Use in CreateIndicator

    global thread

    lstFolders, lstModules = F_moduleIndicators(prefix)

    if not thread.is_alive():

        for i in range(len(lstFolders)):
            if indicatorFolder == lstFolders[i]:

                module = lstModules[i]
                thread = threading.Thread(target = lambda: F_instanceConsole(df, module, selectedSymbol, prefix))
                thread.start()                 
                break

# --------------------------------------------------------------------------- #
def F_instanceConsole(df, module, symbol, prefix):

    classes, filterClass = F_filterClass(module)
    
    if classes:
        for cls in filterClass:

            gui = cls(symbol, df)

            if prefix == '_inp__':
                gui.show()

            break

# --------------------------------------------------------------------------- #
def F_instanceInd(fig, df, symbol, lstInds):  # Use in callback

    lstInd, lstModules = F_moduleIndicators('_ind__')

    foundHistogram = False

    if len(lstInds) > 0:

        # Only selected indicator
        for x in range(len(lstInds)):
            # Search for the module corresponding to the indicator
            for i in range(len(lstModules)):

                if lstInd[i] == lstInds[x]:
            
                    module      = importlib.import_module(lstModules[i])
                    classes     = [cls for cls in module.__dict__.values() if inspect.isclass(cls)]
                    filterClass = [cls for cls in classes if 'Indicators' in cls.__module__]

                    with open(module.__file__, 'r') as file:
                        file_content = file.read()

                    if 'SEPARATE_WINDOW = True' in file_content:
                        
                        foundHistogram = True

                    for cls in filterClass:
                        cls(fig, df, symbol)

    # If a histogram is found, save the flag in a file 'Databases.foundHistogram.txt'
    if foundHistogram:
        F_writeFile('1', PATH_Histogram)
    else:
        F_writeFile('0', PATH_Histogram)

# ___________________________________________________________________________ #
def F_savePlotIndicator( symbol, lstInd ):  # Use in callback

    symbolFound = False
    lines       = readingFile(PATH_PlotInd)

    for i in range(len(lines)):
        partes = lines[i].strip().split(', ')

        if partes[0] == symbol:
            lines[i] = f"{symbol}, {', '.join(map(str, lstInd))}\n"
            symbolFound = True
            break

    if not symbolFound and len(lstInd) > 0:
        lines.append(f"{symbol}, {', '.join(map(str, lstInd))}\n")

    F_writeFile(lines, PATH_PlotInd)

# ___________________________________________________________________________ #
