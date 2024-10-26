import pandas as pd

def size(df: pd.DataFrame) -> int:

    ''' Return the total length of the available series '''

    return len(df['date'])

# ___________________________________________________________________________ #
def dates(df: pd.DataFrame) -> list:

    ''' Return a list containing dates '''

    df['date'] = pd.to_datetime(df['date'])
    return df['date'].to_list()

# ___________________________________________________________________________ #
def opens(df: pd.DataFrame) -> list:

    ''' Return a list containing opening prices '''

    return df['open'].to_list()

# ___________________________________________________________________________ #
def highs(df: pd.DataFrame) -> list:

    ''' Return a list containing high prices '''
    
    return df['high'].to_list()

# ___________________________________________________________________________ #
def lows(df: pd.DataFrame) -> list:

    ''' Return a list containing low prices '''

    return df['low'].to_list()

# ___________________________________________________________________________ #
def closes(df: pd.DataFrame) -> list:

    ''' Return a list containing closing prices '''

    return df['close'].to_list()

# ___________________________________________________________________________ #
def volumes(df: pd.DataFrame) -> list:

    ''' Return a list containing volumes '''

    return df['volume'].to_list()

# ___________________________________________________________________________ #
def indexes(df: pd.DataFrame) -> list:

    ''' Return a list containing indexes '''

    return df['index'].to_list()

# ___________________________________________________________________________ #