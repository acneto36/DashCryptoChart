import sys
from   os  import path
import pandas  as pd

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from DataFrames.mFormatNumber import *

# ___________________________________________________________________________ #
def F_toolTip(df):

    df['date'] = pd.to_datetime(df['date'])
    hovertext  = []

    for i in range(len(df['date'])):

        op = formatNumber(df["open"][i])
        hg = formatNumber(df["high"][i])
        lw = formatNumber(df["low"][i]) 
        cl = formatNumber(df["close"][i])
        vl = F_financialNumber((float(df['volume'][i])))
        
        colorTitle = '#ffffff'
        colorValue = '#00c3ca'

        text = (
            '<span style="font-weight: bold; font-size: 14px; font-family: Monaco, monospace; color: #dd27d4">_________________' + '</span><br>'
            '<span style="font-weight: bold; font-size: 13px; font-family: Monaco, monospace; color: #dd27d4">'
            ' ' + df['date'][i].strftime('%Y/%m/%d %H:%M') + '<br><br>' +
            ' <span style="color: ' + colorTitle + ';">Open:</span>   <span style="color: ' + colorValue + ';">' + op + '</span><br>'
            ' <span style="color: ' + colorTitle + ';">High:</span>   <span style="color: ' + colorValue + ';">' + hg + '</span><br>'
            ' <span style="color: ' + colorTitle + ';">Low:</span>    <span style="color: ' + colorValue + ';">' + lw + '</span><br>'
            ' <span style="color: ' + colorTitle + ';">Close:</span>  <span style="color: ' + colorValue + ';">' + cl + '</span><br>'
            ' <span style="color: ' + colorTitle + ';">Volume:</span> <span style="color: ' + colorValue + ';">' + vl + '</span><br>'
            ' <span style="color: ' + colorTitle + ';">Index:</span>  <span style="color: ' + colorValue + ';">' + str(df['index'][i]) + '</span>'
        )
        
        hovertext.append(text)
    
    return hovertext

# ___________________________________________________________________________ #
def F_financialNumber(_src):

    _txt = (
        '{:.2f} 🅃'.format(_src/1000000000000.0) if _src >= 1000000000000 else
        '{:.2f} Ⓑ'.format(_src/1000000000.0)    if _src >= 1000000000 and _src < 999999999999 else
        '{:.2f} Ⓜ'.format(_src/1000000.0)       if _src >= 1000000 and _src < 999999999 else
        '{:.2f} Ⓚ'.format(_src/1000.0)          if _src >= 1000 and _src < 999999 else
        '{:.2f} Ⓤ'.format(_src/10.0)
    )

    return _txt

# ___________________________________________________________________________ #