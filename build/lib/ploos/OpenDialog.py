import sys
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class Ui_Open(object):
    def setupUi(self):
        self.title = 'Save DOS plot'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open...","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            return fileName

    def openDirectoryDialog(self):
        dirName = QFileDialog.getExistingDirectory(self, 
                'Open project folder...', '.', QFileDialog.ShowDirsOnly)
        if dirName:
            return dirName

class AppOpen(QDialog, Ui_Open):
    def __init__(self, parent=None):
        super(AppOpen, self).__init__(parent)
        self.setupUi()
