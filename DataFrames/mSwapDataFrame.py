import sys
import traceback
from   os  import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)


from paths                    import PATH_Exchanges
from SystemFiles.mWriteRead   import *
from DataFrames.mReturnLists  import *
from DataFrames.mDataFrameBnb import *
from DataFrames.mDataFrameYfi import *

listImports = [F_dtFrameBnb, F_dtFrameYfi]

# ___________________________________________________________________________ #
def F_chooseDataFrame(complete = False):

    try:
        exchange = readingFile(PATH_Exchanges)

        for i in range(len(listImports)):
            if exchange[0] == F_exchanges()[i]:

                imports = listImports[i]

                return imports(complete)
            
    except Exception as e:
        # Capture the complete traceback.
        tb = traceback.format_exc()
        print(f"Error occurred in F_chooseDataFrame:\n{tb}")
        raise  # Propagate the exception so that previous methods can also catch it.

# ___________________________________________________________________________ #
