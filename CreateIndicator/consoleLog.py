import sys
from   os              import path
from   PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QCheckBox
from   PyQt5.QtGui     import QIcon, QTextCursor
from   PyQt5           import uic
from   PyQt5.QtCore    import Qt, QTimer

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from CreateIndicator.Extra.mConsole        import *
from CreateIndicator.Extra.mWriteReadInput import *
from SystemFiles.Fonts.mSystemFont         import *
from paths                                 import *


currentDir = path.dirname(path.realpath(__file__))
pathIcon   = path.join(currentDir, 'Icons', 'warning.png')

class ConsoleLog(QMainWindow):
    def __init__(self, path = ''):
        super().__init__()

        uic.loadUi(PATH_LayoutLog, self)

        self.path  = path

        fontName   = F_enumFont('jetbrains')
        self.fonts = F_systemFont(fontName, 12)

        self.setWindowTitle(f'LOG')
        self.setWindowIcon(QIcon(pathIcon))

        self.centralWindow = self.findChild(QWidget, 'centralWindow')

        self.logText = self.findChild(QTextEdit, 'logText')
        self.logText.setFont(self.fonts)

        self.logText.setLineWrapMode(QTextEdit.NoWrap)
        self.logText.setReadOnly(True)

        self.numText = self.findChild(QTextEdit, 'numText')
        self.numText.setReadOnly(True)
        self.numText.setFont(self.fonts)


        self.logText.setStyleSheet(
            f""" QTextEdit {{
                background-color: #282A36;
                color: #D8DEE9;
                border: 1px solid #4C566A;
                }}
            """
        )

        self.numText.setStyleSheet(
            f""" QTextEdit {{
                background-color: #313131;
                color: #D8DEE9;
                border: 1px solid #4C566A;
                }}
            """
        )
        
        self.logText.verticalScrollBar().valueChanged.connect(self.F_syncScroll)
        self.numText.verticalScrollBar().valueChanged.connect(self.F_syncScroll)
        
        # Remover barra de rolagem do textEdit de números
        self.numText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.btnClear = self.findChild(QPushButton, 'btnClear')
        self.F_styleButton(self.btnClear, '#8a4b10', '#4e6d05')

        self.checkOntop = self.findChild(QCheckBox, 'ccbOntop')
        self.checkOntop.setChecked(True)
        self.checkOntop.clicked.connect(lambda: self.F_ontop(self.checkOntop))
        self.F_styleCheckBox(self.checkOntop)
        self.F_ontop(self.checkOntop)

        self.checkPause = self.findChild(QCheckBox, 'ccbPause')
        self.checkPause.setChecked(True)
        self.F_styleCheckBox(self.checkPause)

        if path:
            self.F_log(path)
            self.btnClear.clicked.connect(lambda: self.F_clearLog(path))
            self.checkPause.stateChanged.connect(lambda: self.F_textCheckbox(self.checkPause))

            self.timer = QTimer(self)
            self.timer.timeout.connect(lambda: self.F_log(path))
            self.timer.start(1000)

    # ___________________________________________________________________________ #
    def F_syncScroll(self):

        # Controlar barra de rolagem através do logText
        value1 = self.logText.verticalScrollBar().value()
        value2 = self.numText.verticalScrollBar().value()

        # Sincronizar as barras de rolagem
        if self.sender() == self.logText.verticalScrollBar():
            self.numText.verticalScrollBar().setValue(value1)
        else:
            self.logText.verticalScrollBar().setValue(value2)

    # ___________________________________________________________________________ #
    def F_clearLog(self, path):
         
        F_checkFileInput(path)
         
        with open(path, 'w') as file:
            file.writelines('')
        
        self.logText.setText('')
        self.numText.setText('')

    # ___________________________________________________________________________ #
    def F_log(self, path):

        F_checkFileInput(path)

        with open(path, 'r') as file:
            content = file.read() 

        lines    = content.splitlines()
        numLines = len(lines)

        self.logText.setText(content)

        numbers = "\n".join(str(i + 1).rjust(4) for i in range(numLines))

        self.numText.setText(numbers)

        self.logText.moveCursor(QTextCursor.End)
     
    # ___________________________________________________________________________ #
    def F_textCheckbox(self, checkbox):

        if checkbox.isChecked():

            checkbox.setText('Updating')

            if not self.timer.isActive():
                self.timer.start(1000)

        else:
            checkbox.setText('Stopped')

            if self.timer.isActive():
                self.timer.stop()

    # ___________________________________________________________________________ #
    def F_styleCheckBox(self, checkbox):

        checkbox.setStyleSheet("""
            QCheckBox {
                font: bold 18px;
                color: #EEEEEC;
            }
            QCheckBox::indicator:checked {
                background-color: #3db306;
                border: 2px solid #ffffff;
            }
            QCheckBox::indicator:unchecked {
                background-color: #c00303;
                border: 2px solid #ffffff;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #ffaa00;
            }
        """)

    # ___________________________________________________________________________ #
    def F_styleButton(self, button, normalColor, hoverColor):

        button.setStyleSheet(
            f""" QPushButton {{
                    background-color: {normalColor};
                    color: #ffffff;
                    font: bold 16px;
                }}
                                        
                QPushButton:hover {{
                    background-color: {hoverColor};
                    color: #ffffff;
                    font: bold 14px;
                }}                     
            """
        )
    
    # ___________________________________________________________________________ #
    def F_ontop(self, checkbox):

        if checkbox.isChecked():
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)

        self.show()

# ___________________________________________________________________________ #
if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = ConsoleLog()

    # gui.show()
    sys.exit(app.exec_())
