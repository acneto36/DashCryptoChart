import os, sys
import importlib

srcPath = os.path.realpath(os.path.join(os.path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from paths import PATH_DirInd


# ___________________________________________________________________________ #
def F_reloadModule(modules: list, path = ''):

    for i in range(len(modules)):

        module = importlib.import_module(modules[i])
        importlib.reload(module)

        #To avoid accusing an error in the wrong file when saving in createIndicator.
        if path != '' and path == module.__file__:
            break
    
    return module

# ___________________________________________________________________________ #
def F_moduleIndicators(prefix):

    lstIndicators = []
    lstModules    = []

    # Go through the "Indicators" folder and its subfolders
    for folder, subfolder, files in os.walk(PATH_DirInd):
        for file in files:

            # Make sure the file name starts with "_ind__" and has the extension ".py"
            if file.startswith(prefix) and file.endswith(".py"):

                indName    = file.replace(prefix, "").replace(".py", "")

                # Remove the extension and add the name to the list
                moduleName = f'Indicators.{indName}.{file[:-3]}'

                lstIndicators.append(indName)
                lstModules.append(moduleName)

    lstIndicators.sort()
    lstModules.sort()

    return lstIndicators, lstModules

# ___________________________________________________________________________ #