import sys
from   os  import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)
    
from DataFrames.mFormatNumber import *

# ___________________________________________________________________________ #
def F_toolTipLines(lstPrices):

    hovertext  = []

    for i in range(len(lstPrices)):

        price = formatNumber(lstPrices[i])
        text  = (
            '<span style="color: #ffffff; font-weight: bold; font-size: 14px; font-family: Monaco, monospace;"> ' + ' Price: '  + price + '</span>'
        )
        hovertext.append(text)

    return hovertext

# ___________________________________________________________________________ #