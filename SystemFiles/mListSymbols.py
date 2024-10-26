from   os import path
import sys

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from SystemFiles.mWriteRead import *

# ___________________________________________________________________________ #
def F_listSymbols(pathFile) -> list:

    symbols = []
    lines   = readingFile(pathFile)
        
    # save selected symbols in lists
    for line in lines:
        
        item = line.strip()
        symbols.append(item)

    return symbols
