import sys
from   os  import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from DataFrames.mFormatNumber import *
from paths                    import *


# ___________________________________________________________________________ #
def F_checkFileInput(pathFile: str):

    if not path.exists(pathFile):
        with open(pathFile, 'w') as file:
            file.write('')

# ___________________________________________________________________________ #
def readFile(pathFile: str) -> list:

    F_checkFileInput(pathFile)

    with open(pathFile, 'r') as file:
        lstStr = file.readlines()
    
    return lstStr

# ___________________________________________________________________________ #
def writeFile(value, pathFile: str):

    F_checkFileInput(pathFile)

    with open(pathFile, 'w') as file:
        file.writelines(value)

# ___________________________________________________________________________ #
def F_checkEmptyValue(pathFile: str):

    lstValues = []
    lines     = readFile(pathFile)

    if len(lines) > 0:

        for i in range(len(lines)):

            parts = lines[i].strip().split('; ')

            if parts[1] != '':  #  and parts[2] != ''
                lstValues.append(lines[i])

    writeFile(lstValues, pathFile)

# ___________________________________________________________________________ #
def writeInput(pathFile: str, symbol: str, lstInputs, isHistogram = False, heightHistogram = 3):

    F_checkEmptyValue(pathFile)

    lstInputs.insert(0, symbol)

    # Ensure that all values become strings.
    lstInputsStr = [str(item) for item in lstInputs]
    strVar       = '; '.join(lstInputsStr)

    # Correction: Depending on the locale, the float separator in the input is changed to a comma. Fixed to '.'.
    strVar      = strVar.replace(',', '.')

    symbolFound = False
    lines       = readFile(pathFile)
    
    for i, linha in enumerate(lines):
        parts = linha.strip().split('; ')

        if parts[0] == symbol:

            lines[i] = f'{strVar}\n'
            symbolFound = True
            break

    if not symbolFound:
        lines.append(f'{strVar}\n')

    writeFile(lines, pathFile)

    if isHistogram:
        writeFile(heightHistogram, PATH_HWaves)

# ___________________________________________________________________________ #
def readingInput(pathFile: str, symbol: str) -> list:

    lines = readFile(pathFile)

    for x in range(len(lines)):
        parts = lines[x].strip().split('; ')

        if parts[0] == symbol:
            return parts

    return []

# ___________________________________________________________________________ #

