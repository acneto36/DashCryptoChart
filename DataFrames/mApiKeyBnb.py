from   os import path 
import sys

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)
    
from paths import *

 # ___________________________________________________________________________ #
def F_apiKey():

    lstApiKey = []
    
    with open(PATH_ApiKey, 'r') as file:
        lstApiKey = file.readlines()

    lstApiKey = [item.replace('\n', '') for item in lstApiKey]

    return lstApiKey

