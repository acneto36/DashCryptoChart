import sys, os
from   PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paths                  import *
from mPyqtWindowPosition    import *
from SystemFiles.mWriteRead import *

# ___________________________________________________________________________ #
class GuiApiKey(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):

        self.setWindowTitle("API_KEY")

        self.setObjectName("Api_Key_Window")
        self.setFixedSize(600, 100)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # Set the window position using values stored in a text file
        x, y, width, height = F_initialPosition(PATH_XY)

        self.setGeometry(x, y, 600, 100)

        self.gridLayout = QGridLayout(self.centralwidget)

        self.labelApi   = QLabel("API_KEY: ", self.centralwidget)
        self.gridLayout.addWidget(self.labelApi, 0, 0)

        self.textBoxApi = QLineEdit(self.centralwidget)
        self.textBoxApi.setFixedWidth(500)
        self.gridLayout.addWidget(self.textBoxApi, 0, 1)

        self.labelKey   = QLabel("S_KEY: ", self.centralwidget)
        self.gridLayout.addWidget(self.labelKey, 1, 0)

        self.textBoxKey = QLineEdit(self.centralwidget)
        self.textBoxKey.setFixedWidth(500)
        self.gridLayout.addWidget(self.textBoxKey, 1, 1)
        
        file = readingFile(PATH_ApiKey)

        if len(file) > 1:
            self.textBoxApi.setText(file[0])
            self.textBoxKey.setText(file[1])

        self.btnSave = QPushButton('Save', self.centralwidget)
        self.btnSave.resize(100, 50)
        self.btnSave.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #d45f1b;
            }
        """)
        self.btnSave.clicked.connect(self.F_save)

        self.gridLayout.addWidget(self.btnSave, 2, 0, 1, 2)

        self.setCentralWidget(self.centralwidget)

    # ___________________________________________________________________________ #
    def closeEvent(self, event):
        event.accept()

    # ___________________________________________________________________________ #
    def closeWindow(self):
        self.close()

    # ___________________________________________________________________________ #
    def F_save(self):
        lstApiKey = []

        lstApiKey.append(f'{self.textBoxApi.text()}\n')
        lstApiKey.append(self.textBoxKey.text())

        F_writeFile(lstApiKey, PATH_ApiKey)

# ___________________________________________________________________________ #
if __name__ == "__main__":
    
    app    = QApplication(sys.argv)
    window = GuiApiKey()
    window.show()
    sys.exit(app.exec_())
