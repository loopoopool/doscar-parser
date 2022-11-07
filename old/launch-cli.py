import sys
from ploos import Doscar, PlotGUI
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
window = PlotGUI.App(path='.')
window.show()
app.exec_()
