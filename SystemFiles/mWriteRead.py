import sys
from   os import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from SystemFiles.mWriteLog import F_writeLog

PATH_Log = path.join(srcPath, 'Log', 'logs.txt')

# ___________________________________________________________________________ #
def contLines(pathFile: str):

    with open(pathFile, 'r') as file:
        count = file.readlines()
    
    return len(count)

# ___________________________________________________________________________ #
def F_checkFileExist(pathFile, value = '', log = False):
    
    if not path.exists(pathFile):
        F_writeFile(value, pathFile)

    if (contLines(pathFile) < 1 and value == '') and log:

        F_writeLog(PATH_Log, f'Value is empty: {pathFile}')
        print(f'Value is empty: {pathFile}')
        return

    # If the file is empty and depends on a value, add a default value.
    if contLines(pathFile) < 1:  
        F_writeFile(value, pathFile)


# ___________________________________________________________________________ #
def readingFile(pathFile: str, defaultValue = '', log = False):

    F_checkFileExist(pathFile, defaultValue, log)

    with open(pathFile, 'r') as file:
        lstStr = file.readlines()
    
    return lstStr

# ___________________________________________________________________________ #
def F_writeFile(value = '', pathFile = ''):

    with open(pathFile, 'w') as file:
        file.writelines(value)

# ___________________________________________________________________________ #
def F_checkEmptyIndicator(pathFile: str):

    lstValues = []
    lines     = readingFile(pathFile)

    if len(lines) > 0:
        for i in range(len(lines)):

            parts = lines[i].strip().split(', ')

            if len(parts) > 1:
                lstValues.append(lines[i])

    F_writeFile(lstValues, pathFile)

# ___________________________________________________________________________ #
def F_checkFileTF(pathFile, value = ''):

    lstFile = readingFile(pathFile)

    if not path.exists(pathFile):
        F_writeFile(value, pathFile)

    else: # Correction if it does not contain 2 filled lines
        if contLines(pathFile) < 2 or not lstFile[0].strip() or not lstFile[1].strip():
            F_writeFile(value, pathFile)

# ___________________________________________________________________________ #
def F_writeTimeframe(timeFrame, pathFile, chosenExchange):

    # Separate each line into a list format.
    with open(pathFile, 'r') as file:
        listOfList = [lst.strip().split(', ') for lst in file]

    for item in listOfList:
        if item[0] == chosenExchange:

            item[1] = timeFrame
            break

    with open(pathFile, 'w') as file:
        file.write('\n'.join(', '.join(item) for item in listOfList))

# ___________________________________________________________________________ #
def F_readTimeframe(exchange, pathFile):

    with open(pathFile, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):

        parts = lines[i].strip().split(', ')

        if parts[0] == exchange:
            return parts[1]

# ___________________________________________________________________________ #
def F_readUpdateSec(pathFile):

    return readingFile(pathFile, '10')[0]

# ___________________________________________________________________________ #
def F_readIndicator(pathFile: str, symbol: str): # used in callBack.py
    
    lstStr = []
    lines  = readingFile(pathFile)

    for x in range(len(lines)):

        partes = lines[x].strip().split(', ')

        if partes[0] == symbol:

            lstStr = partes[1:]  # ignore first element (symbol)
            break

    return lstStr

# ___________________________________________________________________________ #