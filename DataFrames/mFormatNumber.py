
# ___________________________________________________________________________ #  
def scientificNotation(number) -> bool:
    return 'e' in str(number).lower()

# ___________________________________________________________________________ #        
def greaterThanZero(number) -> bool:
        
    parts = str(number).split(".")

    if len(parts) == 2:  # if number is float

        if int(parts[0]) == 0:
            return False # cryptocurrency format 0.000021255

    return True # format 100.0

# ___________________________________________________________________________ #  
def formatNumber(number) -> str:

    '''
        Conversion of numbers with scientific notation
        Float number example: 10.21254, limit to 3 decimal places
        Float number example: 0.000548025555445, limit to 10 decimal places
    '''

    if scientificNotation(number):
        number = "{:.10f}".format(number)
    
    # Splits the string into parts before and after the decimal point
    parts = str(number).split(".")

    # Checks if there is a part before the decimal point
    if len(parts) == 2:  # if number is float

        return ( str("{:.3f}".format(float(number))) if greaterThanZero(number) else
                 str("{:.10f}".format(float(number))) )
       
    else:
        return str(number)  # if number is integer
                 
# ___________________________________________________________________________ #  
def decimalFormat(number) -> str:
        
    ''' Formats the float number, limiting it to 3 decimal places '''

    parts = str(number).split(".")

    if len(parts) == 2 and not '-' in str(number):  # if number is float
        return f'{number:.3f}'
    else:
        return str(number)  # if number is integer

# ___________________________________________________________________________ #   
            

