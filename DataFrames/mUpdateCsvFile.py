import sys
import csv
import pandas as pd
from   os  import path

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from paths                    import *
from DataFrames.mFormatNumber import *

# ___________________________________________________________________________ #
def F_updateCsv(pathFile, dfFileCsv, lastIndexExchange, lastIndexCsv, lastRow, missingRows):

    if lastIndexCsv == lastIndexExchange:

        # "Update only the last row of the existing CSV file."
        dfFileCsv.iloc[-1] = lastRow
        updatedRow         = [formatNumber(value) for value in dfFileCsv.iloc[-1].tolist()]

        with open(pathFile, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows   = list(reader)

        rows[-1] = updatedRow

        with open(pathFile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

    else:  # Fill in missing rows in the CSV file
        try:
            # "Remove the last row from the existing DataFrame."
            dfFileCsv = dfFileCsv.iloc[:-1]

            # "Loop to fill in all missing rows in the CSV file."
            while lastIndexCsv <= lastIndexExchange:

                # Check if the missing row already exists in dfFileCsv
                if lastIndexCsv not in dfFileCsv['index'].values:
                    dfFileCsv = pd.concat([dfFileCsv, missingRows[missingRows['index'] == lastIndexCsv]], ignore_index = True)
                
                lastIndexCsv += 1

            # "Save the updates to the CSV file."
            dfFileCsv.to_csv(pathFile, index = False)

        except Exception as e:

            print(f"UpdateCsv, Error  while updating the existing file: {pathFile}: {e}")