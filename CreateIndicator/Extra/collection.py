import sys
import itertools
import pandas             as pd
from   os             import path
from   datetime       import timedelta


srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

import DataFrames.mDataSeries                    as series
from   CreateIndicator.Extra.mWriteReadInput import *


# ___________________________________________________________________________ #
def selectDay(df: pd.DataFrame, numDay: int = 1) -> int:

    '''
        Returns the index of the first candle of the day
        Example: Count of days from the current day to the oldest day
    '''

    date = series.dates(df)
    size = series.size(df)

    if numDay <= 0:
        return size-1
    
    contDays = 0
    oldDate  = pd.to_datetime(date[-1])

    for i in range(size-2, 0, -1):

        if oldDate.day != date[i].day: 
            contDays += 1
        
        if (contDays == numDay) or (i == 0):
            return i + 1

        oldDate = date[i]

    # If the chosen number of days is greater than the existing number of days
    return 0

# ___________________________________________________________________________ #
def indexByDate(df: pd.DataFrame, date: str) -> int:

    '''
        Return index of a especific date
        Example: "2023-08-20 09:00"\n
        Note: Hours and minutes based in timeframe
    '''

    date = pd.to_datetime(date)
    size = series.size(df)
    dt   = series.dates(df)

    for i in range(size-1, 0, -1):

        if dt[i] == date:
            return i
    
    return size-1

# ___________________________________________________________________________ #
def maxPrice(df: pd.DataFrame, startIndex: int, endIndex: int) -> float:

    ''' Returns the maximum price in the selected range '''

    hg = series.highs(df)

    return max(hg[startIndex:endIndex + 1])

# ___________________________________________________________________________ #
def minPrice(df: pd.DataFrame, startIndex: int, endIndex: int) -> float:

    ''' Returns the minimum price in the selected range '''

    lw = series.lows(df)

    return min(lw[startIndex:endIndex + 1])

# ___________________________________________________________________________ #
def indexMaxPrice(df: pd.DataFrame, startIndex: int, endIndex: int) -> int:

    ''' Returns the index of the candle with the maximum value in the selected range '''
   
    hg    = series.highs(df)
    max   = 0
    index = len(hg)-1

    for i in range(startIndex, endIndex):
        if hg[i] >= max:
            max   = hg[i]
            index = i

    return index

# ___________________________________________________________________________ #
def indexMinPrice(df: pd.DataFrame, startIndex: int, endIndex: int) -> int:

    ''' Returns the index of the candle with the minimum value in the selected range '''
   
    lw    = series.lows(df)
    min   = lw[startIndex]
    index = len(lw) - 1

    for i in range(startIndex, endIndex):
        if lw[i] <= min:
            min   = lw[i]
            index = i

    return index

# ___________________________________________________________________________ #
def shiftDateHours(date: pd.Timestamp, shift: int) -> pd.Timestamp:

    '''
        Shifts the original date by hours.
        Positive number: Shifts to the right.
        Negative number: Shifts to the left.
        Note: Choose the hours according to the selected time frame
    '''

    return date + timedelta(hours = shift)

# ___________________________________________________________________________ #
def shiftDateMinutes(date: pd.Timestamp, shift: int) -> pd.Timestamp:

    '''
        Shifts the original date by minutes.
        Positive number: Shifts to the right.
        Negative number: Shifts to the left.
        Note: Choose the minutes according to the selected time frame
    '''

    return date + timedelta(minutes = shift)

# ___________________________________________________________________________ #
def pdDatetime(date: str) -> pd.Timestamp:

    ''' Converts the date to the pandas datetime format '''

    return pd.to_datetime(date)

# ___________________________________________________________________________ #
def hexcolorToRgba(hexColor: str, alpha: float):

    ''' Convert hexadecimal color to rgba color '''

    hexColor = hexColor.lstrip('#')
    rgba     = []

    for i in (0, 2, 4):

        decimal = int(hexColor[i: i+2], 16)
        rgba.append(decimal)
    
    rgba.append(alpha)

    return f'rgba({rgba[0]}, {rgba[1]}, {rgba[2]}, {rgba[3]})'

# ___________________________________________________________________________ #
def valuesInList(lstSrc: list, lstDefaultValue: list):

    '''
        Function to ensure that the main list contains assigned values.

        Args:

            lstSrc: Main list
            lstDefaultValue: List with default values to be set in the main list.

        Returns:

            A list filled with default values or existing values.
    '''

    combined        = itertools.zip_longest(lstSrc, lstDefaultValue, fillvalue = None)
    extractedValues = [value if value is not None else default for value, default in combined]

    return extractedValues

# ___________________________________________________________________________ #
