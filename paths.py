import os
from   SystemFiles.mWriteRead import *

def F_createFolder(pathFolder):

    if not os.path.exists(pathFolder):
        os.makedirs(pathFolder)

currentDir           = os.path.dirname(os.path.realpath(__file__))
PATH_CreateIndicator = os.path.join(currentDir, 'CreateIndicator')
PATH_Database        = os.path.join(currentDir, 'Databases')

PATH_DirInd          = os.path.join(currentDir, 'Indicators')
PATH_FolderYfi       = os.path.join(currentDir, 'HistoricalYfi')
PATH_FolderBnb       = os.path.join(currentDir, 'HistoricalBnb')

F_createFolder(PATH_Database)
F_createFolder(PATH_FolderYfi)
F_createFolder(PATH_FolderBnb)

PATH_Layout     = os.path.join(currentDir, 'mainUi.ui')
PATH_TrayIcon   = os.path.join(currentDir, 'Icon', 'icon.png')
PATH_Icon       = os.path.join(currentDir, 'Icon', 'eng8.png')
PATH_IconCreate = os.path.join(currentDir, 'Icon', 'eng5.png')
PATH_TutoEn     = os.path.join(currentDir, 'Tutorial', 'Home', 'en', 'index.html')
PATH_TutoPtbr   = os.path.join(currentDir, 'Tutorial', 'Home', 'pt-br','index.html')

PATH_LayoutInd  = os.path.join(PATH_CreateIndicator, 'createIndicator.ui')
PATH_LayoutLog  = os.path.join(PATH_CreateIndicator, 'consoleLog.ui')
PATH_IconPrint  = os.path.join(PATH_CreateIndicator, 'Icons', 'printLog.png')
PATH_IconSave   = os.path.join(PATH_CreateIndicator, 'Icons', 'saveLog.png')
PATH_BaseInd    = os.path.join(PATH_CreateIndicator, 'BaseCode', 'baseCodeIndicator.py')
PATH_BaseInp    = os.path.join(PATH_CreateIndicator, 'BaseCode', 'baseCodeInput.py')


PATH_PlotInd     = os.path.join(PATH_Database, 'plotIndicator.txt')
F_checkFileExist(PATH_PlotInd)

PATH_lstRightBnb = os.path.join(PATH_Database, 'listRightBnb.txt')
F_checkFileExist(PATH_lstRightBnb)
    
PATH_lstLeftBnb  = os.path.join(PATH_Database, 'listLeftBnb.txt')
F_checkFileExist(PATH_lstLeftBnb)
    
PATH_lstRightYfi = os.path.join(PATH_Database, 'listRightYfi.txt')
F_checkFileExist(PATH_lstRightYfi)
    
PATH_lstLeftYfi  = os.path.join(PATH_Database, 'listLeftYfi.txt')
F_checkFileExist(PATH_lstLeftYfi)
    
PATH_TimeFrame   = os.path.join(PATH_Database, 'timeFrames.txt')
F_checkFileTF(PATH_TimeFrame, 'Binance, 1_Hour\nyFinance, 1h')

PATH_UpdateSec   = os.path.join(PATH_Database, 'updateFilesInSec.txt')
F_checkFileExist(PATH_UpdateSec, '10')
    
PATH_Exchanges   = os.path.join(PATH_Database, 'exchanges.txt')
F_checkFileExist(PATH_Exchanges, 'yFinance')

PATH_DateIni     = os.path.join(PATH_Database, 'dateIni.txt')
F_checkFileExist(PATH_DateIni, '2024-04-01') 

PATH_HWaves      = os.path.join(PATH_Database, 'heightWave.txt')
F_checkFileExist(PATH_HWaves, '3') 

PATH_Histogram   = os.path.join(PATH_Database, 'foundHistogram.txt') 
F_checkFileExist(PATH_Histogram, '0') 

PATH_XY          = os.path.join(PATH_Database, 'mainCoordinates.txt')
F_checkFileExist(PATH_XY) 

PATH_XyInd       = os.path.join(PATH_Database, 'createIndCoordinates.txt')
F_checkFileExist(PATH_XyInd) 

PATH_ApiKey      = os.path.join(PATH_Database, 'apiKey.txt')
F_checkFileExist(PATH_ApiKey) 

PATH_Symbol      = os.path.join(PATH_Database, 'chosenSymbol.txt')
F_checkFileExist(PATH_Symbol) 
                    
PATH_Log         = os.path.join(currentDir, 'Log', 'logs.txt')
F_checkFileExist(PATH_Log) 

PATH_ZoomInfo    = os.path.join(PATH_Database, 'zoomInfo.json' )


# *************************************************************************** #
