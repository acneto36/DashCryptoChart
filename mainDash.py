'''
    Dev: @Acneto
    Release 1.0: 26/10/2024

    
'''
 
import os, sys
import setproctitle
import webbrowser
import pyperclip 

from   PyQt5           import uic
from   PyQt5.QtGui     import QIcon, QRegExpValidator
from   PyQt5.QtCore    import Qt, QDate, QRegExp

from   PyQt5.QtWidgets import ( 
    QApplication, 
    QCheckBox, 
    QMainWindow, 
    QComboBox,
    QSpinBox,
    QListWidget, 
    QPushButton, 
    QAbstractItemView, 
    QMessageBox,
    QCalendarWidget,
    QWidget,
    QMenuBar,
    QMenu,
    QAction,
)

projectDir = os.path.realpath(os.path.join(os.path.dirname(__file__)))

if projectDir not in sys.path:
    sys.path.append(projectDir)

from paths                           import *
from mMainStyle                      import *
from trayIcon                        import *
from guiApiKey                       import *
from mSwapComboBox                   import *
from mainThreads                     import *
from mPyqtWindowPosition             import *
from DashFiles.runDash               import *
from SystemFiles.mWriteRead          import *
from SystemFiles.mManageLists        import *
from SystemFiles.Fonts.mSystemFont   import *
from DataFrames.mRecreateFile        import *
from DataFrames.mReturnLists         import *
from DataFrames.updateDataFrame      import *
from CreateIndicator.Extra.mConsole  import *
from CreateIndicator.createIndicator import *


LST_Exchanges  = F_exchanges()

# ================================================================================= #          
class MainClass(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
    
        # Create instance.
        self.createIndicator = CreateIndicator()

        # Connect the closed signal of the window createIndicator to the createIndicatorClosed slot.
        self.createIndicator.closed.connect(self.F_CreateIndicatorClosed)

        # Remove the maximize option
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.setupUi()

    def setupUi(self):
        setproctitle.setproctitle('DashCryptoChart')

        uic.loadUi(PATH_Layout, self)
        self.setWindowTitle("Dash chart")

        self.running     = False
        self.dataFrame   = None
        self.dashThread  = None
        self.shouldClose = True 

        self.selectExchange = readingFile(PATH_Exchanges)[0]
        self.lstTF          = F_LstTF(self.selectExchange)

        self.centralWindow  = self.findChild(QWidget, 'centralwidget')
        self.setCentralWidget(self.centralWindow)
        self.setWindowIcon(QIcon(PATH_TrayIcon))

        # Set the window position using values stored in a text file
        x, y, width, height = F_initialPosition(PATH_XY)
        self.setGeometry(x, y, width, height)
       
        self.left_list = self.findChild(QListWidget, 'listLeft')
        self.left_list.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Multiple selection with Ctrl

        self.right_list = self.findChild(QListWidget, 'listRight')
        self.right_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        # BUTTONS
        self.add_button = self.findChild(QPushButton, 'btnAdd')
        self.add_button.clicked.connect(lambda: F_addNewItem(self.left_list))
        
        self.move_right_button = self.findChild(QPushButton, 'btnRight')
        self.move_right_button.clicked.connect(lambda: F_moveItemsRight(self.left_list, self.right_list))
        
        self.move_left_button = self.findChild(QPushButton, 'btnLeft')
        self.move_left_button.clicked.connect(lambda: F_moveItemsLeft(self.left_list, self.right_list))
        
        self.remove_button = self.findChild(QPushButton, 'btnRemove')
        self.remove_button.clicked.connect(lambda: F_removeSelectedItem(self, self.left_list, self.right_list))
        
        self.btnCreate = self.findChild(QPushButton, 'btnCreate')
        self.btnCreate.clicked.connect(self.F_createIndicator)
        
        self.saveList = self.findChild(QPushButton, 'btnSaveUpdate')
        

        self.btnConsole = self.findChild(QPushButton, 'btnConsole')
        self.btnConsole.clicked.connect(lambda: openConsole(self))
        self.btnConsole.setIcon(QIcon(PATH_IconPrint))

        # CHECKBOX
        self.checkBox = self.findChild(QCheckBox, 'checkDash')
        self.checkBox.setChecked(self.running)
        self.checkBox.clicked.connect(self.toggle_dash)
        self.checkBox.setStyleSheet("QCheckBox {font: bold 18px; color: #EEEEEC;}")
        
        # COMBOBOX
        self.cbbTimeframe = self.findChild(QComboBox, 'cbTimeFrame')
        self.cbbTimeframe.addItems(self.lstTF)

        # Center the text
        self.cbbTimeframe.setEditable(True) 
        line_edit = self.cbbTimeframe.lineEdit() 
        line_edit.setAlignment(Qt.AlignCenter) 
        line_edit.setReadOnly(True) 

        self.cbbExchanges = self.findChild(QComboBox, 'cbExchange')
        self.cbbExchanges.addItems(LST_Exchanges)

        # SPINBOX
        self.spinSec = self.findChild(QSpinBox, 'spinSec')
        spinDefault  = F_readUpdateSec(PATH_UpdateSec)
        regex        = QRegExp("^[1-9][0-9]*$")

        # Number greater than zero
        validator = QRegExpValidator(regex, self.spinSec.lineEdit())
        self.spinSec.lineEdit().setValidator(validator)
        self.spinSec.setMinimum(1)
        
        self.spinSec.setValue(int(spinDefault))  # Set value from text file
        self.spinSec.valueChanged.connect(self.F_spinValue) # Update time in seconds

        # ------------------------------------------------------------------------------- #
        # Value saved as text to be used as the default value when opening the application
        defaultValue = F_readTimeframe(self.selectExchange, PATH_TimeFrame)
        self.cbbTimeframe.setCurrentText(defaultValue)

        self.F_initialValueCbBox(PATH_Exchanges, self.cbbExchanges)
        F_updateLists(self.left_list, self.right_list, self.selectExchange)
        # ------------------------------------------------------------------------------- #

        self.cbbTimeframe.currentIndexChanged.connect(
            lambda index, combo = self.cbbTimeframe: F_swapTimeFrame(combo, self.selectExchange)
        )

        self.cbbExchanges.currentIndexChanged.connect(
            lambda index, combo = self.cbbExchanges: F_updateCheckBox(
                combo,
                self.cbbTimeframe,
                self.left_list,
                self.right_list
            )
        )
 
        self.saveList.clicked.connect(lambda: self.F_saveListToFile([self.left_list, self.right_list]))

        # MENU
        self.menuBars   = self.findChild(QMenuBar, 'menubar')
        self.menuApiKey = self.findChild(QMenu, 'menuApiKey')
        self.openApiKey = self.findChild(QAction, 'openApiKey')
        self.openApiKey.triggered.connect(self.F_guiApiKey)

        # HELP
        self.menuHelp   = self.findChild(QMenu, 'menuHelp')
        self.tutorialEn = self.findChild(QAction, 'tutorial_en')
        self.tutorialEn.triggered.connect(lambda: self.F_openTutorial(PATH_TutoEn))

        self.tutorialPt = self.findChild(QAction, 'tutorial_pt_br')
        self.tutorialPt.triggered.connect(lambda: self.F_openTutorial(PATH_TutoPtbr))

        self.about = self.findChild(QAction, 'abouts')
        self.about.triggered.connect(self.F_about)

        # CALENDAR
        self.calendar = self.findChild(QCalendarWidget, 'periodCalendar')
        self.calendar.selectionChanged.connect(self.F_calendarDateChanged)

        # Read the date from the file
        dates = self.F_readDateFromFile(PATH_DateIni)

        # Set saved date from file
        if dates:
            self.calendar.setSelectedDate(dates)

        self.F_updateStylesheet()

    # ___________________________________________________________________________ #
    def F_updateStylesheet(self):

        fontBase = 15
        fontMax  = 16
        fontMin  = 14

        F_fontStyle(self.menuBars,     'QMenuBar',    'opensans', fontBase, background = '#505050', fontColor = '#ffffff')
        F_fontStyle(self.menuApiKey,   'QMenu',       'opensans', fontBase, fontColor = '#00e0e0')
        F_fontStyle(self.menuHelp,     'QMenu',       'opensans', fontBase, fontColor = '#ebebeb')
        F_fontStyle(self.cbbExchanges, 'QComboBox',   'bold',     fontMax)
        F_fontStyle(self.cbbTimeframe, 'QComboBox',   'bold',     fontMax)
        F_fontStyle(self.right_list,   'QListWidget', 'ubuntub',  fontBase)
        F_fontStyle(self.left_list,    'QListWidget', 'ubuntub',  fontBase)

        F_calendarStyle(self.calendar, 'jetbrainsb', 16)

        F_buttonStyle(self.saveList,          fontMax, fontMin)
        F_buttonStyle(self.add_button,        fontMax, fontMin)
        F_buttonStyle(self.btnCreate,         fontMax, fontMin)
        F_buttonStyle(self.remove_button,     fontMax, fontMin)
        F_buttonStyle(self.move_left_button,  fontMax, fontMin)
        F_buttonStyle(self.move_right_button, fontMax, fontMin)

    # ___________________________________________________________________________ #
    def F_spinValue(self):
        F_writeFile(str(self.spinSec.value()), PATH_UpdateSec)

    # ___________________________________________________________________________ #
    def F_openTutorial(self, pathFile):
        webbrowser.open(pathFile)

    # ___________________________________________________________________________ #
    def F_about(self):

        strKey = '0x9ec80b8e64E5CC69D27929B007534967E86e73e5'

        text = f"""
            DEV: @Acneto    
            Version: 1.0    
            Licence: GPL3   

            Donate crypto "MetaMask key":  
            {strKey}
        """

        mensagem = QMessageBox()
        mensagem.setWindowTitle('About')
        mensagem.setText(text)

        btnCopy = mensagem.addButton('Copy key', QMessageBox.ActionRole)
        mensagem.addButton(QMessageBox.Ok)

        while True:

            mensagem.exec_()

            if mensagem.clickedButton() == btnCopy:

                pyperclip.copy(strKey)
                mensagem.information(None, ' ', 'Key copied')

            else:
                break

    # ___________________________________________________________________________ #
    def F_createIndicator(self):

        self.setEnabled(False)
        self.createIndicator.setWindowModality(1)
        self.createIndicator.show()
        
        # Lock the X button on the main window
        self.shouldClose = False

    # ___________________________________________________________________________ #
    def F_CreateIndicatorClosed(self):

        # Reactivates the button when the task is completed
        self.F_changeColor(self.centralWindow, 'QWidget', '#77767B')
        self.setEnabled(True)

        # Unlock the X button on the main window
        self.shouldClose = True
        self.show() # Return main window

    # ___________________________________________________________________________ #
    def F_initialValueCbBox(self, pathFile, cbBox):

        readFile = readingFile(pathFile)
        cbBox.setCurrentText(readFile[0])

    # ___________________________________________________________________________ #
    def F_saveListToFile(self, lstLista):

        file     = readingFile(PATH_ApiKey)
        exchange = readingFile(PATH_Exchanges)
        lstFile  = F_selectPath(exchange[0], self.left_list, self.right_list)

        if len(file) < 2 and exchange[0] == 'Binance':
            QMessageBox.information(None, 'Info', 'Use the apiKey menu and enter the required data')
            return

        self.F_block(self.saveList)

        for i in range(len(lstLista)):

            dirAtual = os.path.dirname(os.path.realpath(__file__))
            filePath = os.path.join(dirAtual, 'Databases', lstFile[i])

            with open(filePath, 'w') as file:
                for index in range(lstLista[i].count()):

                    item = lstLista[i].item(index)
                    text = item.text()
                    file.write(f"{text}\n")

        self.F_dataFrameFull()

        QMessageBox.information(None, 'Info', '   Saved and loaded list   ')

        F_buttonStyle(self.saveList, 16, 14)
        self.F_changeColor(self.centralWindow, 'QWidget', '#77767B')

        # Unlock gui
        self.setEnabled(True)

    # ___________________________________________________________________________ #
    # ***************************** WINDOW ************************************** #
    def F_updateGeometry(self):
        self.currentScreen = self.geometry()
        F_savePosition(self.currentScreen, PATH_XY)

    # ___________________________________________________________________________ #
    def moveEvent(self, event):
        self.F_updateGeometry()

    # ___________________________________________________________________________ #
    def resizeEvent(self, event):
        self.F_updateGeometry()

    # ___________________________________________________________________________ #
    # *************************************************************************** #

    # ___________________________________________________________________________ #
    def F_guiApiKey(self):

        # Override main window
        if not hasattr(self, 'apiKeyWindow') or not self.apiKeyWindow.isVisible():

            self.apiKeyWindow = GuiApiKey()
            self.apiKeyWindow.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.apiKeyWindow.show()

    # ___________________________________________________________________________ #
    def F_readDateFromFile(self, path):

        dateStr = readingFile(path) # if fist, defaultValue
        qDate   = QDate.fromString(dateStr[0], 'yyyy-MM-dd')
 
        return qDate
    
    # ___________________________________________________________________________ #
    def F_calendarDateChanged(self):

        dateSelected  = self.calendar.selectedDate()
        formattedDate = dateSelected.toString("yyyy-MM-dd")
        formattedDate = formattedDate.replace(".", "")
        formattedDate = ' '.join(word.capitalize() for word in formattedDate.split())
        F_writeFile(formattedDate, PATH_DateIni)

        self.calendar.headerTextFormat()
  
    # ___________________________________________________________________________ #
    def F_dataFrameFull(self):

        dataFrame = UpdateDataFrame()
        dataFrame.start()
        dataFrame.join()

    # ___________________________________________________________________________ #
    def F_changeColor(self, widget, types, color):

        widget.setStyleSheet(f"{types}{{ background-color: {color}; }}")
        QApplication.processEvents()  # Force the update of the GUI

    # ___________________________________________________________________________ #
    def F_block(self, button):
        # Disable gui
        self.setEnabled(False)

        # Change colors
        self.F_changeColor(button, 'QPushButton', '#EDD400')
        self.F_changeColor(self.centralWindow, 'QWidget', '#A40000')
    
    # ___________________________________________________________________________ #
    def toggle_dash(self, state):

        self.running = state

        file     = readingFile(PATH_ApiKey)
        exchange = readingFile(PATH_Exchanges)

        # Necessário estar preenchida as 2 linhas do arquivo
        if (len(file) < 2 or not file[0].strip() or not file[1].strip()) and exchange[0] == 'Binance':

            self.checkBox.setChecked(False)
            QMessageBox.information(None, 'Info', 'Use the apiKey menu and enter the required data')
            return

        if self.running:

            app             = RunDash()
            self.dashThread = DashThread(app)
            self.dashThread.start()

            if self.dataFrame is None or not self.dataFrame.isRunning():
            
                self.dataFrame = DataFrameThread()
                self.dataFrame.start()
                self.checkBox.setStyleSheet("QCheckBox {font: bold 16px; color: #33E111;}")

        else:
            if self.dataFrame:
                self.dataFrame.stop()

            if self.dashThread and self.dashThread.isRunning():

                self.dashThread.terminate()

                QMessageBox.information(None, 'Info', 'Dash finished')

            self.checkBox.setStyleSheet("QCheckBox {font: bold 16px; color: #EEEEEC;}")
           
    # ___________________________________________________________________________ #
    def closeEvent(self, event):

        if self.shouldClose:  # Prevent the main window from closing if another window is open

            if self.dashThread and self.dashThread.isRunning():

                result = QMessageBox.question(self, "Confirmation", "Terminate the application?",
                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                
                if result == QMessageBox.Yes:

                    self.running = False
                    self.dashThread.terminate()
                    self.dashThread.wait() 
                    event.accept()

                else:
                    event.ignore()
            else:
                event.accept()

            # Close guiApiKey window   
            if hasattr(self, 'apiKeyWindow') and self.apiKeyWindow:
                    self.apiKeyWindow.close()
            
        else:
            event.ignore()

    # ___________________________________________________________________________ #

# ================================================================================= #
if __name__ == '__main__':

    ui     = QApplication(sys.argv)
    window = MainClass()
    window.show()
    
    # Create the TrayIcon object
    icon     = QIcon(PATH_TrayIcon)
    trayIcon = TrayIcon(ui, icon, window)

    trayIcon.show()

    sys.exit(ui.exec_())
