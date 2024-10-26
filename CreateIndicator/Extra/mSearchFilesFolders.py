import sys
import os

srcPath = os.path.realpath(os.path.join(os.path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from paths import PATH_DirInd

# ___________________________________________________________________________ #
def F_searchDelFiles(targetFile):

    pathFile        = ''
    excludedFolders = ['Gui', '__pycache__']

    # Go through the "Indicators" folder and its subfolders
    for folder, subfolder, files in os.walk(PATH_DirInd):

        if any(excluded_folder in folder for excluded_folder in excludedFolders):
            continue

        for file in files:
        
            if file.endswith(".py") or file.endswith('.txt'):
                if targetFile == file:
                    
                    pathFile = os.path.join(f'{PATH_DirInd}', f'{folder}', f'{file}')
                    break

    return pathFile 

# ___________________________________________________________________________ #
def F_searchFiles(selectedTab = '', delFiles = True):

    lstFiles        = []
    excludedFolders = ['Gui', '__pycache__']
    excludeFiles    = ['_ind__']

    # Go through the "Indicators" folder and its subfolders
    for folder, subfolder, files in os.walk(PATH_DirInd):
        if any(excluded_folder in folder for excluded_folder in excludedFolders):
            continue

        for file in files:

            if not delFiles and any(file.startswith(excludeFile) for excludeFile in excludeFiles):
                continue

            # Filter files by table
            if selectedTab != '':

                if selectedTab == 'Indicator' and file != '__init__.py' and file.startswith('_ind__') and file.endswith(".py"):
                    lstFiles.append(file)
                
                elif selectedTab == 'Input' and file != '__init__.py' and file.startswith('_inp__') and file.endswith(".py"):
                    lstFiles.append(file)
                
                elif selectedTab == 'Function' and file != '__init__.py' and file.endswith(".py") and not file.startswith('_ind__') and not file.startswith('_inp__'):
                    lstFiles.append(file)

            else:
                if file != '__init__.py' and file.endswith(".py") or file.endswith('.txt'):
                    lstFiles.append(file)

    lstFiles.sort()

    return lstFiles 

# ___________________________________________________________________________ #
def F_searchFolders(folderFunc = False):
    
    folders = ( ([f.name for f in os.scandir(PATH_DirInd) if f.is_dir() and f.name != 'Functions' and f.name != 'Gui' and f.name != '__pycache__']) if not folderFunc else
                ([f.name for f in os.scandir(PATH_DirInd) if f.is_dir() and f.name != 'Gui' and f.name != '__pycache__']) )

    folders.sort()

    return folders


