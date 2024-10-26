from PyQt5.QtCore    import pyqtSignal
from PyQt5.QtWidgets import QAction, QMenu, QMessageBox, QSystemTrayIcon


class TrayIcon(QSystemTrayIcon):

    quit_triggered = pyqtSignal()

    # ___________________________________________________________________________ #
    def __init__(self, app, icon, parent = None):
        super(TrayIcon, self).__init__(icon, parent)

        self.setToolTip("Cryptos")
        self.app  = app
        self.menu = QMenu(parent)

        self.menu.setStyleSheet("QMenu { font-size: 16px; color: white; background-color: #555753; }")

        # Action menu
        self.quitAction  = QAction("Quit", self)
        self.quitAction.triggered.connect(self.quitAplication)

        self.menu.addAction(self.quitAction)

        # Set the menu as the system tray icon context menu
        self.setContextMenu(self.menu)

        # Set up action for left mouse button click
        self.activated.connect(self.trayActivated)

    # ___________________________________________________________________________ #
    def trayActivated(self, reason):
        if reason == self.Trigger:

            if self.parent().isVisible():
                self.parent().hide()

            else:
                self.parent().show()
                
    # ___________________________________________________________________________ #
    def quitAplication(self):

       result = QMessageBox.question(None, "Confirmation", "Terminate the application?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
       
       if result == QMessageBox.Yes:
           self.app.quit()

       else:
           return

# ___________________________________________________________________________ #
 