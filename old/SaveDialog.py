import sys
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class Ui_Save(object):
    def setupUi(self, canvas):
        self.title = 'Save DOS plot'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
    def saveFileDialog(self, canvas):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

        canvas.fig.savefig( fileName )

class AppSave(QDialog, Ui_Save):
    def __init__(self, canvas, parent=None):
        super(AppSave, self).__init__(parent)
        self.setupUi(self)
