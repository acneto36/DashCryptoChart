
from   PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QTabWidget,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QWidget,
    QLabel,
)
  
from   PyQt5.QtGui  import QIcon
from   PyQt5.QtCore import pyqtSignal
from   PyQt5        import uic, QtCore
import shutil
import traceback
import sys
import os


srcPath = os.path.realpath(os.path.join(os.path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from paths                                     import *
from mPyqtWindowPosition                       import *
from CreateIndicator.Extra.mSearchFilesFolders import *
from CreateIndicator.Extra.mWriteReadInput     import *
from CreateIndicator.Extra.mSearchTxt          import *
from CreateIndicator.Extra.highlighter         import Highlighter
from CreateIndicator.Extra.customQTextedit     import *
from CreateIndicator.Extra.mConsole            import *
from CreateIndicator.mCreateStyle              import *
from SystemFiles.Fonts.mSystemFont             import *
from SystemFiles.mInstanceModules              import *
from SystemFiles.mPathModule                   import *
from DataFrames.mValuesDataFrame               import F_valuesDataFrame


# ___________________________________________________________________________ #
class CreateIndicator(QMainWindow):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):

        uic.loadUi(PATH_LayoutInd, self)

        self.setWindowTitle("Create indicator")

        self.functionPath  = ''
        self.oldFolder     = ''
        self.listTabs      = ['Indicator'] * 2
        self.listFolders   = [''] * 3
        self.listPathFiles = [''] * 3

        x, y, width, height = F_initialPosition(PATH_XyInd)

        self.setGeometry(x, y, width, height)

        self.centralWindow = self.findChild(QWidget, 'centralWindow')
        self.setWindowIcon(QIcon(PATH_IconCreate))

        # ------- BUTTOM -------- #
        self.btnNewInd   = self.findChild(QPushButton, 'btnNewInd')
        self.btnNewInd.clicked.connect(self.F_createIndicator)

        self.btnDelInd   = self.findChild(QPushButton, 'btnDelInd')
        self.btnDelInd.clicked.connect(self.F_deleteIndicator)

        self.btnDelFile  = self.findChild(QPushButton, 'btnDelFile')
        self.btnDelFile.clicked.connect(self.F_deleteFiles)

        self.btnEdit     = self.findChild(QPushButton, 'btnEdit')
        self.btnEdit.clicked.connect(self.F_codeEdit)

        self.btnImport   = self.findChild(QPushButton, 'btnImport')
        self.btnImport.clicked.connect(lambda: self.F_importExport(option = "import"))

        self.btnCreateInput = self.findChild(QPushButton, 'btnCreateInput')
        self.btnCreateInput.clicked.connect(lambda: self.F_createFileIndInp(self.listFolders[1], 'inp'))

        self.btnExport   = self.findChild(QPushButton, 'btnExport')
        self.btnExport.clicked.connect(lambda: self.F_importExport(option = "export"))

        self.btnCancel   = self.findChild(QPushButton, 'btnCancel')
        self.btnCancel.clicked.connect(self.F_updateComboBox)

        self.btnClear    = self.findChild(QPushButton, 'btnClear')
        self.btnClear.clicked.connect(self.F_clearTextArea)

        self.btnFunction = self.findChild(QPushButton, 'btnFunction')
        self.btnFunction.clicked.connect(self.F_saveFunction)

        self.btnSave     = self.findChild(QPushButton, 'btnSave')
        self.btnSave.clicked.connect(self.F_saveToFile)
        
        self.lblCount    = self.findChild(QLabel, 'lbContSearch')
        self.txtSearch   = self.findChild(QLineEdit, 'lnSearch')
        self.txtSearch.setPlaceholderText("Entry")

        self.tabWidget   = self.findChild(QTabWidget, 'tabWidget')
        self.tabWidget.currentChanged.connect(self.F_selectedTab)
        self.tabWidget.setCurrentIndex(0)
        self.selectedTab = 'Indicator'

        self.txtBoxInd   = self.findChild(QTextEdit, 'txtBoxInd')
        self.txtBoxInp   = self.findChild(QTextEdit, 'txtBoxInp')
        self.txtBoxFunc  = self.findChild(QTextEdit, 'txtBoxFunc')

        boxList = [self.txtBoxInd, self.txtBoxInp, self.txtBoxFunc]

        F_noWrap(boxList)
        F_tabPlainText(boxList)

        self.lblSearch   = self.findChild(QLabel, 'lblSearch')
        self.lblSelected = self.findChild(QLabel, 'lblSelected')

        # ====================== NUMBERS IN EDITOR ================== #
        self.txtNumInd  = self.findChild(QTextEdit, 'textNumInd')
        self.txtNumInp  = self.findChild(QTextEdit, 'textNumInp')
        self.txtNumFunc = self.findChild(QTextEdit, 'textNumFunc')

        numList = [self.txtNumInd, self.txtNumInp, self.txtNumFunc]

        F_styleSheetNum(numList)
        # =========================================================== #

        self.txtSearch.textChanged.connect(self.F_search)

        self.btnClearSearch = self.findChild(QPushButton, 'btnClearSearch')
        self.btnClearSearch.clicked.connect(lambda: F_clearSearch(self.txtSearch, self.lblCount))

        listTextEdit  = [self.txtBoxInd, self.txtBoxInp, self.txtBoxFunc, 
                         self.txtNumInd, self.txtNumInp, self.txtNumFunc]
        
        F_updateFontSize(listTextEdit)

        self.txtBoxInd.verticalScrollBar().valueChanged.connect(lambda: F_syncScroll(self, self.txtBoxInd, self.textNumInd))
        self.txtNumInd.verticalScrollBar().valueChanged.connect(lambda: F_syncScroll(self, self.txtBoxInd, self.textNumInd))

        self.txtBoxInp.verticalScrollBar().valueChanged.connect(lambda: F_syncScroll(self, self.txtBoxInp, self.txtNumInp))
        self.txtNumInp.verticalScrollBar().valueChanged.connect(lambda: F_syncScroll(self, self.txtBoxInp, self.txtNumInp))

        self.txtBoxFunc.verticalScrollBar().valueChanged.connect(lambda: F_syncScroll(self, self.txtBoxFunc, self.txtNumFunc))
        self.txtNumFunc.verticalScrollBar().valueChanged.connect(lambda: F_syncScroll(self, self.txtBoxFunc, self.txtNumFunc))

        F_removeScrollbar(numList)

        # Set font
        self.txtBoxInd.textChanged.connect(lambda:  self.F_customEdit(self.txtBoxInd,  self.txtNumInd))
        self.txtBoxInp.textChanged.connect(lambda:  self.F_customEdit(self.txtBoxInp,  self.txtNumInp))
        self.txtBoxFunc.textChanged.connect(lambda: self.F_customEdit(self.txtBoxFunc, self.txtNumFunc))

        # Tab key correction.
        self.txtBoxInd.installEventFilter(self)
        self.txtBoxInp.installEventFilter(self)
        self.txtBoxFunc.installEventFilter(self)

        # Set syntax highlighting.
        self.hltInd = Highlighter(self.txtBoxInd.document())
        self.hltInp = Highlighter(self.txtBoxInp.document())
        self.hltFun = Highlighter(self.txtBoxFunc.document())

        self.txtNewInd   = self.findChild(QLineEdit, 'txtNewInd')
        self.txtFuncName = self.findChild(QLineEdit, 'txtFuncName')
        self.txtLnSatus  = self.findChild(QLineEdit, 'lnStatus')

        # ------- COMBOBOX -------- #
        self.cbDeleteInd = self.findChild(QComboBox, 'cbDeleteInd')
        self.cbDelFile   = self.findChild(QComboBox, 'cbDelFile')
        self.cbEdit      = self.findChild(QComboBox, 'cbEdit')
        self.cbExport    = self.findChild(QComboBox, 'cbExport')
        self.cbSymbol    = self.findChild(QComboBox, 'cbSymbol')

        self.btnViewInp  = self.findChild(QPushButton, 'btnViewInp')
        self.btnViewInp.clicked.connect(self.viewInput)

        self.btnIndLog = self.findChild(QPushButton, 'btnIndLog')
        self.btnIndLog.clicked.connect(self.viewIndicator)
        self.btnIndLog.setIcon(QIcon(PATH_IconSave))

        self.btnConsole = self.findChild(QPushButton, 'btnConsole')
        self.btnConsole.clicked.connect(lambda: openConsole(self))
        self.btnConsole.setIcon(QIcon(PATH_IconPrint))

        self.F_updateComboBox()

    # ___________________________________________________________________________ # 
    def F_updateStyle(self):

        fontSize = 16

        F_createButtonStyle(self.btnDelInd,      'notosans', fontSize)
        F_createButtonStyle(self.btnNewInd,      'notosans', fontSize)
        F_createButtonStyle(self.btnDelFile,     'notosans', fontSize)
        F_createButtonStyle(self.btnEdit,        'notosans', fontSize)
        F_createButtonStyle(self.btnExport,      'notosans', fontSize, background = '#75507B', fontColor = '#EEEEEC', borderColor = '#89678f')
        F_createButtonStyle(self.btnFunction,    'notosans', fontSize, background = '#009494', fontColor = '#EEEEEC', borderColor = '#00b6b6')
        F_createButtonStyle(self.btnImport,      'notosans', fontSize, background = '#74671F', fontColor = '#EEEEEC', borderColor = '#a08d22')
        F_createButtonStyle(self.btnCancel,      'notosans', fontSize, background = '#790808', fontColor = '#EEEEEC', borderColor = '#be0000')
        F_createButtonStyle(self.btnSave,        'notosans', fontSize, background = '#134B1F', fontColor = '#EEEEEC', borderColor = '#0f7425')
        F_createButtonStyle(self.btnCreateInput, 'notosans', fontSize, background = '#008000', fontColor = '#EEEEEC', borderColor = '#129912')
        F_createButtonStyle(self.btnClear,       'notosans', fontSize, background = '#790808', fontColor = '#EEEEEC', borderColor = '#be0000')
        F_createButtonStyle(self.btnClearSearch, 'notosans', fontSize, background = '#555753', fontColor = '#EEEEEC', borderColor = '#ffffff', borderWidth = '2px')

        F_fontStyle(self.cbDeleteInd, 'QComboBox', 'notosans', fontSize, background = '#74671F', fontColor = '#ffffff')
        F_fontStyle(self.cbDelFile,   'QComboBox', 'notosans', fontSize, background = '#74671F', fontColor = '#ffffff')
        F_fontStyle(self.cbExport,    'QComboBox', 'notosans', fontSize, background = '#74671F', fontColor = '#ffffff')
        F_fontStyle(self.cbEdit,      'QComboBox', 'notosans', fontSize, background = '#74671F', fontColor = '#ffffff')
        F_fontStyle(self.lnStatus,    'QLineEdit', 'notosans', fontSize, background = '#5a5a5a', fontColor = '#ffffff')
        F_fontStyle(self.cbSymbol,    'QComboBox', 'notosans', fontSize-1, background = '#9E704A', fontColor = '#ffffff')
       
        F_labelStyle(self.lblSelected, 'notosans', fontSize, background = '#485879', fontColor = '#ffffff', borderColor = '#20BABF')
        F_labelStyle(self.lblSearch,   'notosans', fontSize, fontColor = '#ffffff', borderColor = '#ffffff')

    # ___________________________________________________________________________ #
    def F_customEdit(self, textEdit, numText):

        F_applyFontSize(textEdit)
        F_numTextEdit(textEdit, numText)
        
    # ___________________________________________________________________________ #       
    def viewIndicator(self):

        df = readDataFrame(self.cbSymbol.currentText())
        F_loadModules(df, indicatorFolder = self.listFolders[0], selectedSymbol = self.cbSymbol.currentText(), prefix = '_ind__')

    # ___________________________________________________________________________ #
    def viewInput(self):

        df = readDataFrame(self.cbSymbol.currentText())
        F_loadModules(df, indicatorFolder = self.listFolders[1], selectedSymbol = self.cbSymbol.currentText(), prefix = '_inp__')

    # ___________________________________________________________________________ #
    def eventFilter(self, obj, event): # Configure tab key
        
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Tab:

                cursor = obj.textCursor()
                cursor.insertText(' ' * 4)
                return True
            
        return super(CreateIndicator, self).eventFilter(obj, event)

    # ___________________________________________________________________________ #
    def F_search(self):

        qPlainText = (self.txtBoxInd if self.selectedTab == 'Indicator' else
                      self.txtBoxInp if self.selectedTab == 'Input'     else
                      self.txtBoxFunc)

        F_performSearch(qPlainText, self.txtSearch.text(), self.lblCount)

    # ___________________________________________________________________________ #
    def F_updateComboBox(self):

        self.cbDeleteInd.clear()
        self.cbDelFile.clear()
        self.cbEdit.clear()
        self.cbExport.clear()
        self.cbSymbol.clear()
 
        self.cbDeleteInd.addItems( F_searchFolders())
        self.cbDeleteInd.setCurrentIndex(-1)

        self.cbDelFile.addItems(F_searchFiles(delFiles = False)) # Do not list '_ind__' files.
        self.cbDelFile.setCurrentIndex(-1)

        self.cbEdit.addItems(F_searchFiles(self.selectedTab))
        self.cbEdit.setCurrentIndex(-1)

        self.cbExport.addItems(F_searchFolders(True))
        self.cbExport.setCurrentIndex(-1)

        self.cbSymbol.addItems(F_valuesDataFrame()[0])
        self.cbSymbol.setCurrentIndex(0)

        self.F_updateStyle()

    # ___________________________________________________________________________ #
    def F_selectedTab(self, index):

        self.selectedTab = self.tabWidget.tabText(index)
        self.F_updateComboBox()

        self.listTabs[1] = ('Indicator' if self.selectedTab == 'Indicator' else
                            'Input'     if self.selectedTab == 'Input'     else
                            'Function')
        
        (self.lnStatus.setText(str(self.listFolders[0])) if self.selectedTab == 'Indicator' else
         self.lnStatus.setText(str(self.listFolders[1])) if self.selectedTab == 'Input'     else
         self.lnStatus.setText(str(self.listFolders[2])))

        if self.listTabs[0] != self.listTabs[1]:

            F_clearSearch(self.txtSearch, self.lblCount) 
            self.listTabs[0] = self.listTabs[1]

    # ___________________________________________________________________________ #
    def F_createFile(self, folderPath, text = ''):

        with open(folderPath, 'w') as file:
            file.write(text)

    # ___________________________________________________________________________ #
    def F_nameFolder(self, pathFile):
       
        dirPath    = os.path.dirname(pathFile)
        nameFolder = os.path.basename(dirPath)

        return dirPath, nameFolder

    # ___________________________________________________________________________ #
    def F_saveFunction(self):

        if not self.txtFuncName.text():

            QMessageBox.warning(None, 'Warning', 'Insert "Function name"', QMessageBox.Ok)
            return

        folderPath = os.path.join(PATH_DirInd, 'Functions', f'{self.txtFuncName.text()}.py')
        fileName   = os.path.basename(folderPath)

        if os.path.exists(folderPath):

            QMessageBox.warning(None, 'Warning', f'The function {fileName} already exists', QMessageBox.Ok)
            self.txtFuncName.clear()
            return
        
        self.F_createFile(folderPath, f'# Start Function "{self.txtFuncName.text()}"')

        QMessageBox.information(None, 'Information', 'Create function successfully', QMessageBox.Ok)
        self.F_updateComboBox()

        self.txtFuncName.clear()

    # ___________________________________________________________________________ #
    def F_saveToFile(self):

        fileContent = (self.txtBoxInd.toPlainText() if self.selectedTab == 'Indicator' else 
                       self.txtBoxInp.toPlainText() if self.selectedTab == 'Input'     else 
                       self.txtBoxFunc.toPlainText())
        
        filePath    = (self.listPathFiles[0] if self.selectedTab == 'Indicator' else 
                       self.listPathFiles[1] if self.selectedTab == 'Input'     else 
                       self.listPathFiles[2])

        fileName    = os.path.basename(filePath)

        if not fileContent:

            QMessageBox.warning(None, 'Warning', 'No content', QMessageBox.Ok)
            return

        if not fileName:

            QMessageBox.warning(None, 'Warning', 'Indicator or file not selected', QMessageBox.Ok)
            return

        if os.path.exists(filePath):

            confirmReplace = QMessageBox.question(None, 'Question', f'Do you want to replace it? "{fileName}"', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            try:
                if confirmReplace == QMessageBox.Yes:
                    self.F_createFile(filePath, fileContent)

                    QMessageBox.information(None, 'Information', 'File replace successfully', QMessageBox.Ok)

                else:
                    QMessageBox.information(None, 'Information', 'Canceled by the user', QMessageBox.Ok)
            except:
                pass

        else:
            self.F_createFile(filePath, fileContent)
            QMessageBox.information(None, 'Information', f'File saved successfully. "{fileName}"', QMessageBox.Ok)

        # Reload the modules when there is a change.
        try:
            if self.selectedTab == 'Indicator':
                F_reloadModule(F_moduleIndicators('_ind__')[1], filePath)
                
            elif self.selectedTab == 'Input':
                F_reloadModule(F_moduleIndicators('_inp__')[1], filePath)

        except Exception as e:

            errorMsg  = ''.join(traceback.format_exception_only(type(e), e)).strip()
            errorLine = traceback.extract_tb(e.__traceback__)[-1].lineno

            print(f"{errorMsg} -> file '{fileName}' in Line {errorLine}")
            F_writeLog(PATH_Log, f"{errorMsg} -> file '{fileName}' in Line {errorLine}")
            pass

        self.F_updateComboBox()

    # ___________________________________________________________________________ #
    def F_clearTextArea(self, close = False):

        if not close:

            selected = QMessageBox.question(None, 'Question', 'Clear text?', 
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            try:
                if selected == QMessageBox.Yes:

                    (self.txtBoxInd.clear() if self.selectedTab == 'Indicator' else 
                     self.txtBoxInp.clear() if self.selectedTab == 'Input'     else
                     self.txtBoxFunc.clear())
                    
                    (self.txtNumInd.clear() if self.selectedTab == 'Indicator' else 
                     self.txtNumInp.clear() if self.selectedTab == 'Input'     else
                     self.txtNumFunc.clear())
                    
                    self.listFolders[0 if self.selectedTab == 'Indicator' else 1 if self.selectedTab == 'Input' else 2] = ''
                    self.listPathFiles[0 if self.selectedTab == 'Indicator' else 1 if self.selectedTab == 'Input' else 2] = ''

                    self.txtLnSatus.clear()

            except:
                pass

        else:
            self.txtBoxInd.clear()
            self.txtBoxInp.clear()
            self.txtBoxFunc.clear()
            self.txtNumInd.clear()
            self.txtNumInp.clear()
            self.txtNumFunc.clear()
            self.txtLnSatus.clear()

    # ___________________________________________________________________________ #
    def F_createFileIndInp(self, folderName,  indInp):

        baseCode   = PATH_BaseInd if indInp == 'ind' else PATH_BaseInp
        changeName = 'IndNewName' if indInp == 'ind' else 'InpNewName'
        keyword    = 'Ind' if indInp == 'ind' else 'Inp'

        if not folderName:
            return

        pathFile = os.path.join(PATH_DirInd, folderName, f'_{indInp}__{folderName}.py')
        fileName = os.path.basename(pathFile)

        with open(baseCode, 'r') as file:
            fileContent = file.read()

        # Replace specific keywords
        fileContent = fileContent.replace(changeName,   f'{keyword}{folderName.capitalize()}')
        fileContent = fileContent.replace('NewName',    folderName.capitalize())
        fileContent = fileContent.replace('New name',   folderName.capitalize())
        fileContent = fileContent.replace('config.txt', f'config{folderName.capitalize()}.txt')

        if os.path.exists(pathFile):

            confirmReplace = QMessageBox.question(None, 'Question', f'The file "{fileName}" already exists. Do you want to replace it?', 
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if confirmReplace == QMessageBox.Yes:
                self.F_createFile(pathFile, fileContent)

                QMessageBox.information(None, 'Information', 'File replace successfully', QMessageBox.Ok)

            else:
                QMessageBox.information(None, 'Information', 'Canceled by the user', QMessageBox.Ok)

        else:
            self.F_createFile(pathFile, fileContent)

            QMessageBox.information(None, 'Information', f'File saved successfully. "{fileName}"', QMessageBox.Ok)

        F_reloadModule(F_moduleIndicators('_ind__')[1])

        self.F_updateComboBox()

    # ___________________________________________________________________________
    def F_pathFolder(self, fileName):

        if not fileName:
            return ['', ''] # Avoid clearing the indicator name field if clicking on the edit without anything selected.
        
        pathFile   = F_searchDelFiles(fileName)
        nameFolder = self.F_nameFolder(pathFile)[1]

        self.txtLnSatus.setText(nameFolder)

        return pathFile, nameFolder

    # ___________________________________________________________________________ #
    def F_codeEdit(self):

        pathFile, folderName = self.F_pathFolder(self.cbEdit.currentText())  

        if not pathFile:

            QMessageBox.warning(None, 'Warning', 'No file selected!', QMessageBox.Ok)
            return

        # If switching workbooks, clear fields from another tab.#
        if self.oldFolder != folderName and self.selectedTab == 'Indicator':

            self.txtBoxInp.clear()
            self.listFolders[1] = ''
        
        elif self.oldFolder != folderName and self.selectedTab == 'Input':

            self.txtBoxInd.clear()
            self.listFolders[0] = ''
        
        # =========================================== #

        # Store the workbook folder name in a list to keep track when switching tabs.
        if folderName != 'Functions':
            self.listFolders[0:2] = [folderName] * 2

        else:
            self.listFolders[2] = 'Functions'

        # =========================================== #
            
        if pathFile:
            
            with open(pathFile, 'r') as file:
                fileContent = file.read()

            self.oldFolder = folderName if (self.selectedTab == 'Indicator' or self.selectedTab == 'Input') else ''
            
            (self.txtBoxInd.setPlainText(fileContent) if self.selectedTab == 'Indicator' else
             self.txtBoxInp.setPlainText(fileContent) if self.selectedTab == 'Input'     else
             self.txtBoxFunc.setPlainText(fileContent))
            
            self.listPathFiles[0 if self.selectedTab == 'Indicator' else 1 if self.selectedTab == 'Input' else 2] = pathFile

            self.F_updateComboBox()

    # ___________________________________________________________________________ #
    def F_createIndicator(self):

        try:

            if not self.txtNewInd.text():

                QMessageBox.warning(None, 'Warning', 'Enter the name of the indicator!', QMessageBox.Ok)
                return

            selectedName  = self.txtNewInd.text()[0].upper() + self.txtNewInd.text()[1:]
            selectedName  = selectedName.strip().replace(' ', '_') # Remove spaces
            pathNewFolder = os.path.join(PATH_DirInd, selectedName)

            self.txtNewInd.clear()

            if selectedName in F_searchFolders(False):

                QMessageBox.warning(None, 'Warning', 'Indicator already exists!', QMessageBox.Ok)
                return

            if not os.path.exists(PATH_DirInd):
                os.makedirs(PATH_DirInd, exist_ok = True)

            if not os.path.exists(pathNewFolder):
                os.makedirs(pathNewFolder, exist_ok = True)

            self.F_createFileIndInp(selectedName, 'ind')

            self.F_updateComboBox()

            QMessageBox.information(None, 'Information', 'Indicator created successfully', QMessageBox.Ok)
        
        except:
            pass

    # ___________________________________________________________________________ #
    def F_deleteFiles(self):

        if not self.cbDelFile.currentText():

            QMessageBox.warning(None, 'Warning', 'No file selected!', QMessageBox.Ok)
            return

        pathDelFile = F_searchDelFiles(self.cbDelFile.currentText())
        selected    = QMessageBox.question(None, 'Question', 'Delete file?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        try:
            if selected == QMessageBox.Yes:

                os.remove(pathDelFile)
                QMessageBox.information(None, 'Information', f'The file "{self.cbDelFile.currentText()}" was successfully deleted', QMessageBox.Ok)
        
        except:
            pass

        self.F_updateComboBox()

    # ___________________________________________________________________________ #
    def F_deleteIndicator(self):

        if not self.cbDeleteInd.currentText():

            QMessageBox.warning(None, 'Warning', 'No indicator selected!', QMessageBox.Ok)
            return
        
        pathDelFolder = os.path.join(PATH_DirInd, self.cbDeleteInd.currentText())

        # Delete the directory and its contents recursively
        selected = QMessageBox.question(None, 'Question', 'Delete indicator?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
       
        try:
            if selected == QMessageBox.Yes:
                shutil.rmtree(pathDelFolder)
                QMessageBox.information(None, 'Information', f'The indicator "{self.cbDeleteInd.currentText()}" was successfully deleted', QMessageBox.Ok)
        
        except:
            pass
        
        self.F_updateComboBox()

    # ___________________________________________________________________________ #
    def F_importExport(self, option = "import"):

        selectedIndicator = self.cbExport.currentText()

        try:
            if not selectedIndicator and option == 'export':

                QMessageBox.warning(None, 'Warning', 'No folder selected!', QMessageBox.Ok)
                return

            fd                = QFileDialog()
            selectedFolder    = fd.getExistingDirectory()
            pathFolder        = os.path.join(PATH_DirInd, selectedIndicator)
            srcFolder         = pathFolder     if option == 'export' else selectedFolder
            dirFolder         = selectedFolder if option == 'export' else PATH_DirInd

            # Needs this check; if canceled, I must return immediately
            if not selectedFolder: # Cancel

                self.F_updateComboBox()
                return

            dstFolder = os.path.join(dirFolder, os.path.basename(srcFolder))

            if os.path.exists(dstFolder):

                selected = QMessageBox.question(
                    None, 
                    'Question', 
                    f'Replace folder {dstFolder}?', 
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                
                if selected == QMessageBox.Yes:

                    shutil.rmtree(dstFolder)  # Delete existing folder
                    shutil.copytree(srcFolder, dstFolder)

                    QMessageBox.information(None, 'Information', 'Folder replace sucessfull', QMessageBox.Ok)
               
                else:
                    self.F_updateComboBox()
                    return
                
            else:

                strOpt = 'Export folder' if option == "export" else 'Import folder'

                selected = QMessageBox.question(
                    None, 
                    'Question', 
                    f'{strOpt} {srcFolder} ->\n {dstFolder}?', 
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )

                if selected == QMessageBox.Yes:
                    
                    shutil.copytree(srcFolder, dstFolder)

                    QMessageBox.information(None, 'Information', 'Operation completed', QMessageBox.Ok)

        except Exception as e:
            QMessageBox.critical(None, 'Error', f'Error: {str(e)}', QMessageBox.Ok)
        
        self.F_updateComboBox()

    # ___________________________________________________________________________ #
    # ***************************** WINDOW ************************************** #
    def F_updateGeometry(self):

        self.currentScreen = self.geometry()
        F_savePosition(self.currentScreen, PATH_XyInd)

    # ___________________________________________________________________________ #
    def moveEvent(self, event):
        self.F_updateGeometry()

    # ___________________________________________________________________________ #
    def resizeEvent(self, event):
        self.F_updateGeometry()

    # ___________________________________________________________________________ #
    def closeEvent(self, event): # Usage in mainDash

        self.closed.emit()
        event.accept()
        self.F_clearTextArea(close = True)

    # ___________________________________________________________________________ #
    def closeWindow(self):

        
        self.close()

 # ___________________________________________________________________________ #
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = CreateIndicator()
    window.show()
    sys.exit(app.exec_())